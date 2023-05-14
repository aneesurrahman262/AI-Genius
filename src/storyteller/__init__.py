import importlib.metadata

from storyteller.config import StoryTellerConfig
from storyteller.model import StoryTeller

__version__ = None

try:
    __version__ = importlib.metadata.version("storyteller-core")
except importlib.metadata.PackageNotFoundError:
    pass

__all__ = ["__version__", "StoryTellerConfig", "StoryTeller"]
