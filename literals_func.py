################################
# Local dependencies
################################
from literals import Pol, Mon, make_pol
from nums_func import find_num
import settings as sets
import lang


OptionalPol = Pol, None


def find_mon(string: str) -> OptionalPol:
    literal_start = None
    string = string.replace(")", "").replace("(", "")

    if string == "": return None  # It would return one without this

    negative_num = 0
    explicit_positive = 0

    for index, char in enumerate(string):
        try:
            int(char)
        except ValueError:
            lang.write_error_log(
                "ValueError",
                "literals_func.py|find_mon()|for|except",
                sets.settings["debug_mode"]
            )

            if char == "-":
                negative_num = 1

            elif char == "+":
                explicit_positive = 1

            elif char in ".,":
                continue

            else:
                if index == 1:
                    literal_start = index - negative_num - explicit_positive
                else:
                    literal_start = index
                    negative_num = 0
                    explicit_positive = 0
                break

    if literal_start is None: literal_start = len(string)

    if literal_start == 0:
        if negative_num == 0: number = 1
        else: number = -1

    else: number = find_num(string[0:literal_start])

    if number is None: return None

    letters = {}
    last_letter = ""
    temp_number = ""
    ciphers = "0123456789^."  # The "^" character is there just to not be considered in the letters
    allowed_letters = "abcdefghijklmnopqrstuvwxyz"  # To avoid not-operating symbols (@#?...) being considered letters
    literal = string[literal_start + negative_num + explicit_positive:]

    for char in literal:
        if (char not in ciphers) and (char in allowed_letters):
            letters[last_letter] = make_pol(1) if temp_number == "" else make_pol(find_num(temp_number))

            temp_number = ""
            letters[char] = make_pol(1)
            last_letter = char

        elif char in ciphers:
            temp_number += char if char != "^" else ""

        else:
            return None

    letters[last_letter] = make_pol(1) if temp_number == "" else make_pol(find_num(temp_number))

    letters[""] = 1

    found_monomial = Mon(letters=letters, number=number)

    return Pol([found_monomial])
