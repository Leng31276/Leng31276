# cisco-sdwan-api

Setup Python Virtual Environment (requires Python 3.7+)
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
Setup local environment variable
```
export VMANAGE_HOST=<vmanage ip>
export VMANAGE_PORT=<vmanage port>
export VMANAGE_USER=<vmanage username>
export VMANAGE_PASS=<vmanage password>
```
Run python code
```
python main.py
```