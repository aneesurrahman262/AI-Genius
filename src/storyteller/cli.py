import argparse
import dataclasses
import logging
import os

from storyteller import StoryTeller, StoryTellerConfig
from storyteller.utils import set_log_level, set_seed


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--writer_prompt",
        type=str,
        default="Once upon a time, unicorns roamed the Earth.",
        help="The prompt for the writer to generate the story.",
    )
    parser.add_argument(
        "--painter_prompt_prefix",
        type=str,
        default="Beautiful painting",
        help="The prefix for the painter prompt.",
    )
    parser.add_argument(
        "--num_images",
        type=int,
        default=10,
        help="The number of images to generate.",
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        default="out",
        help="The output directory to save the generated images.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="The seed value for random number generation.",
    )
    default_config = StoryTellerConfig()
    for key, value in dataclasses.asdict(default_config).items():
        parser.add_argument(f"--{key}", type=type(value), default=value)
    args = parser.parse_args()
    return args


def main() -> None:
    args = get_args()

    # Set the seed for reproducibility
    set_seed(args.seed)

    # Set the log level
    set_log_level(logging.WARNING)

    # Disable tokenizers parallelism
    os.environ["TOKENIZERS_PARALLELISM"] = "false"

    # Create the StoryTeller configuration
    config = StoryTellerConfig()
    for field in dataclasses.fields(config):
        name = field.name
        setattr(config, name, getattr(args, name))

    # Create a StoryTeller instance
    story_teller = StoryTeller(config)

    # Create the output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)

    # Generate the story
    story_teller.generate(
        args.writer_prompt,
        args.painter_prompt_prefix,
        args.num_images,
        args.output_dir,
    )


if __name__ == "__main__":
    main()
