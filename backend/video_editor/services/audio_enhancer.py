import os
import ffmpeg


def enhance_audio(audio_path):

    os.makedirs(
        "media/temp",
        exist_ok=True
    )

    enhanced_path = os.path.join(
        "media",
        "temp",
        "enhanced_audio.wav"
    )

    (
        ffmpeg
        .input(audio_path)
        .output(
            enhanced_path,
            af="highpass=f=200,lowpass=f=3000"
        )
        .overwrite_output()
        .run(quiet=True)
    )

    return enhanced_path