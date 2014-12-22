from django.contrib import admin
from models import Scenario, LoadRequest


class RequestsInline(admin.TabularInline):
    model = LoadRequest
    extra = 0


class ScenarioAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name', 'description']}),
    ]
    inlines = [RequestsInline]
    list_display = ('name', 'description')

admin.site.register(Scenario, ScenarioAdmin)
# admin.site.register(LoadRequest)
