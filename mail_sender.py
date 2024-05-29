import smtplib
from data import db_session
from data.emails import Emails
from email.mime.text import MIMEText
from email.header import Header


def send_email(emails, message, password, subject=None):
    sender = "cupolmarketplace@yandex.ru"
    server = smtplib.SMTP("smtp.yandex.ru", 587, timeout=10)
    server.starttls()

    try:
        server.login(sender, password)
        msg = MIMEText(message, 'plain', 'utf-8')
        if subject is not None:
            msg["Subject"] = Header(subject, 'utf-8')
        msg['From'] = sender
        msg['To'] = ', '.join(emails)
        server.sendmail(msg['From'], emails, msg.as_string())
    except Exception as ex:
        return ex
    return "Рассылка успешна отправлена"


def main():
    db_session.global_init("db/db.db")
    db_sess = db_session.create_session()
    emails = db_sess.query(Emails).all()
    emails = set([i.email for i in emails])
    password = input("Введите пароль от корпоративной почты: ")
    message = input("Введите сообщение: ")
    subject = input("Введите тему сообщения, если она есть: ")
    print(emails)
    print(send_email(emails, message, password, subject))


if __name__ == "__main__":
    main()
