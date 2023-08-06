"""
Cropped Decoding on BCIC IV 2a Competition Set with skorch and moabb.
=====================================================================
"""

# Authors: Maciej Sliwowski <maciek.sliwowski@gmail.com>
#          Robin Tibor Schirrmeister <robintibor@gmail.com>
#          Lukas Gemein <l.gemein@gmail.com>
#          Hubert Banville <hubert.jbanville@gmail.com>
#
# License: BSD-3
from braindecode.datautil.preprocess import preprocess, MNEPreproc, NumpyPreproc
from braindecode.datautil.preprocess import exponential_moving_standardize
from braindecode.util import set_random_seeds
from braindecode.models.util import to_dense_prediction_model, get_output_shape
from braindecode.models.shallow_fbcsp import ShallowFBCSPNet
from braindecode.models.deep4 import Deep4Net
from braindecode.training.losses import CroppedNLLLoss
from braindecode.datasets import MOABBDataset
from braindecode.classifier import EEGClassifier
from braindecode.datautil.windowers import create_windows_from_events
from functools import partial

import numpy as np
import torch
import mne
from skorch.callbacks import LRScheduler
mne.set_log_level('ERROR')


def run_exp_cropped(subject_id, model_name, low_cut_hz, n_epochs, seed):
    assert model_name in ['shallow', 'deep']
    high_cut_hz = 38.
    trial_start_offset_seconds = -0.5
    input_window_samples = 1000
    batch_size = 64
    factor_new = 1e-3
    init_block_size = 1000
    cuda = torch.cuda.is_available()
    device = 'cuda' if cuda else 'cpu'
    if cuda:
        torch.backends.cudnn.benchmark = True

    n_classes = 4
    n_chans = 22

    set_random_seeds(seed=seed, cuda=cuda)

    if model_name == "shallow":
        model = ShallowFBCSPNet(
            n_chans,
            n_classes,
            input_window_samples=input_window_samples,
            final_conv_length=30,
        )
        lr = 0.0625 * 0.01
        weight_decay = 0

    elif model_name == "deep":
        model = Deep4Net(
            n_chans,
            n_classes,
            input_window_samples=input_window_samples,
            final_conv_length=2,
        )
        lr = 1 * 0.01
        weight_decay = 0.5 * 0.001

    if cuda:
        model.cuda()

    to_dense_prediction_model(model)
    n_preds_per_input = get_output_shape(model, n_chans, input_window_samples)[2]

    dataset = MOABBDataset(dataset_name="BNCI2014001", subject_ids=[subject_id])

    preprocessors = [
        # keep only EEG sensors
        MNEPreproc(fn='pick_types', eeg=True, meg=False, stim=False),
        # convert from volt to microvolt, directly modifying the numpy array
        NumpyPreproc(fn=lambda x: x * 1e6),
        # bandpass filter
        MNEPreproc(fn='filter', l_freq=low_cut_hz, h_freq=high_cut_hz),
        NumpyPreproc(fn=exponential_moving_standardize,
                     factor_new=factor_new,
                     init_block_size=init_block_size)
    ]

    # Preprocess the data
    preprocess(dataset, preprocessors)

    sfreqs = [ds.raw.info['sfreq'] for ds in dataset.datasets]
    assert len(np.unique(sfreqs)) == 1
    trial_start_offset_samples = int(trial_start_offset_seconds * sfreqs[0])

    windows_dataset = create_windows_from_events(
        dataset,
        trial_start_offset_samples=trial_start_offset_samples,
        trial_stop_offset_samples=0,
        window_size_samples=input_window_samples,
        window_stride_samples=n_preds_per_input,
        drop_last_window=False,
        preload=True,
    )

    class TrainTestBCICIV2aSplit(object):
        def __call__(self, dataset, y, **kwargs):
            splitted = dataset.split('session')
            return splitted['session_T'], splitted['session_E']

    clf = EEGClassifier(
        model,
        cropped=True,
        criterion=CroppedNLLLoss,
        optimizer=torch.optim.AdamW,
        train_split=TrainTestBCICIV2aSplit(),
        optimizer__lr=lr,
        optimizer__weight_decay=weight_decay,
        iterator_train__shuffle=True,
        batch_size=batch_size,
        callbacks=[
            "accuracy",
            # seems n_epochs -1 leads to desired behavior of lr=0 after end of training?
            ("lr_scheduler",
             LRScheduler('CosineAnnealingLR', T_max=n_epochs - 1)),
        ],
        device=device,
    )

    clf.fit(windows_dataset, y=None, epochs=n_epochs)
    return clf


def run_exp_trial(subject_id, model_name, low_cut_hz, n_epochs, seed):
    high_cut_hz = 38.
    trial_start_offset_seconds = -0.5
    input_window_samples = 1125
    batch_size = 64
    factor_new = 1e-3
    init_block_size = 1000
    cuda = torch.cuda.is_available()
    device = 'cuda' if cuda else 'cpu'
    if cuda:
        torch.backends.cudnn.benchmark = True

    n_classes = 4
    n_chans = 22

    set_random_seeds(seed=seed, cuda=cuda)

    if model_name == "shallow":
        model = ShallowFBCSPNet(
            n_chans,
            n_classes,
            input_window_samples=input_window_samples,
            final_conv_length='auto',
        )
        lr = 0.0625 * 0.01
        weight_decay = 0

    elif model_name == "deep":
        model = Deep4Net(
            n_chans,
            n_classes,
            input_window_samples=input_window_samples,
            final_conv_length='auto',
        )
        lr = 1 * 0.01
        weight_decay = 0.5 * 0.001

    if cuda:
        model.cuda()

    dataset = MOABBDataset(dataset_name="BNCI2014001", subject_ids=[subject_id])

    preprocessors = [
        # keep only EEG sensors
        MNEPreproc(fn='pick_types', eeg=True, meg=False, stim=False),
        # convert from volt to microvolt, directly modifying the numpy array
        NumpyPreproc(fn=lambda x: x * 1e6),
        # bandpass filter
        MNEPreproc(fn='filter', l_freq=low_cut_hz, h_freq=high_cut_hz),
        NumpyPreproc(fn=exponential_moving_standardize,
                     factor_new=factor_new,
                     init_block_size=init_block_size)
    ]

    # Transform the data
    preprocess(dataset, preprocessors)

    sfreqs = [ds.raw.info['sfreq'] for ds in dataset.datasets]
    assert len(np.unique(sfreqs)) == 1
    trial_start_offset_samples = int(trial_start_offset_seconds * sfreqs[0])

    windows_dataset = create_windows_from_events(
        dataset,
        trial_start_offset_samples=trial_start_offset_samples,
        trial_stop_offset_samples=0,
        window_size_samples=input_window_samples,
        window_stride_samples=input_window_samples,
        drop_last_window=False,
        preload=True,
    )

    class TrainTestBCICIV2aSplit(object):
        def __call__(self, dataset, y, **kwargs):
            splitted = dataset.split('session')
            return splitted['session_T'], splitted['session_E']

    clf = EEGClassifier(
        model,
        cropped=False,
        criterion=torch.nn.NLLLoss,
        optimizer=torch.optim.AdamW,
        train_split=TrainTestBCICIV2aSplit(),
        optimizer__lr=lr,
        optimizer__weight_decay=weight_decay,
        iterator_train__shuffle=True,
        batch_size=batch_size,
        callbacks=[
            "accuracy",
            # seems n_epochs -1 leads to desired behavior of lr=0 after end of training?
            ("lr_scheduler",
             LRScheduler('CosineAnnealingLR', T_max=n_epochs - 1)),
        ],
        device=device,
    )

    clf.fit(windows_dataset, y=None, epochs=n_epochs)
    return clf
