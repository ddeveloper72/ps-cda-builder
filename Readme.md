# CDA Generator Application (in development)

This application is designed to generate a Patient Summary Clinical Document Architecture (CDA) XML file based on data from an Excel file. The generated XML file follows the HL7 CDA standard and can be used for exchanging patient information between healthcare systems.

## Purpose

The purpose of this application is to automate the process of creating a Patient Summary CDA document. It takes an Excel file as input, which contains patient data, author information, and clinical data sections such as allergies, medications, problems list, and procedures. The application reads the data from the Excel file and generates a CDA XML file that conforms to the HL7 CDA standard.

## How to Use

1. Install the required dependencies by running `pip install -r requirements.txt`.
2. Update the `file_path` variable in the `app.py` file with the path to your Excel file.
3. Run the `app.py` file to generate the CDA XML file.
4. The generated XML file will be saved in the `static/out` directory with the name `{PATIENT_ID}_ps_sample_cda.xml`.

## Dependencies

- pandas: Used for reading data from the Excel file.
- xml.etree.ElementTree: Used for creating and manipulating the XML structure.

## Reference Material 

[CDA Generator](https://gazelle.ihe.net/gazelle-documentation/CDA-Generator/user.html)

[ART-DECOR](https://art-decor.ehdsi.eu/)

[IHE Wiki](https://wiki.ihe.net/index.php/Main_Page)

[eHDSI General Repository](https://code.europa.eu/ehdsi/ehdsi-general-repository)

[eHDSI sample CDA templates](https://code.europa.eu/ehdsi/ehdsi-general-repository/-/tree/e521266708aac6e47a1e78f243c178bc0eb7d3b2/cda%20documents)

[Irish SNOMED Reference Sets](https://code.europa.eu/ehdsi/ehdsi-general-repository)