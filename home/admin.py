from django.contrib import admin
from .models import (
    User, UserImage, ImageThumbnail,
    AccountTier, UserImageThumbnail
)


class UserImageAdmin(admin.ModelAdmin):
    # prepopulated_fields = {"slug": ("name",)}
    list_display = ['name', 'user']


admin.site.register(UserImage, UserImageAdmin)


class UserAdmin(admin.ModelAdmin):
    list_display = [
        'username', 'account_tier', 'first_name',
        'last_name', 'is_staff'
        ]


admin.site.register(User, UserAdmin)


class AccountTierAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'display_link_to_original_image', 'generate_expiring_links'
        ]


admin.site.register(AccountTier, AccountTierAdmin)


class ImageThumbnailAdmin(admin.ModelAdmin):
    list_display = ['account_tier', 'height']


admin.site.register(ImageThumbnail, ImageThumbnailAdmin)
admin.site.register(UserImageThumbnail)
# Register your models here.
