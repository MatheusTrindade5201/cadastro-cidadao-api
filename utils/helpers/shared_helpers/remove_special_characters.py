import re


def remove_special_characters(raw_input: str) -> str:
    cleaned_string = re.sub(r"[.\-/]", "", raw_input)
    cleaned_string = cleaned_string.strip()

    return cleaned_string