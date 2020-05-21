from django.db import models


class Account(models.Model):
    username = models.CharField(max_length=50, unique=True)
    realname = models.CharField(max_length=50)
    email_or_phone = models.CharField(max_length=100, unique=True, null=True)
    password = models.CharField(max_length=300)
    avatar = models.URLField(max_length=2000, blank=True, null=True)
    follow = models.ManyToManyField(
        'self', through='Follow', symmetrical=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'accounts'


class Follow(models.Model):
    from_user = models.ForeignKey(
        'Account', on_delete=models.SET_NULL, null=True, related_name='from_user')
    to_user = models.ForeignKey(
        'Account', on_delete=models.SET_NULL, null=True, related_name='to_user')

    class Meta:
        db_table = 'follows'
