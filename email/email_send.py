import smtplib, email
#from and import key word make it possible that use a variable stand for a specified module name
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
#from key word copy a module variable name to a specified domain
from email.utils import parseaddr, formataddr
import sys
import argparse
import os
import time

parser = argparse.ArgumentParser(description="邮件发送")
parser.add_argument("from_addr", help="发件人地址")
parser.add_argument("from_name", help="发件人姓名")
parser.add_argument("password", help="发件人密码")
parser.add_argument("to_addr", help="收件人地址")
parser.add_argument("to_name", help="收件人姓名")
parser.add_argument("heading", help="主题")
parser.add_argument("-c", "--content", action="store",help="正文")
parser.add_argument("-f", "--file", action="append",help="附件")
parser.add_argument("-i", "--images", action="append",help="图片")

args = parser.parse_args()

def _format_addr(s):
    (name, addr) = parseaddr(s)
    return formataddr(( \
        Header(name, 'utf-8').encode(), \
        addr))


from_addr = args.from_addr
from_name = args.from_name
password = args.password
to_addr = args.to_addr
to_name = args.to_name

smtp_server = 'smtp.163.com'

heading = args.heading

main_body_text = 'hello my friend'

main_body_html = '<html><body><h1>'+args.content+'</h1>'
if args.images:
    for i in range(0,len(args.images)):
        main_body_html = main_body_html + '<p><img src="cid:'+str(i)+'"></p>'

main_body_html = main_body_html+'</body></html>'

from_attr = from_name + ' < ' + from_addr + ' > '
to_attr = to_name + ' < ' + to_addr + ' > '

msg = MIMEMultipart('alternative')
msg.attach(MIMEText(main_body_html, 'html', 'utf-8'))
msg['From'] = _format_addr(from_attr)
msg['To'] = _format_addr(to_attr)
msg['Subject'] = Header(heading, 'utf-8').encode()

if args.images:
    for i in range(0,len(args.images)):
        with open(args.images[i], 'rb') as f:
                mime = MIMEBase('image', 'jpg', filename = str(i)+'.jpg')
                mime.add_header('Context-Disposition', 'attachment', filename = str(i)+'.jpg')
                mime.add_header('Content-ID', '<'+str(i)+'>')
                mime.add_header('X-Attachment-ID', str(i))
                mime.set_payload(f.read())
                encoders.encode_base64(mime)
                msg.attach(mime)

if args.file:
    for i in range(0,len(args.file)):
        filename = os.path.split(args.file[i])[1]
        att = MIMEText(open(args.file[i], 'rb').read(), 'base64', 'utf-8')
        att["Content-Type"] = 'application/octet-stream'
        att["Content-Disposition"] = 'attachment; filename="'+filename+'"'
        msg.attach(att)

msg.attach(MIMEText(main_body_text, 'plain', 'utf-8'))
server = smtplib.SMTP(smtp_server, 25)
server.starttls()
server.connect(smtp_server, 25)
server.helo()
server.ehlo()
server.login(from_addr, password)
server.sendmail(from_addr, [to_addr], msg.as_string())

server.quit()
