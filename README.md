# Simple OpenAI Speech-to-Text and Summarization

[日本語版はこちら](README_ja.md)

This project provides a simple way to transcribe audio files to text using OpenAI's Whisper model and then summarize the transcribed text using OpenAI's GPT-4 model.

## Prerequisites

*   Python 3.7+
*   OpenAI API key
*   An OpenAI organization

## Installation

1.  Clone the repository:

    ```bash
    git clone https://github.com/masykur8d/simple_openai_speech_to_text.git
    cd simple_openai_speech_to_text
    ```
2.  Create a virtual environment:

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```
3.  Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1.  Set your OpenAI organization and API key in `simple_openai_speech_to_text.py`.
2.  Place your audio files in the `/audio_files` directory.
3.  Run the script:

    ```bash
    python simple_openai_speech_to_text.py
    ```

    This will transcribe the audio files, summarize the transcriptions, and save the results to `all_translation_result.xlsx`.

## Contributing

Please read `CONTRIBUTING.md` for details on how to contribute to this project.

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.
