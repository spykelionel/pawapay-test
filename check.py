import requests

# Use the same token from your deposit request
token = "eyJraWQiOiIxIiwiYWxnIjoiRVMyNTYifQ.eyJ0dCI6IkFBVCIsInN1YiI6IjM2NTAiLCJtYXYiOiIxIiwiZXhwIjoyMDY0MTkzNTQ3LCJpYXQiOjE3NDg2NjA3NDcsInBtIjoiREFGLFBBRiIsImp0aSI6ImZiNTc5Mjk4LTVhMDAtNGQ3Ni05ZWEyLTQ3YWFkNzlhYzdhZiJ9.pKxwa1t4fe4cQKhZRyHUH-xcYZ3Y0sm1s0lkCsd2DPQ7T6nsJ7qPhUIrkSvLQRN7MhaFcDZ9k4D8q_x06G67_Q"

# Replace this with the deposit ID you want to check
deposit_id = "a57ad85d-4310-4ae6-9343-323727114217"

url = f"https://api.sandbox.pawapay.io/deposits/{deposit_id}"
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

response = requests.request("GET", url, headers=headers)

print("Status Code:", response.status_code)
print("Response:", response.text) 