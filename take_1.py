import requests
import smtplib
from bs4 import BeautifulSoup
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Email credentials
SENDER_EMAIL = 'otre@mailtesting.gtp.renu.ac.ug'  
RECIPIENT_EMAIL = 'tomudu@renu.ac.ug'  
SMTP_USER = 'notifications@renu.ac.ug'
SMTP_PASSWORD = '@SysAdm-Rnotifications!#'  
SMTP_PORT = '587'  
SMTP_SERVER = 'webmail.renu.ac.ug'

# Function to send email notification
def send_email(subject, body):
    
    message = MIMEMultipart()
    message['From'] = SENDER_EMAIL
    message['To'] = RECIPIENT_EMAIL
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))
        
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(SMTP_USER, SMTP_PASSWORD)
    text = message.as_string()
    server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, text)
    server.quit()


# Function to send mattermost notification
def send_mattermost_notification(text):
    payload = {'text': text}
    response = requests.post("https://chat.renu.ac.ug/hooks/tkeaszt3cfd4mp6sfxgo1tp6ar", json=payload)
        
       

# Function to fetch and parse data
def get_data():
    try:
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

        # Parse the HTML content of the response using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Locate the first table
        table_1 = soup.find('table', {'class': 'db', 'border': '1'})

        listed_prefixes = []

        # Check if table one was found
        if table_1:
            # Extract the table rows
            for row in table_1.find_all('tr')[1:]:  # Skip the header row
                columns = [td.text.strip() for td in row.find_all('td')]
                # Check if "NOT LISTED" is not in the columns
                if "NOT LISTED" not in columns:
                    listed_prefixes.append(" | ".join(columns))  # Collect listed prefixes
        else:
            print("Table 1 not found in the response.")
        
        # Return the listed prefixes as a string (joined by newlines)
        return "\n".join(listed_prefixes) if listed_prefixes else "No prefixes are listed."

    except Exception as e:
        return f"An error occurred: {e}"

# Main logic
output = get_data()
if output.strip():
    send_email("Listed Prefixes Notification", output)
    send_mattermost_notification(f"**Listed Prefixes:**\n```{output}```")
else:
    send_email("Listed Prefixes Notifications", "No prefixes listed")
    send_mattermost_notification(f"**Listed Prefixes:**\n```{'No listed prefix'}```")
