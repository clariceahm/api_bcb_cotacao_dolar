###------------------------------------------------------------------------------------------------
## Description: Sending automatic emails
###------------------------------------------------------------------------------------------------

##------------------------
## REQUIRED PACKAGES
##------------------------
import os
import ast

## For sending with SMTP
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email.mime.base import MIMEBase
from email import encoders
import smtplib,ssl
from email.mime.base import MIMEBase






##-----------------------------
## FUNCTIONS
##-----------------------------
def sending_email(df_attachment):

    ##----------------------------
    ## RECIPIENT LIST
    ##----------------------------
    # Gets the directory where the script is located
    main_dir = os.path.dirname(os.path.abspath(__file__))

    # Create relative path from script directory
    emails_list_path = os.path.join(main_dir, 'recipient_list.txt')


    # Reading email recipients
    with open(emails_list_path, "r") as file:
        recipient_list = file.read()

    recipient_list = recipient_list.split(';')
    # print(recipient_list)




    ##----------------------------
    ## EMAIL ACCOUNT
    ##----------------------------
    # Gets the directory where the script is located
    main_dir = os.path.dirname(os.path.abspath(__file__))

    # Create relative path from script directory
    email_account = os.path.join(main_dir, 'email_account.txt')


    # Reading information about the email sender
    with open(email_account, "r") as file:
        email_account = file.read()

    ## Moving to dictionary
    email_account = ast.literal_eval(email_account)


    ## Email Account
    server_name = email_account['server_name']
    port = email_account['port']
    username = email_account['username']
    password = email_account['password']

    ## df_attachment
    compra = df_attachment.loc[0,'cotacao_compra']
    data_cotacao = df_attachment.loc[0,'data_cotacao']
    data_cotacao = data_cotacao.strftime('%Y-%m-%d')


    send_from = username
    send_to = recipient_list
    subject = 'Dollar Rate'
    text = 'Hello, follow the dollar rate \nDollar Rate: {} \nDate: {}'.format(compra,data_cotacao)

    ##--------------------
    ## Email message settings
    ##-------------------
    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = "; ".join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    ## Adding text to the message body
    msg.attach(MIMEText(text))


    ## Connecting to the server and sending the email
    smtp = smtplib.SMTP(server_name, port)
    smtp.starttls()
    smtp.login(username,password)
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.quit()

    print('Email sent to: ')
    print(send_to)
