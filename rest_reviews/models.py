from django.db.models import *
from django.contrib.auth.models import User
from django.urls import reverse

class Restaurant(Model):
    title = CharField(max_length=80)
    adress = CharField(max_length=100)
    description = TextField(max_length=4096)
    rest_image = ImageField(null=True, blank=True, upload_to="images/")

    def __str__(self):
        return str(self.title)
    
    def get_absolute_url(self):
        return reverse("rest_by_id", kwargs={'rest_id': self.id})


class Review(Model):
    rest = ForeignKey(Restaurant, on_delete=CASCADE)
    subject = CharField(max_length=80)
    author = ForeignKey(User, on_delete=CASCADE, default=1)
    stars = IntegerField(null=True, blank=True)
    text = TextField(max_length=4096, null=True, blank=True)
    review_image = ImageField(null=True, blank=True, upload_to="images/")
    created_at = DateTimeField('creation timestamp', auto_now_add=True)
    updated_at = DateTimeField('update timestamp', auto_now=True)

    def __str__(self):
        return '"%s" by @%s' % (self.subject, self.author.username)
