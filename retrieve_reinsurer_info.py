import requests
from bs4 import BeautifulSoup
import db_connector

url = "https://www.reinsurancene.ws/top-50-reinsurance-groups/"

response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")
    
    table = soup.find("table")
    
    
    for row in table.find_all("tr")[1:]:
        
        columns = row.find_all("td")

        ranking = columns[0].text.strip()
        company_name = columns[1].text.strip()

        def to_int_or_none(value):
            value = value.strip()
            return int(value) if value and value != 'N/A' else None
        
        glnl = to_int_or_none(''.join(filter(str.isdigit, columns[2].text)))
        nlnl = to_int_or_none(''.join(filter(str.isdigit, columns[3].text)))
        gnlo = to_int_or_none(''.join(filter(str.isdigit, columns[4].text)))
        nnlo = to_int_or_none(''.join(filter(str.isdigit, columns[5].text)))
        shareholders_fund = to_int_or_none(''.join(filter(str.isdigit, columns[6].text)))
        loss_ratio = to_int_or_none(''.join(filter(str.isdigit, columns[7].text)))
        expense_ratio = to_int_or_none(''.join(filter(str.isdigit, columns[8].text)))
        combined_ratio = to_int_or_none(''.join(filter(str.isdigit, columns[9].text)))


        db_connector.add_reinsurer(ranking, company_name, glnl, nlnl, gnlo, nnlo, shareholders_fund, loss_ratio, expense_ratio, combined_ratio)

else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
