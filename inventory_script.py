import os
import subprocess

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

def add_html_file(tracking_number, label_name):
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Item {tracking_number}</title>
    </head>
    <body>
        <h1>This item belongs to Monty Morris</h1>
        <p>Tracking Number: {tracking_number}</p>
        <p>Details: {label_name}</p>
    </body>
    </html>
    """

    with open(f"{tracking_number}.html", "w") as file:
        file.write(html_content)

def main():
    label_name = input("Enter label name: ")

    if label_name == "counter_reset":
        with open("tracking_number.txt", "w") as file:
            file.write("0000")
    else:
        tracking_number = get_next_tracking_number()
        add_html_file(tracking_number, label_name)

        # Push changes to Git repository
        subprocess.run(["git", "add", "."])
        subprocess.run(["git", "commit", "-m", f"Added item {tracking_number}"])
        subprocess.run(["git", "push", "origin", "main"])

if __name__ == "__main__":
    main()
