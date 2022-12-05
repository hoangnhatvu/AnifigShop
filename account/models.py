from django.core.checks.messages import Error
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password=None):
        if not email:
            raise ValueError('Bạn chưa nhập địa chỉ email')

        if not username:
            raise ValueError('Bạn chưa nhập username !')

        # Tạo đối tượng user mới
        user = self.model(
            email=self.normalize_email(email=email),    # Chuyển email về dạng bình thường
            username=username,
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email=email),
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_admin = True
        user.is_active = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)

    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'    # Trường quyêt định khi login
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']    # Các trường yêu cầu khi đk tài khoản (mặc định đã có email), mặc định có password

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True

    def full_name(self):
        return self.last_name + " " + self.first_name


class UserProfile(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=50)
    address = models.CharField(blank=True, max_length=100)
    profile_picture = models.ImageField(null=True, blank=True, upload_to='user_profile/')


    def __str__(self):
        return self.user.first_name