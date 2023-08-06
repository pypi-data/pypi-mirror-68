import torch.backends.cudnn as cudnn
import torch
from hyperoptim.parse import cartesian_dict_of_lists_product, \
    product_of_list_of_lists_of_dicts
import logging
import time
import os

os.sys.path.insert(0, '/home/schirrmr/code/invertible-reimplement/')


logging.basicConfig(format='%(asctime)s | %(levelname)s : %(message)s')


log = logging.getLogger(__name__)
log.setLevel('INFO')


def get_templates():
    return {}


def get_grid_param_list():
    dictlistprod = cartesian_dict_of_lists_product

    save_params = [
        {
            'save_folder': '/home/schirrmr/data/exps/braindecode/bcic-iv-2a-reproduction/trial-fixed-preproc/',
        },
    ]

    debug_params = [{
        'debug': False,
    }]

    data_params = dictlistprod({
        'subject_id': range(1, 10),
        'low_cut_hz': [0, 4],
    })

    train_params = dictlistprod({
        'n_epochs': [800],
        'cropped_or_trial': ['cropped']
    })

    random_params = dictlistprod({
        'seed': range(0, 3),
    })

    model_params = dictlistprod({
        'model_name': ['shallow', 'deep'],
    })

    grid_params = product_of_list_of_lists_of_dicts([
        save_params,
        data_params,
        train_params,
        debug_params,
        random_params,
        model_params,
    ])

    return grid_params


def sample_config_params(rng, params):
    return params


def run(
        ex,
        subject_id,
        debug,
        low_cut_hz,
        n_epochs,
        seed,
        model_name,
        cropped_or_trial,
):
    kwargs = locals()
    kwargs.pop('ex')
    if not debug:
        log.setLevel('INFO')
    if debug:
        kwargs['n_epochs'] = 3
    kwargs.pop('debug')
    kwargs.pop('cropped_or_trial')
    assert cropped_or_trial in ['cropped', 'trial']

    #file_obs = ex.observers[0]
    #output_dir = file_obs.dir
    #kwargs['output_dir'] = output_dir
    torch.backends.cudnn.benchmark = True
    import sys
    logging.basicConfig(format='%(asctime)s %(levelname)s : %(message)s',
                        level=logging.DEBUG, stream=sys.stdout)
    start_time = time.time()
    ex.info['finished'] = False
    from braindecode.experiments.bcic_iv_2a.run import run_exp_cropped, run_exp_trial
    if cropped_or_trial == 'cropped':
        clf = run_exp_cropped(**kwargs)
    else:
        assert cropped_or_trial == 'trial'
        clf = run_exp_trial(**kwargs)

    end_time = time.time()
    run_time = end_time - start_time
    ex.info['finished'] = True
    ignore_keys = [
        'batches', 'epoch', 'train_batch_count', 'valid_batch_count',
        'train_loss_best',
        'valid_loss_best', 'train_trial_accuracy_best',
        'valid_trial_accuracy_best']
    results = dict([(key, val) for key, val in clf.history[-1].items() if
                    key not in ignore_keys])

    for key, val in results.items():
        ex.info[key] = float(val)
    ex.info['runtime'] = run_time
