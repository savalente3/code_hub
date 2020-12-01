from flask import render_template, url_for
from flask_mail import Message

from app import app, s, mail

    
def send_email(email, url, subject, recipients, html):
    token = s.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])
    confirm_url = url_for(url, token=token, _external=True)
    resetPassword_html = render_template(f'auth/email/{html}', confirm_url=confirm_url)
                
    msg = Message(subject, 
                    sender=app.config['MAIL_DEFAULT_SENDER'], 
                    recipients=recipients,
                    html=resetPassword_html)                
                    
    mail.send(msg)
