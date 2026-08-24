"""Send an HTML email with optional attachments via Gmail SMTP.

Usage:
    python tools/send_email.py --html <path> --subject <str> --to <email> \\
        [--attach <path> [--attach <path> ...]]

Auth: Gmail SMTP with an app password. Reads GMAIL_ADDRESS and
GMAIL_APP_PASSWORD from .env (never hardcoded, never logged). Requires
2-Step Verification enabled on the Gmail account and an app password
generated at Google Account -> Security -> App passwords.

On failure: logs the full exception, retries exactly once after a short
pause, then exits non-zero. No silent or repeated retries — a failed send
must make the run visibly fail (this matters most for the unattended
GitHub Actions cron).
"""

import argparse
import mimetypes
import os
import smtplib
import sys
import time
import traceback
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465
RETRY_DELAY_SECONDS = 5


def build_message(html_path: Path, subject: str, sender: str, to: str, attachments: list[Path]) -> MIMEMultipart:
    message = MIMEMultipart("mixed")
    message["From"] = sender
    message["To"] = to
    message["Subject"] = subject

    html_content = html_path.read_text(encoding="utf-8")
    message.attach(MIMEText(html_content, "html"))

    for attach_path in attachments:
        ctype, encoding = mimetypes.guess_type(str(attach_path))
        if ctype is None or encoding is not None:
            ctype = "application/octet-stream"
        _, sub_type = ctype.split("/", 1)
        part = MIMEApplication(attach_path.read_bytes(), _subtype=sub_type)
        part.add_header("Content-Disposition", "attachment", filename=attach_path.name)
        message.attach(part)

    return message


def send(html_path: Path, subject: str, to: str, attachments: list[Path]) -> None:
    sender = os.environ.get("GMAIL_ADDRESS")
    app_password = os.environ.get("GMAIL_APP_PASSWORD")
    if not sender or not app_password:
        print(
            "Error: GMAIL_ADDRESS and GMAIL_APP_PASSWORD must both be set in .env.",
            file=sys.stderr,
        )
        sys.exit(1)

    message = build_message(html_path, subject, sender, to, attachments)

    last_error = None
    for attempt in (1, 2):
        try:
            with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
                server.login(sender, app_password)
                server.sendmail(sender, [to], message.as_string())
            print(f"Sent '{subject}' to {to} with {len(attachments)} attachment(s).")
            return
        except smtplib.SMTPException as e:
            last_error = e
            print(f"Attempt {attempt} failed: {e}", file=sys.stderr)
            traceback.print_exc()
            if attempt == 1:
                time.sleep(RETRY_DELAY_SECONDS)

    print(f"Error: failed to send email after 2 attempts: {last_error}", file=sys.stderr)
    sys.exit(1)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--html", required=True, type=Path, help="Path to the HTML body file.")
    parser.add_argument("--subject", required=True, help="Email subject line.")
    parser.add_argument("--to", required=True, help="Recipient email address.")
    parser.add_argument("--attach", action="append", default=[], type=Path, help="Path to attach (repeatable).")
    args = parser.parse_args()

    if not args.html.exists():
        print(f"Error: HTML file not found: {args.html}", file=sys.stderr)
        sys.exit(1)

    for attach_path in args.attach:
        if not attach_path.exists():
            print(f"Error: attachment not found: {attach_path}", file=sys.stderr)
            sys.exit(1)

    send(args.html, args.subject, args.to, args.attach)


if __name__ == "__main__":
    main()
