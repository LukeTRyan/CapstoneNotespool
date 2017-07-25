from django.contrib import admin
from .models import Admin,Student,Staff,Unit

# Register your models here.

admin.site.register(Admin)
admin.site.register(Student)
admin.site.register(Staff)
admin.site.register(Unit)