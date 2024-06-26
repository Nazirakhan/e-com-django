from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from django.dispatch import receiver
from django.shortcuts import get_object_or_404

# Create your models here.
# Model for superadmin
class MyAccountManager(BaseUserManager):
    def create_user(self,first_name,last_name,username,email,password=None):
        if not email:
            raise ValueError("User must have an email address")
        
        if not username:
            raise ValueError("User must have an username")
        
        user = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
        )
        user.set_password(password)
        user.save(using = self._db)
        return user
    
    def create_superuser(self,first_name,last_name,username,email,password):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password = password,
            first_name= first_name,
            last_name= last_name,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using = self._db)
        return user





# Model for User
class Account(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name  = models.CharField(max_length=50)
    username   = models.CharField(max_length=50, unique=True)
    email      = models.EmailField(max_length=100, unique=True)
    phone      = models.CharField(max_length=50)

    # <--Required-->
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default = False)
    is_staff = models.BooleanField(default = False)
    is_active = models.BooleanField(default = False)
    is_superadmin = models.BooleanField(default = False)

    objects = MyAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj = None):
        return self.is_admin
    
    def has_module_perms(self,add_label):
        return True
    
class ProfileUser(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    address_line_1 = models.CharField(max_length=200, blank=True,null=True)
    address_line_2 = models.CharField(max_length=200, blank=True,null=True)
    profile_picture = models.ImageField(blank=True, upload_to='userProfilePic',null=True)
    city = models.CharField(max_length=20, blank=True,null=True)
    state = models.CharField(max_length=20, blank=True,null=True)
    country = models.CharField(max_length=20, blank=True, null=True)
    pincode = models.IntegerField(default=751002, blank=True)

    def __str__(self):
        return self.user.first_name
    
    def full_address(self):
        return f"{self.address_line_1} {self.address_line_2}"
    
    def save(self, *args, **kwargs):
        if self.id:
            existing = get_object_or_404(ProfileUser,id=self.id)
            if existing.profile_picture != self.profile_picture:
                existing.profile_picture.delete(save=False)

        super(ProfileUser, self).save(*args, **kwargs)
        
    @receiver(models.signals.pre_delete, sender="accounts.ProfileUser")
    def server_delete_image(sender, instance, **kwargs):
        for field in instance._meta.fields:
            if field.name=="profile_picture":
                file = getattr(instance,field.name)
                if file:
                    file.delete(save=False)
    