import os
import ffmpeg


def extract_audio(video_path):

    os.makedirs(
        "media/temp",
        exist_ok=True
    )

    audio_path = os.path.join(
        "media",
        "temp",
        "audio.wav"
    )

    (
        ffmpeg
        .input(video_path)
        .output(
            audio_path,
            ac=1,      # mono
            ar=16000   # 16kHz
        )
        .overwrite_output()
        .run(quiet=True)
    )

    return audio_path