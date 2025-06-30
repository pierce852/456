Cityline/UrbTix Ticket Bot
A Python-based Selenium bot for automating ticket purchases on Cityline and UrbTix platforms, configurable via settings.json. Warning: Automated ticketing may violate platform terms; use responsibly and comply with local laws.

Features
Command-line interface to select Cityline or UrbTix.
Automates login and detects captchas (requires manual completion).
Partially supports ticket type and quantity selection.
Prerequisites
Python 3.8+
Google Chrome
ChromeDriver (auto-managed by Selenium)
Required packages:
pip install selenium undetected-chromedriver python-decouple

Usage
Run the script:
python main.py
Choose platform: 1 for Cityline, 2 for UrbTix.
Manually complete captchas when prompted.
Extend scripts for full ticket selection and checkout as needed.

Project Structure
main.py: Selects and runs Cityline or UrbTix bot.
cityline_bot.py: Cityline automation script.
urbtix_bot.py: UrbTix automation with undetected_chromedriver.
settings.json: Configuration for credentials and event details.
Known Issues
Requires manual completion for puzzle slider captchas.
Unable to reliably locate login elements via XPath for auto-login.
Limited to login automation; ticket selection and checkout need implementation.
Cityline’s standard Chrome driver may trigger bot detection.
Future Improvements
Automate puzzle slider captchas (e.g., via 2Captcha).
Improve XPath reliability for login automation.
Complete ticket selection and checkout logic.
Add robust error handling and logging.
Legal Notice
Automated ticketing may violate Cityline/UrbTix terms of service, risking account bans. Use only for personal, non-commercial purposes and ensure compliance with local regulations.

License
MIT License