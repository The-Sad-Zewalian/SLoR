# SLoR
 ***Spotify Local Recoder***

 The main concept of the script is that we record the audio played on the main speaker and then save the files locally.

 ***Note-1**: The script runs only on `Windows` due to the usage of `PyAudioWPatch` and `pywin32` packages.*
 
 ***Note-2**: Only Spotify should be running.*
___

### 1. Installation
Download the main.py file and install the packages listed in the `requirements.txt`.
```bash
pip install -r requirements.txt
```

### 2. Usage
The script will create an output directory where it runs.
```bash
python3 main.py
```
___


### Requirements
The projects require Python 3 and the following libraries:
- **PyAudioWPatch**
- **psutil**
- **PyAutoGUI**