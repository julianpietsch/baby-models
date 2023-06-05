import pytest
from pathlib import Path
import json

MODELS_PATH = '.'
SHARE_PATH = 'shared'
EXCLUDE_DIRS = {'tests', 'shared'}
ROOT_KEYS = {'name', 'meta', 'brain_params'}
META_STR_KEYS = {'species', 'device', 'channel', 'camera'}
META_INT_KEYS = {'z_sections'}
META_FLT_KEYS = {'optical_zoom', 'pixel_size'}
META_KEYS_OPT_LIST = {'channel', 'z_sections'}
FILE_PARAMS = {'morph_model_file', 'flattener_file', 'params'
               'celltrack_model_file', 'budassign_model_file'}


@pytest.fixture(scope='module')
def model_dirs():
    root = Path(MODELS_PATH)
    return [model_dir for model_dir in root.iterdir()
            if model_dir.is_dir()
            and not model_dir.name.startswith('.')
            and not model_dir.name in EXCLUDE_DIRS]


@pytest.fixture(scope='module')
def model_sets(model_dirs):
    msets = []
    for model_dir in model_dirs:
        with open(model_dir / 'modelset.json') as f:
            msets.append(json.load(f))
    return msets


def test_models_path():
    root = Path(MODELS_PATH)
    assert root.is_dir()


def test_model_dirs_have_modelset(model_dirs):
    for model_dir in model_dirs:
        assert (model_dir / 'modelset.json').is_file()


def test_valid_json(model_dirs):
    for model_dir in model_dirs:
        with open(model_dir / 'modelset.json') as f:
            json.load(f)


def test_root_keys(model_sets):
    for mset in model_sets:
        assert ROOT_KEYS.issubset(mset.keys())


def test_name(model_sets):
    for mset in model_sets:
        assert type(mset['name']) == str


def test_meta(model_sets):
    META_KEYS = META_STR_KEYS.union(META_INT_KEYS).union(META_FLT_KEYS)
    assert META_KEYS_OPT_LIST.issubset(META_KEYS)
    for mset in model_sets:
        assert META_KEYS.issubset(mset['meta'].keys())
        for mkey in META_KEYS:
            val = mset['meta'][mkey]
            if mkey in META_KEYS_OPT_LIST:
                if type(val) != list:
                    val = [val]
            else:
                val = [val]
            for v in val:
                if mkey in META_STR_KEYS:
                    assert type(v) == str
                elif mkey in META_INT_KEYS:
                    assert type(v) == int
                else:
                    assert mkey in META_FLT_KEYS
                    assert type(v) == float or type(v) == int


def test_brain_params(model_dirs, model_sets):
    for mdir, mset in zip(model_dirs, model_sets):
        for k, v in mset['brain_params'].items():
            # TODO add test that checks BabyBrain arguments

            if k in FILE_PARAMS:
                if k == "params" and type(v) == dict:
                    continue
                f_local = mdir / v
                f_shared = Path(SHARE_PATH) / v
                assert f_local.is_file() or f_shared.is_file()
