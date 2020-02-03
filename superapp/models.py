from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class AboutStartup(models.Model):
    startup_name = models.CharField(max_length=254)
    Domains_Covered = models.CharField(max_length=300)
    description = models.TextField(default='')

    class Meta:
        verbose_name_plural = 'About Startup'

    def __str__(self):
        return self.startup_name


class UserProfile(models.Model):
    STATUS_CHOICES = [
        ('MENTOR', 'MENTOR/INVESTOR'),
        ('STUDENT', 'STUDENT'),
        ('EXPLORER', 'EXPLORER'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    startup = models.ForeignKey(
        AboutStartup, on_delete=models.SET_NULL, null=True, related_name='startup')
    contact = models.CharField(max_length=13)
    role = models.CharField(max_length=254)
    status = models.CharField(
        max_length=200, choices=STATUS_CHOICES, default='EXPLORER')

    def __str__(self):
        return self.user.username


class StartupGroup(models.Model):
    group_name = models.CharField(max_length=256)
    users = models.ManyToManyField(UserProfile)
    description = models.TextField()
    def __str__(self):
        return self.group_name


class Post(models.Model):
    group = models.ForeignKey(StartupGroup,on_delete=models.CASCADE,related_name='groupname')
    title = models.CharField(max_length = 84)
    description = models.CharField(max_length = 255)
    author = models.ForeignKey(UserProfile,on_delete=models.SET_NULL,null = True,related_name='authorname')
    def __str__(self):
        return self.title