# IntelliopsBackend

## Install dependencies
python3 -m venv venv
source venv/bin/activate
pip3 install -r mock_server/requirements.txt

## Run server
uvicorn main:app

## Run mock server
uvicorn mock_server.app.main:app --port 5000
