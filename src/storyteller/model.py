import os
from typing import List

import soundfile as sf
import torch
from diffusers import StableDiffusionPipeline
from nltk.tokenize import sent_tokenize
from PIL.Image import Image
from transformers import pipeline
from TTS.api import TTS

from storyteller import StoryTellerConfig
from storyteller.utils import (
    make_timeline_string,
    require_ffmpeg,
    require_punkt,
    subprocess_run,
)


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

    @torch.inference_mode()
    def paint(self, prompt: str) -> Image:
        return self.painter(prompt).images[0]

    @torch.inference_mode()
    def speak(self, prompt: str) -> List[int]:
        return self.speaker.tts(prompt)

    @torch.inference_mode()
    def write(self, prompt: str) -> str:
        return self.writer(prompt, max_new_tokens=self.config.max_new_tokens)[0][
            "generated_text"
        ]

    def get_output_path(self, file: str) -> str:
        return os.path.join(self.output_dir, file)

    def generate(
        self,
        writer_prompt: str,
        painter_prompt_prefix: str,
        num_images: int,
        output_dir: str,
    ) -> None:
        video_paths = []
        self.output_dir = output_dir
        sentences = self.write_story(writer_prompt, num_images)
        for i, sentence in enumerate(sentences):
            try:
                video_path = self._generate(i, sentence, painter_prompt_prefix)
                video_paths.append(video_path)
            except Exception as e:
                # Handle any exceptions that occur during the generation process
                print(f"Error generating video for sentence {i+1}: {str(e)}")
        self.concat_videos(video_paths)

    def concat_videos(self, video_paths: List[str]) -> None:
        files_path = self.get_output_path("files.txt")
        output_path = self.get_output_path("out.mp4")
        with open(files_path, "w+") as f:
            for video_path in video_paths:
                f.write(f"file {os.path.split(video_path)[-1]}\n")
        subprocess_run(f"ffmpeg -f concat -i {files_path} -c copy {output_path}")

    def _generate(self, id_: int, sentence: str, painter_prompt_prefix:
