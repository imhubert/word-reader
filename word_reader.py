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
from googletrans import Translator
from gtts import gTTS
from pydub import AudioSegment

def parse_file(words_file)->list:
    try:
        output = []
        with open(words_file, 'r') as file:
            for line_number, line in enumerate(file, start=1):
                output.append(line)
        return output
    except FileNotFoundError:
        print(f"Error: The file '{words_file}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

async def translate_text(text, src_lang:str, dest_lang:str):
    try:
        translator = Translator()
        translated = await translator.translate(text, src=src_lang, dest=dest_lang)
        return translated.text
    except Exception as e:
        return f"An error occurred: {e}"

def generate_audio(text_src:str, src_lang:str, text_dest:str, dest_lang:str):

    # Convert the texts to audio using gTTS
    tts1 = gTTS(text=text_src, lang=src_lang, slow=False)
    tts2 = gTTS(text=text_dest, lang=dest_lang, slow=False)

    # Check if 'output' folder exists, otherwise create it
    output_folder = "output"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Created folder: {output_folder}")

    # Save both texts as audio files in 'output' folder
    part1_path = os.path.join(output_folder, "part1.mp3")
    part2_path = os.path.join(output_folder, "part2.mp3")
    tts1.save(part1_path)
    tts2.save(part2_path)

    # Load the audio files using pydub
    audio1 = AudioSegment.from_file(os.path.join(output_folder, "part1.mp3"))
    audio2 = AudioSegment.from_file(os.path.join(output_folder, "part2.mp3"))

    # Create 2 seconds of silence
    silence = AudioSegment.silent(duration=1000)

    # Combine audio1, silence, and audio2
    combined_audio = audio1 + silence + audio2

    # Export the combined audio to 'output' folder
    final_audio_path = os.path.join(output_folder, f"{text_src}.mp3")
    combined_audio.export(final_audio_path, format="mp3")
    os.remove(part1_path)
    os.remove(part2_path)

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: word_reader.py <words_file> <from_lang> <to_lang>")
    else:
        words_file = sys.argv[1]
        from_lang = sys.argv[2]
        to_lang = sys.argv[3]
        words = parse_file(words_file)
        trans_words = []
        print("start translating text\n")
        for word in words:
            trans_words.append(asyncio.run(translate_text(word, from_lang, to_lang)))
        if len(trans_words) != len(words):
            print("Incorrect output")
            exit()
        i = 0
        print("start generate audio\n")
        for i in range(0, len(words)):
            generate_audio(words[i], from_lang, trans_words[i], to_lang)
            i+=1
        print("Done!")

        
        
        
