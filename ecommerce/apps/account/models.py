from django.db import models
from django.utils import timezone
from django.db import models
from django.core.mail import send_mail
from django.template.loader import get_template
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


# send_mail(subject, message, from_email, recipient_list, html_message)






class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user




class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='adresse email',
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True, verbose_name='compté deja activé ?')
    staff = models.BooleanField(default=False) # a admin user; non super-user
    admin = models.BooleanField(default=False) # a superuser

    # notice the absence of a "Password field", that is built in.
    objects = UserManager()

    class Meta:
        verbose_name = 'Compte'
        verbose_name_plural = 'Comptes'
        
        
        
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] # Email & Password are required by default.

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_perms(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True
    

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        if self.admin:
            return True
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin











class GuestEmail(models.Model):
    email = models.EmailField(max_length=254)
    active = models.BooleanField(default=True)
    update = models.DateTimeField("dernière modification", auto_now=True)
    timestamp = models.DateTimeField("date de creation", default=timezone.now)
    
    

    class Meta:
        verbose_name = "Email invité"
        verbose_name_plural = "Emails invités"

    def __str__(self):
        return self.email
""" 
    def get_absolute_url(self):
        return reverse("GuestEmail_detail", kwargs={"pk": self.pk})
 """