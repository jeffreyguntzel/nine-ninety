#!/usr/bin/env python3

"""
Script to Fetch Nonprofit Information from ProPublica's Nonprofit Explorer API

Purpose:
- Reads a CSV file ('list.csv') containing names of nonprofit organizations.
- For each name, queries the ProPublica Nonprofit Explorer API to fetch details.
- Extracts the organization's name and EIN (Employer Identification Number).
- Outputs the results into a new CSV file ('ein.csv').

"""

import requests
import csv

def query_nonprofit(name):
    """
    Queries the ProPublica API for a given nonprofit name to retrieve its details.
    
    Args:
        name (str): The name of the nonprofit organization.

    Returns:
        tuple: A tuple containing the organization's name and EIN.
               Returns 'Not Found' for both fields if there's an error or no data.
    """
    # Construct the API endpoint URL with the query parameter
    url = f'https://projects.propublica.org/nonprofits/api/v2/search.json?q={name}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        # Check if the organizations list is not empty
        if data['organizations']:
            # Assume the first result is the desired organization
            org = data['organizations'][0]
            # Safely get the values using 'get' method to avoid KeyError
            org_name = org.get('name', 'Not Found')
            org_ein = org.get('ein', 'Not Found')
            return org_name, org_ein
    # Return 'Not Found' for both fields if there's an error or no data
    return name, 'Not Found'

# File names for input and output
input_filename = 'list.csv'
output_filename = 'ein.csv'

# Process the input file and write to the output file
with open(input_filename, newline='') as input_file, open(output_filename, 'w', newline='') as output_file:
    csv_reader = csv.reader(input_file)
    csv_writer = csv.writer(output_file)
    
    # Writing header row to the output file
    csv_writer.writerow(['entity', 'ein'])

    # Iterating over each row in the input file
    for row in csv_reader:
        if row:  # Ensure the row is not empty
            name = row[0]
            # Query the API for each nonprofit name
            result = query_nonprofit(name)
            # Write the results to the output file
            csv_writer.writerow(result)

print("Data saved to ein.csv")
