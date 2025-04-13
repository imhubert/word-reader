#!/usr/bin/python3
###############################################################################
# word_reader.py
#
# Copyright (C) 2025.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
###############################################################################
import sys
import asyncio
import os
import shutil
from googletrans import Translator
from gtts import gTTS
from pydub import AudioSegment

def parse_file(words_file) -> list:
    try:
        with open(words_file, 'r') as file:
            return [line.strip() for line in file]
    except Exception as e:
        print(f"File error: {e}")
        return []

async def multi_translate(text, languages: list) -> list:
    translator = Translator()
    results = [text]
    current_text = text

    for i in range(len(languages) - 1):
        src = languages[i]
        dest = languages[i + 1]

        # Await the async translate method directly
        translated_obj = await translator.translate(current_text, src=src, dest=dest)
        current_text = translated_obj.text
        results.append(current_text)

    return results

output_folder = "audio_output"

def generate_audio_chain(texts: list, languages: list, base_filename: str):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    silence = AudioSegment.silent(duration=1000)
    combined_audio = AudioSegment.empty()

    for i, (text, lang) in enumerate(zip(texts, languages)):
        tts = gTTS(text=text, lang=lang, slow=False)
        temp_path = os.path.join(output_folder, f"temp_{i}.mp3")
        tts.save(temp_path)

        audio_part = AudioSegment.from_file(temp_path)
        combined_audio += audio_part + silence

        os.remove(temp_path)

    final_audio_path = os.path.join(output_folder, f"{base_filename}.mp3")
    combined_audio.export(final_audio_path, format="mp3")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: word_reader.py <words_file> <lang1> <lang2> ... <langN>")
        sys.exit(1)

    words_file = sys.argv[1]
    language_chain = sys.argv[2:]  # e.g. ['en', 'fr', 'de', 'es']
    words = parse_file(words_file)

    if not words:
        sys.exit(1)

    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)

    print("Starting multi-language translation and audio...\n")

    for word in words:
        translations = asyncio.run(multi_translate(word, language_chain))
        generate_audio_chain(translations, language_chain, base_filename=translations[0])

    print("Task Done! Bye!")
