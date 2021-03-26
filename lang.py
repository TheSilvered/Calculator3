import json


class Language:


    class Msg:
        info = \
        help = \
        advanced_help = \
        example = \
        available_languages = \
        added_to_mem = \
        deleted_from_mem = \
        empty_mem = \
        settings_res = \
        mem_res = \
        lang_loaded = \
        file_saved = \
        file_opened = \
        ""


    class Err:
        syntax_error = \
        complex = \
        file_not_found = \
        invalid_command = \
        permission_error = \
        no_num_name = \
        no_mem_cell = \
        invalid_answer = \
        no_such_cmd = \
        no_such_lang = \
        impossible_div_error = \
        non_int_pow_error = \
        name_error = \
        inaccessible_mem = \
        other_error = \
        ""


    class Inp:
        expression = \
        stop = \
        lang_acronym = \
        add_mem = \
        del_mem = \
        mem_res = \
        settings_res = \
        save_path = \
        open_path = \
        file_name = \
        ""


    class Out:
        debug_mode = \
        ignore_prth = \
        us_uk_sys = \
        output_string = \
        accept_all = \
        lang = \
        switch = \
        literal = \
        operation_cancelled = \
        ""


    class Lan:
        infinity = \
        true = \
        false = \
        undetermined = \
        impossible = \
        ""


    class Cmd:
        # bs_ -> Basic, ad_ -> advanced
        bs_acal = \
        bs_addm = \
        bs_advn = \
        bs_delm = \
        bs_exmp = \
        bs_expr = \
        bs_help = \
        bs_info = \
        bs_lang = \
        bs_load = \
        bs_open = \
        bs_save = \
        bs_show = \
        bs_smem = \
        bs_stop = \
        bs_swap = \
        bs_vshs = \
        ad_cmem = \
        ad_dbug = \
        ad_exit = \
        ad_prth = \
        ad_rset = \
        ad_path = \
        ad_ltrl = \
        ""


    msg = Msg
    err = Err
    inp = Inp
    out = Out
    lan = Lan
    cmd = Cmd


language = Language


def write_error_log(message: str, module: str, print_message: bool = False):
    with open("calclog/error.log", "a") as log:
        log.write(f"{module} - {message}\n")

    if print_message: print(message)


def write_info_log(message: str, module: str, print_message: bool = False):
    with open("calclog/info.log", "a") as log:
        log.write(f"{module} - {message}\n")

    if print_message: print(message)


def write_debug_log(message: str, module: str, print_message: bool = False):
    with open("calclog/debug.log", "a") as log:
        log.write(f"{module} - {message}\n")

    if print_message: print(message)


def write_process_started_log():
    with open("settings/process_count.json") as process_j:
        process = json.load(process_j)

    with open("calclog/error.log", "a") as log:
        log.write(f"============== Process started {process} ==============\n")

    with open("calclog/info.log", "a") as log:
        log.write(f"============== Process started {process} ==============\n")

    with open("calclog/debug.log", "a") as log:
        log.write(f"============== Process started {process} ==============\n")

    process[0] += 1

    with open("settings/process_count.json", "w") as process_j:
        json.dump(process, process_j)


def write_process_ended_log():
    with open("calclog/error.log", "a") as log:
        log.write(f"=============== Process ended ===============\n")

    with open("calclog/info.log", "a") as log:
        log.write(f"=============== Process ended ===============\n")

    with open("calclog/debug.log", "a") as log:
        log.write(f"=============== Process ended ===============\n")


def load_txt(acronym: str):
    global language

    language = Language

    file = open(f"langs/{acronym}.lang", "r")
    main_set = ""
    attribute = ""
    previous_invalid_attribute = ""
    first_line = False

    for line_count, line in enumerate(file):
        if line[0] == "$":
            main_set = line.replace("$", "").replace("\n", "")

        elif line[0] == "@":
            attribute = line.replace("@", "").replace("\n", "")
            first_line = True

        else:
            if line[0] == "&":
                line = line.replace("&", "").replace("\n", "")

            elif line[0:2] == "::":
                continue

            if hasattr(getattr(language, main_set), attribute):
                if first_line: setattr(getattr(language, main_set), attribute, "")
                setattr(getattr(language, main_set), attribute, getattr(getattr(language, main_set), attribute) + line)
                first_line = False

            elif previous_invalid_attribute != attribute:
                write_error_log(
                    f"Invalid attribute: '@{attribute}' at line {line_count}",
                    "lang.py|load_txt()|for|else|elif",
                    True
                )
                previous_invalid_attribute = attribute  # Prevents spam in a multiline invalid attribute

    file.close()

    write_info_log("Text loaded", "lang.py|load_txt()")

    return language
