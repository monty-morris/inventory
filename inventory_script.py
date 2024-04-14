import os
import subprocess

# Function to get the next tracking number
def get_next_tracking_number():
    if not os.path.exists("tracking_number.txt"):
        with open("tracking_number.txt", "w") as file:
            file.write("0000")

    with open("tracking_number.txt", "r+") as file:
        tracking_number = int(file.read())
        file.seek(0)
        file.write(str(tracking_number + 1).zfill(4))
        file.truncate()
        return str(tracking_number).zfill(4)

# Function to create HTML file for the new item
def add_html_file(tracking_number, item_name):
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Item {tracking_number}</title>
    </head>
    <body>
        <h1>This item belongs to Monty Morris</h1>
        <p>Tracking Number: {tracking_number}</p>
        <p>Item Name: {item_name}</p>
        <p>Email: montymorris1@icloud.com</p>
        <p>Phone: 07587434466</p>
    </body>
    </html>
    """

    with open(f"{tracking_number}.html", "w") as file:
        file.write(html_content)

# Main function
def main():
    # Ask for the item name
    item_name = input("Enter item name: ")

    # Reset the tracking number if requested
    if item_name == "counter_reset":
        with open("tracking_number.txt", "w") as file:
            file.write("0000")
    else:
        # Increment the tracking number
        tracking_number = get_next_tracking_number()

        # Create HTML file for the new item
        add_html_file(tracking_number, item_name)

        # Push changes to Git repository
        subprocess.run(["git", "add", "."])
        subprocess.run(["git", "commit", "-m", f"Added item {tracking_number}"])
        subprocess.run(["git", "push", "origin", "main"])

if __name__ == "__main__":
    main()
