Cityline/UrbTix Ticket Bot

Overview

A Python-based Selenium bot to automate ticket purchasing on Cityline and UrbTix. Configurable via settings.json for credentials, event URLs, and ticket preferences. Note: Automated ticketing may violate platform terms; use responsibly.

Features





CLI to choose Cityline or UrbTix.



Automates login and captcha detection (manual completion).



Supports ticket type and quantity selection (partially implemented).

Prerequisites





Python 3.8+



Google Chrome



ChromeDriver (auto-managed by Selenium)



Install dependencies:

pip install selenium undetected-chromedriver python-decouple

Usage





Run:

python main.py



Enter 1 (Cityline) or 2 (UrbTix).



Complete captchas manually when prompted.



Extend scripts for full ticket selection and checkout.

Structure





main.py: Platform selector.



cityline_bot.py: Cityline automation.



urbtix_bot.py: UrbTix automation with undetected_chromedriver.



settings.json: Configuration file.

Limitations





Partial automation (login only; ticket selection needs implementation).



Manual captcha handling; puzzle slider captchas remain unresolved.



Unable to reliably locate login elements via XPath for auto-login.



Web selectors may break with site updates.



Cityline may detect standard Chrome driver.

Legal Note

Automated ticketing may violate platform policies and lead to bans. Use for personal purposes and comply with local laws.

Improvements





Implement full ticket selection and checkout logic.



Resolve puzzle slider captcha automation.



Improve XPath-based login reliability.



Enhance error handling and logging.

License

MIT License. See LICENSE for details.