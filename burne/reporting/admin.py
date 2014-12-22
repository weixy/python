from django.contrib import admin
from models import Scenario, LoadRequest


class RequestsInline(admin.TabularInline):
    model = LoadRequest


class ScenarioAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name']}),
    ]
    inlines = [RequestsInline]
    list_display = ('name',)

admin.site.register(Scenario)
# admin.site.register(LoadRequest)
