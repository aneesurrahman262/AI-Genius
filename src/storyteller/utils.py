import logging
import os
import random
import shutil
import subprocess
from functools import wraps

import nltk
import numpy as np
import torch
import warnings


def require_ffmpeg(func):
    """Decorator for checking ffmpeg installation."""

    @wraps(func)
    def wrapper_func(*args, **kwargs):
        if shutil.which("ffmpeg") is None:
            raise RuntimeError(
                "`ffmpeg` not found. Please install `ffmpeg` and try again."
            )
        func(*args, **kwargs)

    return wrapper_func


def require_punkt(func):
    """Decorator for checking nltk punkt module."""

    @wraps(func)
    def wrapper_func(*args, **kwargs):
        try:
            nltk.data.find("tokenizers/punkt")
        except LookupError:
            nltk.download("punkt")
        func(*args, **kwargs)

    return wrapper_func


def make_timeline_string(start, end):
    """Create timeline string to write onto .srt subtitle files."""
    start = format_time(start)
    end = format_time(end)
    return f"{start} --> {end}"


def format_time(time):
    """Transform time (seconds) to .srt format."""
    mm, ss = divmod(time, 60)
    hh, mm = divmod(mm, 60)
    return f"{hh:02d}:{mm:02d}:{ss:02d},000"


def subprocess_run(command):
    """Wrapper around `subprocess.run()` with /dev/null redirection in stdout and stderr."""
    try:
        subprocess.run(
            command.split(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True
        )
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Command '{command}' failed with exit code {e.returncode}.")


def set_seed(seed):
    """Set seed."""
    random.seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = True


def set_log_level(level: int) -> None:
    """Set the logging level."""
    logging.basicConfig(level=level)


warnings.filterwarnings("ignore")

from dataclasses import dataclass

import torch

@dataclass
class StoryTellerConfig:
    max_new_tokens: int = 50
    writer: str = "gpt2"
    painter: str = "stabilityai/stable-diffusion-2"
    speaker: str = "tts_models/en/ljspeech/glow-tts"
    writer_device: str = "cuda:0" if torch.cuda.is_available() else "cpu"
    painter_device: str = "cuda:0" if torch.cuda.is_available() else "cpu"


class StoryTeller:
    @require_ffmpeg
    @require_punkt
    def __init__(self, config: StoryTellerConfig):
        self.config = config
        writer_device = torch.device(config.writer_device)
        painter_device = torch.device(config.writer_device)
        self.writer = pipeline(
            "text-generation", model=config.writer, device=writer_device
        )
        self.painter = StableDiffusionPipeline.from_pretrained(
            config.painter,
            use_auth_token=False,
        ).to(painter_device)
        self.speaker = TTS(config.speaker)
        self.sample_rate = self.speaker.synthesizer.output_sample_rate
        self.output_dir = None

    @classmethod
    def from_default(cls):
        config = StoryTellerConfig()
        return cls(config)

    @torch
