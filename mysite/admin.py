from django.contrib import admin
from mysite.models import Population

@admin.register(Population)
class PopulationAdmin(admin.ModelAdmin):
    list_display = ['name', 'total', 'male', 'female']
