from django.db.models import *
from django.contrib.auth.models import User


class Restaurant(Model):
    title = CharField(max_length=80)
    adress = CharField(max_length=100)
    description = TextField(max_length=4096)
    author = ForeignKey(User, on_delete=CASCADE, default=1)

    def __str__(self):
        return str(self.title)


class Review(Model):
    rest = ForeignKey(Restaurant, on_delete=CASCADE)
    subject = CharField(max_length=80)

    stars = CharField(max_length=2, null=True, blank=True)
    text = TextField(max_length=4096)
    created_at = DateTimeField('creation timestamp', auto_now_add=True)
    updated_at = DateTimeField('update timestamp', auto_now=True)

    def __str__(self):
        return str(self.subject)
