from dataclasses import dataclass

import torch


@dataclass
class StoryTellerConfig:
    """Configuration options for the StoryTeller."""

    max_new_tokens: int = 50  # Maximum number of tokens for text generation.
    writer: str = "gpt2"  # Model used for writing the story.
    painter: str = "stabilityai/stable-diffusion-2"  # Model used for generating images.
    speaker: str = "tts_models/en/ljspeech/glow-tts"  # Model used for text-to-speech synthesis.
    writer_device: str = "cuda:0" if torch.cuda.is_available() else "cpu"  # Device for the writer model.
    painter_device: str = "cuda:0" if torch.cuda.is_available() else "cpu"  # Device for the painter model.
