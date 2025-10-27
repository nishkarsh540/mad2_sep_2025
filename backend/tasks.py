import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from io import StringIO
from datetime import datetime
from celery_config import celery
from app import app
from model import db,User,Category
import csv 



@celery.task
def generate_monthly_reports():
    with app.app_context():
        current_month = datetime.now().month
        current_year = datetime.now().year
        users = User.query.all()

        for user in users:
            html_content = f"""
            <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Monthly Activity Report</title>
</head>
<body>
    <p>{user.username}</p>
    <p>{user.email,current_month,current_year}</p>
</body>
</html>"""

            from_email = 'GROCERY@gmail.com'
            subject = 'Monthly Activity Report'
            msg = MIMEMultipart('alternative')
            msg['From'] = from_email
            msg['To'] = user.email
            msg['Subject'] = subject

            part1 = MIMEText(html_content,'html')

            msg.attach(part1)

            smtp_server ='localhost'
            smpt_port = 1025

            with smtplib.SMTP(smtp_server,smpt_port) as server:
                server.sendmail(from_email,user.email,msg.as_string())


@celery.task
def export_categories_details_as_csv():
    with app.app_context():
        categories = Category.query.all()
        csv_buffer = StringIO()
        csv_writer = csv.writer(csv_buffer)
        csv_writer.writerow(['ID','Name'])
        for category in categories:
            csv_writer.writerow([
                category.id,
                category.name
            ])
        base_dir = os.path.abspath(os.path.dirname(__name__))
        csv_file_path = os.path.join(base_dir,'category_details.csv')
        with open(csv_file_path,'w',newline='') as csv_file:
            csv_file.write(csv_buffer.getvalue())
        return csv_buffer.getvalue()