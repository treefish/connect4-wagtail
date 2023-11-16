#!/usr/bin/env python
#
# Created by: David Apimerika
# Date......: 17 November 2023
#
# For testing sending e-mail messages

# Updated...: 
#

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.conf import settings
from django.core.mail import EmailMessage

class Command(BaseCommand):
    help = "Send e-mail message."

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write("Send e-mail message.")
        send_email_message()
        self.stdout.write("Done.")


def send_email_message():
    print('######## Send E-Mail Message ########')
    recipients = ["test@treefish.co.nz"]
    bcc = ["wagtail@treefish.co.nz"]
    subject = "***TEST *** Connect4Families E-Mail"
    body = """\
Subject: Kia ora

This message is sent through Django and an Admin Command (bookings -> send_email.py).

David
"""

    email = EmailMessage(subject, body, "wagtail@treefish.co.nz", recipients, bcc,
        reply_to=["admin@connect4.org.uk"],
        headers={"Message-ID": "pcs"}, )
    email.send()
