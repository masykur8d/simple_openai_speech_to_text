import openai
import os
import aiometer
import asyncio
from functools import partial
from tenacity import retry, stop_after_attempt, wait_fixed
import pandas as pd

# Set OpenAI organization (replace with your actual organization ID)
openai.organization = "insert your OpenAI organization here"
# Set OpenAI API key (replace with your actual API key)
openai.api_key      = "insert your OpenAI api key here"

# Async function to transcribe speech from an audio file to text using OpenAI's Whisper model.
@retry(stop=stop_after_attempt(3), wait=wait_fixed(0.5), reraise=True)
async def speech_to_text(filepath: str) -> str:
    """
    Transcribes speech from an audio file to text using OpenAI's Whisper model.
    Retries up to 3 times with a fixed delay of 0.5 seconds between attempts.

    Args:
        filepath (str): The path to the audio file.

    Returns:
        str: The transcribed text.

    Raises:
        Exception: If transcription fails after multiple retries.
    """
    print(f'Start processing: {filepath}')
    try:
        # Open the audio file in binary read mode
        with open(filepath, mode="rb") as audio_file:

            # Transcribe the audio file using OpenAI's asychronous API
            response = await openai.Audio.atranscribe(
                model = "whisper-1",  # Speech-to-Text model
                file  = audio_file,   # Audio file
            )
        print(f'Finish processing: {filepath}')
        # Return the transcribed text
        return response.text
    except Exception as e:
        print(f'Error on speech_to_text. Error detail: {e}')
        raise

# Async function to summarize text using OpenAI's GPT-4 model.
@retry(stop=stop_after_attempt(3), wait=wait_fixed(0.5), reraise=True)
async def text_to_summary(input_text:str) -> str:
    """
    Summarizes the given text using OpenAI's GPT-4 model.
    Retries up to 3 times with a fixed delay of 0.5 seconds between attempts.

    Args:
        input_text (str): The text to summarize.

    Returns:
        str: The summarized text.

    Raises:
        Exception: If summarization fails after multiple retries.
    """
    print(f'Processing summary')
    try:
        # Define the message payload for the OpenAI ChatCompletion API
        message = [
            {"role": "user", "content": f"{input_text}\nPlease summarize this conversation for a report to the client."},
        ]
        # Create a chat completion request to OpenAI
        summary_response = await openai.ChatCompletion.acreate(
            model = "gpt-4",  # Specify the GPT-4 model
            messages = message   # Pass the message payload
        )

        # Extract and return the summarized text from the response
        return summary_response['choices'][0]['message']['content']
    except Exception as e:
        print(f'Error on text_to_summary. Error detail: {e}')
        raise

# Async main function to orchestrate audio transcription and text summarization.
async def main():
    """
    Orchestrates audio transcription and text summarization for multiple audio files.
    It reads audio files from a directory, transcribes them, summarizes the transcribed text,
    and saves the results to an Excel file.
    """
    # Initialize lists to store tasks and filenames
    all_translation_task = []
    all_file_name = []
    # Define the target directory containing audio files
    target_directory = '/audio_files'
    # Iterate over files in the target directory
    for filename in os.listdir(target_directory):
        # Check if the file has a supported audio extension
        if filename.endswith(('.flac', '.m4a', '.mp3', '.mp4', '.mpeg', '.mpga', '.oga', '.ogg', '.wav', '.webm')):
            # Create the full file path
            file_path = os.path.join(target_directory, filename)
            # Append the filename to the list
            all_file_name.append(filename)
            # Create a partial function for the speech_to_text task
            all_translation_task.append(
                partial(speech_to_text, file_path)
            )
    # Run all translation tasks concurrently with a maximum of 4 concurrent tasks
    all_translation_task_result = await aiometer.run_all(all_translation_task, max_at_once=4)

    # Initialize a list to store summary tasks
    create_summary_task = []
    # Iterate over the transcribed texts
    for transcript in all_translation_task_result:
        # Create a partial function for the text_to_summary task
        create_summary_task.append(
            partial(text_to_summary, str(transcript))
        )
    # Run all summary tasks concurrently with a maximum of 4 concurrent tasks
    all_summary_task_response = await aiometer.run_all(create_summary_task, max_at_once=4)

    # Initialize a list to store all translation results
    list_all_translation = []
    # Iterate over the translation task results
    for position, task_result in enumerate(all_translation_task_result):
        # Append the translation result to the list
        list_all_translation.append(
            {'通番': f'{position+1}', 'ファイル名': all_file_name[position], 'OpenAI文字起こしの結果':task_result, 'ChatGPT要約': all_summary_task_response[position]}
        )
    # Create a Pandas DataFrame from the list of translation results
    df_all_translation = pd.DataFrame(list_all_translation)

    # Save the DataFrame to an Excel file
    df_all_translation.to_excel('all_translation_result.xlsx', index=False)

# Entry point of the script
if __name__ == '__main__':
    # Run the main function asynchronously
    asyncio.run(main())
