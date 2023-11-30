from django.contrib import admin
from .models import EnrolledCourse,Payment,Transcation,ModuleProgress


admin.site.register(EnrolledCourse)
admin.site.register(Payment)
admin.site.register(Transcation)
admin.site.register(ModuleProgress)

