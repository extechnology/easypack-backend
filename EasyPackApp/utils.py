import requests
import random
from django.core.mail import EmailMultiAlternatives
from django.conf import settings


def googl_auth_login_mail(email, username):
    subject = "Welcome to easypack.in"
    from_email = "no-reply@easypack.in"
    to = [email]
    text_content = f"Welcome {email} to easypack.in! We're excited to have you on board."
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body style="margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f7fafc;">
        
        <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="margin: 0; padding: 0; " style="box-shadow: rgba(0, 0, 0, 0.35) 0px 5px 15px;">
            <tr>
                <td style="padding: 40px 20px;">
                    
                    <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="max-width: 500px; margin: 0 auto; background-color: #ffffff; border-radius: 16px;">
                        <tr>
                            <td style="padding: 48px 40px; text-align: center;">
                                
                                <!-- Icon -->
                                <table role="presentation" cellspacing="0" cellpadding="0" border="0" style="margin: 0 auto 24px;">
                                    <tr>
                                        <td style="width: 80px; height: 80px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); background-color: #667eea; border-radius: 40px; text-align: center; font-size: 40px; line-height: 80px;">
                                            👋
                                        </td>
                                    </tr>
                                </table>
                                
                                <!-- Heading -->
                                <h1 style="margin: 0 0 12px 0; font-size: 32px; font-weight: 600; color: #1a202c;">
                                    Welcome to EasyPack!
                                </h1>
                                
                                <!-- Email Display (no underline) -->
                                <div style="margin: 0 0 12px 0; font-size: 32px; font-weight: 600; color: #1a202c;">
                                    <span style="text-decoration: none; color: #1a202c;">{email}</span>
                                </div>
                                
                                <!-- Text -->
                                <p style="margin: 0 0 32px 0; font-size: 16px; color: #718096; line-height: 1.6;">
                                    We're excited to have you here. Let's get started on something amazing together.
                                </p>
                                
                                
                            </td>
                        </tr>
                    </table>
                    
                </td>
            </tr>
        </table>
        
    </body>
    </html>
    """
    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    
def send_registration_otp_email(email, otp):
    subject = "Your OTP Code - easypack.in"
    from_email = "no-reply@easypack.in"
    to = [email]

    text_content = f"Your OTP for registration is: {otp}"

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <title>Email Verification - OTP</title>
    </head>
    <body style="margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; padding: 40px 20px;">

        <!-- Main Container -->
        <div style="max-width: 480px; margin: 0 auto; background: #ffffff; border-radius: 12px; overflow: hidden; box-shadow: rgba(0, 0, 0, 0.35) 0px 5px 15px;">

            <!-- Header Section -->
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; text-align: center;">
                <h1 style="color: #ffffff; margin: 0; font-size: 22px; font-weight: 600;">Verify Your Email</h1>
            </div>

            <!-- Content Section -->
            <div style="padding: 25px 20px;">
                <p style="font-size: 15px; color: #555555; line-height: 1.5; margin: 0 0 20px 0;">
                    Thank you for signing up with <strong style="color: #667eea;">easypack.in</strong>! Please use the OTP below to complete your registration:
                </p>

                <!-- OTP Box -->
                <div style="background: #f8f9fa; border-radius: 8px; padding: 20px; text-align: center; margin: 20px 0; border: 2px solid #667eea;">
                    <span style="font-size: 32px; font-weight: 700; color: #667eea; letter-spacing: 6px; font-family: 'Courier New', monospace;">
                        {otp}
                    </span>
                </div>

                <!-- Important Notice -->
                <p style="margin: 0; font-size: 13px; color: #666; line-height: 1.5; text-align: center;">
                    This OTP is valid for <strong>10 minutes</strong>. Do not share it with anyone.
                </p>
            </div>

            <!-- Footer Section -->
            <div style="background: #f8f9fa; padding: 15px 20px; border-top: 1px solid #e0e0e0; text-align: center;">
                <p style="margin: 0; font-size: 11px; color: #aaa;">
                    &copy; 2025 <strong style="color: #667eea;">easypack.in</strong>. All rights reserved.
                </p>
            </div>

        </div>

    </body>
    </html>
    """

    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def send_contact_enquiry_to_admin(name, email, phone_number, subject, message):
    """Send contact enquiry notification to configured admin email"""
    admin_email = getattr(settings, 'CONTACT_ADMIN_EMAIL', 'info2easypack@gmail.com')
    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', getattr(settings, 'EMAIL_HOST_USER', 'info2easypack@gmail.com'))
    mail_subject = f"New Contact Enquiry from {name}: {subject}"
    to = [admin_email]
    phone_display = phone_number if phone_number else 'Not provided'

    text_content = f"""
New Contact Enquiry Received

Name: {name}
Email: {email}
Phone: {phone_display}
Subject: {subject}
Message:
{message}
"""

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>New Contact Enquiry</title>
    </head>
    <body style="margin: 0; padding: 30px 15px; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f7fafc;">
        <div style="max-width: 560px; margin: 0 auto; background: #ffffff; border-radius: 12px; overflow: hidden; box-shadow: rgba(0, 0, 0, 0.12) 0px 4px 16px;">
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 24px; text-align: center;">
                <h2 style="color: #ffffff; margin: 0; font-size: 22px; font-weight: 600;">📩 New Contact Enquiry</h2>
            </div>
            <div style="padding: 28px 24px;">
                <p style="font-size: 15px; color: #4a5568; margin-top: 0; margin-bottom: 20px;">
                    A new enquiry has been submitted on <strong>easypack.in</strong>. Here are the details:
                </p>
                <table style="width: 100%; border-collapse: collapse; margin-bottom: 20px;">
                    <tr>
                        <td style="padding: 10px 0; color: #718096; font-size: 14px; font-weight: 600; width: 90px; vertical-align: top; border-bottom: 1px solid #edf2f7;">Name:</td>
                        <td style="padding: 10px 0; color: #1a202c; font-size: 14px; font-weight: 500; border-bottom: 1px solid #edf2f7;">{name}</td>
                    </tr>
                    <tr>
                        <td style="padding: 10px 0; color: #718096; font-size: 14px; font-weight: 600; vertical-align: top; border-bottom: 1px solid #edf2f7;">Email:</td>
                        <td style="padding: 10px 0; color: #1a202c; font-size: 14px; border-bottom: 1px solid #edf2f7;">
                            <a href="mailto:{email}" style="color: #667eea; text-decoration: none; font-weight: 500;">{email}</a>
                        </td>
                    </tr>
                    <tr>
                        <td style="padding: 10px 0; color: #718096; font-size: 14px; font-weight: 600; vertical-align: top; border-bottom: 1px solid #edf2f7;">Phone:</td>
                        <td style="padding: 10px 0; color: #1a202c; font-size: 14px; font-weight: 500; border-bottom: 1px solid #edf2f7;">
                            <a href="tel:{phone_display}" style="color: #667eea; text-decoration: none; font-weight: 500;">{phone_display}</a>
                        </td>
                    </tr>
                    <tr>
                        <td style="padding: 10px 0; color: #718096; font-size: 14px; font-weight: 600; vertical-align: top; border-bottom: 1px solid #edf2f7;">Subject:</td>
                        <td style="padding: 10px 0; color: #1a202c; font-size: 14px; font-weight: 500; border-bottom: 1px solid #edf2f7;">{subject}</td>
                    </tr>
                </table>
                <div style="background: #f8fafc; border-left: 4px solid #667eea; padding: 16px; border-radius: 6px; margin-top: 15px;">
                    <p style="margin: 0 0 8px 0; font-weight: 600; color: #4a5568; font-size: 13px; text-transform: uppercase; letter-spacing: 0.5px;">Message</p>
                    <p style="margin: 0; color: #2d3748; white-space: pre-line; line-height: 1.6; font-size: 14px;">{message}</p>
                </div>
            </div>
            <div style="background: #f8f9fa; padding: 15px 20px; border-top: 1px solid #e2e8f0; text-align: center;">
                <p style="margin: 0; font-size: 12px; color: #a0aec0;">EasyPack Enquiry Notification System</p>
            </div>
        </div>
    </body>
    </html>
    """

    msg = EmailMultiAlternatives(mail_subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def send_contact_reply_to_customer(name, email, subject, message):
    """Send confirmation/acknowledgement reply email to the customer"""
    admin_email = getattr(settings, 'CONTACT_ADMIN_EMAIL', 'info2easypack@gmail.com')
    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', getattr(settings, 'EMAIL_HOST_USER', 'info2easypack@gmail.com'))
    mail_subject = f"Thank you for contacting EasyPack - We've received your message"
    to = [email]

    text_content = f"""
Hi {name},

Thank you for contacting EasyPack! We have received your message regarding:
"{subject}"

Our team is reviewing your enquiry and will respond as soon as possible.

Your submitted message:
{message}

Best regards,
The EasyPack Team
{admin_email}
"""

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Thank You for Contacting EasyPack</title>
    </head>
    <body style="margin: 0; padding: 30px 15px; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f7fafc;">
        <div style="max-width: 560px; margin: 0 auto; background: #ffffff; border-radius: 12px; overflow: hidden; box-shadow: rgba(0, 0, 0, 0.12) 0px 4px 16px;">
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px 20px; text-align: center;">
                <h1 style="color: #ffffff; margin: 0; font-size: 24px; font-weight: 600;">We've Received Your Message!</h1>
                <p style="color: #e2e8f0; margin: 8px 0 0 0; font-size: 14px;">Thank you for getting in touch with us</p>
            </div>
            <div style="padding: 30px 24px;">
                <p style="font-size: 16px; color: #2d3748; margin-top: 0;">Hi <strong>{name}</strong>,</p>
                <p style="font-size: 15px; color: #4a5568; line-height: 1.6;">
                    Thank you for reaching out to <strong>EasyPack</strong>! We have successfully received your enquiry and our support team will get back to you shortly.
                </p>
                
                <div style="background: #f8fafc; border-radius: 8px; padding: 18px 20px; margin: 24px 0; border: 1px solid #e2e8f0;">
                    <h3 style="margin: 0 0 12px 0; color: #667eea; font-size: 13px; text-transform: uppercase; letter-spacing: 0.5px;">Your Enquiry Summary</h3>
                    <p style="margin: 0 0 8px 0; font-size: 14px; color: #4a5568;">
                        <strong style="color: #2d3748;">Subject:</strong> {subject}
                    </p>
                    <p style="margin: 0 0 6px 0; font-size: 14px; color: #2d3748;"><strong>Message:</strong></p>
                    <div style="background: #ffffff; padding: 12px 14px; border-radius: 6px; border: 1px solid #edf2f7; color: #4a5568; font-size: 14px; line-height: 1.6; white-space: pre-line;">
                        {message}
                    </div>
                </div>

                <p style="font-size: 14px; color: #718096; line-height: 1.6; margin-bottom: 0;">
                    If you have any further questions in the meantime, feel free to reply to this email or contact us directly at <a href="mailto:{admin_email}" style="color: #667eea; text-decoration: none; font-weight: 500;">{admin_email}</a>.
                </p>
            </div>
            <div style="background: #f8f9fa; padding: 18px 20px; border-top: 1px solid #e2e8f0; text-align: center;">
                <p style="margin: 0 0 4px 0; font-size: 12px; color: #718096;">
                    Best regards,<br>
                    <strong>The EasyPack Team</strong>
                </p>
                <p style="margin: 8px 0 0 0; font-size: 11px; color: #a0aec0;">
                    &copy; 2026 <strong style="color: #667eea;">easypack.in</strong>. All rights reserved.
                </p>
            </div>
        </div>
    </body>
    </html>
    """

    msg = EmailMultiAlternatives(mail_subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def send_contact_emails(name, email, subject, message, phone_number=None):
    """
    Helper function to send both enquiry email to admin and reply email to the customer.
    Catches exceptions to prevent breaking the request if SMTP fails.
    """
    admin_sent = False
    customer_sent = False

    try:
        send_contact_enquiry_to_admin(name, email, phone_number, subject, message)
        admin_sent = True
    except Exception as e:
        print(f"Failed to send contact enquiry to admin: {e}")

    try:
        send_contact_reply_to_customer(name, email, subject, message)
        customer_sent = True
    except Exception as e:
        print(f"Failed to send contact reply to customer: {e}")

    return {'admin_sent': admin_sent, 'customer_sent': customer_sent}
