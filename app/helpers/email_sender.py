from smtplib import SMTPException
from app import Message, mail
from app import current_app, render_template

async def send(args, **kwargs):
    print("SENDING EMAIL>>>>>>>>>>>>>>>>>>>>>>>>")
    try:
        message = Message(
            sender = current_app.config.get('MAIL_USERNAME'),
            subject = args.get("subject"),
            recipients = [str(args.get("recipient"))],
            html = render_template(str(args.get("template")), **kwargs))

        await mail.send_message(message)
    except SMTPException as err:
        print(str(err))
        return str(err)
