from django.contrib import admin
from .models import LandRecord, UserProfile, DocumentCategory

# Custom admin display for land records
class LandRecordAdmin(admin.ModelAdmin):
    list_display = ('title', 'property_address', 'owner', 'category', 'date_added')
    list_filter = ('category', 'date_added')
    search_fields = ('title', 'property_address', 'description')
    date_hierarchy = 'date_added'

# Custom admin display for categories
class DocumentCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

# Register models with admin site
admin.site.register(LandRecord, LandRecordAdmin)
admin.site.register(UserProfile)
admin.site.register(DocumentCategory, DocumentCategoryAdmin)
