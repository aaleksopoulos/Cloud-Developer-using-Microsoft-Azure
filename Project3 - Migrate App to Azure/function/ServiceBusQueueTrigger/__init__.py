import logging
import azure.functions as func
import psycopg2
import os
from datetime import datetime
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content

def main(msg: func.ServiceBusMessage):

    notification_id = int(msg.get_body().decode('utf-8'))
    #notification_id = msg.get_body().decode('utf-8')
    logging.info('Python ServiceBus queue trigger processed message: %s',notification_id)

    #define db info
    db_name = "techconfdb"
    db_user = "project3user@project3-dbserver"
    db_host = "project3-dbserver.postgres.database.azure.com"
    db_pass = "Ab1234!!"
    # TODO: Get connection to database   
    connection = psycopg2.connect(
        host=db_host,
        database=db_name,
        user=db_user,
        password=db_pass
    )
    cursor = connection.cursor()
    logging.info('connected to db')
    try:
        # TODO: Get notification message and subject from database using the notification_id
        cmd = "SELECT message, subject FROM notification WHERE id = {};".format(notification_id)
        logging.info("cmd is {}".format(cmd))
        cursor.execute(cmd)
        logging.info("with notification id {}, getting message and subject".format(notification_id))
        
        for notification_data in cursor.fetchall():
            message = notification_data[0]
            subject = notification_data[1]
        logging.info('msg={}, subject={}'.format(message, subject) )
        
        # TODO: Get attendees email and name
        cursor.execute("SELECT first_name, last_name, email FROM attendee;")
        attendees = cursor.fetchall()
        logging.info("got {} number of attendees".format(len(attendees)))

        # TODO: Loop through each attendee and send an email with a personalized subject
        sg = SendGridAPIClient('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')
        from_email=Email("athanasios_al@hotmail.com")
        for attendee in attendees:
            to_email = To(attendee[2])
            subject = 'Hello {} {}'.format(attendee[0], attendee[1])
            content = Content("text/plain", message)
            mail = Mail(from_email, to_email, subject, content)
            sg.send(mail)

        # TODO: Update the notification table by setting the completed date and updating the status with the total number of attendees notified
        notification_completed_date = datetime.utcnow()  #utcnow was used in routes.py
        notification_status = 'Notified {} attendees'.format(len(attendees))
        
        cursor.execute("UPDATE notification SET status = '{}', completed_date = '{}' WHERE id = {};".format(notification_status, notification_completed_date, notification_id))
        connection.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(error)
    finally:
        # TODO: Close connection
        connection.close()
