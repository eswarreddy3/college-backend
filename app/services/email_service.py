from flask import current_app
from flask_mail import Message
from app.extensions import mail


def send_activation_email(admin_email: str, admin_name: str, college_name: str, activation_token: str):
    frontend_url = current_app.config['FRONTEND_URL']
    activation_link = f"{frontend_url}/activate?token={activation_token}"

    msg = Message(
        subject=f"Activate your Fynity account — {college_name}",
        recipients=[admin_email],
    )
    msg.html = f"""
    <div style="font-family: sans-serif; max-width: 600px; margin: 0 auto;">
      <h2 style="color: #00D4C8;">Welcome to Fynity, {admin_name}!</h2>
      <p>Your college <strong>{college_name}</strong> has been registered on Fynity.</p>
      <p>Click the button below to activate your admin account and set your password:</p>
      <a href="{activation_link}"
         style="display:inline-block;padding:12px 24px;background:#00D4C8;color:#000;
                text-decoration:none;border-radius:6px;font-weight:bold;">
        Activate Account
      </a>
      <p style="color:#666;margin-top:24px;font-size:13px;">
        This link expires in 7 days. If you didn't request this, ignore this email.
      </p>
    </div>
    """
    try:
        mail.send(msg)
    except Exception as e:
        current_app.logger.error(f"Failed to send activation email to {admin_email}: {e}")


def send_reminder_email(student_email: str, student_name: str):
    frontend_url = current_app.config['FRONTEND_URL']
    msg = Message(
        subject="Don't lose your streak — Fynity",
        recipients=[student_email],
    )
    msg.html = f"""
    <div style="font-family: sans-serif; max-width: 600px; margin: 0 auto;">
      <h2 style="color: #00D4C8;">Hey {student_name}, we miss you!</h2>
      <p>You haven't logged in for a few days. Jump back in to keep your streak alive and stay ahead of your peers.</p>
      <a href="{frontend_url}/dashboard"
         style="display:inline-block;padding:12px 24px;background:#00D4C8;color:#000;
                text-decoration:none;border-radius:6px;font-weight:bold;">
        Resume Learning
      </a>
    </div>
    """
    try:
        mail.send(msg)
    except Exception as e:
        current_app.logger.error(f"Failed to send reminder email to {student_email}: {e}")


def send_student_welcome_email(student_email: str, student_name: str, temp_password: str):
    frontend_url = current_app.config['FRONTEND_URL']

    msg = Message(
        subject="Your Fynity account is ready",
        recipients=[student_email],
    )
    msg.html = f"""
    <div style="font-family: sans-serif; max-width: 600px; margin: 0 auto;">
      <h2 style="color: #00D4C8;">Hello {student_name}!</h2>
      <p>Your Fynity placement preparation account has been created.</p>
      <p><strong>Login credentials:</strong></p>
      <ul>
        <li>Email: {student_email}</li>
        <li>Temporary password: <code style="background:#f4f4f4;padding:2px 6px;">{temp_password}</code></li>
      </ul>
      <p>You will be prompted to set a new password on first login.</p>
      <a href="{frontend_url}/login"
         style="display:inline-block;padding:12px 24px;background:#00D4C8;color:#000;
                text-decoration:none;border-radius:6px;font-weight:bold;">
        Login to Fynity
      </a>
    </div>
    """
    try:
        mail.send(msg)
    except Exception as e:
        current_app.logger.error(f"Failed to send welcome email to {student_email}: {e}")
