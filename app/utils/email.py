
import logging

logger = logging.getLogger(__name__)


def send_reset_password_email(email_to: str, token: str):
    # TODO: edit link:

    project_name = "دیتاست"
    subject = f"{project_name} - Password Reset"
    link = f"http://localhost:3000/reset-password?token={token}"
    message = f"""
    سلام،
    
    برای بازنشانی رمز عبور خود، لطفاً روی لینک زیر کلیک کنید:
    {link}
    
    این لینک تا 15 دقیقه معتبر است.
    
    با تشکر،
    تیم {project_name}
    """
    # TODO: send email:

    logger.info(f"Password reset email sent to {email_to}:\n{message}")
