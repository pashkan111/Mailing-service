from django.contrib import admin
from . import models


admin.site.register(models.Client)
admin.site.register(models.Mailing)
admin.site.register(models.Message)
