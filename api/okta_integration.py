import requests

OKTA_DOMAIN = "https://your-okta-domain.okta.com"
API_TOKEN = "your-api-token"

headers = {
    "Authorization": f"SSWS {API_TOKEN}",
    "Content-Type": "application/json"
}

def create_user(email, first_name, last_name):
    payload = {
        "profile": {
            "email": email,
            "login": email,
            "firstName": first_name,
            "lastName": last_name
        }
    }
    response = requests.post(f"{OKTA_DOMAIN}/api/v1/users", json=payload, headers=headers)
    return response.json()

if __name__ == "__main__":
    new_user = create_user("user@example.com", "John", "Doe")
    print(new_user)

# Function to create a new user in Okta
import okta
from okta.client import Client as OktaClient
from okta.models import CreateUserRequest, UserProfile, UserCredentials, PasswordCredential

def create_okta_user(api_token, org_url, first_name, last_name, email, login, password):
    config = {
        "orgUrl": org_url,
        "token": api_token
    }
    client = OktaClient(config)

    user_profile = UserProfile({
        "firstName": first_name,
        "lastName": last_name,
        "email": email,
        "login": login
    })

    password_credential = PasswordCredential({
        "value": password
    })

    user_credentials = UserCredentials({
        "password": password_credential
    })

    create_user_request = CreateUserRequest({
        "profile": user_profile,
        "credentials": user_credentials
    })

    try:
        user = client.create_user(create_user_request)
        return user
    except Exception as e:
        print(f"Error creating user: {e}")
        return None
