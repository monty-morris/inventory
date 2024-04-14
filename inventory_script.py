import os
import subprocess

PAT = "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"
REPO_URL = "git@github.com:monty-morris/inventory.git"

def get_next_tracking_number():
    # Check if a file exists to store the last used tracking number
    if not os.path.exists("tracking_number.txt"):
        with open("tracking_number.txt", "w") as file:
            file.write("0000")

    # Read the last used tracking number from the file
    with open("tracking_number.txt", "r") as file:
        last_tracking_number = int(file.read())

    # Increment the last used tracking number
    next_tracking_number = last_tracking_number + 1

    # Limit the tracking number to be between 0001 and 9999
    next_tracking_number = max(1, min(next_tracking_number, 9999))

    # Write the next tracking number back to the file
    with open("tracking_number.txt", "w") as file:
        file.write(str(next_tracking_number).zfill(4))

    return str(next_tracking_number).zfill(4)

def reset_tracking_number():
    with open("tracking_number.txt", "w") as file:
        file.write("0000")
    print("Tracking number reset to 0000")

def create_html_file(item_name, tracking_number):
    html_content = f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Item {tracking_number}</title>
      <style>
        body {{
          font-family: Arial, sans-serif;
          margin: 0;
          padding: 0;
          background-color: #f4f4f4;
        }}
        .container {{
          max-width: 800px;
          margin: 20px auto;
          padding: 20px;
          background-color: #fff;
          border-radius: 5px;
          box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }}
        h1, h2, p {{
          margin-bottom: 20px;
        }}
        .location {{
          margin-top: 20px;
        }}
      </style>
    </head>
    <body>
      <div class="container">
        <h1>This item belongs to Monty Morris</h1>
        <p>Item name: {item_name}</p>
        <p>Tracking number: {tracking_number}</p>
        <p>Email: <a href="mailto:montymorris1@icloud.com">montymorris1@icloud.com</a></p>
        <p>Phone: 07587434466</p>
        <p class="location" id="locationText">Your location will appear here</p>
      </div>
    
      <script>
        // JavaScript code for geolocation and sending data to Google Sheets
      </script>
    </body>
    </html>
    '''

    filename = f'{tracking_number}.html'
    with open(filename, 'w') as file:
        file.write(html_content)

    return filename

def commit_and_push_changes():
    # Git add
    subprocess.run(["git", "add", "."])

    # Git commit
    subprocess.run(["git", "commit", "-m", "Added new item"])

    # Git push
    subprocess.run(["git", "push", "origin", "main"])

def main():
    item_name = input("Enter the item name: ")

    if item_name.lower() == "counter_reset":
        reset_tracking_number()
        return

    # Get the next tracking number
    tracking_number = get_next_tracking_number()

    # Create HTML file
    html_filename = create_html_file(item_name, tracking_number)
    print(f"HTML file '{html_filename}' created successfully.")

    # Commit changes to Git repository and push changes to origin
    commit_and_push_changes()

if __name__ == "__main__":
    main()
