import requests
from bs4 import BeautifulSoup

# Load the initial form page to get the dynamic 'subchannel' value
form_page_url = "https://www.uceprotect.net/en/rblcheck.php"
response = requests.get(form_page_url)
soup = BeautifulSoup(response.text, 'html.parser')

# Extract the 'subchannel' value from the hidden input field
subchannel_value = soup.find('input', {'name': 'subchannel'})['value']


# Submit the form with the extracted 'subchannel' value
form_data = {   
    'whattocheck': 'ASN',
    'ipr': '327687',
    'subchannel': subchannel_value
}

# Submit the form using a POST request
post_url = "https://www.uceprotect.net/en/rblcheck.php"
response = requests.post(post_url, data=form_data)

# Process the response
if response.status_code == 200:
   #print("Form submitted successfully!")
    
    # Parse the HTML content of the response using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Locate the first table
    table_1 = soup.find('table', {'class': 'db', 'border': '1'})

       
    # Check if table one was found
    if table_1:
        # Extract the table one headers
        headers = [th.text.strip() for th in table_1.find_all('th')]
        print(" | " .join(headers))
        
        # Extract the table rows
        for row in table_1.find_all('tr')[1:]:  # Skip the header row
            columns = [td.text.strip() for td in row.find_all('td')]
            print(" |            " .join(columns))
    else:
        print("Table not found in the response.")

   
    table_2 = soup.find_all('table', {'class':'db', 'border': '1'})[1]

    if table_2: 
        # Extract table 2 headers
        headers = [th.text.strip() for th in table_2.find_all('th')]
        print(" | " .join(headers))

        for row in table_2.find_all('tr')[1:]:
        # Extract table 2 rows
            columns= [td.text.strip() for td in row.find_all('td')]
            print(" |   " .join(columns))
    else:
        print("Table not there")


    
else:
    print(f"Failed to submit form. Status code: {response.status_code}")

