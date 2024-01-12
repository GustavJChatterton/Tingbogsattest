
def GetBFENumber():
    import uuid
    import requests
    import json
    from robot_framework.GetKMDAcessToken import GetKMDToken

    # URL of the API endpoint
    url = 'https://novaapi.kmd.dk/api/Case/GetList?api-version=1.0-Case'
    access_token = GetKMDToken()
    CaseNumber = 'S2021-456011'
    TransactionID = str(uuid.uuid4())

    print("Henter BFENR og CaseUuid på følgende sag: " + CaseNumber)

    # JSON data to be sent in the request body
    payload = {
        "common": {
            "transactionId": TransactionID
        },
        "paging": {
            "startRow": 1,
            "numberOfRows": 200
        },
        "caseAttributes": {
            "userFriendlyCaseNumber": "S2021-456011"
        },
        "caseGetOutput": {
            "caseAttributes": {
                "title": True
            },
            "buildingCase": {
                "buildingCaseAttributes": {
                    "buildingCaseClassName": True,
                    "bbrCaseId": True
                },
                "propertyInformation": {
                    "caseAddress": True,
                    "esrPropertyNumber": True,
                    "bfeNumber": True
                }
            }
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
    response = requests.put(url, data=json_payload, headers=headers)

    # Check the response status
    if response.status_code == 200:
        print("POST request successful!")
        # If you want to access the response content
        json_data = response.json()
        CaseUuid = json_data['cases'][0]['common']['uuid']
        BFENR = json_data['cases'][0]['buildingCase']['propertyInformation']['bfeNumber']
        CaseAdress = json_data["cases"][0]["buildingCase"]["propertyInformation"]["caseAddress"]
        # Check if CaseAdress is None or empty, and return False if it is
        if CaseAdress is None or CaseAdress == '':
            return CaseUuid, BFENR, False
        else:
            return CaseUuid, BFENR, CaseAdress


    else:
        print("POST request failed with status code:", response.status_code)
        print("Response:", response.text)