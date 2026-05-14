# app.py

# this is the main frontend file of the project
# here i created the complete user interface using streamlit
# user uploads electricity bill and system automatically processes it
# after extraction system generates excel report for solar analysis

import streamlit as st
import time

# importing custom functions from our backend files
# extractor handles OCR and AI extraction
# excel writer fills template automatically

from extractor import extract_text_from_file, extract_structured_data
from excel_writer import fill_excel

# configuring streamlit page
# wide layout makes dashboard look cleaner and more professional

st.set_page_config(
    page_title="Solar Load Calculator",
    page_icon="☀️",
    layout="wide"
)

# adding custom styling using css
# this improves UI without needing frontend frameworks

st.markdown("""
<style>

.main {
    padding-top: 2rem;
}

.stDownloadButton button {
    width: 100%;
    border-radius: 10px;
    height: 50px;
    font-size: 16px;
    font-weight: 600;
}

.stMetric {
    background-color: #111827;
    padding: 15px;
    border-radius: 12px;
    border: 1px solid #1f2937;
}

</style>
""", unsafe_allow_html=True)

# sidebar section
# added branding and project explanation
# makes project look more product oriented

with st.sidebar:

    st.title("EnergyBae AI")

    st.markdown("""
    AI powered electricity bill analyser

    Features included

    • OCR based bill reading

    • Smart data extraction

    • Automatic excel generation

    • Solar load estimation

    """)

    st.markdown("---")

    st.caption("Built for EnergyBae by Yashraj")

# main heading section

st.title("Solar Load Calculator")

# this line explains actual business problem solved by project
# recruiter can immediately understand use case

st.markdown("""
Automates manual electricity bill analysis for solar capacity estimation.
""")

st.markdown("")

# upload section
# user uploads pdf or image bill here

st.markdown("## Upload Electricity Bill")

uploaded_file = st.file_uploader(
    "Supported formats PDF,PNG,JPG (For faster processing upload cropped JPG bills instead of PDF) ",
    type=["pdf", "png", "jpg"]
)

# this block only runs after file upload

if uploaded_file:

    # starting timer to measure total processing time
    # useful for performance tracking

    start_time = time.time()

    # creating dynamic status box
    # instead of one static loader i used multiple status updates
    # this improves perceived speed and user experience

    status = st.empty()

    # progress bar gives visual feedback during processing

    progress = st.progress(0)

    # first stage of pipeline

    status.info("Uploading and reading bill")

    progress.progress(20)

    # OCR step
    # image or pdf gets converted into raw text

    text = extract_text_from_file(uploaded_file)

    # second stage

    status.info("Extracting structured information")

    progress.progress(50)

    # structured extraction step
    # regex and AI fallback extract important fields

    data = extract_structured_data(text)

    # third stage

    status.info("Generating excel report")

    progress.progress(80)

    # excel automation step
    # extracted values are inserted into formatted template

    fill_excel(data, "template.xlsx", "output.xlsx")

    # processing complete

    progress.progress(100)

    status.success("Report generated successfully")

    # calculating total processing time

    end_time = time.time()

    processing_time = round(end_time - start_time, 2)

    # divider for cleaner layout separation

    st.markdown("---")

    # dashboard summary section
    # quick insights shown using metric cards

    st.markdown("## Consumption Summary")

    col1, col2, col3, col4 = st.columns(4)

    # units consumed card

    col1.metric(
        "Units Consumed",
        data.get("units_consumed") or "Not Found"
    )

    # bill amount card

    col2.metric(
        "Bill Amount",
        f"Rs {data.get('billing_amount')}"
        if data.get("billing_amount")
        else "Not Found"
    )

    # tariff type card

    col3.metric(
        "Tariff Type",
        data.get("tariff_type") or "Not Found"
    )

    # bill month card

    col4.metric(
        "Bill Month",
        data.get("bill_month") or "Not Found"
    )

    # customer details section

    st.markdown("## Customer Information")

    left, right = st.columns(2)

    # customer name section

    with left:

        st.success("Customer name extracted")

        st.write(
            data.get("customer_name")
            or "Customer name not found"
        )

    # consumer number section

    with right:

        st.success("Consumer number extracted")

        st.write(
            data.get("consumer_number")
            or "Consumer number not found"
        )

    # using tabs to organize data properly
    # makes UI cleaner and recruiter friendly

    st.markdown("## Detailed Analysis")

    tab1, tab2 = st.tabs([
        "Structured Data",
        "OCR Output"
    ])

    # structured json tab
    # useful for debugging extracted values

    with tab1:

        st.json(data)

    # raw OCR output tab
    # useful to compare OCR quality and extraction

    with tab2:

        st.text_area(
            "Raw OCR Text",
            text,
            height=300
        )

    # success confirmation after everything completes

    st.success("Solar analysis report ready for download")

    # showing processing time to user

    st.caption(
        f"Processed successfully in {processing_time} seconds"
    )

    # final excel download button
    # generated excel file gets downloaded from here

    with open("output.xlsx", "rb") as file:

        st.download_button(
            label="Download Solar Report",
            data=file,
            file_name="solar_report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )

# footer section
# adds professional touch to application

st.markdown("---")

st.caption(
    "Built by Yashraj for EnergyBae"
)