from django.db import models

# Create your models here.

# class User(models.Model):
#     user_id = models.AutoField(primary_key=True, null=False)
#     email = models.CharField(null=False, max_length=50)
#     user_name = models.CharField(max_length=20, null=False)
#     password = models.CharField(max_length=20, null=False)
#     img_address = models.CharField(null=True, max_length=100)
#     motto = models.CharField(max_length=100, null=True)
#     time = models.DateField()

class Article(models.Model):
    user_id = models.IntegerField()
    title = models.CharField(max_length=50)
    content = models.TextField(null=True)
    create_time = models.DateTimeField(null=True)
    last_time = models.DateTimeField(null=True)
    class MetaArticle:
        unique_article = ('user_id', 'user_article_id')

class Tag(models.Model):
    user_id = models.IntegerField()
    user_article_id = models.IntegerField()
    tag = models.CharField(max_length=12)
    class MetaTag:
        unique_tag = ('user_id', 'user_article_id')

