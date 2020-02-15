from django.db import models

from django.contrib.auth.models import User

from django.utils import timezone

from mdeditor.fields import MDTextField

from uuslug import uuslug,slugify

# Create your models here.


class ColumnPost(models.Model):

    administator = models.ForeignKey(User, on_delete=models.CASCADE)

    name = models.CharField(max_length=30)

    excerpt = models.CharField(max_length=100)

    created_time = models.DateTimeField(default=timezone.now)

    updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
       
        return self.name


class ArticlePost(models.Model):

    title = models.CharField(max_length=50)

    slug_title = models.SlugField(max_length=100)

    author = models.ForeignKey(User, on_delete=models.CASCADE)

    column = models.ForeignKey(ColumnPost, on_delete=models.CASCADE, null=True)

    excerpt = models.TextField()

    body = MDTextField()

    total_views = models.PositiveIntegerField(default=0)

    created_time = models.DateTimeField(default=timezone.now)

    updated_time = models.DateTimeField(auto_now=True)


    def __str__(self):

        return self.title

    def __unicode__(self):
        
        return self.title

    def save(self, *args, **kwargs):

        self.slug_title = slugify(self.title, max_length=15)
        super(ArticlePost, self).save(*args, **kwargs)