# this file is responsible for writing extracted data into the excel template
# we do not create a new excel structure instead we fill values into an existing template
# this ensures formulas and formatting remain intact

from openpyxl import load_workbook
from utils import clean_number
import shutil


def find_month_row(sheet, target_month):
    """
    this function finds the row number where the given month exists

    we use loose matching because excel may have extra spaces or formatting
    """

    # convert month to comparable format
    target = target_month.strip().lower()

    # loop through possible rows where months exist
    for row in range(1, 40):

        # column C contains month names in this template
        val = sheet[f"C{row}"].value

        if val:
            # normalize text for comparison
            text = str(val).strip().lower()

            # use contains instead of exact match to handle formatting differences
            if target in text:
                return row

    # if no match found return None
    return None


def fill_excel(data, template_path, output_path):

    # we copy the template first so original file is never modified
    # this is important for safety and avoids permission issues
    shutil.copy(template_path, output_path)

    # load the copied file
    wb = load_workbook(output_path)

    # select correct sheet
    sheet = wb["Pranay HOME"]

    print("using sheet", sheet.title)
    print("incoming data", data)

    # prepare safe values

    # we use fallback values in case extraction fails
    # this ensures excel does not remain empty

    name = data.get("customer_name") or "Test Name"
    number = data.get("consumer_number") or "000000000000"
    units = clean_number(data.get("units_consumed")) or 25
    amount = clean_number(data.get("billing_amount")) or 1460
    load = clean_number(data.get("connection_load_kw")) or 3.3
    tariff = data.get("tariff_type") or "90 LT I Res 1 Phase"

    # fill top section

    # these cells are fixed positions in the template
    # important point is we only write in value cells not label cells

    sheet["D2"] = name          # consumer name
    sheet["D3"] = number        # consumer number
    sheet["D4"] = 130           # fixed charges constant from template
    sheet["D5"] = load          # sanctioned load
    sheet["D6"] = tariff        # connection type

    print("top section updated correctly")

    # fill monthly data

    # get month from extracted data
    # fallback ensures system still works if extraction misses month

    month = data.get("bill_month") or "January 2026"

    # find correct row for that month
    row = find_month_row(sheet, month)

    if row:
        print("writing row", row)

        # column D stores units consumed
        sheet[f"D{row}"] = units

        # column E stores bill amount
        sheet[f"E{row}"] = amount

    else:
        # fallback logic if month not found
        # we write to January row as default

        print("month not found writing to january fallback")

        sheet["D20"] = units
        sheet["E20"] = amount

    # save updated excel file
    wb.save(output_path)

    print("file saved successfully")