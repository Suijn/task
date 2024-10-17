from django.contrib import admin

from task.apps.prefixes.models import Item, Prefix


class ItemInline(admin.TabularInline):
    model = Item


class PrefixAdmin(admin.ModelAdmin):
    inlines = [
        ItemInline,
    ]


class ItemAdmin(admin.ModelAdmin):
    pass


admin.site.register(Prefix, PrefixAdmin)
admin.site.register(Item, ItemAdmin)
