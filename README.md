#Warbler

### to run
```
python3 -m venv venv
source venv/bin/activate
```
you will now see (venv) in your terminal to confirm you're using the virtual environment, continue
```
pip install -r requirements.txt
createdb warbler
python3 seed.py
FLASK_ENV=development flask run
```