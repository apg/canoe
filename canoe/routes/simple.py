import smtplib
import rfc822

from email.mime.text import MIMEText


class EchoRoute(object):
    
    def __init__(self, prefix=None):
        self._prefix = prefix or ''
    
    def __call__(self, line, buffer):
        print "%s%s" % (self._prefix, line)


def quote_addrs(addrs):
    return map(smtplib.quoteaddr, addrs)


def sanitize_addrs(addrs):
    naddrs = []
    for addr in addrs:
        _, a = rfc822.parseaddr(addr.strip())
        if a and len(a) > 0:
            naddrs.append(a)
        else:
            print "ERROR: ", _, a

    return quote_addrs(naddrs)


class SMTPRoute(object):

    def __init__(self, **kwargs):
        self._to = map(lambda x: x.strip(), 
                       kwargs.pop('toaddr', '').split(','))
        self._from = kwargs.pop('fromaddr', 'Canoe <noreply@localhost>')
        self._subject = kwargs.pop('subject', 'Message from canoe')
        self._buffer_lines = kwargs.pop('buffer_lines')
        self._testing = kwargs.pop('testing', False)
        self._smtp_host = kwargs.pop('smtp_host')
        self._smtp_port = kwargs.pop('smtp_port')
        self._smtp_login = kwargs.pop('smtp_login')
        self._smtp_password = kwargs.pop('smtp_password')

    def __call__(self, line, buffer):
        tos = sanitize_addrs(self._to)
        bt = buffer.copyn(20)
        text = '\r\n'.join(bt) + '\r\n' + line
        msg = MIMEText(text)
        msg['Subject'] = self._subject
        msg['To'] = ', '.join(tos)
        msg['From'] = ', '.join(sanitize_addrs([self._from]))

        if self._testing:
            # TODO: send this of course
            print msg.as_string()
            print "-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\n\n\n"
        else:
            smtp = smtplib.SMTP(self._smtp_host, self._smtp_port)
            smtp.login(self._smtp_login, self._smtp_password)
            smtp.sendmail(msg['From'], tos, msg.as_string())
            smtp.quit()
            self._testing = True
