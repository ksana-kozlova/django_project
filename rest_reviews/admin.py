from django.contrib import admin
from django.db.models import Max
from . import models

class ReviewInline(admin.TabularInline):
    model = models.Review

    field = ('subject', 'text', 'created_at', 'stars', 'review_image')
    readonly_fields = ('subject', 'text', 'created_at', 'stars')
    ordering = ('-created_at',)
    show_change_link = True

    def has_add_permission(self, request, obj):
        return False


class RestaurantAdmin(admin.ModelAdmin):

    list_display = ('title', 'adress', 'description', 'rest_image')
    ordering = ('title',)
    fields = ('title', 'adress', 'description', 'rest_image')
    view_on_site = True
    inlines = [ReviewInline]


class ReviewAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(updated=Max('created_at'))

    def created(self, obj):
        return obj.created_at

    def has_add_permission(self, request):
        return False

    list_display = ('subject', 'author','text','rest', 'created_at', 'stars', 'review_image')
    ordering = ('-created_at', 'subject')
    fields = ('subject', 'author','text', 'created_at', 'stars', 'review_image')
    readonly_fields = ('author', 'created_at', 'stars')
    



# Register your models here.
admin.site.register(models.Restaurant, RestaurantAdmin)
admin.site.register(models.Review, ReviewAdmin)