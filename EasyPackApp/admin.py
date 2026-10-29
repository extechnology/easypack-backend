from django.contrib import admin
from .models import *

class BoxSizeModelInline(admin.StackedInline):
    model = BoxSizeModel
    extra = 1
    show_change_link = True
    
@admin.register(BoxModel)
class BoxModelAdmin(admin.ModelAdmin):
    list_display = ('title', 'paper_brown_price', 'paper_white_price', 'is_available', 'created_at', 'updated_at')
    search_fields = ('title', 'description')
    list_filter = ('is_available', 'created_at', 'updated_at')
    inlines = [BoxSizeModelInline]


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_number', 'subject', 'created_at')
    search_fields = ('name', 'email', 'phone_number', 'subject', 'message')
    list_filter = ('created_at',)
    readonly_fields = ('created_at', 'updated_at')
