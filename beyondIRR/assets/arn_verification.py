import requests
from bs4 import BeautifulSoup

url = 'https://www.amfiindia.com/modules/NearestFinancialAdvisorsDetails'

# Function to check ARN number
def check_arn(arn_number: int):
    arn_number = str(arn_number)
    if len(arn_number) == 0:
        arn_number = "0000"
    elif len(arn_number) == 1:
        arn_number = "000"+arn_number
    elif len(arn_number) == 2:
        arn_number = "00"+arn_number
    elif len(arn_number) == 3:
        arn_number = "0"+arn_number
        
    payload = {
        "nfaARN": arn_number,
        "nfaType": "All"
    }
    
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        status_element = soup.find_all('tr')[1]
        try:
            if status_element:
                td_details = status_element.find_all('td')
                amfi_arn_number = td_details[1].text.strip()
                amfi_email = td_details[5].text.strip()
                return {"amfi_arn_number": amfi_arn_number, "amfi_email": amfi_email}
            else:
                return 'ARN number not found in AMFI website.'
        except:
            return 'ARN number not found in AMFI website.'
    else:
        return 'Failed to retrieve data. Status code: ' + str(response.status_code)

