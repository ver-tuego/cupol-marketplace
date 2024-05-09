import smtplib
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
    password = input("Введите пароль от корпоративной почты: ")
    message = input("Введите сообщение: ")
    subject = input("Введите тему сообщения, если она есть: ")
    print(send_email(["cupolmarketplace@yandex.ru"], message, password, subject))


if __name__ == "__main__":
    main()
