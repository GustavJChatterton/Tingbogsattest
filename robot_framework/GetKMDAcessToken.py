def GetKMDToken():
    # Anvender denne video: https://www.youtube.com/watch?v=qbLc5a9jdXo

    # Henter API token:
    import requests

    # Replace these values with your actual keys
    client_id = 'aarhus_kommune'
    client_secret = 'lottNjMyx07BBfEzkVx5P2HwPWpvz2sG'
    scope = 'client'
    grant_type = 'client_credentials'

    # API endpoint to get the access token
    token_url = 'https://novaauth.kmd.dk/realms/NovaIntegration/protocol/openid-connect/token'

    # Data to be sent in the POST request
    keys = {
        'client_id': client_id,
        'client_secret': client_secret,
        'scope': scope,
        'grant_type': grant_type,  # Specify the grant type you're using
    }

    # Sending POST request to get the access token
    response = requests.post(token_url, data=keys)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        access_token = response.json().get('access_token')
        print("Access token granted")
        return access_token
    else:
        print("Failed to get the access token")
