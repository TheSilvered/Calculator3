################################
# Local dependencies
################################
import nums_func
import lang
from settings import update_settings

################################
# External modules
################################
from os import path
from json import load, dump


LANGUAGE = lang.language
last_result = None

# It opens the settings here because they can be modified
with open("settings/settings.json") as json_settings:
    settings = load(json_settings)

with open("settings/lang_acronyms.json") as json_acronym_lang:
    acronym_lang = load(json_acronym_lang)


def command(usr_inp) -> str:
    global json_settings, settings, acronym_lang, json_acronym_lang, LANGUAGE

    def switch_settings(dict_key: str):
        global settings, LANGUAGE

        settings[dict_key] = not settings[dict_key]

        set_to = str(settings[dict_key]).lower()

        parameter_changed = getattr(LANGUAGE.out, dict_key)
        is_now = LANGUAGE.out.switch
        true_or_false = getattr(LANGUAGE.lan, set_to)

        print(f"'{parameter_changed}' {is_now} {true_or_false}\n")

    cmd = usr_inp[:5]  # Defines what command is it, conveniently they are all 5 characters, with _ and # included
    args = usr_inp[5:]  # Defines the optional argument such as <command> in _help

    if usr_inp[0] != "_" and usr_inp[0] != "#": return ""

    ################################
    # Messages
    ################################
    if cmd == "_help":
        # If there is no command specified
        if args == "": print(LANGUAGE.msg.help)

        elif len(args) == 5:
            attr = args.replace("_", "bs_").replace("#", "ad_")

            if hasattr(LANGUAGE.cmd, attr):
                print(getattr(LANGUAGE.cmd, attr))

            else: print(f"{LANGUAGE.err.no_such_cmd} '{args}'\n")

        else: print(f"{LANGUAGE.err.no_such_cmd}, '{args}'\n")
#-----------------------------------------------------------------------------------------------------------------------
    elif cmd == "_info": print(LANGUAGE.msg.info)
#-----------------------------------------------------------------------------------------------------------------------
    elif cmd == "_exmp": print(LANGUAGE.msg.example)
#-----------------------------------------------------------------------------------------------------------------------
    elif cmd == "_advn": print(LANGUAGE.msg.advanced_help)
#-----------------------------------------------------------------------------------------------------------------------
    elif cmd == "_show":
        print()

        print(f"{LANGUAGE.out.debug_mode   }: {getattr(LANGUAGE.lan, str(settings['debug_mode']).lower())   }")
        print(f"{LANGUAGE.out.ignore_prth  }: {getattr(LANGUAGE.lan, str(settings['ignore_prth']).lower())  }")
        print(f"{LANGUAGE.out.output_string}: {getattr(LANGUAGE.lan, str(settings['output_string']).lower())}")
        print(f"{LANGUAGE.out.literal      }: {getattr(LANGUAGE.lan, str(settings['literal']).lower())      }")
        print()

        print(f"{LANGUAGE.out.us_uk_sys    }: {getattr(LANGUAGE.lan, str(settings['us_uk_sys']).lower())    }")
        print(f"{LANGUAGE.out.accept_all   }: {getattr(LANGUAGE.lan, str(settings['accept_all']).lower())   }")
        print()

        print(f"{LANGUAGE.out.lang         }: {acronym_lang[settings['lang']]                               }")
        print()
#-----------------------------------------------------------------------------------------------------------------------
    elif cmd == "_smem" or cmd == "_seem":
        if settings["literal"]:
            print(LANGUAGE.err.inaccessible_mem)
            return "continue"

        if nums_func.memory == {}:
            print(LANGUAGE.msg.empty_mem)
        else:
            print()
            for key in nums_func.memory:
                try:
                    print(f"{key} = {nums_func.num_to_str(nums_func.memory[key])}")
                except OverflowError:
                    lang.write_error_log(
                        "OverflowError",
                        "cmds.py|command()|elif|else|for|except",
                        settings["debug_mode"]
                    )
                    
                    print(f"{key} = {LANGUAGE.lan.infinity}")
            print()
#-----------------------------------------------------------------------------------------------------------------------
    elif cmd == "_vshs":
        news = ["last", "latest", "news"]

        if args == "":
            print()
            with open("other/installer/VERSION_HISTORY.txt", "r") as version_history_file:
                for line in version_history_file:
                    print(line.replace("\n", ""))
            print()

        elif args in news:
            with open("other/installer/VERSION_HISTORY.txt", "r") as version_history_file:
                for line_count, line in enumerate(version_history_file):
                    if line_count == 3:
                        # The last version is always in this position in the file
                        last_version = line[8:15].replace(".", "")
                        break

            with open(f"other/infos/versions/{last_version}.txt", "r") as last_version_file:
                for line in last_version_file:
                    print(line.replace("\n", ""))
            print()

        else:  # If there is something as an argument but is not a keyword
            try:
                version = open(f"other/infos/versions/{usr_inp[5:].replace('.', '')}.txt")
                for line in version:
                    print(line.replace("\n", ""))
                print()

            except FileNotFoundError:
                lang.write_error_log(
                    "FileNotFoundError",
                    "cmds.py|command()|elif|else|except",
                    settings["debug_mode"]
                )
                
                print(LANGUAGE.err.file_not_found)

            except PermissionError:
                lang.write_error_log(
                    "PermissionError",
                    "cmds.py|command()|elif|else|except",
                    settings["debug_mode"]
                )
                
                print(LANGUAGE.err.permission_error)

            except OSError:
                lang.write_error_log(
                    "OSError",
                    "cmds.py|elif|else|except",
                    settings["debug_mode"]
                )
                
                print(LANGUAGE.err.file_not_found)
#-----------------------------------------------------------------------------------------------------------------------
    elif cmd == "#path": print(path.abspath(".") + "\n")  # "." is the local folder


    ################################
    # Settings management
    ################################
    elif cmd == "_swap": switch_settings("us_uk_sys")
#-----------------------------------------------------------------------------------------------------------------------
    elif cmd == "_expr": switch_settings("output_string")
#-----------------------------------------------------------------------------------------------------------------------
    elif cmd == "_acal": switch_settings("accept_all")
#-----------------------------------------------------------------------------------------------------------------------
    elif cmd == "#dbug": switch_settings("debug_mode")
#-----------------------------------------------------------------------------------------------------------------------
    elif cmd == "#prth": switch_settings("ignore_prth")
#-----------------------------------------------------------------------------------------------------------------------
    elif cmd == "#ltrl": switch_settings("literal")
#-----------------------------------------------------------------------------------------------------------------------
    elif cmd == "#rset":
        answer = input(f"\n{LANGUAGE.inp.settings_res}> ").lower()
        try:
            lang.write_info_log(
                f"Answer: {answer}",
                "cmds.py|command()|elif|try"
            )

        except UnicodeError:
            lang.write_error_log(
                "UnicodeError",
                "cmds.py|command()|elif|except",
                settings["debug_mode"]
            )

        if answer == "y":
            settings["debug_mode"] = False
            settings["us_uk_sys"] = False
            settings["ignore_prth"] = False
            settings["output_string"] = True
            settings["accept_all"] = True
            settings["literal"] = False

            print(LANGUAGE.msg.settings_res)

        elif answer == "n":
            print(LANGUAGE.out.operation_cancelled)

        else:
            print(LANGUAGE.err.invalid_answer)


    ################################
    # Program stop
    ################################
    elif cmd == "_stop":
        answer = input(f"\n{LANGUAGE.inp.stop}> ").lower()
        try:
            lang.write_info_log(
                f"Answer: {answer}",
                "cmds.py|elif|try"
            )

        except UnicodeError:
            lang.write_error_log(
                "UnicodeError",
                "cmds.py|command()|elif|except",
                settings["debug_mode"]
            )

        if answer == "y":
            lang.write_process_ended_log()
            return "break"

        elif answer == "n": print(LANGUAGE.out.operation_cancelled)

        else: print(LANGUAGE.err.invalid_answer)
#-----------------------------------------------------------------------------------------------------------------------
    elif cmd == "#exit" or cmd == "#inst":
        lang.write_process_ended_log()
        return "break"

    ################################
    # Language management
    ################################
    elif cmd == "_lang":
        if args == "":
            # Prints out the list of available languages
            print(LANGUAGE.msg.available_languages)
            for lang_acronym in acronym_lang:
                print(f"{lang_acronym} -> {acronym_lang[lang_acronym]}")

            language = input(f"\n{LANGUAGE.inp.lang_acronym}> ").upper()

        else: language = args.upper()

        try:
            lang.write_info_log(
                f"Acronym: {language}",
                "cmds.py|command()|elif|try"
            )

        except UnicodeError:
            lang.write_error_log(
                "UnicodeError",
                "cmds.py|command()|elif|except",
                settings["debug_mode"]
            )

        if language in acronym_lang:
            settings["lang"] = language
            lang.load_txt(language)
            print(f"'{LANGUAGE.out.lang}' {LANGUAGE.out.switch} {acronym_lang[language]}\n")

        else:
            print(LANGUAGE.err.no_such_lang)
#-----------------------------------------------------------------------------------------------------------------------
    elif cmd == "_load":
        with open("settings/settings.json") as json_settings:
            settings = load(json_settings)
            lang.load_txt(settings["lang"])

        print(LANGUAGE.msg.lang_loaded)
#-----------------------------------------------------------------------------------------------------------------------
    elif cmd == "#addl":  # It's useful when adding a language, but not available to the public
        language = input("Insert the language and the acronym:\n> ")
        space_pos = language.find(" ")

        lang_acronym = language[:space_pos].upper()
        lang_name = language[space_pos + 1:]

        lang.write_info_log(f"language = {language}",    "cmds.py|command()|elif")
        lang.write_info_log(f"acronym = {lang_acronym}", "cmds.py|command()|elif")
        lang.write_info_log(f"lang_name = {lang_name}",  "cmds.py|command()|elif")

        try:
            # To make sure the file exists
            with open(f"langs/{lang_acronym}.lang"):
                pass

            acronym_lang[lang_acronym] = lang_name
            with open("settings/lang_acronyms.json", "w") as json_acronym_lang:
                dump(acronym_lang, json_acronym_lang)

        except ValueError:
            lang.write_error_log(
                "ValueError",
                "cmds.py|command()|elif|except",
                settings["debug_mode"]
            )
            print(LANGUAGE.err.invalid_command)

        except FileNotFoundError:
            lang.write_error_log(
                "FileNotFoundError",
                "cmds.py|command()|elif|except",
                settings["debug_mode"]
            )
            print(LANGUAGE.err.file_not_found)


    ################################
    # Memory management
    ################################
    elif cmd == "_addm" or cmd == "_amem":
        if settings["literal"]:
            print(LANGUAGE.err.inaccessible_mem)
            return "continue"

        add_mem = input(f"\n{LANGUAGE.inp.add_mem}> ")
        space_pos = add_mem.find(" ")

        mem_cell_name = add_mem[:space_pos]
        mem_cell_value = nums_func.find_num(add_mem[space_pos + 1:])
        mem_cell_value = last_result if mem_cell_value is None else mem_cell_value

        try:
            lang.write_info_log(f"Input: {add_mem}",        "cmds.py|command()|elif|try")
            lang.write_info_log(f"Name: {mem_cell_name}",   "cmds.py|command()|elif|try")
            lang.write_info_log(f"Value: {mem_cell_value}", "cmds.py|command()|elif|try")

        except UnicodeError:
            lang.write_error_log(
                "UnicodeError",
                "cmds.py|command()|elif|except",
                settings["debug_mode"])
            print(LANGUAGE.err.invalid_command)
            return "continue"

        if nums_func.find_num(mem_cell_name) is not None:
            print(LANGUAGE.err.no_num_name)
            return "continue"

        if mem_cell_value is not None:
            nums_func.memory[mem_cell_name] = mem_cell_value
            print(f"'{mem_cell_name} = {nums_func.num_to_str(mem_cell_value)}' "
                  f"{LANGUAGE.msg.added_to_mem}\n")

        else: print(LANGUAGE.err.invalid_command)
#-----------------------------------------------------------------------------------------------------------------------
    elif cmd == "_delm" or cmd == "_dmem":
        if settings["literal"]:
            print(LANGUAGE.err.inaccessible_mem)
            return "continue"

        mem_cell_name = input(f"\n{LANGUAGE.inp.del_mem}> ")

        try:
            lang.write_info_log(f"Cell: {mem_cell_name}", "cmds.py|elif")

        except UnicodeError:
            lang.write_error_log(
                "UnicodeError",
                "cmds.py|command()|elif|except",
                settings["debug_mode"]
            )

        try:
            del nums_func.memory[mem_cell_name]
            print(f"'{mem_cell_name}' {LANGUAGE.msg.deleted_from_mem}\n")

        except KeyError:
            lang.write_error_log(
                "KeyError",
                "cmds.py|command()|elif|except",
                settings["debug_mode"]
            )

            print(LANGUAGE.err.no_mem_cell)
#-----------------------------------------------------------------------------------------------------------------------
    elif cmd == "#cmem":
        if settings["literal"]:
            print(LANGUAGE.err.inaccessible_mem)
            return "continue"

        answer = input(f"\n{LANGUAGE.inp.mem_res}> ").lower()
        try:
            lang.write_info_log(f"Answer: {answer}", "cmds.py|command()|elif")

        except UnicodeError:
            lang.write_error_log(
                "UnicodeError",
                "cmds.py|command()|elif|except",
                settings["debug_mode"]
            )

        if answer == "y":
            nums_func.memory = {}
            print(LANGUAGE.msg.mem_res)

        elif answer == "n": print(LANGUAGE.out.operation_cancelled)

        else: print(LANGUAGE.err.invalid_answer)
#-----------------------------------------------------------------------------------------------------------------------
    elif cmd == "_open":
        if settings["literal"]:
            print(LANGUAGE.err.inaccessible_mem)
            return "continue"

        if args == "" or args == "*overwrite":
            file_path = input(f"\n{LANGUAGE.inp.open_path}> ")
            overwrite = True if "*overwrite" in file_path else False

        else:
            overwrite = True if "*overwrite" in args else False
            file_path = args

        file_path = file_path.replace("*overwrite", "")

        try:
            lang.write_info_log(f"Open file path: {file_path}", "cmds.py|command()|elif|try")
            lang.write_info_log(f"overwrite = {overwrite}",     "cmds.py|command()|elif|try")

        except UnicodeError:
            lang.write_error_log(
                "UnicodeError",
                "cmds.py|command()|elif|except",
                settings["debug_mode"]
            )

        if len(file_path) >= 4 and file_path[-4] != ".":  # If the name has been put in the path
            file_path += "/" if file_path != "" else ""
            file_path += input(f"\n{LANGUAGE.inp.file_name}> ") + ".mem"

            try:
                lang.write_info_log(f"Open file lang_name: {file_path}", "cmds.py|command()|elif|if|try")

            except UnicodeError:
                lang.write_error_log(
                    "UnicodeError",
                    "cmds.py|command()|elif|if|except",
                    settings["debug_mode"]
                )

        try:
            mem_file = open(file_path, "r")
            if overwrite:
                lang.memory = load(mem_file)

            else:
                temp_mem = load(mem_file)
                for key in temp_mem:
                    nums_func.memory[key] = temp_mem[key]

            print("'" + file_path.replace("/", "\\") + "' " + LANGUAGE.msg.file_opened + "\n")

        except FileNotFoundError:
            lang.write_error_log(
                "FileNotFoundError",
                "cmds.py|command()|elif|except",
                settings["debug_mode"]
            )

            print(LANGUAGE.err.file_not_found)

        except PermissionError:  # Shouldn't occur but to be save it's here
            lang.write_error_log(
                "PermissionError",
                "cmds.py|command()|elif|except",
                settings["debug_mode"]
            )

            print(LANGUAGE.err.permission_error)

        except OSError:
            lang.write_error_log(
                "OSError",
                "cmds.py|command()|elif|except",
                settings["debug_mode"]
            )

            print(LANGUAGE.err.file_not_found)
#-----------------------------------------------------------------------------------------------------------------------
    elif cmd == "_save":
        if settings["literal"]:
            print(LANGUAGE.err.inaccessible_mem)
            return "continue"

        if args == "":
            file_path = input(f"\n{LANGUAGE.inp.save_path}> ")

        else:
            file_path = args

        if len(file_path) >= 4 and file_path[-4] != ".":  # If the name has been put in the path
            file_path += "/" + input(f"\n{LANGUAGE.inp.file_name}> ") + ".mem"

        try:
            lang.write_info_log(f"Save file path: {file_path}", "cmds.py|command()|elif|try")

        except UnicodeError:
            lang.write_error_log(
                "UnicodeError",
                "cmds.py|command()|elif|except",
                settings["debug_mode"]
            )

        last_slash = 0
        for i, char in enumerate(file_path):
            if char == "\\" or char == "/":
                last_slash = i + 1

        file_name = file_path[last_slash:].replace(".mem", "").lower()
        reserved_file_names = [
            "con", "prn", "aux", "nul", "com1", "com2", "com3", "com4", "com5", "com6", "com7", "com7", "com8", "com9",
            "com0", "lpt1", "lpt2", "lpt3", "lpt4", "lpt5", "lpt6","lpt7", "lpt8", "lpt9", "lpt0"
        ]

        try:
            if file_name in reserved_file_names:
                raise NameError

            with open(file_path, "w") as mem_file:
                dump(nums_func.memory, mem_file)
            print(LANGUAGE.msg.file_saved + " " + file_path.replace("/", "\\"), "\n")

        except FileNotFoundError:
            lang.write_error_log(
                "FileNotFoundError",
                "cmds.py|command()|elif|except",
                settings["debug_mode"]
            )

            print(LANGUAGE.err.file_not_found)

        except PermissionError:
            lang.write_error_log(
                "PermissionError",
                "cmds.py|command()|elif|except",
                settings["debug_mode"]
            )

            print(LANGUAGE.err.permission_error)

        except OSError:
            lang.write_error_log(
                "OSError",
                "cmds.py|command()|elif|except",
                settings["debug_mode"]
            )

            print(LANGUAGE.err.file_not_found)

        except NameError:
            lang.write_error_log(
                "NameError",
                "cmds.py|command()|elif|except",
                settings["debug_mode"]
            )

            print(LANGUAGE.err.name_error)
#-----------------------------------------------------------------------------------------------------------------------

    # If the command was not valid
    else:
        print(LANGUAGE.err.invalid_command)

    # Saves the settings whether or not there were any changes
    with open("settings/settings.json", "w") as json_settings:
        dump(settings, json_settings)

    update_settings()

    return "continue"  # If the input started with _ or #
