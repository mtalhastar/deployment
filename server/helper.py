from django.core.mail import send_mail
from django.conf import settings

def send_forgetPassword_mail(email,code):
    subject='MindCare: Forgot Password Link'
    message=f'Your verification code is {code} \n The code will expire within 10 minutes'
    email_from=settings.EMAIL_HOST_USER
    recipient_list=[email]
    send_mail(subject,message,email_from,recipient_list)
    return True
    
    
def send_EmailToSevereStudent(email,message):
    subject='MindCare: Thankyou for giving Test-1 previously we encourage you to appear for Test-2 to help us re-evaluate'
    message=f'https://mindcare-ten.vercel.app/'
    email_from=settings.EMAIL_HOST_USER
    recipient_list=[email]
    send_mail(subject,message,email_from,recipient_list)
    return True
    
    