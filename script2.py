import sys
from whisper import _download, _MODELS

_download(_MODELS["base"], "/home/yash/Documents/models", False)