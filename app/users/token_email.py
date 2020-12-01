from flask import render_template, url_for, current_app
from flask_mail import Message

from app import mail

    
def send_email(email, url, subject, recipients, html):
    token = current_app.s.dumps(email, salt=current_app.config['SECURITY_PASSWORD_SALT'])
    confirm_url = url_for(url, token=token, _external=True)
    resetPassword_html = render_template(f'auth/email/{html}', confirm_url=confirm_url)
                
    msg = Message(subject, 
                    sender=current_app.config['MAIL_DEFAULT_SENDER'], 
                    recipients=recipients,
                    html=resetPassword_html)                
                    
    mail.send(msg)
