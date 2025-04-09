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
#!/usr/bin/python

import sys


def parse_file(words_file, from_lang, to_lang):
    try:
        with open(words_file, 'r') as file:
            for line_number, line in enumerate(file, start=1):
                if from_lang <= line_number <= to_lang:
                    print(f"Line {line_number}: {line.strip()}")
    except FileNotFoundError:
        print(f"Error: The file '{words_file}' was not found.")
    except ValueError:
        print("Error: Invalid input for 'from_lang' or 'to_lang'. They must be integers.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python word_reader.py <words_file> <from_lang> <to_lang>")
    else:
        words_file = sys.argv[1]
        try:
            from_lang = int(sys.argv[2])
            to_lang = int(sys.argv[3])
            parse_file(words_file, from_lang, to_lang)
        except ValueError:
            print("Error: 'from_lang' and 'to_lang' must be integers.")
