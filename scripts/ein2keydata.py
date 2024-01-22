#!/usr/bin/env python3

"""
Script to Interact with ProPublica Nonprofit Explorer API

Purpose:
- Reads 'ein.csv' from the current working directory.
- Extracts EINs from the 'ein' column.
- For each EIN, requests specific data from ProPublica Nonprofit Explorer API.
- Extracts specified fields from the 'organization' section and 'filings_with_data' for each year from 2011 to 2020, in a specified order.
- Outputs the data into a CSV file, preserving the year context in 'filings_with_data' fields.

"""

import requests
import csv
import pandas as pd

def get_nonprofit_data(ein):
    """
    Fetches data for a given nonprofit EIN from the ProPublica API.
    Args:
        ein (str): The EIN of the nonprofit organization.
    Returns:
        dict: JSON data from the API response.
    """
    # Construct the API URL for the given EIN
    url = f'https://projects.propublica.org/nonprofits/api/v2/organizations/{ein}.json'
    response = requests.get(url)
    # Return JSON data if request is successful
    if response.status_code == 200:
        return response.json()
    else:
        return None

def extract_required_data(data):
    """
    Extracts required fields from organization data and filings_with_data.
    Args:
        data (dict): JSON data for a nonprofit.
    Returns:
        dict: Extracted data with required fields.
    """
    org_data = data.get('organization', {})
    filings_data = data.get('filings_with_data', [])

    # Extract organization fields
    org_fields = {key: org_data.get(key, '') for key in organization_fields}

    # Extract filings_with_data fields with year context
    for filing in filings_data:
        year = filing.get('tax_prd_yr')
        if year and 2011 <= year <= 2020:
            for field in filings_fields:
                org_fields[f'{field}_{year}'] = filing.get(field, '')

    return org_fields

# Fields to extract from the organization data and filings_with_data
organization_fields = [
    # List of fields under 'organization' in the specified order
    'id', 'ein', 'name', 'careofname', 'address', 'city', 'state', 'zipcode', 
    'exemption_number', 'subsection_code', 'affiliation_code', 'classification_codes', 
    'ruling_date', 'deductibility_code', 'foundation_code', 'activity_codes', 
    'organization_code', 'exempt_organization_status_code', 'tax_period', 
    'asset_code', 'income_code', 'filing_requirement_code', 
    'pf_filing_requirement_code', 'accounting_period', 'asset_amount', 
    'income_amount', 'revenue_amount', 'ntee_code', 'sort_name', 'created_at', 
    'updated_at', 'data_source', 'have_extracts', 'have_pdfs', 'latest_object_id']

filings_fields = [
    # Common fields under 'filings_with_data' for each year from 2011 to 2020
    'ein', 'formtype', 'pct_compnsatncurrofcr', 'pdf_url', 'tax_prd', 
    'tax_prd_yr', 'totassetsend', 'totfuncexpns', 'totliabend', 'totrevenue', 'updated']

# Read EINs from 'ein.csv'
input_filename = 'ein.csv'
ein_df = pd.read_csv(input_filename)

# Initialize a list to hold all extracted data
all_data = []

# Fetch and extract data for each EIN
for ein in ein_df['ein']:
    data = get_nonprofit_data(ein)
    if data:
        extracted_data = extract_required_data(data)
        all_data.append(extracted_data)

# Define the ordered list of column names
ordered_fieldnames = organization_fields[:]
for year in range(2011, 2021):
    for field in filings_fields:
        ordered_fieldnames.append(f'{field}_{year}')

# Write the extracted data to 'nonprofit_data.csv' using the ordered fieldnames
output_filename = 'nonprofit_data.csv'
with open(output_filename, 'w', newline='') as output_file:
    csv_writer = csv.DictWriter(output_file, fieldnames=ordered_fieldnames)
    csv_writer.writeheader()
    for data in all_data:
        # Fill in missing data with an empty string
        row = {field: data.get(field, '') for field in ordered_fieldnames}
        csv_writer.writerow(row)

print("Data saved to nonprofit_data.csv")
