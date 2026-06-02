import os
import subprocess


def render_subtitles(
    video_path,
    ass_path,
    output_path
):

    os.makedirs(
        os.path.dirname(output_path),
        exist_ok=True
    )

    video_path = video_path.replace(
        "\\",
        "/"
    )

    ass_path = ass_path.replace(
        "\\",
        "/"
    )

    subtitle_filter = (
        f"ass={ass_path}"
    )

    command = [

        "ffmpeg",

        "-y",

        "-i",
        video_path,

        "-vf",
        subtitle_filter,

        "-c:v",
        "libx264",

        "-preset",
        "fast",

        "-crf",
        "23",

        "-c:a",
        "copy",

        output_path
    ]

    print("\n===== ASS DEBUG =====")
    print("ASS File:", ass_path)
    print("Subtitle Filter:", subtitle_filter)
    print("=====================\n")

    subprocess.run(
        command,
        check=True
    )

    return output_path
