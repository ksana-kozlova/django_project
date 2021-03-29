from django.db.models import *
from django.contrib.auth.models import User


class Restaurant(Model):
    title = CharField(max_length=80)
    adress = CharField(max_length=100)
    description = TextField(max_length=4096)
    rest_image = ImageField(null=True, blank=True, upload_to="images/")

    def __str__(self):
        return str(self.title)


class Review(Model):
    rest = ForeignKey(Restaurant, on_delete=CASCADE)
    subject = CharField(max_length=80)
    author = ForeignKey(User, on_delete=CASCADE, default=1)
    stars = IntegerField(null=True, blank=True)
    text = TextField(max_length=4096)
    review_image = ImageField(null=True, blank=True, upload_to="images/")
    created_at = DateTimeField('creation timestamp', auto_now_add=True)
    updated_at = DateTimeField('update timestamp', auto_now=True)

    def __str__(self):
        return '"%s" by @%s' % (self.subject, self.author.username)
