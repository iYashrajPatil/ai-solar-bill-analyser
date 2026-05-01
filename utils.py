# utils.py

# this file contains helper functions used across the project
# here we focus on cleaning numeric values extracted from OCR text

import re


def clean_number(value):
    """
    this function converts messy extracted values into clean numeric format

    why this is needed
    OCR output is not clean
    values may contain text symbols like Rs commas or spaces

    example
    Rs 1,460 becomes 1460
    """

    # if value is missing return 0 to avoid errors
    if value is None:
        return 0

    # convert value to string so regex can be applied safely
    value = str(value)

    # remove everything except digits and decimal point
    # this strips currency symbols spaces and unwanted characters
    cleaned = re.sub(r"[^\d.]", "", value)

    # if nothing is left after cleaning return 0
    if cleaned == "":
        return 0

    # convert cleaned string to float for calculations
    return float(cleaned)