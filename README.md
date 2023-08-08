# faro

To run code locally, run
```
pip install venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
gunicorn wsgi:app
```

To use the Dockerfile, you'll be needing to add the certificate and key .pem files, which can be obtained from certbot. If not to run as a local docker container change the docker file command without the command line arguments of the key and certificate.

Create your own persistant db, with your own docs, by running the newdb.py as a standalone script
```
python3 newdb.py
```

This is still a prototype model of the backend.
