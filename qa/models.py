from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User


# Create your models here.


class Question(models.Model):
    question_title = models.CharField(max_length=100)
    question_text = models.TextField(max_length=2000)
    date_posted = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    qid = models.AutoField(primary_key=True)
    posted_by = models.TextField(max_length=50)
    slug = models.SlugField(max_length=40)

    def save(self, *args,  **kwargs):
        self.slug = slugify(self.question_title)
        super(Question, self).save(*args, **kwargs)

class Answer(models.Model):
    answer_text = models.TextField(max_length=2000)
    date_posted = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    qid = models.ForeignKey(Question, on_delete=models.CASCADE)
    aid = models.AutoField(primary_key=True)
    posted_by = models.TextField(max_length=50)
    
    def save(self, *args,  **kwargs):
        super(Answer, self).save(*args, **kwargs)


