# Create the virtualenv named venv
python -m venv .venv

# Figure out how to activate the venv depending on your OS

# Install the packages from the requirements.txt into the venv
pip install -r requirements.txt


# To add installed packages to requirements.txt
pip freeze > requirements.txt


# To start the server, make sure you have the venv activated and run:
uvicorn main:app
