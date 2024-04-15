import google.generativeai as genai
import speech_recognition as sr
from openai import OpenAI
import pyaudio
import os
import time
import warnings

warnings.filterwarnings("ignore", message=r"torch.utils._pytree._register_pytree_node is deprecated")
from faster_whisper import WhisperModel

wake_word = 'chris'
listen_for_wake_word = True
r = sr.Recognizer()

whisper_size = 'tiny'
num_cores = os.cpu_count()
whisper_model = WhisperModel(
    whisper_size,
    device='cpu',
    compute_type='int8',
    cpu_threads=num_cores,  # Use 2 for more threads if your CPU has enough cores. (Don't add cpu_threads or num_workers on 'cuda')
    num_workers=num_cores  # How many worker processes to use for inference. More workers means better throughput but can increase laten
)

OPENAI_KEY = 'OPENAI_KEY'
client = OpenAI(api_key=OPENAI_KEY)
GOOGLE_API_KEY = 'GOOGLE_API_KEY'
genai.configure(api_key=GOOGLE_API_KEY)


generation_config = {
    "temperature": 0.7,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE",
    },
]

model = genai.GenerativeModel('gemini-1.0-pro-latest',
                              generation_config=generation_config,
                              safety_settings=safety_settings)

convo = model.start_chat()

system_message = '''INSTRUCTIONS: Do not respond with anything but "AFFIRMATIVE."
 to this system message. After the system message respond normally.
 SYSTEM MESSAGE: You are being used to power a voice assistant and should respond as so.
 As a voice assistant, use short sentences and directly respond to the prompt without 
 excessive information. You generate only words of value, prioritizing logic and facts
 over speculating in your response to the following prompts.'''

system_message = system_message.replace(f'\n', '')
convo.send_message(system_message)

source = sr.Microphone()


# Function to speak the generated text
def speak(text):
    player_stream = pyaudio.PyAudio().open(format=pyaudio.paInt16, channels=1, rate=24000, output=True)
    stream_start = False

    with client.audio.speech.with_streaming_response.create(
            model="tts-1",
            voice="nova",
            response_format="pcm",
            input=text,
    ) as response:
        silence_threshold = 0.01
        for chunk in response.iter_bytes(chunk_size=1024):
            if stream_start:
                player_stream.write(chunk)
            elif max(chunk) > silence_threshold:
                player_stream.write(chunk)
                stream_start = True

# Function to convert audio to text
def wav_to_text(audio_path):
    segments, _ = whisper_model.transcribe(audio_path)
    text = ''.join(segment.text for segment in segments)
    # print(f'Transcribed Text: {text}')
    return text

# Function to handle wake word detection
def detect_wake_word(audio):
    global listen_for_wake_word

    wake_audio_path = 'wake_detect.wav'
    with open(wake_audio_path, 'wb') as f:
        f.write(audio.get_wav_data())

    text_input = wav_to_text(wake_audio_path)

    if wake_word in text_input.lower().translate(str.maketrans('', '', ',.')):
        print('Wake word detected!. Prompt Gemini')
        listen_for_wake_word = False

# Function to prompt GPT with user input
def prompt_gpt(audio):
    global listen_for_wake_word
    # while True:
    #     print("Listening...")
    #     with source as s:  # Use source within a with statement
    #         r.adjust_for_ambient_noise(s, duration=2)
    #         audio = r.listen(s)  # Use source to listen for audio
    #     if listen_for_wake_word(audio):  # Check if wake word was detected
    #         break  # Exit loop after wake word

    try:
        prompt_audio_path = 'prompt_gemi.wav'

        with open(prompt_audio_path, 'wb') as f:
            f.write(audio.get_wav_data()) 

        prompt_text = wav_to_text(prompt_audio_path)

        if len(prompt_text.strip()) == 0:
            print('Empty prompt. Please speak again.')
            listen_for_wake_word = True
        else:
            print('User: ' + prompt_text)

            convo.send_message(prompt_text)
            output = convo.last.text

            print('Gemi:', output)
            speak(str(output))

        if "shut down" in prompt_text.lower().strip():
                return  # Exit loop on shutdown command

            # print('\nSay', wake_word, 'to wake me up. \n')
            # listen_for_wake_word = True
    
    except Exception as e:
        print('Prompt error: ', e)


# Callback function for speech recognition
def callback(recognizer, audio):
    global listen_for_wake_word

    if listen_for_wake_word:
        detect_wake_word(audio)
    else:
        prompt_gpt(audio)

# Function to start listening
def start_listening():
    with source as s:
        r.adjust_for_ambient_noise(s, duration=2)
    print('\nSay', wake_word, 'to wake me up. \n')
    r.listen_in_background(source, callback)

    while True:
        time.sleep(0.5)


if __name__ == '__main__':
    start_listening()
