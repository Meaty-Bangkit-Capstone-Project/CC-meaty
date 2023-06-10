from django.contrib import admin

# Register your models here.
from .models import User
from .models import UploadedImage

admin.site.register(User)
@admin.register(UploadedImage)
class UploadedImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'image', 'timestamp', 'prediction')
    list_filter = ('user', 'timestamp')
    search_fields = ('user__username', 'user__first_name', 'user__last_name')