from django.contrib import admin
from django.db.models import Max
from . import models

class ReviewInline(admin.TabularInline):
    model = models.Review

    def is_edited(self, obj):
        return self.is_edited()

    is_edited.boolean = True

    field = ('subject', 'text', 'created_at', 'is_edited')
    readonly_fields = ('subject', 'text', 'created_at')
    ordering = ('-created_at',)
    show_change_link = True

    def has_add_permission(self, request, obj):
        return False


class RestaurantAdmin(admin.ModelAdmin):

    def has_add_permission(self, request):
        return False

    list_display = ('title', 'adress', 'description', 'rest_image')
    ordering = ('title',)
    fields = ('title', 'adress', 'description', 'rest_image')
    view_on_site = True
    inlines = [ReviewInline]


class ReviewAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(updated=Max('updated_at'))

    def updated(self, obj):
        return obj.updated_at
    
    updated.admin_order_field = 'updated_at'

    def has_add_permission(self, request):
        return False

    list_display = ('subject', 'author', 'updated_at')
    ordering = ('subject',)
    fields = ('subject', 'author', 'created_at')
    readonly_fields = ('author', 'created_at')
    view_on_site = True



# Register your models here.
admin.site.register(models.Restaurant, RestaurantAdmin)
admin.site.register(models.Review, ReviewAdmin)