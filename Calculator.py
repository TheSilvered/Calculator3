################################
# Local dependencies
################################
import cmds
import lang
import settings as sets
from nums_func import num_to_str
from calc_expression import Expression
from make_expression import make_expr

lang.write_process_started_log()

LANGUAGE = lang.load_txt(sets.settings["lang"])
print(LANGUAGE.msg.info)


def main():
    usr_inp = input(LANGUAGE.inp.expression + "> ")
    try:
        lang.write_info_log(
            f"usr_inp = '{usr_inp}'",
            "Calculator.py|main()|try"
        )

    except UnicodeError:
        lang.write_error_log(
            "UnicodeError",
            "Calculator.py|main()|except",
            sets.settings["debug_mode"]
        )

        print(LANGUAGE.err.syntax_error)
        return

    usr_inp = usr_inp \
        .replace(" ", "") \
        .replace("{", "(") \
        .replace("[", "(") \
        .replace("}", ")") \
        .replace("]", ")")

    if sets.settings["ignore_prth"]:
        usr_inp = usr_inp \
            .replace("(", "") \
            .replace(")", "")

    lang.write_info_log(f"fixed usr_inp = '{usr_inp}'", "Calculator.py")

    if usr_inp == "":
        lang.write_info_log(LANGUAGE.err.syntax_error, "Calculator.py", True)
        return

    return_command = cmds.command(usr_inp.lower())
    # If it's not a command, the function returns an empty string
    if return_command == "break":
        return "break"
    elif return_command == "continue":
        return

    expression_defined = make_expr(usr_inp)
    expression = Expression(expression_defined)

    out_nums = expression_defined[5]
    out_operators = expression_defined[6]
    out_opening_prth = expression_defined[7]
    out_closing_prth = expression_defined[8]

    result, error_occurred = expression.optimized_calculation()

    if result is None: return  # The message is printed in the function

    output_string = ""
    result_string = ""

    if error_occurred != "":
        try:
            print(getattr(LANGUAGE.lan, error_occurred))
        except AttributeError:
            print(getattr(LANGUAGE.err, error_occurred))
        return

    elif not sets.settings["output_string"]:
        print(num_to_str(result))
        return

    ################################
    # Output string building
    ################################

    # Adds any opening parenthesis that are before everything
    output_string += "(" * out_opening_prth.count(0)
    if not sets.settings["literal"]:
        output_string += num_to_str(out_nums[0])
    else:
        output_string += str(out_nums[0])

    for i, operator in enumerate(out_operators):
        output_string += ")" * out_closing_prth.count(i)
        output_string += (" " if operator != "R" else "") + f"{operator} "
        output_string += "(" * out_opening_prth.count(i + 1)

        if not sets.settings["literal"]:
            output_string += num_to_str(out_nums[i + 1])

        else:
            pol_string = str(out_nums[i + 1])
            if pol_string[0] == "-" and operator not in "^R":
                output_string = output_string[:-3]  # Removes the last operator and puts a minus instead
                output_string += " - " + pol_string[1:]
            else:
                output_string += pol_string

        output_string += ")" * out_closing_prth.count(len(out_operators))

    output_string += " = "

    # The function num_to_str fixes the numbers by itself, manages OverflowErrors and TypeErrors
    result_string += num_to_str(result)
    cmds.last_result = result

    result_string += "\n"
    print(output_string + result_string)

    if sets.settings["output_string"]:
        lang.write_info_log(
            output_string,
            "Calculator.py|main()|if"
        )

    return


################################
# Main loop
################################
if __name__ == "__main__":
    while True:
        try:
            output = main()
        except Exception as exception:
            lang.write_error_log(
                str(exception),
                "Calculator.py|if|while|except",
                sets.settings["debug_mode"]
            )

            print(LANGUAGE.err.other_error + " '" + str(exception) + "'\n")
            continue

        if output == "break": break
