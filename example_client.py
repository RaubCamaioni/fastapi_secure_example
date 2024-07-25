import requests

cert = "certs/client.crt"
key = "certs/client.key"
ca = "certs/server.crt"

url = "https://localhost:8080"

# cert: client side certificate authentication
# verify: certificate authority (server is self signed)
response = requests.get(url, cert=(cert, key), verify=ca)

print(f"Status Code: {response.status_code}")
print(f"Response Content: {response.text}")