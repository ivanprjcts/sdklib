import poplib
import imaplib
import smtplib
import exceptions
import email
import datetime

from email import parser


def add_email_domain_if_it_is_not_added(email_adress, domain):
    if '@' not in email_adress:
        return "%s@%s" % email_adress, domain
    else:
        return email_adress


def from_email_message_to_json(msg):
    json_obj_to_return = dict()
    msg = email.message_from_string(msg)
    decode = email.Header.decode_header(msg['Subject'])[0]
    encoding = decode[1] or "utf-8"
    json_obj_to_return['subject'] = unicode(decode[0], encoding=encoding)
    json_obj_to_return['date'] = msg['Date']
    json_obj_to_return['from'] = msg['From']
    json_obj_to_return['to'] = msg['To']
    # Now convert to local date-time
    date_tuple = email.utils.parsedate_tz(json_obj_to_return['date'])
    if date_tuple:
        local_date = datetime.datetime.fromtimestamp(
            email.utils.mktime_tz(date_tuple))
        json_obj_to_return['localDate'] = local_date.strftime("%a, %d %b %Y %H:%M:%S")

    if msg.is_multipart():
        for part in msg.walk():
            ctype = part.get_content_type()
            cdispo = str(part.get('Content-Disposition'))

            # skip any text/plain (txt) attachments
            if ctype == 'text/plain' and 'attachment' not in cdispo:
                json_obj_to_return['payload'] = part.get_payload(decode=True)  # decode
                break
                # not multipart - i.e. plain text, no attachments, keeping fingers crossed
    else:
        json_obj_to_return['payload'] = msg.get_payload()

    return json_obj_to_return


class POPMailSdk(object):

    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password

    def read_all_mails(self):
        pop_conn = poplib.POP3_SSL(self.host)
        pop_conn.user(self.user)
        pop_conn.pass_(self.password)
        # Get messages from server:
        messages = [pop_conn.retr(i) for i in range(1, len(pop_conn.list()[1]) + 1)]
        # Concat message pieces:
        messages = ["\n".join(mssg[1]) for mssg in messages]
        # Parse message intom an email object:
        messages = [parser.Parser().parsestr(mssg) for mssg in messages]
        pop_conn.quit()
        return messages

    def read_last_mail(self):
        mails = self.read_all_mails()
        if mails:
            return mails[-1]
        return None


class GmailPOPlSdk(POPMailSdk):

    def __init__(self, user, password):
        super(GmailPOPlSdk, self).__init__('pop.gmail.com', user, password)


class OutlookPOPlSdk(POPMailSdk):

    def __init__(self, user, password):
        super(OutlookPOPlSdk, self).__init__('pop-mail.outlook.com', user, password)


class OutlookOffice365POPlSdk(POPMailSdk):

    def __init__(self, user, password):
        super(OutlookOffice365POPlSdk, self).__init__('outlook.office365.com', user, password)


class IMAPMailSdk(object):

    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password

    @staticmethod
    def process_mailbox(M):
        """
        Do something with emails messages in the folder.
        For the sake of this example, print some headers.
        """
        messages = []

        rv, data = M.search(None, "ALL")
        if rv != 'OK':
            print "No messages found!"
            return

        for num in data[0].split():
            rv, data = M.fetch(num, '(RFC822)')
            if rv != 'OK':
                print "ERROR getting message", num
                return

            msg = from_email_message_to_json(data[0][1])
            messages.append(msg)
        return messages

    def read_all_mails(self):
        mail = imaplib.IMAP4_SSL(self.host)
        try:
            mail.login(self.user, self.password)
        except imaplib.IMAP4.error:
            raise exceptions.BaseException("Login failed")

        mail.select("inbox")  # connect to inbox.
        data = self.process_mailbox(mail)
        return data


class GmailIMAPlSdk(IMAPMailSdk):

    def __init__(self, user, password):
        super(GmailIMAPlSdk, self).__init__('imap.gmail.com', user, password)


class OutlookIMAPlSdk(IMAPMailSdk):

    def __init__(self, user, password):
        super(OutlookIMAPlSdk, self).__init__('imap-mail.outlook.com', user, password)


class OutlookOffice365IMAPlSdk(IMAPMailSdk):

    def __init__(self, user, password):
        super(OutlookOffice365IMAPlSdk, self).__init__('outlook.office365.com', user, password)


class SMTPMailSdk(object):

    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password

    def send_email(self, to_address, subject, message, from_address="no@address.com"):
        # Prepare actual message
        msg = """\From: %s\nTo: %s\nSubject: %s\n\n%s
        """ % (from_address, ", ".join(to_address), subject, message)

        server = smtplib.SMTP(self.host)
        server.ehlo()
        server.starttls()
        server.login(self.user, self.password)
        server.sendmail(from_address, to_address, msg)
        server.quit()


class GmailSMTPlSdk(SMTPMailSdk):

    def __init__(self, user, password):
        super(GmailSMTPlSdk, self).__init__('smtp.gmail.com:587', user, password)

