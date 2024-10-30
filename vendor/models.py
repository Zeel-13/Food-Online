from django.db import models
from accounts.models import User,UserProfile
from accounts.utils import send_notification_email
# Create your models here.
class  Vendor(models.Model):
    vendor_name = models.CharField(max_length=50)
    user = models.OneToOneField(User,related_name='user',on_delete=models.CASCADE)
    user_profile = models.OneToOneField(UserProfile,related_name='userprofile',on_delete=models.CASCADE)
    vendor_license=models.ImageField(upload_to='vendor/license')
    is_approved=models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.vendor_name
    
    def save(self,*args,**kwargs):
        if self.pk is not None:
            original=Vendor.objects.get(pk=self.pk)
            mail_template='accounts/emails/admin_vendor_approval_email.html'
            context={
                'user':self.user,
                'is_approved':self.is_approved,
            }
            if original.is_approved!=self.is_approved:
                if self.is_approved==True:
                    #send email to vendor
                    mail_subject='Congratulations your account has been approved'
                    send_notification_email(mail_subject,mail_template,context)
                else:
                    #send email to vendor
                    mail_subject='Sorry you cannot use our platform'
                    send_notification_email(mail_subject,mail_template,context)
        return super(Vendor,self).save(*args,**kwargs)