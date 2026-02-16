import json
import os

_config_dir = os.path.dirname(os.path.abspath(__file__))
_podcasts_path = os.path.join(_config_dir, "podcasts.json")

with open(_podcasts_path) as f:
    PODCASTS = json.load(f)
