# this file is responsible for converting raw bill into structured data
# the process has three main steps
# 1. convert file into text using OCR
# 2. extract meaningful fields using pattern based logic
# 3. use AI as fallback when rule based extraction fails

from pdf2image import convert_from_bytes
import pytesseract
from PIL import Image
import re
import json
import os
from dotenv import load_dotenv
import google.generativeai as genai
import streamlit as st

# configure gemini model using API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# set local path of tesseract OCR engine
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def preprocess_image(img):
    """
    convert image to grayscale

    reason
    OCR works better when image noise is reduced
    grayscale removes color complexity and improves text detection
    """
    return img.convert("L")


def extract_text_from_file(uploaded_file):
    """
    this function converts input file into raw text

    it supports both pdf and image formats
    """

    text = ""

    # if file is pdf convert each page into image
    if uploaded_file.type == "application/pdf":

        images = convert_from_bytes(
            uploaded_file.read(),
            poppler_path=r"C:\poppler\Library\bin"
        )

        # run OCR on each page
        for img in images:
            img = preprocess_image(img)
            text += pytesseract.image_to_string(img) + "\n"

    else:
        # if file is image directly apply OCR
        image = Image.open(uploaded_file)
        image = preprocess_image(image)
        text = pytesseract.image_to_string(image)

    return text


def extract_with_regex(text):
    """
    extract structured data using rule based approach

    reason
    rule based extraction is fast and reliable for known formats
    """

    data = {
        "customer_name": None,
        "consumer_number": None,
        "billing_amount": None,
        "units_consumed": None,
        "connection_load_kw": None,
        "tariff_type": None,
        "bill_month": None
    }

    # extract consumer number

    # consumer number is a 12 digit value
    match = re.search(r"\b\d{12}\b", text)

    if match:
        data["consumer_number"] = match.group()

    # extract customer name

    # OCR may distort SHRI into SHR or SHRL so we handle flexible pattern
    match = re.search(r"SHR\S*\s+([A-Z\s]{8,})", text)

    if match:
        name = match.group(1)

        # clean extra spaces
        name = " ".join(name.split())

        data["customer_name"] = name

    # extract units consumed

    # electricity bill pattern usually contains values like 25 0 25
    # we capture the first value as units consumed
    match = re.search(r"\b(\d{1,3})\s+0\s+\d{1,3}\b", text)

    if match:
        data["units_consumed"] = match.group(1)

    # fallback logic if pattern fails
    if not data["units_consumed"]:

        # find all small numbers and pick a realistic one
        nums = re.findall(r"\b\d{1,3}\b", text)

        for n in nums:
            val = int(n)

            # realistic household consumption range
            if 1 <= val <= 400:
                data["units_consumed"] = val
                break

    # extract billing amount

    match = re.search(r"Rs[,.\s]*(\d{3,5})", text)

    if match:
        data["billing_amount"] = match.group(1)

    # extract connection load

    match = re.search(r"(\d+\.\d+)\s*KW", text)

    if match:
        data["connection_load_kw"] = match.group(1)

    # extract tariff type

    match = re.search(r"LT\s*I\s*Res\s*1-Phase", text)

    if match:
        data["tariff_type"] = match.group()

    # extract bill month

    # extract date and convert to readable month
    match = re.search(r"(\d{2})-(\d{2})-(\d{4})", text)

    if match:
        d, m, y = match.groups()

        months = {
            "01": "January", "02": "February", "03": "March",
            "04": "April", "05": "May", "06": "June",
            "07": "July", "08": "August", "09": "September",
            "10": "October", "11": "November", "12": "December"
        }

        data["bill_month"] = months.get(m) + " " + y

    return data


def extract_structured_data(text):
    """
    this is the main function used by the app

    flow
    first try rule based extraction
    if important values are missing then use AI fallback
    """

    data = extract_with_regex(text)

    # if critical fields are missing we use AI model
    if not data.get("units_consumed") or not data.get("billing_amount"):

        try:
            model = genai.GenerativeModel("gemini-pro")

            prompt = f"""
            extract structured json from electricity bill

            fields
            customer_name
            consumer_number
            billing_amount
            units_consumed
            connection_load_kw
            tariff_type
            bill_month

            text
            {text}
            """

            response = model.generate_content(prompt)

            gemini_data = json.loads(response.text)

            # merge AI output only where needed
            for k in gemini_data:
                if gemini_data[k]:
                    data[k] = gemini_data[k]

        except:
            # fail silently to avoid breaking app
            pass

    return data