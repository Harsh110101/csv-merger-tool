import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="CSV Merger", layout="wide")
st.title("📁 CSV Merger for ZoomInfo, Apollo, Seamless, and Salesgenie")

UNIFIED_COLUMNS = [
    "First Name", "Last Name", "Full Name", "Title", "Seniority", "Department",
    "Email", "Mobile Phone", "Work Phone", "Person LinkedIn URL",
    "Company Name", "Website","Founding Year", "Facebook URL", "LinkedIn URL", "Twitter URL", "Company Address", "City", "State", "Country",
    "Company Revenue", "Employees", "Industry",
    "NAICS Code", "SIC Code", "Total number of locations", "Source"
]

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
        "Person LinkedIn URL": df.get("LinkedIn Contact Profile URL"),
        "Company Name": df.get("Company Name"),
        "Website": df.get("Website"),
        "Founding Year": df.get("Founded Year"),
        "Facebook URL": df.get("Facebook URL"),
        "LinkedIn URL": df.get("LinkedIn URL"),
        "Twitter URL": df.get("Twitter URL"),
        "Company Address": df.get("Company Street Address"),
        "City": df.get("Company City"),
        "State": df.get("Company State"),
        "Country": df.get("Company Country"),
        "Company Revenue": df.get("Revenue (in 000s USD)").apply(lambda x: int(x * 1000) if pd.notna(x) else x),
        "Employees": df.get("Employees"),
        "Industry": df.get("Primary Industry"),
        "NAICS Code": df.get("NAICS Code 1"),
        "SIC Code": df.get("SIC Code 1"),
        "Total number of locations": df.get("Number of Locations"),
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
        "Person LinkedIn URL": df.get("Person Linkedin Url"),
        "Company Name": df.get("Company"),
        "Website": df.get("Website"),
        "Founding Year": "",
        "Facebook URL": df.get("Facebook Url"),
        "LinkedIn URL": df.get("Company Linkedin Url"),
        "Twitter URL": df.get("Twitter Url"),
        "Company Address": df.get("Company Address"),
        "City": df.get("City"),
        "State": df.get("State"),
        "Country": df.get("Country"),
        "Company Revenue": df.get("Annual Revenue"),
        "Employees": df.get("# Employees"),
        "Industry": df.get("Industry"),
        "NAICS Code": "",
        "SIC Code": "",
        "Total number of locations": df.get("Number of Retail Locations"),
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
        "Person LinkedIn URL": "",
        "Company Name": df.get("Company Name"),
        "Website": df.get("Website"),
        "Founding Year": "",
        "Facebook URL": "",
        "LinkedIn URL": "",
        "Twitter URL": "",
        "Company Address": df.get("Address"),
        "City": df.get("City"),
        "State": df.get("Province"),
        "Country": "Canada",
        "Company Revenue": df.get("Location Sales Volume").apply(lambda x: int(str(x).replace("$", "").replace(",", "").strip()) if pd.notna(x) and str(x).strip() != '' else ""),
        "Employees": df.get("Location Number of Employees"),
        "Industry": df.get("Primary NAICS Description"),
        "NAICS Code": df.get("Primary NAICS"),
        "SIC Code": df.get("Primary SIC"),
        "Total number of locations": "",
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
        "Person LinkedIn URL": df.get("Contact LI Profile URL"),
        "Company Name": df.get("Company Name - Cleaned"),
        "Website": df.get("Website"),
        "Founding Year": df.get("Company Founded Year"),
        "Facebook URL": "",
        "LinkedIn URL": df.get("Company LI Profile Url"),
        "Twitter URL": "",
        "Company Address": df.get("Company Location"),
        "City": df.get("Contact City"),
        "State": df.get("Contact State"),
        "Country": df.get("Contact Country"),
        "Company Revenue": df.get("Company Annual Revenue"),
        "Employees": df.get("Company Staff Count"),
        "Industry": df.get("Company Industry"),
        "NAICS Code": df.get("NAICS Code"),
        "SIC Code": df.get("SIC Code"),
        "Total number of locations": "",
        "Source": "Seamless"
    })

# Upload
uploaded_files = st.file_uploader("📂 Upload CSV files", type="csv", accept_multiple_files=True)

if uploaded_files:
    all_data = pd.DataFrame(columns=UNIFIED_COLUMNS)

    for file in uploaded_files:
        filename = file.name
        df = pd.read_csv(file)
        parsed = None

        # Universal source detection
        if {"ZoomInfo Contact ID", "LinkedIn Contact Profile URL", "Direct Phone Number"}.intersection(df.columns):
            parsed = parse_zoominfo(df)
        elif {"Person Linkedin Url", "Work Direct Phone", "Departments"}.intersection(df.columns):
            parsed = parse_apollo(df)
        elif {"Email 1", "Company Name - Cleaned", "Contact LI Profile URL"}.intersection(df.columns):
            parsed = parse_seamless(df)
        elif {"Executive First Name", "Primary SIC", "Location Sales Volume"}.intersection(df.columns):
            parsed = parse_salesgenie(df)

        if parsed is None:
            st.warning(f"❌ Unknown format: {filename}")
            with st.expander(f"📂 Columns in {filename}"):
                st.write(df.columns.tolist())
            continue

        all_data = pd.concat([all_data, parsed], ignore_index=True)

       # all_data.drop_duplicates(subset=["Full Name", "Company Name"], inplace=True)
    #Removing Duplicates by ranking the designation

    # Step 1: Create a seniority ranking map
seniority_map = {
    "ceo": 1, "chief executive officer": 1, "cto": 1, "chief technology officer": 1, "owner": 1,
    "coo": 1, "chief operating officer": 1, "cio": 1, "chief information officer": 1, "cheif financial officer": 1, "founder": 1,
    "co-founder": 2,
    "president": 3,
    "vp": 4, "vice president": 4,
    "director": 5,
    "head": 6,
    "manager": 7,
    "lead": 8,
    "senior": 9,
    "consultant": 10,
    "analyst": 11,
    "associate": 12,
    "intern": 13
}

# Step 2: Define function to assign rank
def get_seniority(title):
    if pd.isna(title):
        return 999
    title = title.lower()
    for keyword, rank in seniority_map.items():
        if keyword in title:
            return rank
    return 999  # default for unranked or unknown titles

# Step 3: Apply ranking to DataFrame
all_data["Seniority Rank"] = all_data["Title"].apply(get_seniority)

# Step 4: Sort by company and seniority
all_data.sort_values(by=["Company Name", "Seniority Rank"], ascending=[True, True], inplace=True)

# Step 5: Drop duplicates to keep only the most senior contact per company
all_data = all_data.drop_duplicates(subset=["Company Name"], keep="first")

# Optional: Drop the helper column if you don’t want to export it
all_data.drop(columns=["Seniority Rank"], inplace=True)


st.success(f"✅ Merged {len(all_data)} unique leads!")
st.dataframe(all_data.head(50))

csv = all_data.to_csv(index=False).encode("utf-8")
st.download_button("📥 Download Merged CSV", csv, "merged_leads.csv", "text/csv")
