import pdfplumber
import pandas as pd
import re
import xml.etree.ElementTree as ET
import os

pdf_path = "/Users/bharatoraon/Desktop/Thesis/Data/Demographics & Boundary Data/2011-District-Handbook-Part-B.pdf"
csv_path = "/Users/bharatoraon/Desktop/Thesis/Data/Demographics & Boundary Data/Demographic_Profile_Chennai.csv"
kml_input = "/Users/bharatoraon/Desktop/Thesis/Data/Demographics & Boundary Data/chennai_wards.kml"
kml_output = "/Users/bharatoraon/Desktop/Thesis/Data/Demographics & Boundary Data/chennai_wards_enriched.kml"

def extract_pdf_data():
    data = []
    # Relevant pages for Primary Census Abstract - Ward data
    pages_to_extract = range(101, 116) 
    
    with pdfplumber.open(pdf_path) as pdf:
        for page_num in pages_to_extract:
            if page_num >= len(pdf.pages): break
            page = pdf.pages[page_num]
            text = page.extract_text()
            lines = text.split('\n')
            
            for line in lines:
                # Look for "WARD NO. <number>"
                match = re.search(r'WARD NO\.\s*(\d+)', line, re.IGNORECASE)
                if match:
                    ward_no = int(match.group(1))
                    if ward_no > 155: continue
                    
                    # Try to extract the numbers on this line or next lines
                    # Based on structure observed: SC, ST, Literates, Workers are usually in columns
                    # We look for a line that starts with "Total" after the ward line or numbers following it
                    # But the PCA table has a very specific column order.
                    # Column 10: SC (Total), 13: ST (Total), 16: Literates (Total), 19: Total Workers (Total)
                    pass

    # Actually, I'll use the mapper I built before which was more reliable.
    # I'll just re-implement the logic of finding the rows.
    # The table structure in the PDF is:
    # Row for Total, Row for Male, Row for Female
    
    ward_stats = {}
    
    with pdfplumber.open(pdf_path) as pdf:
        for page_num in pages_to_extract:
            page = pdf.pages[page_num]
            table = page.extract_table()
            if not table: continue
            
            current_ward = None
            for row in table:
                if not row or not any(row): continue
                # Check for Ward No. in any column
                row_str = " ".join([str(cell) for cell in row if cell])
                ward_match = re.search(r'WARD NO\.\s*(\d+)', row_str, re.IGNORECASE)
                if ward_match:
                    current_ward = int(ward_match.group(1))
                    if current_ward not in ward_stats:
                        ward_stats[current_ward] = {}
                
                # Check for "Total" row to extract counts
                if current_ward and "Total" in row_str:
                    # PCA Column Indices (approximate based on inspection):
                    # 4: Total Pop, 7: SC, 10: ST, 13: Literate, 16: Total Worker
                    # Since table extraction is messy, we'll try to find numbers.
                    nums = [re.sub(r'[, ]', '', str(c)) for c in row if c and re.search(r'\d', str(c))]
                    nums = [int(n) for n in nums if n.isdigit()]
                    
                    if len(nums) >= 10:
                        # Indexing into nums list (Total is usually index 1, SC is index 4, ST is index 7, Literate is index 10, Worker is index 13)
                        # This depends on specific row parsing.
                        pass
    
    # Actually, I'll rely on my previous successful extraction results if I can find them.
    # Since I can't find the file, I'll re-run a simplified extraction.
    return ward_stats

# RE-IMPLEMENTING THE ROBUST PARSER
def get_full_data():
    # 1. Load CSV
    df_csv = pd.read_csv(csv_path)
    df_csv['Ward No.'] = pd.to_numeric(df_csv['Ward No.'], errors='coerce')
    df_csv = df_csv.dropna(subset=['Ward No.'])
    df_csv['Ward No.'] = df_csv['Ward No.'].astype(int)
    
    # 2. Extract PDF data (SC, ST, Literates, Workers)
    # Mapping ward_no to {SC, ST, Literates, Workers}
    pdf_data = {}
    
    # Based on previous turns, I know the columns for SC/ST/Literates/Workers
    # are often separated across lines or in specific columns.
    # To be fast and correct, I'll use a regex-based line parser.
    
    with pdfplumber.open(pdf_path) as pdf:
        for p in range(101, 120): # Covers all 155 wards
            if p >= len(pdf.pages): break
            page = pdf.pages[p]
            text = page.extract_text()
            if not text: continue
            
            # Divide into ward blocks
            parts = re.split(r'WARD NO\.\s*\d+', text, flags=re.IGNORECASE)
            ward_ids = re.findall(r'WARD NO\.\s*(\d+)', text, flags=re.IGNORECASE)
            
            for i, w_id in enumerate(ward_ids):
                w_num = int(w_id)
                if w_num > 155: continue
                content = parts[i+1]
                total_line_match = re.search(r'Total\s+([\d, ]+)', content)
                if total_line_match:
                    nums = re.findall(r'\d+', total_line_match.group(1).replace(',', ''))
                    # Structure: TotalPop, Male, Female, SC_Total, SC_Male, SC_Female, ST_Total, ...
                    if len(nums) >= 12:
                        pdf_data[w_num] = {
                            'SC_Pop': int(nums[3]),
                            'ST_Pop': int(nums[6]),
                            'Literates': int(nums[9]),
                            'Total_Workers': int(nums[12]) if len(nums) > 12 else 0
                        }

    # 3. Merge
    final_data = []
    for w in range(1, 156):
        row = {'Ward No.': w}
        # CSV Data
        csv_row = df_csv[df_csv['Ward No.'] == w]
        if not csv_row.empty:
            row['Total_Pop'] = csv_row.iloc[0]['Total Population (in thousands)']
            row['Male_Pop'] = csv_row.iloc[0]['Population - Male (in thousands)']
            row['Female_Pop'] = csv_row.iloc[0]['Population - female (in thousands)']
            row['Area_sqkm'] = csv_row.iloc[0]['Area (in sq km)']
            row['Pop_0_14'] = csv_row.iloc[0]['population - children aged 0-14 (in thousands)']
            row['Pop_15_24'] = csv_row.iloc[0]['Population - youth aged 15-24 (in thousands)']
            row['Pop_25_60'] = csv_row.iloc[0]['Population - adults aged 25-60 (in thousands)']
            row['Pop_60_plus'] = csv_row.iloc[0]['Population - Senior citizens aged 60+ (in thousands)']
        
        # PDF Data
        if w in pdf_data:
            row.update(pdf_data[w])
        
        final_data.append(row)
    
    return pd.DataFrame(final_data)

def enrich_kml(df):
    ET.register_namespace('', "http://www.opengis.net/kml/2.2")
    tree = ET.parse(kml_input)
    root = tree.getroot()
    ns = {'kml': 'http://www.opengis.net/kml/2.2'}
    
    # 1. Update Schema
    schema = root.find(".//kml:Schema", ns)
    if schema is not None:
        # Clear existing non-standard fields if they exist
        fields_to_add = [
            ('Total_Pop', 'float'), ('Male_Pop', 'float'), ('Female_Pop', 'float'),
            ('SC_Pop', 'int'), ('ST_Pop', 'int'), ('Literates', 'int'),
            ('Total_Workers', 'int'), ('Area_sqkm', 'float'),
            ('Pop_0_14', 'float'), ('Pop_15_24', 'float'), 
            ('Pop_25_60', 'float'), ('Pop_60_plus', 'float')
        ]
        
        # Add fields
        existing_names = [f.get('name') for f in schema.findall("kml:SimpleField", ns)]
        for name, dtype in fields_to_add:
            if name not in existing_names:
                sf = ET.SubElement(schema, "{http://www.opengis.net/kml/2.2}SimpleField", name=name, type=dtype)
                ds = ET.SubElement(sf, "{http://www.opengis.net/kml/2.2}displayName")
                ds.text = name.replace('_', ' ')

    # 2. Update Placemarks
    for placemark in root.findall(".//kml:Placemark", ns):
        name_elem = placemark.find("kml:name", ns)
        if name_elem is None or not name_elem.text: continue
        
        ward_no_str = name_elem.text.strip()
        if not ward_no_str.isdigit(): continue
        
        ward_no = int(ward_no_str)
        if ward_no not in df['Ward No.'].values: continue
        
        ward_data = df[df['Ward No.'] == ward_no].iloc[0]
        
        ext_data = placemark.find("kml:ExtendedData", ns)
        if ext_data is None:
            ext_data = ET.SubElement(placemark, "{http://www.opengis.net/kml/2.2}ExtendedData")
        
        sch_data = ext_data.find("kml:SchemaData", ns)
        if sch_data is None:
            sch_data = ET.SubElement(ext_data, "{http://www.opengis.net/kml/2.2}SchemaData", schemaUrl="#J_gcc_divisions_SS")
            
        # Add data points
        for col in df.columns:
            if col == 'Ward No.': continue
            val = ward_data[col]
            if pd.isna(val): val = ""
            
            # Check if SimpleData already exists for this field
            sd = sch_data.find(f".//kml:SimpleData[@name='{col}']", ns)
            if sd is None:
                sd = ET.SubElement(sch_data, "{http://www.opengis.net/kml/2.2}SimpleData", name=col)
            sd.text = str(val)

    tree.write(kml_output, encoding='utf-8', xml_declaration=True)
    print(f"Enriched KML written to {kml_output}")

df = get_full_data()
enrich_kml(df)
