import os
import json

from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def cleanup_subtitles(
    subtitles,
    language="hinglish"
):

    try:

        subtitle_lines = [
            sub["text"]
            for sub in subtitles
        ]

        # ----------------------------------
        # Output Language Rules
        # ----------------------------------

        if language == "hindi":

            language_instruction = """
TARGET LANGUAGE: HINDI

STRICT RULES:

- Use ONLY Devanagari script.
- Do NOT use English sentences.
- Correct Hindi grammar.
- Preserve original meaning.
- Use natural spoken Hindi.
"""

        elif language == "english":

            language_instruction = """
TARGET LANGUAGE: ENGLISH

STRICT RULES:

- Use ONLY English.
- Translate Hindi/Hinglish into English.
- No Hindi words.
- No Devanagari characters.
- Use natural spoken English.
"""

        else:

            language_instruction = """
TARGET LANGUAGE: HINGLISH

STRICT RULES:

- Use ONLY Roman script.
- Never use Devanagari characters.
- Keep English words in English.
- Convert Hindi words to Roman Hindi.
- Use natural creator-style Hinglish.

Examples:

Aapko nahi pata ki questions kahan se pooche jayenge.
University exam par focus karo.
Sirf syllabus revise karo.
Agar ek saal bacha hai to 50-50 split rakho.

Common Corrections:

AIAPGT -> AIAPGET
BIMS -> BMS
BGT -> AIAPGET
University -> University
Exam -> Exam
"""

        # ----------------------------------
        # Gemini Prompt
        # ----------------------------------

        prompt = f"""
You are an expert subtitle correction engine.

{language_instruction}

CRITICAL REQUIREMENTS:

1. Correct spelling mistakes.
2. Correct grammar mistakes.
3. Preserve original meaning.
4. Keep subtitle length similar.
5. Do NOT summarize.
6. Do NOT explain.
7. Do NOT add information.
8. Do NOT remove information.
9. Do NOT add notes.
10. Do NOT write markdown.
11. Do NOT write code blocks.
12. Do NOT merge subtitle lines.
13. Do NOT split subtitle lines.
14. Number of output lines MUST exactly equal number of input lines.
15. Return ONLY a JSON array of strings.
16. Every subtitle line must be entirely in the target language.
17. Never mix Hindi and English scripts in the same subtitle.
18. Correct obvious transcription mistakes using context.
19. If uncertain, keep the original wording instead of inventing content.

Input Subtitle Count:
{len(subtitle_lines)}

Input:

{json.dumps(subtitle_lines, ensure_ascii=False)}

Return format example:

[
  "Subtitle 1",
  "Subtitle 2",
  "Subtitle 3"
]
"""

        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=prompt
        )

        cleaned_text = response.text.strip()

        cleaned_text = (
            cleaned_text
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

        cleaned_lines = json.loads(
            cleaned_text
        )

        print(
            f"Input Lines: {len(subtitle_lines)}"
        )

        print(
            f"Output Lines: {len(cleaned_lines)}"
        )

        # ----------------------------------
        # Safety Check
        # ----------------------------------

        if len(cleaned_lines) != len(subtitles):

            print(
                "Gemini returned mismatched subtitle count."
            )

            return subtitles

        cleaned_subtitles = []

        for i, sub in enumerate(subtitles):

            cleaned_subtitles.append({
                "start": sub["start"],
                "end": sub["end"],
                "text": cleaned_lines[i]
            })

        return cleaned_subtitles

    except Exception as e:

        print(
            "Gemini Cleanup Failed:",
            str(e)
        )

        return subtitles

