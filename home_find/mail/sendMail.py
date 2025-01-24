import home_find.constants as constants
import home_find.mailText as mailText

from django.core.mail import send_mail


class SendMail:
    
    def send(self):
        
        result = send_mail(
            mailText.aritcle,
            mailText.text,
            constants.EMAIL,
            [constants.EMAIL],
            fail_silently=False,
        )
        
        print(result)
        
        pass