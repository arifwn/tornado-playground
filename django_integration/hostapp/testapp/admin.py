from testapp.models import Registrant
from django.contrib import admin

class RegistrantAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'country', 'institution',
                    'creation_date', 'modified_date', 'confirmed']

admin.site.register(Registrant, RegistrantAdmin)

