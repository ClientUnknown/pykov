# Work In Progress

This is an API, written in Python, for Escape From Tarkov based on dank's work: https://github.com/dank/tarkov

The main goal of this API is to provide simple and concise methods for retrieving various information from the Escape From Tarkov REST API in Python. Most methods will return a Python dictionary with requested information.

# Login

Login with two-factor authentication is supported, but the user will need to manually enter the authentication code when prompted. Captcha bypass is possible thanks to Cosmos3904 https://github.com/Cosmo3904/Recaptcha-Harvester-V2

**Notes For Captcha:**
To bypass the Captcha you will need to download ChromeDriver first and then add it to your system's path https://sites.google.com/a/chromium.org/chromedriver/downloads

# Features so far include:

* Automatic version updating upon launch, with functions to update as needed
* Retrieval of information like items, traders, and profiles
* Easy to use JSON in Python's dictionary format

# Pip Package

There is currently a pip package available using **pip install pykov-eft**. Please note that the package may not be as up-to-date as this repository.

Requires Flask and selenium.

# Example

A basic example is included under example.py, along with the example_get_all_items.txt file that it produces. More example usage will be provided in the future.

# UNOFFICIAL

This project is not affiliated to BattleState Games or Escape From Tarkov in any way.