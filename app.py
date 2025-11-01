from readline import redisplay
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

# Upload CSV files
uploaded_files = st.file_uploader("📂 Drop your CSV files here", type="csv", accept_multiple_files=True)


# Define all your parser functions here
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

def parse_salesgenie_us(df):
    return pd.DataFrame({
        "First Name": df.get("Executive First Name"),
        "Last Name": df.get("Executive Last Name"),
        "Full Name": df.get("Executive First Name") + " " + df.get("Executive Last Name"),
        "Title": df.get("Executive Title"),
        "Seniority": "",  # Not explicitly provided
        "Department": "",  # Not available
        "Email": "",  # No email field in US export
        "Mobile Phone": "",  # Not present in schema
        "Work Phone": df.get("Phone Number Combined"),
        "Person LinkedIn URL": "",  # Not present
        "Company Name": df.get("Company Name"),
        "Website": df.get("Company Website"),
        "Founding Year": df.get("Year Established"),
        "Facebook URL": "",
        "LinkedIn URL": "",
        "Twitter URL": "",
        "Company Address": df.get("Location Address"),
        "City": df.get("Location City"),
        "State": df.get("Location State"),
        "Country": "USA",
        "Company Revenue": df.get("Location Sales Volume Actual").apply(
            lambda x: int(str(x).replace("$", "").replace(",", "").strip()) if pd.notna(x) and str(x).strip() != "" else ""
        ),
        "Employees": df.get("Location Employee Size Actual"),
        "Industry": df.get("Primary NAICS Description"),
        "NAICS Code": df.get("Primary NAICS Code"),
        "SIC Code": df.get("Primary SIC Code"),
        "Total number of locations": df.get("Affiliated Locations"),
        "Source": "Salesgenie US"
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
        "Company Name": df.get("Company Name"),
        "Website": df.get("Website"),
        "Founding Year": "",
        "Facebook URL": df.get("Facebook Url"),
        "LinkedIn URL": df.get("Company Linkedin Url"),
        "Twitter URL": df.get("Twitter Url"),
        "Company Address": df.get("Company Address"),
        "City": df.get("Company City"),
        "State": df.get("Company State"),
        "Country": df.get("Company Country"),
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
        "Founding Year": df.get("Primary SIC Year Appeared"),
        "Facebook URL": "",
        "LinkedIn URL": "",
        "Twitter URL": "",
        "Company Address": df.get("Address"),
        "City": df.get("City") or df.get("Location City"),
        "State": df.get("Province") or df.get("Location State"),
        "Country": "Canada",
        revenue_col = df.get("Location Sales Volume") or df.get("Location Sales Volume Actual")
        "Company Revenue": revenue_col.apply(lambda x: int(str(x).replace("$", "").replace(",", "").strip()) if pd.notna(x) and str(x).strip() != '' else ""),
        "Employees": df.get("Location Number of Employees") or df.get("Location Number of Employees Actual"),
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
        "City": df.get("Company City"),
        "State": df.get("Company State"),
        "Country": df.get("Company Country"),
        "Company Revenue": df.get("Company Annual Revenue"),
        "Employees": df.get("Company Staff Count"),
        "Industry": df.get("Company Industry"),
        "NAICS Code": df.get("NAICS Code"),
        "SIC Code": df.get("SIC Code"),
        "Total number of locations": "",
        "Source": "Seamless"
    })

#Merging starts
all_data = pd.DataFrame(columns=UNIFIED_COLUMNS) # Initialize an empty DataFrame

for uploaded_files in uploaded_files:
    file_name = uploaded_files.name
    file_content = uploaded_files.read()
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

    # Salesgenie US detection
    elif {"Executive First Name", "Phone Number Combined", "Primary NAICS Code"}.intersection(df.columns):
        parsed = parse_salesgenie_us(df)

    # Unknown fallback
    if parsed is None:
        print(f"❌ Unknown format: {file_name}")
        print(f"📂 Columns in {file_name}: {df.columns.tolist()}")
        continue

    # Append parsed data to the all_data DataFrame
    all_data = pd.concat([all_data, parsed[UNIFIED_COLUMNS]], ignore_index=True)

#print("✅ All files processed and merged!")
#display(all_data.head())

#all_data = pd.concat([all_data, parsed], ignore_index=True)

#Removing the duplicates

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

# Rename columns for final export (e.g., "First Name" → "First Name (Clay)")
column_renames = {
    "First Name": "First Name (Clay)",
    "Last Name": "Last Name (Clay)",
    "Full Name": "Full Name (Clay)",
    "Title": "Title (Clay)",
    "Seniority": "Seniority (Clay)",
    "Department": "Department (Clay)",
    "Email": "Email (Clay)",
    "Mobile Phone": "Mobile Phone (Clay)",
    "Work Phone": "Work Phone (Clay)",
    "Person LinkedIn URL": "Person LinkedIn URL (Clay)",
    "Company Name": "Company Name (Clay)",
    "Website": "Website (Clay)",
    "Founding Year": "Founding Year (Clay)",
    "Facebook URL": "Facebook URL (Clay)",
    "LinkedIn URL": "LinkedIn URL (Clay)",
    "Twitter URL": "Twitter URL (Clay)",
    "Company Address": "Company Address (Clay)",
    "City": "City (Clay)",
    "State": "State (Clay)",
    "Country": "Country (Clay)",
    "Company Revenue": "Company Revenue (Clay)",
    "Employees": "Employees (Clay)",
    "Industry": "Industry (Clay)",
    "NAICS Code": "NAICS Code (Clay)",
    "SIC Code": "SIC Code (Clay)",
    "Total number of locations": "Total Locations (Clay)",
    "Source": "Source (Clay)"
}

# Apply renaming
all_data.rename(columns=column_renames, inplace=True)


# Step 6: Show result
st.success(f"✅ Unique companies retained with highest-ranked titles: {len(all_data)}")


st.success(f"✅ Merged {len(all_data)} unique leads!")
st.dataframe(all_data.head(50))

csv = all_data.to_csv(index=False).encode("utf-8")
st.download_button("📥 Download Merged CSV", csv, "merged_leads.csv", "text/csv")






