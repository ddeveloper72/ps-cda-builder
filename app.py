import pandas as pd
from datetime import datetime
import json
import xml.etree.ElementTree as ET

# Load the Excel file
file_path = 'static/in/sample_ps.xlsx'  # Update this with your file path
excel_file = pd.ExcelFile(file_path)


# Helper function to add sub-elements with text and attributes
def add_sub_element(parent, tag, text=None, attrib={}):
    element = ET.SubElement(parent, tag, attrib)
    if text:
        element.text = text
    return element

class CDAData:
    def __init__(self):
        with open('static/codes/ehdsi.json', encoding='utf-8') as json_file:
            data = json.load(json_file)
            self.head = [(p['displayName'], p['code'], p['codeSystem'], p['codeSystemName']) for p in data['code']]
            self.conf = [(p['confidentiality'], p['codeSystem'], p['displayName']) for p in data['confidentialityCode']]
            self.custodian = [(p['title'], p['extension'], p['oid']) for p in data['custodian']]

    def get_headers(self):
        return self.head

    def get_confidentiality(self):
        return self.conf
    
    def get_custodian(self):
        return self.custodian

cda_data = CDAData()

# Create the root element for the CDA document
def create_root_element():
    root = ET.Element('ClinicalDocument', xmlns="urn:hl7-org:v3", xsi="schemaLocation=http://www.w3.org/2001/XMLSchema-instance")
    add_header_elements(root)
    return root


# Add header elements required for CDA
def add_header_elements(root):

    head = cda_data.get_headers()
    conf = cda_data.get_confidentiality()

    for displayName, code, codeSystem, codeSystemName in head:
        add_sub_element(root, 'id', attrib={'root': '2.16.840.1.113883.19.5.99999.1'})
        add_sub_element(root, 'code', attrib={'code': code, 'codeSystem': codeSystem, 'codeSystemName': codeSystemName})
        add_sub_element(root, 'title', text=displayName)
        add_sub_element(root, 'effectiveTime', attrib={'value': datetime.now().strftime('%Y%m%d%H%M%S')})
        
    for confidentiality, codeSystem, displayName in conf:  
        add_sub_element(root, 'confidentialityCode', attrib={'code': confidentiality, 'codeSystem': codeSystem, 'displayName': displayName})


# Record Target (Patient Information)
def add_patient_record_target():
    record_target = ET.SubElement(root, 'recordTarget')
    patient_role = ET.SubElement(record_target, 'patientRole')

    # Extract Patient Data and add to XML
    patient_data = pd.read_excel(excel_file, sheet_name='Patient Data')
    for _, row in patient_data.iterrows():

        PATIENT_ID = str(row['Patient ID'])

        id = ET.SubElement(patient_role, 'id', attrib={'root': '2.16.840.1.113883.19.5.99999.2', 'extension': str(row['Patient ID'])})
        telecom = ET.SubElement(patient_role, 'telecom', attrib={'use':row['Use'], 'value': row['Phone Number']})

        addr = ET.SubElement(patient_role, 'addr')
        add_sub_element(addr, 'streetAddressLine', text=row['Address'])
        add_sub_element(addr, 'city', text=row['City'])
        add_sub_element(addr, 'state', text=row['State'])
        add_sub_element(addr, 'postalCode', text=row['Zip Code'])
        add_sub_element(addr, 'country', text=row['Country'])

        patient = ET.SubElement(patient_role, 'patient')
        name = ET.SubElement(patient, 'name')
        add_sub_element(name, 'family', text=row['Family Name'])
        add_sub_element(name, 'given', text=row['Given Name'])
        add_sub_element(patient, 'administrativeGenderCode', attrib={'code': '2.16.840.1.113883.5.1', 'codeSystem':'', 'codeSystemName': '', 'codeSystemVersion': '', 'displayName': str(row['Gender'])})
        languageCommunication = ET.SubElement(patient, 'languageCommunication')
        add_sub_element(languageCommunication, 'languageCode', attrib={'code': row['Language'], 'codeSystem': '2.16.840.1.113883.6.99'})


    for _, row in patient_data.iterrows():
        # Extract Date of Birth and add to XML
        birth_time = datetime.strptime(str(row['Date of Birth']), '%Y-%m-%d %H:%M:%S')
        add_sub_element(patient, 'birthTime', attrib={'value': birth_time.strftime('%Y%m%d %H:%M:%S')})

add_patient_record_target()


# Author (Document Author Information)
def add_author_record_target():
    author_section = ET.SubElement(root, 'author')
    author_data = pd.read_excel(excel_file, sheet_name='Author Data')
    for _, row in author_data.iterrows():
        assigned_author = ET.SubElement(author_section, 'assignedAuthor')
        add_sub_element(assigned_author, 'id', attrib={'extension': str(row['Author ID'])})
        person = ET.SubElement(assigned_author, 'assignedPerson')
        name = ET.SubElement(person, 'name')
        add_sub_element(name, 'given', text=row['Given Name'])
        add_sub_element(name, 'family', text=row['Family Name'])
        represented_organization = ET.SubElement(assigned_author, 'representedOrganization')
        add_sub_element(represented_organization, 'id', attrib={'root': '2.16.840.1.113883.19.5.99999.2', 'extension': '12345'})
        add_sub_element(represented_organization, 'name', text='Healthcare Provider')

add_author_record_target()


# Custodian (Organization Information)
def add_custodian():
    custodian = cda_data.get_custodian()

    for title, extension, oid in custodian:
        custodian = ET.SubElement(root, 'custodian')
        assigned_custodian = ET.SubElement(custodian, 'assignedCustodian')
        represented_custodian_organization = ET.SubElement(assigned_custodian, 'representedCustodianOrganization')
        add_sub_element(represented_custodian_organization, 'id', attrib={'root': oid, 'extension': extension})
        add_sub_element(represented_custodian_organization, 'name', text=title)

add_custodian()



# Function to add clinical data sections (e.g., Allergies, Medications)
def add_clinical_section(section_title, sheet_name):
    component = ET.SubElement(root, 'component')
    structured_body = ET.SubElement(component, 'structuredBody')
    section = ET.SubElement(structured_body, 'component')
    section_elem = ET.SubElement(section, 'section')
    add_sub_element(section_elem, 'title', text=section_title)


    # Read the data for the section
    data_frame = pd.read_excel(excel_file, sheet_name=sheet_name)
    
    # Debug: Print column names
    print(f"Sheet '{sheet_name}' columns: {data_frame.columns.tolist()}")
    
    # Check if the required columns exist
    if 'Code' not in data_frame.columns or 'Description' not in data_frame.columns:
        print(f"Warning: Required columns 'Code' or 'Description' not found in sheet '{sheet_name}'. Skipping section.")
        return
    
    for _, row in data_frame.iterrows():
        entry = ET.SubElement(section_elem, 'entry')
        act = ET.SubElement(entry, 'act', attrib={'classCode': 'ACT', 'moodCode': 'EVN'})
        code = ET.SubElement(act, 'code', attrib={'code': str(row['Code']), 'displayName': str(row['Description'])})

# Add a table to the section element of the XML tree with the headers from the sheet data frame and return 
# the headers as a list of strings
def add_section_headers(section_elem, sheet_name):
    data_frame = pd.read_excel(excel_file, sheet_name=sheet_name)
    headers = data_frame.columns.tolist()
    return headers

# Add data rows to the table element of the XML tree with the data from the sheet data frame.  
# Populate the table with the data from the sheet data frame
def add_section_data(section_elem, sheet_name):
    data_frame = pd.read_excel(excel_file, sheet_name=sheet_name)
    return data_frame

        
# Add different sections
# IHE Resource https://wiki.ihe.net/index.php/
def add_clinical_sections():

    sections = get_sections()

    # Create the structured body element
    component = ET.SubElement(root, 'component')
    structured_body = ET.SubElement(component, 'structuredBody')

    # Add different sections
    # IHE Resource https://wiki.ihe.net/index.php/
    for section_title, sheet_name, oid1, oid2, code, display_name, code_system, code_system_name  in sections:
        if sheet_name in excel_file.sheet_names:
            section = ET.SubElement(structured_body, 'component')
            section_elem = ET.SubElement(section, 'section')
            add_clinical_section(section_title, sheet_name)
            add_sub_element(section_elem, 'templateId', attrib={'root': oid1})
            add_sub_element(section_elem, 'templateId', attrib={'root': oid2})
            add_sub_element(section_elem, 'id', attrib={'root': ' ', 'extension': ' '})
            add_sub_element(section_elem, 'code', attrib={'code': code, 'displayName': display_name, 'codeSystem': code_system, 'codeSystemName': code_system_name})
            # Create the text element
            text = ET.SubElement(section_elem, 'text')

            # Create the table element
            table = ET.SubElement(text, 'table')

            # Create the thead element
            thead = ET.SubElement(table, 'thead')

            # Add the headers
            headers = add_section_headers(section_elem, sheet_name)
            header_row = ET.SubElement(thead, 'tr')
            for header in headers:
                add_sub_element(header_row, 'th', text=header)
            
            # Create the tbody element
            tbody = ET.SubElement(table, 'tbody')
           
            # Add the data cells
            data_frame = add_section_data(section_elem, sheet_name)
            for _, row in data_frame.iterrows():
                row_elem = ET.SubElement(tbody, 'tr')
                for _, cell in row.items():
                    add_sub_element(row_elem, 'td', text=str(cell))

            # add_sub_element(section_elem, 'entry', attrib={'root': '1.3.6.1.4.1.19376.1.5.3.1.4.5.3'})  # Adjust entry root as needed
        else:
            print(f"Warning: Sheet '{sheet_name}' not found in the Excel file. Skipping section.")


# Function to read the JSON file and return the sections
def get_sections():
    with open('static/codes/ihe-sections.json', encoding='utf-8') as json_file:
        data = json.load(json_file)
        sections = []
        for p in data['sections']:
            sections.append((p['section_title'], p['sheet_name'], p['oid1'], p['oid2'], p['code'], p['display_name'], p['code_system'], p['code_system_name']))

    return sections

add_clinical_sections()


  
# Convert the XML tree to a string and write to a file
tree = ET.ElementTree(root)

# Save the XML file
def save_xml_file(patient_id):
    
    file_name = f"static/out/{ patient_id }_ps_sample_cda.xml"
    tree.write(file_name, encoding='utf-8', xml_declaration=True)
    print(f"Customized XML file '{file_name}' created successfully.")

save_xml_file(patient_id='P01')
