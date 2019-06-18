from .mail_handler import Mailer, Email

def main(sender='iic2333', evaluation='I1', attachments=[('.', 'mail_handler.py')]):
    mailer = Mailer(server='localhost', sender=sender)
    
    receiver_list = ['schau@uc.cl']
    bbc_list = []
    cc_list = []
    
    mail_list = receiver_list + bbc_list + cc_list
    
    email = Email(sender=sender, subject=evaluation, text_body='Text body', attachments=attachments)
    email.create_content(receiver_list, cc_list)
    
    mailer.send_mail(email._email, mail_list)
    
    mailer.stop_server()

if __name__ == '__main__':
    main()