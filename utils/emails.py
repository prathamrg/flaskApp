import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(message, patient_health):

    # set up the SMTP server
    s = smtplib.SMTP(host='smtp.gmail.com', port=587) #port number 587 for tls using gmail smtp server
    s.starttls()

    USERNAME = 'virtualnurse.helpdesk@gmail.com'
    PASSWORD = 'virtualnurse_2019'
    s.login(USERNAME, PASSWORD)

    msg = MIMEMultipart()
    msg['From']=USERNAME
    msg['To']='prathamgoel95@gmail.com'
    msg['Subject']="Condition {0} for Patient ID : {1}, Patient Name : {2}".format(patient_health, message.get("patient_id"), message.get("patient_name"))

    message = "Hello Dr. James, the patient's history is as below: \n" + str(message)
    # add in the message body
    msg.attach(MIMEText(message, 'plain'))

    # send the message via the server set up earlier.
    s.send_message(msg)

    del msg