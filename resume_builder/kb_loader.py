import os
import yaml
from typing import Dict

def load_yaml_files(kb_dir: str) -> Dict[str, dict]:
    kb_data = {}
    for filename in os.listdir(kb_dir):
        if filename.endswith('.yml') or filename.endswith('.yaml'):
            filepath = os.path.join(kb_dir, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                kb_data[filename] = yaml.safe_load(f)
    return kb_data
