"""This module contains the main process of the robot."""
import requests
import os
import uuid
import json
import datetime
from robot_framework import GetBFENR, GetTingBogsUrl, GetKMDAcessToken

##Henter BFE-nummer og Case uuid
CaseInfo = GetBFENR.GetBFENumber()
CaseUuid = CaseInfo[0]
BFENumber = str(CaseInfo[1])
CaseAdress = CaseInfo[2]
print(CaseUuid)
print(BFENumber)

## Henter Tingbogsurl:
TingsbogsInfo = GetTingBogsUrl.TingBogsURL()
URL = [row[3] for row in TingsbogsInfo]
URL = URL[0]
if CaseAdress is False:
    CaseAdress = [row[1] for row in TingsbogsInfo]
    CaseAdress = CaseAdress[0]
    print("Henter adresse i database: " + CaseAdress)
else:
    print(CaseAdress)

# Local path where you want to save the PDF
ExcelFilNavn = "Tingbogsattest - " + CaseAdress + ".pdf"

# Get the current user's username
username = os.getlogin()  # or use os.environ['USERNAME']
# Construct the save path
save_path = f"C:\\Users\\{username}\\Downloads\\" + ExcelFilNavn  # Replace 'your_file.pdf' with your desired file name

# Send a GET request to the PDF URL
response = requests.get(URL)

# Check if the request was successful
if response.status_code == 200:
    # Write the content of the response to a file
    with open(save_path, 'wb') as pdf_file:
        pdf_file.write(response.content)
    print(f"PDF successfully downloaded to {save_path}")
else:
    print(f"Failed to download PDF. Status code: {response.status_code}")

# URL of the API endpoint
TransactionID = str(uuid.uuid4())
DocumentID = str(uuid.uuid4())
access_token = GetKMDAcessToken.GetKMDToken()
url = 'https://novaapi.kmd.dk/api/Document/UploadFile/' + TransactionID + '/' + DocumentID + '?api-version=1.0-Case'

# Set the Authorization header with the bearer token
headers = {
    'Authorization': f'Bearer {access_token}'
}

# Open the file in binary mode

with open(save_path, 'rb') as file:
    files = {
        'file': (save_path, file, 'application/pdf')
    }

    # Make the POST request with headers and file
    response = requests.post(url, headers=headers, files=files)

# Check the response status
if response.status_code == 200:
    print("POST request successful!")
else:
    print("POST request failed with status code:", response.status_code)
    print("Response:", response.text)

# Definerer variable, som skal sende med sidste API-kald:
ID = str(uuid.uuid4())

# Get the current date and time
now = datetime.datetime.now(datetime.timezone.utc)
# Format the date and time in the specified format: "yyyy-mm-ddThh:mm:ssZ"
ConfigDate  = now.strftime("%Y-%m-%dT%H:%M:%SZ")
print(ConfigDate)

NovaUnitId = '0c89d77b-c86f-460f-9eaf-d238e4f451ed'
UnitNumber = '70528'
UnitName = 'Plan og Byggeri'
UserKey = '2GBYGSAG'
identificationType = 'BfeNummer'

url = 'https://novaapi.kmd.dk/api/Document/Import?api-version=1.0-Case'

# JSON data to be sent in the request body
payload = {
    "common": {
        "transactionId": ID,
        "uuid": DocumentID
    },
    "caseUuid": CaseUuid,
    "documentType": "Internt",
    "title": ExcelFilNavn,
    "approved": True,
    "acceptReceived": True,
    "AccessToDocuments": True,
    "sensitivity": "Følsomme",
    "documentDate": ConfigDate,
        "caseworker": {
            "losIdentity": {
                "novaUnitId": NovaUnitId,
                "administrativeUnitId": UnitNumber,
                "fullName": UnitName,
                "userKey": UserKey
            }
        },
        "documentParty": {
            "identificationType": identificationType,
            "identification": BFENumber
        }
    }

# Convert the payload to JSON format
json_payload = json.dumps(payload)

# Set the Authorization header with the bearer token
headers = {
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/json'  # Specify content type as JSON
}

   # Make the POST request with headers
response = requests.post(url, data=json_payload, headers=headers)

# Check the response status
if response.status_code == 200:
    print("POST request successful!")
    print("Response:", response.text)
else:
    print("POST request failed with status code:", response.status_code)
    print("Response:", response.text)

if os.path.exists(save_path):
    os.remove(save_path)
    print("File is deleted")
else:
    print("The file does not exists")

# if __name__ == '__main__':
#    conn_string = os.getenv("OpenOrchestratorConnString")
#    crypto_key = os.getenv("OpenOrchestratorKey")
#    oc = OrchestratorConnection("Sletning Test", conn_string, crypto_key, "")
#     process(oc)