#!/usr/bin/env python3

from pathlib import Path
import json

MODELS_PATH = '.'
MODEL_SPECS_FILE = 'modelsets.json'
SHARE_PATH = 'shared'
EXCLUDE_DIRS = {'tests', 'shared'}


def model_dirs():
    root = Path(MODELS_PATH)
    return [model_dir for model_dir in root.iterdir()
            if model_dir.is_dir()
            and not model_dir.name.startswith('.')
            and not model_dir.name in EXCLUDE_DIRS]


def get_all_model_specs():
    model_specs = {}
    for model_dir in model_dirs():
        with open(model_dir / 'modelset.json') as f:
            model_specs[model_dir.name] = json.load(f)
    return model_specs


def main():
    modelsdir = Path(MODELS_PATH)
    sharedir =  modelsdir / SHARE_PATH
    model_specs = get_all_model_specs()
    for k in model_specs:
        model_specs[k]['files'] = [p.name for p in (modelsdir / k).iterdir()]
    metadata = {
        'models': model_specs,
        'shared': [p.name for p in sharedir.iterdir()],
    }
    with open(modelsdir / MODEL_SPECS_FILE, 'wt') as f:
        json.dump(model_specs, f)


if __name__ == '__main__':
    main()
