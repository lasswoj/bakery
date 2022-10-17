This project needs:
* git
* bash
* conda
* configured database

to set up project run script/proj_setup.sh from bash (or git cmd if you are on windows)
if something goes wrong :
* create venv with python 3.8 and activate it
* install the dependencies using poetry install
* add the pre-push hooks script/create_hook.sh

connection to database is set up on few envvars
* u_name = database username (default is "postgres")
* u_password = password for u_name (default is "admin")
* host = database host (default is "localhost")
* db_name = name of database (default is "postgres")
* db_type = type of database (psql/mysql...) (default is "postgresql")


to run tests simply set the envvars and run the "python app.py" (to start the server) and "pytest test"
