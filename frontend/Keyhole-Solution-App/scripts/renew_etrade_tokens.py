import os
import json
import webbrowser
from requests_oauthlib import OAuth1Session

# Constants
URLS = {
    "sandbox": "https://apisb.etrade.com",
    "production": "https://api.etrade.com"
}

def renew_etrade_tokens(env: str, consumer_key: str, consumer_secret: str):
    base_url = URLS[env]
    request_token_url = f"{base_url}/oauth/request_token"
    authorize_url = f"{base_url}/oauth/authorize"
    access_token_url = f"{base_url}/oauth/access_token"

    oauth = OAuth1Session(consumer_key, client_secret=consumer_secret, callback_uri="oob")

    # Step 1: Get request token
    fetch_response = oauth.fetch_request_token(request_token_url)
    resource_owner_key = fetch_response.get("oauth_token")
    resource_owner_secret = fetch_response.get("oauth_token_secret")

    # Step 2: Prompt user to authorize
    auth_url = f"{authorize_url}?key={consumer_key}&token={resource_owner_key}"
    print(f"\n🔗 Visit this URL to authorize E*TRADE access ({env}):\n{auth_url}")
    webbrowser.open(auth_url)

    verifier = input("🔑 Enter the verification code (PIN): ").strip()

    # Step 3: Exchange for access token
    oauth = OAuth1Session(
        consumer_key,
        client_secret=consumer_secret,
        resource_owner_key=resource_owner_key,
        resource_owner_secret=resource_owner_secret,
        verifier=verifier,
    )
    access_tokens = oauth.fetch_access_token(access_token_url)

    token_data = {
        "access_token": access_tokens.get("oauth_token"),
        "access_token_secret": access_tokens.get("oauth_token_secret")
    }

    save_path = f"/app/data/etrade_tokens_{env}.json"
    with open(save_path, "w") as f:
        json.dump(token_data, f)
    print(f"\n✅ Access token saved to {save_path}")

    # Step 4: Optional verification
    account_list_url = f"{base_url}/v1/accounts/list.json"
    oauth = OAuth1Session(
        consumer_key,
        client_secret=consumer_secret,
        resource_owner_key=token_data["access_token"],
        resource_owner_secret=token_data["access_token_secret"]
    )
    response = oauth.get(account_list_url)
    if response.status_code == 200:
        print("🎉 Verified: Account access is working.")
    else:
        print(f"⚠️ Token may be invalid. Status: {response.status_code}, Body: {response.text}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--env", choices=["sandbox", "production"], required=True)
    parser.add_argument("--key", required=True, help="Consumer key")
    parser.add_argument("--secret", required=True, help="Consumer secret")
    args = parser.parse_args()

    renew_etrade_tokens(args.env, args.key, args.secret)
