import time

from .srt_service import generate_srt
from .ass_service import generate_ass
from .ffmpeg_service import render_subtitles

from .audio_enhancer import (
    enhance_audio
)

from .audio_service import (
    extract_audio
)

from .groq_service import (
    transcribe_audio
)

from .subtitle_service import (
    generate_subtitles
)

from .ai_cleanup_service import (
    cleanup_subtitles
)


def handle_video_edit(
    video_path,
    config
):

    # -------------------------
    # Extract Audio
    # -------------------------

    start = time.time()

    audio_path = extract_audio(
        video_path
    )

    print(
        f"Audio Extraction Time: {time.time() - start:.2f} sec"
    )

    # -------------------------
    # Enhance Audio
    # -------------------------

    start = time.time()

    enhanced_audio_path = enhance_audio(
        audio_path
    )

    print(
        f"Audio Enhancement Time: {time.time() - start:.2f} sec"
    )

    print(
        "Original Audio:",
        audio_path
    )

    print(
        "Enhanced Audio:",
        enhanced_audio_path
    )

    # -------------------------
    # Transcription
    # -------------------------

    start = time.time()

    language = config.get(
        "language",
        "auto"
    )

    use_audio_enhancement = config.get(
        "audio_enhancement",
        True
    )

    if use_audio_enhancement:

        transcript = transcribe_audio(
            enhanced_audio_path,
            language
        )

        print(
            "Using Enhanced Audio"
        )

    else:

        transcript = transcribe_audio(
            audio_path,
            language
        )

        print(
            "Using Original Audio"
        )

    print("\n===== RAW TRANSCRIPT =====")
    print(transcript["text"])
    print("==========================\n")

    print(
        f"Transcription Time: {time.time() - start:.2f} sec"
    )

    # -------------------------
    # Subtitle Generation
    # -------------------------

    start = time.time()

    raw_subtitles = generate_subtitles(
        transcript
    )

    print(
        f"Subtitle Time: {time.time() - start:.2f} sec"
    )

    # -------------------------
    # Gemini Cleanup
    # -------------------------

    start = time.time()

    language = config.get(
        "language",
        "hinglish"
    )

    if language == "auto":
        language = "hinglish"

    subtitles = cleanup_subtitles(
        raw_subtitles,
        language
    )

    print(
        f"Gemini Time: {time.time() - start:.2f} sec"
    )

    # -------------------------
    # Generate SRT
    # -------------------------

    srt_path = generate_srt(
        subtitles,
        "media/temp/output.srt"
    )

    print(
        "SRT Generated:",
        srt_path
    )

    # -------------------------
    # Generate ASS
    # -------------------------

    ass_path = generate_ass(
        subtitles,
        "media/temp/output.ass"
    )

    print(
        "ASS Generated:",
        ass_path
    )

    # -------------------------
    # Render Final Video
    # -------------------------

    output_video = render_subtitles(
        video_path,
        ass_path,
        "media/exports/final_video.mp4"
    )

    print(
        "Video Exported:",
        output_video
    )

    # -------------------------
    # Response
    # -------------------------

    return {

        "status": "transcription_complete",

        "video_path": video_path,

        "audio_path": audio_path,

        "enhanced_audio_path": enhanced_audio_path,

        "srt_path": srt_path,

        "ass_path": ass_path,

        "output_video": output_video,

        "subtitles": subtitles[:20],

        "config": config
    }

