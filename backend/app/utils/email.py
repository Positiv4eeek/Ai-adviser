from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from app.db import settings

conf = ConnectionConfig(
    MAIL_USERNAME   = settings.smtp_user,     
    MAIL_PASSWORD   = settings.smtp_password,
    MAIL_FROM       = settings.smtp_user,
    MAIL_PORT       = settings.smtp_port,
    MAIL_SERVER     = settings.smtp_host,
    MAIL_STARTTLS   = False,
    MAIL_SSL_TLS    = True,
    USE_CREDENTIALS = True,
)
fm = FastMail(conf)
