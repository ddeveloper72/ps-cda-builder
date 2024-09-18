a# 🚧 CDA Generator Application (in development)

This application is designed to generate a Patient Summary Clinical Document Architecture (CDA) XML file based on data from an Excel file. The generated XML file will follow the <a href="https://art-decor.ehdsi.eu/art-decor/decor-templates--epsos-?section=templates&id=1.3.6.1.4.1.12559.11.10.1.3.1.1.3&effectiveDate=2024-04-19T10:03:32&language=en-US" target="_blank">eHDSI CDA standard</a> once fully developed and can be used for exchanging patient information between healthcare systems.

## Purpose

The purpose of this application is to automate the process of creating a Patient Summary CDA document. It takes an Excel file as input, which contains patient data, author information, and clinical data sections such as allergies, medications, problems list, and procedures. The application reads the data from the Excel file and generates a CDA XML file that will conform to the eHDSI CDA standard.

## How to Use

1. Install the required dependencies by running `pip install -r requirements.txt`.
2. Update the `file_path` variable in the `app.py` file with the path to your Excel file.
3. Run the `app.py` file to generate the CDA XML file.
4. The generated XML file will be saved in the `static/out` directory with the name `{PATIENT_ID}_ps_sample_cda.xml`.

## Dependencies

- pandas: Used for reading data from the Excel file.
- xml.etree.ElementTree: Used for creating and manipulating the XML structure.

## Reference Material 

<a href="https://gazelle.ihe.net/gazelle-documentation/CDA-Generator/user.html" about="_blank">CDA Generator</a>

<a href="https://art-decor.ehdsi.eu/" about="_blank">ART-DECOR</a>

<a href="https://art-decor.ehdsi.eu/art-decor/decor-templates--epsos-?section=templates&id=1.3.6.1.4.1.12559.11.10.1.3.1.1.3&effectiveDate=2024-04-19T10:03:32&language=en-US" about="_blank">eHDSI Patient Summary</a>

<a href="https://wiki.ihe.net/index.php/Main_Page" about="_blank">IHE Wiki</a>

<a href="https://code.europa.eu/ehdsi/ehdsi-general-repository" about="_blank">eHDSI General Repository</a>

<a href="https://code.europa.eu/ehdsi/ehdsi-general-repository/-/tree/e521266708aac6e47a1e78f243c178bc0eb7d3b2/cda%20documents" about="_blank">eHDSI sample CDA templates</a>

<a href="https://code.europa.eu/ehdsi/ehdsi-general-repository" about="_blank">Irish SNOMED Reference Set</a>