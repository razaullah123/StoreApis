from django.contrib import admin
from store.admin import AdminProduct
from tags.models import TaggedItem
from django.contrib.contenttypes.admin import GenericTabularInline
from store.models import Product


class TagInline(GenericTabularInline):
    autocomplete_fields = ['tag']
    model = TaggedItem


class CustomProductAdmin(AdminProduct):
    inlines = [TagInline]


admin.site.unregister(Product)
admin.site.register(Product, CustomProductAdmin)
