import os
import gspread
from google.oauth2 import service_account

def get_next_tracking_number():
    if not os.path.exists("tracking_number.txt"):
        with open("tracking_number.txt", "w") as f:
            f.write("0001")
        return "0001"
    else:
        with open("tracking_number.txt", "r+") as f:
            tracking_number = f.read()
            next_number = str(int(tracking_number) + 1).zfill(4)
            f.seek(0)
            f.write(next_number)
            f.truncate()
            return next_number

def create_html_page(item_name, tracking_number):
    html_content = f"""
<!DOCTYPE html>
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
        <li>Name: Monty Morris</li>
        <li>Email: montymorris1@icloud.com</li>
        <li>Phone: 07587434466</li>
        <li>Item Name: {item_name}</li>
        <li>Tracking Number: {tracking_number}</li>
    </ul>
</body>
</html>
"""
    with open(f"{tracking_number}.html", "w") as f:
        f.write(html_content)

def update_google_sheets(item_name, tracking_number):
    scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    credentials = service_account.Credentials.from_service_account_file("/Users/monty/Documents/Inventory/credentials.json", scopes=scope)
    client = gspread.authorize(credentials)

    spreadsheet_id = "1M0XRvO3zvHtmNkB6NUFkW10bs2EWSUbuFmRrhZDotJY"
    sheet = client.open_by_key(spreadsheet_id).sheet1

    cell = sheet.find(tracking_number, in_column=2)
    row = cell.row
    sheet.update_cell(row, 1, item_name)

def main():
    item_name = input("Enter item name: ")
    if item_name.lower() == "counter_reset":
        with open("tracking_number.txt", "w") as f:
            f.write("0001")
        print("Tracking number reset to 0001")
        return
    tracking_number = get_next_tracking_number()
    create_html_page(item_name, tracking_number)
    update_google_sheets(item_name, tracking_number)
    print(f"Item '{item_name}' with tracking number '{tracking_number}' has been added.")

if __name__ == "__main__":
    main()
