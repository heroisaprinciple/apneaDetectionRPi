# 🔹 Raspberry Pi Apnea Recorder (Raw Audio + AWS S3 Upload)

This repository provides a Python script to record **10-second raw audio segments** using a **USB microphone on Raspberry Pi**, save the recordings locally, and upload them to an **AWS S3 bucket**.

For now there is no filtering implemented.

This repository is a significant part of [Apnea Detection](https://github.com/heroisaprinciple/sleepApneaDetection) repository.

---

## Overview

- Records 10-second mono audio at 16 kHz
- Stores as `.wav` in a timestamped directory structure
- Uploads to an encrypted AWS S3 bucket
- Fully configurable with environment variables and constants

---

## Environment Setup

### 1. Clone the Repository
```bash
git clone https://github.com/heroisaprinciple/apneaDetectionRPi.git
cd apneaDetectionRPi
```

### 2. Create and Activate a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

#### `requirements.txt`
```
pyaudio
boto3
librosa
numpy
scipy
matplotlib
soundfile
```

---

## Usage

### Run the recorder:
```bash
python record_and_upload.py
```

Each run will:
1. Record a 10-second segment using `pyaudio`
2. Save it to:
```
recordings/PATIENT_ID/YYYY/MM/DD/HH/MM/SS/recorded_raw.wav
```

3. Upload it to the S3 bucket (apnearecordings) or create it yourself!
```
s3://apnearecordings/PATIENT_ID/YYYY/MM/DD/HH/MM/SS/recorded_raw.wav
```

**Please note that in order to access apnearecordings, you need to be admin user and have admin credentials. Your root user must share those with you.
Please store as those as env varibales and never expose in code.
If you want to play with cloud, you might want to create a separate bucket yourself. In that case, no worries.**

## Future Improvements
- Add filtering (bandpass, noise reduction)
- Include audio visualizations (spectrogram/FFT) -> right now it happens on PC
