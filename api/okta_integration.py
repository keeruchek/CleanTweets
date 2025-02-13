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
