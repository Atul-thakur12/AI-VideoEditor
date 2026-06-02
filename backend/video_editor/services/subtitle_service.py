def generate_subtitles(transcript):

    subtitles = []

    for segment in transcript["segments"]:

        subtitles.append({
            "start": segment["start"],
            "end": segment["end"],
            "text": segment["text"]
        })

    return subtitles