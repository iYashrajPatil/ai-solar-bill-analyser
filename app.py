# app.py

# this file creates the user interface using streamlit
# user uploads electricity bill and system processes it
# then we show insights and allow excel download

import streamlit as st
from extractor import extract_text_from_file, extract_structured_data
from excel_writer import fill_excel

# set page layout to wide for better spacing
st.set_page_config(page_title="Solar Load Calculator", layout="wide")

# main title of app
st.title("Solar Load Calculator")

# short description to explain purpose to user
st.markdown("""
Upload your electricity bill to extract consumption details and generate a solar analysis report.
""")

# section for uploading file
st.markdown("### Upload Electricity Bill")

uploaded_file = st.file_uploader(
    "Supported formats PDF PNG JPG",
    type=["pdf", "png", "jpg"]
)

# only run processing when user uploads file
if uploaded_file:
    
    # processing indicator so user knows system is working
    with st.spinner("Extracting data and generating report"):

        # step 1 convert image or pdf to text using OCR
        text = extract_text_from_file(uploaded_file)

        # step 2 extract structured data using regex and fallback logic
        data = extract_structured_data(text)

        # step 3 fill excel template with extracted values
        fill_excel(data, "template.xlsx", "output.xlsx")

    # divider for clean UI separation
    st.markdown("---")

    # show key insights first instead of raw data
    st.markdown("## Key Insights")

    col1, col2, col3 = st.columns(3)

    # these metrics give quick summary to user
    col1.metric("Units Consumed", data.get("units_consumed"))
    col2.metric("Bill Amount", data.get("billing_amount"))
    col3.metric("Tariff Type", data.get("tariff_type"))

    # customer information section
    st.markdown("### Customer Details")

    st.write("Customer Name:", data.get("customer_name"))
    st.write("Consumer Number:", data.get("consumer_number"))

    # expandable sections keep UI clean but allow debugging
    with st.expander("View OCR Output"):
        st.text_area("Extracted Text", text, height=200)

    with st.expander("View Structured Data"):
        st.json(data)

    # success message after everything completes
    st.success("Excel report generated successfully")

    # download button with correct file type handling
    with open("output.xlsx", "rb") as f:
        st.download_button(
            label="Download Solar Report",
            data=f,
            file_name="solar_report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )