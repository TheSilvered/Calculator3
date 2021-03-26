from json import load, dump

settings = {
    "debug_mode"   : False,
    "ignore_prth"  : False,
    "us_uk_sys"    : False,
    "output_string": True,
    "accept_all"   : True,
    "literal"      : False,
    "lang"         : "EN"
}


def update_settings():
    global settings, j_settings

    with open("settings/settings.json") as j_settings:
        settings = load(j_settings)


with open("settings/settings.json") as j_settings:
    new_settings = load(j_settings)

is_file_valid = True
for key in new_settings:
    if key not in settings:
        is_file_valid = False
        break

if is_file_valid: settings = new_settings
else:
    with open("settings\\settings.json", "w") as json_settings:
        dump(settings, json_settings)
