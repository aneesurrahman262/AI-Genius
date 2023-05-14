# StoryTeller

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A multimodal AI story teller, built with [Stable Diffusion](https://huggingface.co/spaces/stabilityai/stable-diffusion), GPT, and neural text-to-speech (TTS).

Given a prompt as an opening line of a story, GPT writes the rest of the plot; Stable Diffusion draws an image for each sentence; a TTS model narrates each line, resulting in a fully animated video of a short story, replete with audio and visuals.

![out](https://user-images.githubusercontent.com/25360440/210071764-51ed5872-ba56-4ed0-919b-d9ce65110185.gif)

## Installation

### PyPI

Story Teller is available on [PyPI](https://pypi.org/project/storyteller-core/).

```bash
$ pip install storyteller-core
