from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.http import HttpResponse
import requests
from bs4 import BeautifulSoup

def vehicle_form(request):
    if request.method == 'POST':
        wheel = request.POST.get('wheel')
        cc = request.POST.get('cc')
        from_field = request.POST.get('from')
        renew = request.POST.get('renew')
        expiry = request.POST.get('expiry')
        province = request.POST.get('province')
        manufacture = request.POST.get('manufacture')
        seat = request.POST.get('seat', '')  # Handle empty seat field
        insurance = 'insurance' in request.POST

        # Prepare the query parameters
        params = {
            'wheel': wheel,
            'cc': cc,
            'from': from_field,
            'renew': renew,
            'expiry': expiry,
            'province': province,
            'manufacture': manufacture,
            'seat': seat,
            'insurance': 1 if insurance else 0
        }
        print(params)

        # API URL
        url = "https://www.hellobeema.com/"

        # Make the GET request to the API
        response = requests.get(url, params=params)

        # Assuming the API returns a JSON response
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
                    return render(request, 'result.html', {'data_received': data})


                    print(data)
        else:
            data_received = {'error': 'Failed to retrieve data from API'}

        # Render the result template with the received data
        return render(request, 'result.html', {'data_received': data_received})

    return render(request, 'vehicle_form.html')
