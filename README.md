<!DOCTYPE html>
<html>
<head>
  <title>StoryTeller</title>
  <link rel="stylesheet" href="styles.css"> <!-- Link to your CSS file for custom styling -->
</head>
<body>
  <header>
    <h1>StoryTeller</h1>
    <p>A multimodal AI story teller, built with Stable Diffusion, GPT, and neural text-to-speech (TTS).</p>
  </header>
  
  <section id="description">
    <h2>Description</h2>
    <p>
      Given a prompt as an opening line of a story, GPT writes the rest of the plot; Stable Diffusion draws an image for each sentence;
      a TTS model narrates each line, resulting in a fully animated video of a short story, replete with audio and visuals.
    </p>
    <img src="https://user-images.githubusercontent.com/25360440/210071764-51ed5872-ba56-4ed0-919b-d9ce65110185.gif" alt="out">
  </section>

  <section id="installation">
    <h2>Installation</h2>
    <h3>PyPI</h3>
    <p>
      Story Teller is available on <a href="https://pypi.org/project/storyteller-core/">PyPI</a>.
    </p>
    <pre><code>$ pip install storyteller-core</code></pre>

    <h3>Source</h3>
    <ol>
      <li>Clone the repository.</li>
      <pre><code>$ git clone https://github.com/jaketae/storyteller.git</code></pre>
      <li>Install dependencies.</li>
      <pre><code>$ pip install .</code></pre>
      <p>Note: For Apple M1/2 users, <a href="https://github.com/SamuraiT/mecab-python3">mecab-python3</a> is not available. You need to install mecab before running pip install. You can do this with Hombrew via brew install mecab. For more information, refer to <a href="https://github.com/SamuraiT/mecab-python3/issues/84">this issue</a>.</p>
      <li>(Optional) To develop locally, install dev dependencies and install pre-commit hooks. This will automatically trigger linting and code quality checks before each commit.</li>
      <pre><code>$ pip install -e .[dev]
$ pre-commit install</code></pre>
    </ol>
  </section>

  <section id="quickstart">
    <h2>Quickstart</h2>
    <p>The quickest way to run a demo is through the CLI. Simply type</p>
    <pre><code>$ storyteller</code></pre>
    <p>The final video will be saved as <code>/out/out.mp4</code>, alongside other intermediate images, audio files, and subtitles.</p>
    <p>To adjust the defaults with custom parameters, toggle the CLI flags as needed.</p>
    <pre><code>$ storyteller --help
usage: storyteller [-h] [--writer_prompt WRITER_PROMPT]
                   [--painter_prompt_prefix PAINTER_PROMPT_PREFIX] [--num_images NUM_IMAGES]
                   [--output_dir OUTPUT_DIR] [--seed SEED] [--max_new_tokens MAX_NEW_TOKENS]
                   [--writer
