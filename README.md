# RUNS ON WINDOWS ###

## For creating Virtual Environment
```sh
pip install virtualenv
virtualenv venv
./venv/Scripts/activate
pip install -r requirements.txt
```


## For fetching, creating database and making queries

* Please ensure to have mysql server running with zing42 database already present
* can also change the configurations from the connect.py

```sh
python fetcher.py
python db.py
python query.py
```