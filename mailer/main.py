from .mail_handler import Mailer, Email

def main(sender='iic2333', evaluation='I1'):
    mailer = Mailer(server='localhost', sender=sender)
    
    attachments = [('.', 'mail_handler.py')]
    receiver_list = ['schau@uc.cl']
    bbc_list = []
    cc_list = []
    
    mail_list = receiver_list + bbc_list + cc_list
    
    email = Email(sender=sender, subject=evaluation, text_body='Text body', attachments=attachments)
    email.create_content(receiver_list, cc_list)
    
    mailer.send_mail(email._email, mail_list)
    

if __name__ == '__main__':
    main()