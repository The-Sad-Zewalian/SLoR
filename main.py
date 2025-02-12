"""
A simple example of recording Spotify songs from speakers ('What you hear') using the WASAPI loopback device.
"""

import pyaudiowpatch as pyaudio
import wave
import pyautogui, win32gui, psutil, win32process
import os
from threading import Thread
import time


# Set the global variables used
CHANGED = False
current_song = ''

# Create the output directory
output_dir = "./songs"
os.makedirs(output_dir, exist_ok=True) 

def get_song_name():
    """
    Keeps getting the name of the song playing.
    """
    global current_song, CHANGED
    while True:
        spotify_pids = []
        for proc in psutil.process_iter(['pid', 'name']):
            if 'spotify' in proc.info['name'].lower():
                spotify_pids.append(proc.info['pid'])

        if len(spotify_pids)==0:
            print("Spotify is not running!")
    
        for x in pyautogui.getAllTitles():  
            hwnd = win32gui.FindWindow(None, x)
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            if pid in spotify_pids:
                new_name = x+'.wav'
                CHANGED = (current_song!=new_name)
                current_song = new_name
                break
            
        time.sleep(0.5)


with pyaudio.PyAudio() as p:
    """
    Create PyAudio instance via context manager.
    """

    try:
        # Get loopback of default WASAPI speaker
        default_speakers = p.get_default_wasapi_loopback()

    except OSError:
        exit()

    RATE = int(default_speakers["defaultSampleRate"])
    SAMPLE_SIZE = p.get_sample_size(pyaudio.paInt8)
    
    namechecker = Thread(target=get_song_name, args=())
    namechecker.start()
    time.sleep(1)

    # Keeps recording "what you hear" and saving the files based on the title of the spotify window
    while True:
        # Reset the flag for new songs.
        CHANGED = False

        # Create the save path
        song_path = os.path.join(output_dir, current_song)

        # Check if the path exists to avoid recording the same song again.
        if not os.path.exists(song_path):
            wave_file = wave.open(song_path, 'wb')
            wave_file.setnchannels(default_speakers["maxInputChannels"])
            wave_file.setsampwidth(SAMPLE_SIZE)
            wave_file.setframerate(RATE)

            with p.open(
                    format=pyaudio.paInt8,
                    channels=default_speakers["maxInputChannels"],
                    rate=RATE,
                    input=True,
                    input_device_index=default_speakers["index"],
            ) as stream:
                """
                Opena PA stream via context manager.
                After leaving the context, everything will
                be correctly closed(Stream, PyAudio manager)            
                """
                while not CHANGED:
                    """Record audio step-by-step"""
                    data = stream.read(SAMPLE_SIZE)
                    wave_file.writeframes(data)

            # Close the file
            wave_file.close()