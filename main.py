import requests
from bs4 import BeautifulSoup
import csv
import os
import sys
import logging
from time import sleep
from datetime import datetime, timezone

# Configuration
VERSION = "1.1"
TIMEOUT = 50  # API request timeout
SLEEP_TIME = 0.7  # Delay to avoid spam
MAX_RETRIES = 3  # Retry attempts for API failures

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
print(f"GotMajorIssues version {VERSION}")

UserAgent = input("Please enter your main nation's name: ").strip()
if not UserAgent:
    logging.error("UserAgent cannot be empty.")
    sys.exit(1)
UAText = f"{UserAgent} GotMajorIssues v{VERSION} developed by Vulxo, based on code by 9003"

def get_fetch_choice():
    """Prompt user for input and validate it."""
    choices = {"1": "issues", "2": "packs", "3": "issues+packs"}
    while True:
        choice = input("Do you want to fetch (1) issues, (2) packs, or (3) both? (1/2/3): ").strip()
        if choice in choices:
            return choices[choice]
        logging.warning("Invalid choice, please enter 1, 2, or 3.")

fetch_query = get_fetch_choice()

filename = "puppet.csv"
issue_file = "link_list.txt"
pack_file = "pack_list.txt"
login_file = "login_list.txt"

if not os.path.exists(filename):
    logging.error(f"Error: '{filename}' not found. Please make sure the file exists.")
    sys.exit(1)

nations, passwords = [], []
try:
    with open(filename, newline='', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            if len(row) >= 2:
                nation, password = row[0].strip().replace(" ", "_"), row[1].strip()
                if nation and password:  # Ensure valid data
                    if nation not in nations:  # Avoid duplicates
                        nations.append(nation)
                        passwords.append(password)
                    else:
                        logging.warning(f"Duplicate entry found for nation '{nation}', skipping.")
                else:
                    logging.warning(f"Skipping malformed row: {row}")
            else:
                logging.warning(f"Skipping malformed row: {row}")
except Exception as e:
    logging.error(f"Error reading CSV file: {e}")
    sys.exit(1)

for file in (issue_file, pack_file, login_file):
    if os.path.exists(file):
        logging.info(f"Removing old file: {file}")
        os.remove(file)

def fetch_nation_data(nation, password):
    """Fetch issues and/or packs data from NationStates API with retries"""
    headers = {
        "User-Agent": UAText,
        "X-Password": password.replace(" ", "_"),
    }
    params = {"nation": nation, "q": fetch_query}

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = requests.get("https://www.nationstates.net/cgi-bin/api.cgi", headers=headers, params=params, timeout=TIMEOUT)
            response.raise_for_status()
            return BeautifulSoup(response.content, "xml")
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching data for {nation} (attempt {attempt}/{MAX_RETRIES}): {e}")
            if attempt == MAX_RETRIES:
                return None
        sleep(2)

def generate_login_url(nation, password):
    """Generate login URL for a given nation."""
    timestamp = int(datetime.now(timezone.utc).timestamp() * 1000)
    password_clean = password.replace(" ", "_")
    return (
        f"https://www.nationstates.net/?nation={nation}&password={password_clean}"
        f"&logging_in=1&script=GotIssues_by_{UserAgent}_usedBy_{UserAgent}&userclick={timestamp}"
    )

def write_to_file(filename, data):
    """Append data to a file safely."""
    with open(filename, "a+", encoding="utf-8") as file:
        file.write(data + "\n")

# Process each nation
if not nations:
    logging.error("No valid nations found in the CSV file.")
    sys.exit(1)

for index, nation in enumerate(nations):
    logging.info(f"Fetching {fetch_query} for {nation}...")

    # Fetch data
    soup = fetch_nation_data(nation, passwords[index])
    if not soup:
        continue

    has_issues = bool(soup.find_all("ISSUE")) if "issues" in fetch_query else False
    has_packs = bool(soup.find("PACKS") and soup.find("PACKS").text.isdigit() and int(soup.find("PACKS").text) > 0) if "packs" in fetch_query else False

    if has_issues or has_packs:
        write_to_file(login_file, generate_login_url(nation, passwords[index]))

    if "packs" in fetch_query:
        pack_count = soup.find("PACKS")
        if pack_count and pack_count.text.isdigit():
            for _ in range(int(pack_count.text)):
                write_to_file(pack_file, f"https://www.nationstates.net/nation={nation}/page=deck/?open_loot_box=1?generated_by=GotMajorIssues_developed_by_Vulxo_usedBy_{UserAgent}")
        else:
            logging.info(f"No packs found for {nation}.")

    if "issues" in fetch_query:
        issues = soup.find_all("ISSUE")
        if issues:
            for issue in issues:
                write_to_file(issue_file, f"https://www.nationstates.net/nation={nation}/page=show_dilemma/dilemma={issue.get('id')}?generated_by=GotMajorIssues_developed_by_Vulxo_usedBy_{UserAgent}")
        else:
            logging.info(f"No issues found for {nation}.")

    sleep(SLEEP_TIME) # Delay to prevent API spam

logging.info("Done! Please run generate.py to generate the HTML.")
