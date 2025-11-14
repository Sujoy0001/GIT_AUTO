import os
import subprocess
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import google.generativeai as genai

# --------------------------
# CONFIG
# --------------------------
REPO_PATH = "/path/to/your/repo"      # <-- change
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"

EMAIL_SENDER = "YOUR_EMAIL@gmail.com"
EMAIL_PASSWORD = "YOUR_APP_PASSWORD"   # Gmail App Password
EMAIL_RECEIVER = "YOUR_EMAIL@gmail.com"

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

genai.configure(api_key=GEMINI_API_KEY)

# --------------------------
# Run Shell Command
# --------------------------
def run_cmd(command):
    result = subprocess.run(
        command,
        shell=True,
        cwd=REPO_PATH,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    return result.stdout.strip(), result.stderr.strip()

# --------------------------
# Generate Commit Message
# --------------------------
def generate_commit_message():
    model = genai.GenerativeModel("gemini-1.5-flash")

    prompt = f"""
    Generate a simple Git commit message for daily update.
    Today: {datetime.now().strftime("%Y-%m-%d")}.
    No emojis.
    """

    response = model.generate_content(prompt)
    return response.text.strip()

# --------------------------
# Send Email Notification
# --------------------------
def send_email(subject, body):
    msg = MIMEText(body)
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER
    msg["Subject"] = subject

    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(EMAIL_SENDER, EMAIL_PASSWORD)
    server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
    server.quit()

# --------------------------
# Main Auto Commit Function
# --------------------------
def auto_commit():
    # Check changes
    out, err = run_cmd("git status --porcelain")
    if out.strip() == "":
        send_email("No Commit Needed", "No changes found in repo.")
        return

    # Create commit message
    commit_msg = generate_commit_message()

    run_cmd("git add .")
    run_cmd(f'git commit -m "{commit_msg}"')
    push_out, push_err = run_cmd("git push")

    # Email result
    email_body = f"""
Daily Git Commit Completed

Commit Message:
{commit_msg}

Push Output:
{push_out}

Errors:
{push_err}
"""

    send_email("Daily Commit Successful", email_body)


if __name__ == "__main__":
    auto_commit()
