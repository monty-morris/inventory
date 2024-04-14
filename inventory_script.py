import os
import re
import gspread
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
from git import Repo
from datetime import datetime
import time

def get_next_tracking_number():
    if not os.path.exists("tracking_number.txt"):
        with open("tracking_number.txt", "w") as file:
            file.write("0000")
    with open("tracking_number.txt", "r+") as file:
        current_number = file.read()
        next_number = str(int(current_number) + 1).zfill(4)
        file.seek(0)
        file.write(next_number)
        file.truncate()
    return next_number

def create_html_file(tracking_number, item_name):
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Item Details</title>
    </head>
    <body>
        <h1>Item Details</h1>
        <p>This item belongs to Monty Morris.</p>
        <p>Details:</p>
        <ul>
            <li>Item Name: {item_name}</li>
            <li>Tracking Number: {tracking_number}</li>
            <li>Phone: 07587434466</li>
            <li>Email: monty.morris@example.com</li>
        </ul>
    </body>
    </html>
    """
    filename = f"{tracking_number}.html"
    with open(filename, "w") as file:
        file.write(html_content)

def update_google_sheets(item_name, tracking_number):
    scope = ["https://www.googleapis.com/auth/spreadsheets"]
    credentials = Credentials.from_service_account_file("/Users/monty/Documents/Inventory/credentials.json", scopes=scope)
    gc = gspread.authorize(credentials)
    spreadsheet_id = "1M0XRvO3zvHtmNkB6NUFkW10bs2EWSUbuFmRrhZDotJY"
    sheet = gc.open_by_key(spreadsheet_id).sheet1
    while True:
        try:
            row = sheet.find(tracking_number).row
            sheet.update_cell(row, 1, item_name)
            break
        except gspread.exceptions.APIError as e:
            if e.response.status_code == 429:
                print("Quota exceeded. Retrying in 60 seconds...")
                time.sleep(60)
            else:
                raise e

def commit_and_push_to_github(tracking_number):
    repo = Repo("/Users/monty/Documents/Inventory/")
    repo.git.add("*.html")
    repo.index.commit(f"Added HTML file for item {tracking_number}")
    origin = repo.remote(name="origin")
    origin.push()

def delete_google_sheet_entries():
    scope = ["https://www.googleapis.com/auth/spreadsheets"]
    credentials = Credentials.from_service_account_file("/Users/monty/Documents/Inventory/credentials.json", scopes=scope)
    gc = gspread.authorize(credentials)
    spreadsheet_id = "1M0XRvO3zvHtmNkB6NUFkW10bs2EWSUbuFmRrhZDotJY"
    sheet = gc.open_by_key(spreadsheet_id).sheet1
    while True:
        try:
            cell_list = sheet.findall(re.compile(r'\b\d{4}\b'))
            for cell in cell_list:
                sheet.update_cell(cell.row, 1, '')
            break
        except gspread.exceptions.APIError as e:
            if e.response.status_code == 429:
                print("Quota exceeded. Retrying in 60 seconds...")
                time.sleep(60)
            else:
                raise e

def main():
    while True:
        action = input("Enter action (enter item name, batch_import, or counter_reset): ").strip().lower()
        if action == "counter_reset":
            confirmation = input("Are you sure you want to reset the counter? (confirm with 'y' or 'yes'): ").strip().lower()
            if confirmation in ["y", "yes"]:
                with open("tracking_number.txt", "w") as file:
                    file.write("0000")
                print("Tracking number reset to 0000.")
            else:
                print("Reset canceled.")
        elif action == "batch_import":
            batch_import()
        else:
            tracking_number = get_next_tracking_number()
            if action == "complete_reset":
                confirmation = input("Are you sure you want to perform a complete reset? (confirm with 'y' or 'yes'): ").strip().lower()
                if confirmation in ["y", "yes"]:
                    for file in os.listdir():
                        if file.endswith(".html"):
                            os.remove(file)
                    print("HTML files deleted.")
                    delete_google_sheet_entries()
                    print("Google Sheet entries deleted.")
                    commit_and_push_to_github(tracking_number)
                    print("Changes committed and pushed to GitHub.")
                else:
                    print("Reset canceled.")
            else:
                item_name = action
                create_html_file(tracking_number, item_name)
                update_google_sheets(item_name, tracking_number)
                commit_and_push_to_github(tracking_number)
                print(f"Item '{item_name}' added with tracking number '{tracking_number}'.")

if __name__ == "__main__":
    main()
