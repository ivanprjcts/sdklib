import poplib
from email import parser


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


class GmailPOPlSdk(POPMailSdk):

    def __init__(self, user, password):
        super(GmailPOPlSdk, self).__init__('pop.gmail.com', user, password)
