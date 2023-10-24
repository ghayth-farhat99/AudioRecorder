from flask import Flask, render_template, request, redirect, url_for, send_file
import pyaudio
import wave
import threading  # Add the threading module
import time  # Add the time module

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0  # Disable caching during development

# Initialize the timer variables
recording_finished = False
countdown = 15  # Set the initial countdown time

def update_timer():
    global countdown
    while countdown > 0:
        time.sleep(1)
        countdown -= 1

# Add a route to serve the recorded audio file
@app.route('/download_audio')
def download_audio():
    audio_file = 'output.wav'  # Replace with the actual path to your recorded audio file
    return send_file(audio_file, as_attachment=True)

@app.route('/')
def index():
    return render_template('index.html', recording_finished=recording_finished)

@app.route('/record', methods=['POST'])
def record_audio():
    global recording_finished
    global countdown
    # Start the timer thread
    timer_thread = threading.Thread(target=update_timer)
    timer_thread.start()
    
    # Add code here to start and stop audio recording (use the code you provided)
    # Save the recorded audio to a WAV file
    # Parameters for audio recording
    FORMAT = pyaudio.paInt16  # Sample format
    CHANNELS = 1  # Number of audio channels (1 for mono, 2 for stereo)
    RATE = 44100  # Sample rate (samples per second)
    RECORD_SECONDS = 15  # Duration of the recording
    OUTPUT_FILENAME = "output.wav"  # Output WAV file name

    # Initialize PyAudio
    audio = pyaudio.PyAudio()

    # Set up the audio stream
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=1024)

    print("Recording...")

    frames = []

    # Record audio
    for _ in range(0, int(RATE / 1024 * RECORD_SECONDS)):
        data = stream.read(1024)
        frames.append(data)

    print("Recording finished.")
    recording_finished = True

    # Stop and close the audio stream
    stream.stop_stream()
    stream.close()

    # Terminate PyAudio
    audio.terminate()

    # Save the recorded audio to a WAV file
    with wave.open(OUTPUT_FILENAME, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

    print(f"Audio saved to {OUTPUT_FILENAME}")
    return redirect(url_for('index'))
# Change the route name to 'serve_audio' instead of 'download_audio'
@app.route('/serve_audio')
def serve_audio():
    audio_file = 'output.wav'  # Replace with the actual path to your recorded audio file
    return send_file(audio_file, mimetype='audio/wav')

if __name__ == '__main__':
    app.run(debug=True)
