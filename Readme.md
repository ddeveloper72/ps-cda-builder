# 🚧 CDA Builder Application (in development)

The live application is hosted on Heroku at [CDA PS Generator](https://ddeveloper72-cda-builder-6e7de819f3a3.herokuapp.com/)

The CDA Builder Application is a Flask-based web application that allows users to generate Clinical Document Architecture (CDA) documents for patients. CDAs are XML-based documents used for exchanging clinical information between healthcare systems.


This application is designed to generate a L3 Patient Summary Clinical Document Architecture (CDA) XML file based on data from an Excel file. The generated XML file will follow the <a href="https://art-decor.ehdsi.eu/art-decor/decor-templates--epsos-?section=templates&id=1.3.6.1.4.1.12559.11.10.1.3.1.1.3&effectiveDate=2024-04-19T10:03:32&language=en-US" target="_blank">eHDSI (eHealth Digital Service Infrastructure) CDA standard</a> 

## Features

- View a list of patients
- Generate CDA documents for selected patients
- Download generated CDA documents


## Purpose

The purpose of this application is to automate the process of creating a L3 Patient Summary CDA document. It takes an Excel file as input, which contains patient data, author information, and clinical data sections such as allergies, medications, problems list, and procedures. The application reads the data from the Excel file and generates a CDA XML file that will conform to the eHDSI CDA standard.

The clinical sections of the patient summary, uses template ID's as well as codes that come from the IHE Wiki.  The codes for this application are stored as a separate JSON file and are referenced when a particular clinical section is included in the original patient clinical record (synthetic data).  Keeping this data separate, will allow for simpler code maintenance should the IHE make changes or additions to the clinical section templates.

The CDA generator tool also references a second eHDSI JSON file, containing data for the non clinical header sections of the Patient Summary CDA document.  Keeping this data separate, will allow for simpler code maintenance should the we ever make changes as a result of rebranding, or make other additions to the template headers.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/ddeveloper72/ps-cda-builder.git
    ```

2. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Run the application:

    ```bash
    python app.py
    ```

4. Access the application in your web browser at `http://localhost:5000`.

## Dependencies

- pandas: Used for reading data from the Excel file.
- xml.etree.ElementTree: Used for creating and manipulating the XML structure.

## Usage

1. Open the application in your web browser.

2. The main page displays a list of patients. Click on a patient to generate a CDA document for them.

3. After generating the CDA document, you will be redirected to the download page.

4. Click the "Download" button to download the generated CDA document.


## Reference Material 

<a href="https://gazelle.ihe.net/gazelle-documentation/CDA-Generator/user.html" target="_blank">CDA Generator</a>

<a href="https://art-decor.ehdsi.eu/" target="_blank">ART-DECOR</a>

<a href="https://art-decor.ehdsi.eu/art-decor/decor-templates--epsos-?section=templates&id=1.3.6.1.4.1.12559.11.10.1.3.1.1.3&effectiveDate=2024-04-19T10:03:32&language=en-US" target="_blank">eHDSI Patient Summary</a>

<a href="https://wiki.ihe.net/index.php/Main_Page" target="_blank">IHE Wiki</a>

<a href="https://code.europa.eu/ehdsi/ehdsi-general-repository" target="_blank">eHDSI General Repository</a>

<a href="https://code.europa.eu/ehdsi/ehdsi-general-repository/-/tree/e521266708aac6e47a1e78f243c178bc0eb7d3b2/cda%20documents" target="_blank">eHDSI sample CDA templates</a>

<a href="https://www.ehealthireland.ie/technology-and-transformation-functions/standards-and-shared-care-records-sscr/standards-and-terminologies/snomed-ct/" target="_blank">Irish SNOMED Reference Set</a>