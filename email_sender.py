import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path
from typing import List
from dotenv import load_dotenv

class EmailSender:
    """Sends beat files via email."""

    def __init__(self):
        """Initialize the EmailSender with SMTP configuration from environment."""
        load_dotenv()

        self.smtp_server = os.getenv('SMTP_SERVER')
        self.smtp_port = int(os.getenv('SMTP_PORT', 587))
        self.username = os.getenv('SMTP_USERNAME')
        self.password = os.getenv('SMTP_PASSWORD')
        self.sender_email = os.getenv('SENDER_EMAIL')
        self.sender_name = os.getenv('SENDER_NAME', 'Beat Producer')

        # Validate configuration
        if not all([self.smtp_server, self.username, self.password, self.sender_email]):
            raise ValueError(
                "Missing email configuration. Please set SMTP_SERVER, SMTP_USERNAME, "
                "SMTP_PASSWORD, and SENDER_EMAIL in your .env file"
            )

    def send_beat(self, beat_file: Path, recipient_email: str, subject: str, body: str) -> bool:
        """
        Send a beat file to a recipient via email.

        Args:
            beat_file: Path to the beat file
            recipient_email: Recipient's email address
            subject: Email subject
            body: Email body text

        Returns:
            True if sent successfully, False otherwise
        """
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = f"{self.sender_name} <{self.sender_email}>"
            msg['To'] = recipient_email
            msg['Subject'] = subject

            # Add body
            msg.attach(MIMEText(body, 'plain'))

            # Attach beat file
            with open(beat_file, 'rb') as f:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(f.read())
                encoders.encode_base64(part)
                part.add_header(
                    'Content-Disposition',
                    f'attachment; filename= {beat_file.name}'
                )
                msg.attach(part)

            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.username, self.password)
                server.send_message(msg)

            print(f"✓ Sent '{beat_file.name}' to {recipient_email}")
            return True

        except Exception as e:
            print(f"✗ Failed to send '{beat_file.name}' to {recipient_email}: {str(e)}")
            return False

    def send_beats_to_recipients(self, beat_file: Path, recipients: List[str],
                                  subject: str, body: str) -> dict:
        """
        Send a beat file to multiple recipients.

        Args:
            beat_file: Path to the beat file
            recipients: List of recipient email addresses
            subject: Email subject
            body: Email body text

        Returns:
            Dictionary with success/failure counts
        """
        results = {'success': 0, 'failed': 0}

        for recipient in recipients:
            if self.send_beat(beat_file, recipient, subject, body):
                results['success'] += 1
            else:
                results['failed'] += 1

        return results
