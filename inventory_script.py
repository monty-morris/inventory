import os
import re
import gspread
from git import Repo
from google.oauth2.service_account import Credentials
from github import Github

def get_next_tracking_number():
    if not os.path.exists("tracking_number.txt"):
        with open("tracking_number.txt", "w") as file:
            file.write("0000")
    with open("tracking_number.txt", "r") as file:
        current_number = file.read()
    next_number = str(int(current_number) + 1).zfill(4)
    with open("tracking_number.txt", "w") as file:
        file.write(next_number)
    return next_number

def update_google_sheets(item_name, tracking_number):
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    credentials = Credentials.from_service_account_file("/Users/monty/Documents/Inventory/credentials.json", scopes=scope)
    client = gspread.authorize(credentials)
    spreadsheet_id = "1M0XRvO3zvHtmNkB6NUFkW10bs2EWSUbuFmRrhZDotJY"
    sheet = client.open_by_key(spreadsheet_id).sheet1
    row = sheet.find(tracking_number).row
    sheet.update_cell(row, 1, item_name)

def update_github(tracking_number):
    repo_path = "/Users/monty/Documents/Inventory"
    repo = Repo(repo_path)
    repo.git.add(update=True)
    repo.index.commit(f"Item added with tracking number: {tracking_number}")
    origin = repo.remote(name='origin')
    origin.push()

def main():
    while True:
        action = input("Enter action (item name, counter_reset, batch_import, complete_reset, script_stop): ")
        if action == "item name":
            item_name = input("Enter item name: ")
            tracking_number = get_next_tracking_number()
            html_content = f"""<!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Item Info</title>
            </head>
            <body>
                <h1>Item Information</h1>
                <p>This item belongs to Monty Morris, details are below:</p>
                <p>Item Name: {item_name}</p>
                <p>Tracking Number: {tracking_number}</p>
                <p>Email: montymorris1@icloud.com</p>
                <p>Phone: 07587434466</p>
            </body>
            </html>"""
            html_file_name = f"{tracking_number}.html"
            with open(html_file_name, "w") as html_file:
                html_file.write(html_content)
            update_google_sheets(item_name.lower(), tracking_number)
            update_github(tracking_number)
        elif action == "counter_reset":
            with open("tracking_number.txt", "w") as file:
                file.write("0000")
            print("Tracking number reset to 0000.")
        elif action == "batch_import":
            items = input("Enter multiple item names separated by commas and a space: ").split(", ")
            for item_name in items:
                tracking_number = get_next_tracking_number()
                html_content = f"""<!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Item Info</title>
                </head>
                <body>
                    <h1>Item Information</h1>
                    <p>This item belongs to Monty Morris, details are below:</p>
                    <p>Item Name: {item_name}</p>
                    <p>Tracking Number: {tracking_number}</p>
                    <p>Email: montymorris1@icloud.com</p>
                    <p>Phone: 07587434466</p>
                </body>
                </html>"""
                html_file_name = f"{tracking_number}.html"
                with open(html_file_name, "w") as html_file:
                    html_file.write(html_content)
                update_google_sheets(item_name.lower(), tracking_number)
                update_github(tracking_number)
        elif action == "complete_reset":
            confirm = input("Are you sure you want to perform a complete reset? (y/n): ")
            if confirm.lower() == "y" or confirm.lower() == "yes":
                for file_name in os.listdir("."):
                    if file_name.endswith(".html"):
                        os.remove(file_name)
                with open("tracking_number.txt", "w") as file:
                    file.write("0000")
                print("Complete reset performed.")
                delete_google_sheet_entries()
        elif action == "script_stop":
            print("Script stopped.")
            break

def delete_google_sheet_entries():
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    credentials = Credentials.from_service_account_file("/Users/monty/Documents/Inventory/credentials.json", scopes=scope)
    client = gspread.authorize(credentials)
    spreadsheet_id = "1M0XRvO3zvHtmNkB6NUFkW10bs2EWSUbuFmRrhZDotJY"
    sheet = client.open_by_key(spreadsheet_id).sheet1
    cell_list = sheet.findall(re.compile(r'\b\d{4}\b'))
    for cell in cell_list:
        sheet.update_cell(cell.row, 1, '')

if __name__ == "__main__":
    main()
