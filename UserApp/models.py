from django.db import models
from django.contrib.auth.models import User
from autoslug import AutoSlugField
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True


class Profile(BaseModel):
    user = models.OneToOneField(User,on_delete=models.SET_NULL,null=True,related_name="Profile")
    profilePhoto = models.ImageField(upload_to="user/images/profilePhoto",blank=True,null=True)
    followers = models.ManyToManyField(User,blank=True,null=True, related_name='follower')
    following = models.ManyToManyField(User,blank=True,null=True, related_name='following')
    profile_slug = AutoSlugField(populate_from='user',unique=True)

    def __str__(self):
        return self.user.username
    
    def number_of_followers(self):
        return self.followers.count()
    
    def number_of_following(self):
        return self.following.count()
    

class Posts(BaseModel):
    post_title = models.CharField(max_length=255)
    post = models.ImageField(upload_to="user/images/posts")
    likes = models.ManyToManyField(User,blank=True,null=True, related_name='post_like')
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,related_name="Posts")
    profile = models.ForeignKey(Profile,on_delete=models.SET_NULL,null=True,blank=True,related_name="post_profile")
    post_slug = AutoSlugField(populate_from='post_title',unique=True)


    def __str__(self):
        return self.post_title

    def number_of_likes(self):
        return self.likes.count()

    class Meta:
        ordering = ['-created_at']


class Comments(BaseModel):
    Post = models.ForeignKey(Posts,on_delete=models.SET_NULL,null=True,related_name='post_comments')
    Comment = models.TextField(blank=True,null=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='comments')
    profile = models.ForeignKey(Profile,on_delete=models.SET_NULL,blank=True,null=True,related_name="comment_profile")

    def __str__(self):
        return f"{self.Post},{self.Comment},{self.user}"
    
    class Meta:
        ordering = ['-created_at']

class Notification(BaseModel):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,related_name="notifications")
    message = models.TextField()
    profile = models.ForeignKey(Profile,on_delete=models.SET_NULL,related_name="notifications_profile",null=True,blank=True)

    def __str__(self):
        return f"{self.user},{self.message}"