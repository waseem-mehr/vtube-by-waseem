from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class UserModel(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='media/',default='media/user.png')
    def __str__(self):
        return self.user.username



class Categorey(models.Model):
    name=models.CharField(max_length=20,null=True)
    date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name='Categorey'
        verbose_name_plural='Categories'

class Video(models.Model):
    title=models.CharField(max_length=100)
    categorey=models.ForeignKey(Categorey,on_delete=models.CASCADE)
    date=models.DateTimeField(auto_now_add=True)
    thumbnail=models.ImageField(upload_to='media/')
    video=models.FileField(upload_to='media/')
    user=models.ForeignKey(UserModel,on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name='Video'
        verbose_name_plural='Videos'

class Commment(models.Model):
    comment_text=models.TextField(max_length=200)
    date=models.DateTimeField(auto_now_add=True)
    video=models.ForeignKey(Video,on_delete=models.CASCADE)
    user=models.ForeignKey(UserModel,on_delete=models.CASCADE)

    def __str__(self):
        return self.comment_text
    class Meta:
        verbose_name='Comment'
        verbose_name_plural='Comments'

class Reply(models.Model):
    comment_text=models.TextField(max_length=200)
    comment=models.ForeignKey(Commment,on_delete=models.CASCADE)
    user=models.ForeignKey(UserModel,on_delete=models.CASCADE)
    date=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.comment_text
    class Meta:
        verbose_name='Reply'
        verbose_name_plural='Replies'

class Like(models.Model):
    video=models.ForeignKey(Video,on_delete=models.CASCADE)
    user=models.ForeignKey(UserModel,on_delete=models.CASCADE)
    date=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.user.username
    class Meta:
        verbose_name='Like'
        verbose_name_plural='Likes'

class Unlike(models.Model):
    video=models.ForeignKey(Video,on_delete=models.CASCADE)
    user=models.ForeignKey(UserModel,on_delete=models.CASCADE)
    date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return  self.user.user.username

    class Meta:
        verbose_name='Unlike'
        verbose_name_plural='Unlikes'


class Views(models.Model):
    video=models.ForeignKey(Video,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    def __str__(self):
        return self.user.username