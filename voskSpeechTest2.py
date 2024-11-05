import sys
import os
from vosk import Model, KaldiRecognizer
import pyaudio
import json  # Add this for parsing JSON results if needed

# load the vosk model !!
if not os.path.exists("model"):
    print("Please download the model from https://alphacephei.com/vosk/models and unpack as 'model' in the current folder.")
    sys.exit(1)

# initialise the provided Vosk model (small-en-us-0.15)
model = Model("model")
recognizer = KaldiRecognizer(model, 16000)

# initialise pyaudio input stream
mic = pyaudio.PyAudio()

try:
    stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
    stream.start_stream()
    print("Listening...")

    # continuously/repeatedly(?) process audio data (idk which word sounds right)
    while True:
        data = stream.read(4000, exception_on_overflow=False)  # Handle buffer overflow gracefully
        if len(data) == 0:
            continue

        # check if complete result is available
        if recognizer.AcceptWaveform(data):
            result = recognizer.Result()
            result_dict = json.loads(result)  # Parse JSON for structured data
            print("Recognized:", result_dict.get("text", ""))  # Extract and print recognized text
        else:
            # Print partial recognition result
            partial_result = recognizer.PartialResult()
            partial_dict = json.loads(partial_result)
            print("Partial:", partial_dict.get("partial", ""))

except KeyboardInterrupt:
    print("\nStopped by user.")

finally:
    # close stream and pyaudio
    stream.stop_stream()
    stream.close()
    mic.terminate()