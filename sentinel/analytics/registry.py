"""Discover independent analysis plugins, never import arbitrary uploaded code."""
from importlib import import_module
from pathlib import Path

def analyze(values):
    result = {}
    for file in sorted(Path(__file__).parent.glob('*.py')):
        if file.stem.startswith('_') or file.stem == 'registry':
            continue
        module = import_module('sentinel.analytics.' + file.stem)
        result[file.stem] = round(module.calculate(values), 5)
    return result
