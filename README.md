# AI Solar Bill Analyzer

An AI powered system that extracts data from electricity bills and generates a solar analysis report using an Excel template.

---

## Overview

This project automates the process of reading electricity bills and converting them into structured data for solar capacity estimation.

The system combines OCR, rule based extraction, and AI fallback to handle real world noisy inputs.

---

## Features

- OCR based text extraction from PDF and image bills
- Pattern based data extraction using regex
- AI fallback using Gemini for improved accuracy
- Automatic Excel report generation using template
- Clean and interactive Streamlit interface

---

## Tech Stack

- Python
- Streamlit
- Tesseract OCR
- pdf2image
- OpenPyXL
- Google Gemini API

---

## Project Workflow

1. User uploads electricity bill
2. OCR extracts raw text from the bill
3. Regex based logic extracts structured fields
4. Gemini API is used if extraction is incomplete
5. Data is written into Excel template
6. User downloads final solar analysis report

---

## Folder Structure

```
project/
│
├── app.py # Streamlit UI
├── extractor.py # OCR and data extraction logic
├── excel_writer.py # Excel automation
├── utils.py # helper functions
├── template.xlsx # predefined Excel template
├── requirements.txt # dependencies
├── .env # API keys
```

---

## Setup Instructions

### 1 Clone the repository
```
git clone https://github.com/iYashrajPatil/ai-solar-bill-analyser

cd ai-solar-bill-analyzer