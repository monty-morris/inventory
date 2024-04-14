import os
import subprocess
import re  # Added import statement for regular expressions
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials

def get_next_tracking_number():
    if not os.path.exists("tracking_number.txt"):
        with open("tracking_number.txt", "w") as file:
            file.write("0000")
            return "0000"
    else:
        with open("tracking_number.txt", "r+") as file:
            current_number = file.read()
            if current_number.strip() == "":
                current_number = "0000"
            next_number = str(int(current_number) + 1).zfill(4)
            file.seek(0)
            file.write(next_number)
            return next_number

def create_html_page(tracking_number, item_name):
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Item {tracking_number}</title>
</head>
<body>
    <h1>Item {tracking_number}</h1>
    <p>This item belongs to Monty Morris. Details are below:</p>
    <ul>
        <li>Item Name: {item_name}</li>
        <li>Email: montymorris1@icloud.com</li>
        <li>Phone: 07587434466</li>
    </ul>
</body>
</html>"""
    with open(f"{tracking_number}.html", "w") as file:
        file.write(html_content)

def update_google_sheets(item_name, tracking_number):
    scope = ['https://www.googleapis.com/auth/spreadsheets']
    credentials = Credentials.from_service_account_file("/Users/monty/Documents/Inventory/credentials.json", scopes=scope)
    client = gspread.authorize(credentials)
    spreadsheet_id = "1M0XRvO3zvHtmNkB6NUFkW10bs2EWSUbuFmRrhZDotJY"
    sheet = client.open_by_key(spreadsheet_id).sheet1
    row = sheet.find(tracking_number).row
    sheet.update_cell(row, 1, item_name)

def delete_html_files():
    for i in range(10000):
        if os.path.exists(f"{str(i).zfill(4)}.html"):
            os.remove(f"{str(i).zfill(4)}.html")

def delete_google_sheet_entries():
    scope = ['https://www.googleapis.com/auth/spreadsheets']
    credentials = Credentials.from_service_account_file("/Users/monty/Documents/Inventory/credentials.json", scopes=scope)
    client = gspread.authorize(credentials)
    spreadsheet_id = "1M0XRvO3zvHtmNkB6NUFkW10bs2EWSUbuFmRrhZDotJY"
    sheet = client.open_by_key(spreadsheet_id).sheet1
    cell_list = sheet.findall(re.compile(r'\b\d{4}\b'))
    for cell in cell_list:
        sheet.update_cell(cell.row, 1, '')

def main():
    action = input("Enter item name: ").strip()

    if action == "counter_reset":
        confirm = input("Confirm (y/n): ").strip().lower()
        if confirm in ['y', 'yes']:
            subprocess.run(["git", "pull", "origin", "main"])
            subprocess.run(["rm", "tracking_number.txt"])
            subprocess.run(["touch", "tracking_number.txt"])
            subprocess.run(["echo", "0001", ">", "tracking_number.txt"])
            subprocess.run(["git", "add", "."])
            subprocess.run(["git", "commit", "-m", "'Reset tracking number to 0001'"])
            subprocess.run(["git", "push", "origin", "main"])
            print("Tracking number reset to 0001.")
            delete_html_files()
            delete_google_sheet_entries()
            print("HTML files and Google Sheet entries deleted.")
        else:
            print("Reset cancelled.")
    elif action == "complete_reset":
        confirm = input("Confirm (y/n): ").strip().lower()
        if confirm in ['y', 'yes']:
            subprocess.run(["git", "pull", "origin", "main"])
            subprocess.run(["rm", "tracking_number.txt"])
            subprocess.run(["touch", "tracking_number.txt"])
            subprocess.run(["echo", "0001", ">", "tracking_number.txt"])
            subprocess.run(["git", "add", "."])
            subprocess.run(["git", "commit", "-m", "'Reset tracking number to 0001'"])
            subprocess.run(["git", "push", "origin", "main"])
            print("Tracking number reset to 0001.")
            delete_html_files()
            delete_google_sheet_entries()
            print("HTML files and Google Sheet entries deleted.")
        else:
            print("Reset cancelled.")
    else:
        item_name = action
        tracking_number = get_next_tracking_number()
        create_html_page(tracking_number, item_name)
        update_google_sheets(item_name, tracking_number)
        subprocess.run(["git", "pull", "origin", "main"])
        subprocess.run(["git", "add", "."])
        subprocess.run(["git", "commit", "-m", f"'Add item {tracking_number}: {item_name}'"])
        subprocess.run(["git", "push", "origin", "main"])
        print(f"Item {tracking_number} added with name: {item_name}")

if __name__ == "__main__":
    main()
