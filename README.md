# Cityline/UrbTix Ticket Bot

A Python-based Selenium automation tool for ticket purchasing on Cityline and UrbTix platforms.

This bot automates login and captcha detection (with manual intervention) for ticket purchasing on Cityline and UrbTix. It uses a configurable `settings.json` file to manage user credentials, event URLs, and ticket preferences.

> **⚠️ Warning**: Automated ticketing may violate platform terms of service. Use responsibly and ensure compliance with local laws.

## Features
- **Platform Selection**: Choose between Cityline or UrbTix via CLI.
- **Login Automation**: Automates login for both platforms.
- **Captcha Handling**: Detects captchas and prompts for manual input.
- **Configurable Settings**: Customize credentials, event URLs, and ticket preferences.

## Prerequisites
- Python 3.8+
- Google Chrome browser
- ChromeDriver (managed automatically by Selenium)
- Required Python packages:
  ```bash
  pip install selenium undetected-chromedriver python-decouple

Usage





Run the Script:
  python main.py

Select Platform: Enter 1 for Cityline or 2 for UrbTix.



Complete Captchas: Follow prompts to manually resolve captchas.



Note: The bot currently automates login only; ticket selection and checkout require manual steps or further development.

Project Structure





main.py: Entry point to select and run the bot.



cityline_bot.py: Cityline-specific automation logic.



urbtix_bot.py: UrbTix automation using undetected_chromedriver.



settings.json: Configuration file for user settings.

Known Issues





Puzzle Slider Captchas: Manual completion required; automation not yet implemented.



XPath-Based Login: Unreliable element location for automated login.



Partial Automation: Ticket selection and checkout are not fully automated.



Bot Detection: Cityline may flag standard ChromeDriver usage.

Future Improvements





Automate puzzle slider captchas (e.g., integrate 2Captcha).



Enhance login reliability with better element detection.



Complete ticket selection and checkout automation.



Add robust error handling and logging.

Legal Notice

Automated ticket purchasing may breach Cityline or UrbTix terms of service, risking account suspension or legal action. Use this tool solely for personal purposes and comply with applicable laws.

License

Licensed under the MIT License.

