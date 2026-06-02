import os


def seconds_to_ass_time(seconds):

    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = seconds % 60

    return f"{hours}:{minutes:02}:{secs:05.2f}"


def generate_ass(
    subtitles,
    output_path
):

    os.makedirs(
        os.path.dirname(output_path),
        exist_ok=True
    )

    ass_header = """
[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding

Style: Default,Poppins,26,&H00FFFFFF,&H0000FFFF,&H00000000,&H64000000,1,0,0,0,100,100,0,0,1,3,0,2,40,40,100,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

    with open(
        output_path,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(ass_header)

        for sub in subtitles:

            start = seconds_to_ass_time(
                sub["start"]
            )

            end = seconds_to_ass_time(
                sub["end"]
            )

            text = (
                sub["text"]
                .replace("\n", " ")
            )

            line = (
                f"Dialogue: 0,{start},{end},Default,,0,0,0,,{text}\n"
            )

            f.write(line)

    print(
        "ASS Generated:",
        output_path
    )

    return output_path