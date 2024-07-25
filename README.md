# uvicorn: http
```
# Start the uvicorn/fastapi website
uvicorn app.app:app --host 0.0.0.0 --port 8080
```
You can now reach the website at http://localhost:8080  

# generating self signed certificate
You will need to understand the settings inside the openssl.cnf, they will need to match your website values.  
```
# generate private key
openssl genpkey -algorithm RSA -out certs/server.key
# generate certificate request (This would be sent to a Certicate Authority (CA) for a real website)
openssl req -new -key certs/server.key -out certs/server.csr --config config/server.cnf
# generate self signed certificate
openssl x509 -req -days 365 -in certs/server.csr -signkey certs/server.key -out certs/server.crt -extensions v3_ca -extfile config/server.cnf
```

# uvicorn: https
Use your own or generate new certificates to use.
```
uvicorn app.app:app --host 0.0.0.0 --port 8080 --ssl-keyfile certs/server.key --ssl-certfile certs/server.crt
```
You can now reach the website at https://localhost:8080  

Your browser will should warn you the site is not secure.  
This is because the self sign certificate has not been added to your certificate store.  

Adding certificate to windows certificate store:  
```
-Double click certificate.crt in file browser
-Click install certificate button
-Click current user / local machine then click Next
--Current User only adds certificate for the currently logged in user
--Local Machine adds certificate for all users on the machine
-Click "Place all certificate in following store"
--Click Browse button
--Click "Trusted Root Certification Authorities"
--Click OK
--Click Next
-Click Finish
-Click Yes
-Click OK to import successful
-Click OK to close last windows
```

Adding certificate to linux certificate store (Ubuntu):
```
sudo cp server.crt /usr/local/share/ca-certificates/server.crt
sudo update-ca-certificates
```

Restart your browser:
You should now be able to reach your website without a security warning


# uvicorn: https, client authentication
Adding client authentication to fastapi/uvicorn website.
Only clients with signed certificates will be allowed to reach the website.

# generate client private key and certificate
```
# create certs directory
mkdir certs
# generate private key
openssl genpkey -algorithm RSA -out certs/client.key
# generate certificate request (This would be sent to a Certicate Authority (CA) for a real website)
openssl req -new -key certs/client.key -out certs/client.csr --config config/client.cnf
# generate server signed certificate
openssl x509 -req -days 365 -in certs/client.csr -CA certs/server.crt -CAkey certs/server.key -CAcreateserial -out certs/client.crt
```

verify client file
```
openssl verify -CAfile certs/server.crt certs/client.crt
```

Create PKCS#12 file for import into Windows
```
openssl pkcs12 -export -out certs/client.pfx -inkey certs/client.key -in certs/client.crt -name "localhost-custom"
```
Install pkcs12, use all defaults, place in Personal certificates location when clicking "browse" button.

Add client certificate verification flags
```
uvicorn app.app:app \
    --host 0.0.0.0 \
    --port 8080 \
    --ssl-keyfile certs/server.key \
    --ssl-certfile certs/server.crt \
    --ssl-ca-certs certs/server.crt \
    --ssl-cert-reqs 2
```

You should now be able to reach the website when using the certificate.  
There should be a pop up asking for what certificate to use.  

# Testing with curl: client side authentication (Ubuntu)
```
curl --cert certs/client.key --key certs/server.key https://localhost:8080
```

# Testing with python: client side authentication
Review the included python file.  
```
python example_client.py
```

# Running server with python vs uvicorn cli commands
Depending on your entrypoint you might need to execute uvicorn from python.  
This shows how to execute ubicorn using only python, instead of uvicorn cli.  
```
python app/app.py \
    --host 0.0.0.0 \
    --port 8080 \
    --key certs/server.key \
    --server_cert certs/server.crt \
    --client_ca certs/server.crt \
    --cert_required 2
```
