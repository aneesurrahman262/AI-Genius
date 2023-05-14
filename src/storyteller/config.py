@dataclass
class StoryTellerConfig:
    max_new_tokens: int = 100  # Increased token limit
    writer: str = "gpt2"
    painter: str = "stabilityai/stable-diffusion-2"
    speaker: str = "tts_models/en/ljspeech/glow-tts"
    writer_device: str = "cuda:0" if torch.cuda.is_available() else "cpu"
    painter_device: str = "cuda:0" if torch.cuda.is_available() else "cpu"
