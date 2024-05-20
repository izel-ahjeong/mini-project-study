from django.db import models
from django.conf import settings 


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name



class Article(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    abstract = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    content_url = models.URLField()
    article_public_Date = models.CharField(max_length=255)

    def __str__(self):
        return self.title

    
class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    content = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} 가 {self.article.title} 기사에 남긴 댓글"

class Bookmark(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} 가 {self.article.title} 기사를 북마크함"

class Rating(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    ratings_choices = [
        (0.5, 0.5),
        (1.0, 1.0),
        (1.5, 1.5),
        (2.0, 2.0),
        (2.5, 2.5),
        (3.0, 3.0),
        (3.5, 3.5),
        (4.0, 4.0),
        (4.5, 4.5),
        (5.0, 5.0)
    ]
    ratings = models.FloatField(choices=ratings_choices)

    def __str__(self):
        return f"{self.user}가 {self.article.title} 기사에 남긴 평점"


class User_Article_Bookmark_TB(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    user_age = models.IntegerField(verbose_name="나이")
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    abstract = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user_age} 연령의 {self.user}가 {self.article.title} 기사를 북마크"


class User_Article_Rating_TB(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    user_age = models.IntegerField(verbose_name="나이")
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    ratings = models.FloatField()
    abstract = models.TextField()
    article_public_Date = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user_age} 연령의 {self.user}가 {self.article.title} 기사에 대한 평점"
        

class age_recommand_Article_TB(models.Model):
    age = models.IntegerField(verbose_name="나이")
    tag = models.TextField()

    def __str__(self):
        return f"연령대: {self.age}, Tag: {self.tag}"