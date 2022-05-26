from django.db import models

class Post(models.Model):
    category = models.ForeignKey('Category', on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=100, verbose_name='Title')
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    publish_date = models.DateTimeField(auto_now_add=True)
    published = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.title}'

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField()
    publish_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey("auth.User", on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.text}'

class Category(models.Model):
    text = models.CharField(max_length=70, verbose_name='Category')

    def __str__(self):
        return f'{self.text}'