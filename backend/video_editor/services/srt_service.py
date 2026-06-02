def format_time(seconds):

    hours = int(seconds // 3600)

    minutes = int(
        (seconds % 3600) // 60
    )

    secs = int(seconds % 60)

    milliseconds = int(
        (seconds - int(seconds)) * 1000
    )

    return (
        f"{hours:02}:{minutes:02}:"
        f"{secs:02},{milliseconds:03}"
    )


def generate_srt(
    subtitles,
    output_path
):

    with open(
        output_path,
        "w",
        encoding="utf-8"
    ) as f:

        for i, sub in enumerate(
            subtitles,
            start=1
        ):

            f.write(f"{i}\n")

            f.write(
                f"{format_time(sub['start'])}"
                f" --> "
                f"{format_time(sub['end'])}\n"
            )

            f.write(
                f"{sub['text']}\n\n"
            )

    return output_path