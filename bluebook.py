import requests
from bs4 import BeautifulSoup

# API URL
url = "https://www.hellobeema.com/"
params = {
    "wheel": 2,
    "cc": 159,
    "from": "web",
    "renew": "2079-04-12",
    "expiry": "2080-04-11",
    "province": "Province 3",
    "manufacture": 2021,
    "seat": "",
    "insurance": "on"
}

# Send GET request
response = requests.get(url, params=params)

# Check if the request was successful
if response.status_code == 200:
    # Parse HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the modal with id 'calcData'
    modal = soup.find('div', id='calcData')
    
    if modal:
        # Extract the table data
        table = modal.find('table')
        if table:
            rows = table.find_all('tr')
            
            data = {}
            for row in rows:
                cols = row.find_all('td')
                if len(cols) == 2:
                    key = cols[0].get_text(strip=True)
                    value = cols[1].get_text(strip=True)
                    data[key] = value
            
            # Extract the total bill amount
            total_row = table.find('tfoot').find('tr')
            if total_row:
                total_amount = total_row.find('th', id='total')
                if total_amount:
                    data['Total Bill Amount'] = total_amount.get_text(strip=True)

            print(data)
            for key, value in data.items():
                print(f"{key}: {value}")
        else:
            print("Table not found in modal.")
    else:
        print("Modal with id 'calcData' not found.")
else:
    print("Failed to retrieve data. Status code:", response.status_code)
