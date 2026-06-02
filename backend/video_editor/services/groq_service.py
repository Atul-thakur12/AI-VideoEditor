import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def transcribe_audio(
    audio_path,
    language="auto"
):

    try:

        # -------------------------
        # Language Mapping
        # -------------------------

        groq_language = None

        if language == "hindi":
            groq_language = "hi"

        elif language == "hinglish":
            groq_language = "hi"

        elif language == "english":
            groq_language = "en"

        with open(audio_path, "rb") as audio_file:

            transcription = client.audio.transcriptions.create(
                file=audio_file,
                model="whisper-large-v3-turbo",
                language=groq_language,
                response_format="verbose_json",
                timestamp_granularities=["segment"]
            )

        print(
            "Detected Language:",
            transcription.language
        )

        result = {
            "text": transcription.text,
            "segments": []
        }

        # -------------------------
        # Segment Handling
        # -------------------------

        if hasattr(
            transcription,
            "segments"
        ):

            for segment in transcription.segments:

                result["segments"].append({
                    "start": segment["start"],
                    "end": segment["end"],
                    "text": segment["text"].strip()
                })

        # -------------------------
        # Fallback
        # -------------------------

        if len(result["segments"]) == 0:

            result["segments"].append({
                "start": 0,
                "end": 9999,
                "text": transcription.text
            })

        return result

    except Exception as e:

        print(
            "Groq Transcription Failed:",
            str(e)
        )

        return {
            "text": "",
            "segments": []
        }


def test_groq():

    try:

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": "Say Hello"
                }
            ]
        )

        print(
            response.choices[0]
            .message
            .content
        )

    except Exception as e:

        print(
            "Groq Test Failed:",
            str(e)
        )

