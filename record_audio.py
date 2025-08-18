import pyaudio
import wave
from datetime import datetime, timezone
import os
import boto3
from pathlib import Path

FORMAT = pyaudio.paInt16
CHANNELS = 1
SAMPLE_RATE = 16000
SECONDS = 10
CHUNK = 1024
DEFAULT_DIR = "recordings"
PATIENT_ID = "patient001"
BUCKET_NAME = "apnearecordings"

def record_audio(format=FORMAT, channels=CHANNELS, rate=SAMPLE_RATE, seconds=SECONDS, input=True, chunk=CHUNK):
    audio = pyaudio.PyAudio()
    stream = audio.open(format=format, channels=channels, rate=rate, input=True, frames_per_buffer=chunk)
 
    print(f"Recording for {SECONDS} seconds...")
    frames = []

    for _ in range(0, int(rate / chunk * seconds)):
        data = stream.read(chunk)
        # apppend to frames array
        frames.append(data)

    stream.stop_stream()
    stream.close()
    audio.terminate()

    print("Recording is finished!!")
    return frames, audio

# create a dir of format [patient_d]/YEAR/MONTH/DAY/HOUR/MIN/SEC
def build_dir(patient_id=PATIENT_ID, def_dir=DEFAULT_DIR):
    now = datetime.now()
    directory = Path(def_dir) / patient_id / now.strftime("%Y/%m/%d/%H/%M/%S")
    directory.mkdir(parents=True, exist_ok=True)
    return directory

# save as .wav
def save_wav(frames, path, audio, format=FORMAT, rate=SAMPLE_RATE, channels=CHANNELS):
    recorded_file = path / "recorded.wav"

    with wave.open(str(recorded_file), 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(audio.get_sample_size(format))
        wf.setframerate(rate)
        wf.writeframes(b''.join(frames))

    print(f"Saved as {recorded_file}")
    return recorded_file

# upload to s3 bucket
def upload_to_s3(file_path, bucket, patient_id):
    timestamp = datetime.now(timezone.utc)
    # data will be saved to the location similar to the format for saving recordings locally
    # the only exception is that s3 buckets have prefixes, not directories
    prefix = f"{patient_id}/{timestamp:%Y/%m/%d/%H/%M/%S}"
    key = f"{prefix}/{os.path.basename(file_path)}"

    s3 = boto3.client("s3")
    # if not encrypted, bucket policy will forbid from uploading data to the bucket
    s3.upload_file(Filename=str(file_path), Bucket=bucket, Key=key, ExtraArgs={"ServerSideEncryption": "AES256", "ContentType": "audio/wav"})

    print(f"Uploaded to s3://{bucket}/{key}")


if __name__ == "__main__":
    frames, audio = record_audio()
    output_dir = build_dir()
    wav_file = save_wav(frames, output_dir, audio)
    upload_to_s3(wav_file, BUCKET_NAME, PATIENT_ID)

