# Create the virtualenv named venv
python -m venv .venv

# Install the packages from the requirements.txt into the venv
pip install -r requirements.txt


# To add installed packages to requirements.txt
pip freeze > requirements.txt