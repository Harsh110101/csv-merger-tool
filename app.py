import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="CSV Merger", layout="wide")
st.title("📁 CSV Merger for ZoomInfo, Apollo, Seamless, and Salesgenie")

UNIFIED_COLUMNS = [
    "First Name", "Last Name", "Full Name", "Title", "Seniority", "Department",
    "Email", "Mobile Phone", "Work Phone", "LinkedIn URL",
    "Company Name", "Website", "Company Address", "City", "State", "Country",
    "Company Revenue", "Employees", "Industry",
    "NAICS Code", "SIC Code", "Source"
]

# Define parser functions
def parse_zoominfo(df):
    return pd.DataFrame({
        "First Name": df.get("First Name"),
        "Last Name": df.get("Last Name"),
        "Full Name": df.get("First Name") + " " + df.get("Last Name"),
        "Title": df.get("Job Title"),
        "Seniority": df.get("Management Level"),
        "Department": df.get("Department"),
        "Email": df.get("Email Address"),
        "Mobile Phone": df.get("Mobile phone"),
        "Work Phone": df.get("Direct Phone Number"),
        "LinkedIn URL": df.get("LinkedIn Contact Profile URL"),
        "Company Name": df.get("Company Name"),
        "Website": df.get("Website"),
        "Company Address": df.get("Company Street Address"),
        "City": df.get("Company City"),
        "State": df.get("Company State"),
        "Country": df.get("Company Country"),
        "Company Revenue": df.get("Revenue (in 000s USD)"),
        "Employees": df.get("Employees"),
        "Industry": df.get("Primary Industry"),
        "NAICS Code": df.get("NAICS Code 1"),
        "SIC Code": df.get("SIC Code 1"),
        "Source": "ZoomInfo"
    })

def parse_apollo(df):
    return pd.DataFrame({
        "First Name": df.get("First Name"),
        "Last Name": df.get("Last Name"),
        "Full Name": df.get("First Name") + " " + df.get("Last Name"),
        "Title": df.get("Title"),
        "Seniority": df.get("Seniority"),
        "Department": df.get("Departments"),
        "Email": df.get("Email"),
        "Mobile Phone": df.get("Mobile Phone"),
        "Work Phone": df.get("Work Direct Phone"),
        "LinkedIn URL": df.get("Person Linkedin Url"),
        "Company Name": df.get("Company"),
        "Website": df.get("Website"),
        "Company Address": df.get("Company Address"),
        "City": df.get("City"),
        "State": df.get("State"),
        "Country": df.get("Country"),
        "Company Revenue": df.get("Annual Revenue"),
        "Employees": df.get("# Employees"),
        "Industry": df.get("Industry"),
        "NAICS Code": "",
        "SIC Code": "",
        "Source": "Apollo"
    })

def parse_salesgenie(df):
    return pd.DataFrame({
        "First Name": df.get("Executive First Name"),
        "Last Name": df.get("Executive Last Name"),
        "Full Name": df.get("Executive First Name") + " " + df.get("Executive Last Name"),
        "Title": df.get("Executive Title"),
        "Seniority": "",
        "Department": "",
        "Email": "",
        "Mobile Phone": "",
        "Work Phone": df.get("Phone Number"),
        "LinkedIn URL": "",
        "Company Name": df.get("Company Name"),
        "Website": df.get("Website"),
        "Company Address": df.get("Address"),
        "City": df.get("City"),
        "State": df.get("Province"),
        "Country": "Canada",
        "Company Revenue": df.get("Location Sales Volume"),
        "Employees": df.get("Location Number of Employees"),
        "Industry": "",
        "NAICS Code": df.get("Primary NAICS"),
        "SIC Code": df.get("Primary SIC"),
        "Source": "Salesgenie"
    })

def parse_seamless(df):
    return pd.DataFrame({
        "First Name": df.get("First Name"),
        "Last Name": df.get("Last Name"),
        "Full Name": df.get("First Name") + " " + df.get("Last Name"),
        "Title": df.get("Title"),
        "Seniority": df.get("Seniority"),
        "Department": df.get("Department"),
        "Email": df.get("Email 1"),
        "Mobile Phone": df.get("Contact Mobile Phone"),
        "Work Phone": df.get("Contact Phone 1"),
        "LinkedIn URL": df.get("Contact LI Profile URL"),
        "Company Name": df.get("Company Name - Cleaned"),
        "Website": df.get("Website"),
        "Company Address": df.get("Company Location"),
        "City": df.get("Contact City"),
        "State": df.get("Contact State"),
        "Country": df.get("Contact Country"),
        "Company Revenue": df.get("Company Revenue Range"),
        "Employees": df.get("Company Staff Count"),
        "Industry": df.get("Company Industry"),
        "NAICS Code": df.get("NAICS Code"),
        "SIC Code": df.get("SIC Code"),
        "Source": "Seamless"
    })

parsed = None  # default
all_data = pd.DataFrame(columns=UNIFIED_COLUMNS) # Initialize an empty DataFrame

for file_name, file_content in uploaded.items():
    df = pd.read_csv(io.StringIO(file_content.decode('utf-8')))
    parsed = None  # Reset parsed for each file

    # ZoomInfo detection
    if {"ZoomInfo Contact ID", "LinkedIn Contact Profile URL", "Direct Phone Number"}.intersection(df.columns):
        parsed = parse_zoominfo(df)

    # Apollo detection
    elif {"Person Linkedin Url", "Work Direct Phone", "Departments"}.intersection(df.columns):
        parsed = parse_apollo(df)

    # Seamless.ai detection
    elif {"Email 1", "Company Name - Cleaned", "Contact LI Profile URL"}.intersection(df.columns):
        parsed = parse_seamless(df)

    # Salesgenie detection
    elif {"Executive First Name", "Primary SIC", "Location Sales Volume"}.intersection(df.columns):
        parsed = parse_salesgenie(df)

    # Unknown fallback
    if parsed is None:
        print(f"❌ Unknown format: {file_name}")
        print(f"📂 Columns in {file_name}: {df.columns.tolist()}")
        continue

    # Append parsed data to the all_data DataFrame
    all_data = pd.concat([all_data, parsed[UNIFIED_COLUMNS]], ignore_index=True)

print("✅ All files processed and merged!")
display(all_data.head())
    
    st.success(f"✅ Merged {len(all_data)} unique leads!")
    st.dataframe(all_data.head(50))

    csv = all_data.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Download Merged CSV", csv, "merged_leads.csv", "text/csv")
