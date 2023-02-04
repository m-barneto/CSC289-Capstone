# If virtualenv isn't already installed
pip install virtualenv
# Create the virtualenv named venv
python -m virtualenv venv

# Activate the venv
.\venv\Scripts\Activate.ps1

# Install the packages from the requirements.txt into the venv
pip install -r requirements.txt


# To add packages

pip freeze > requirements.txt