from django.contrib import admin

from .models import Interest, StudentInterest, StudentProfile, StudentTestAttempt

admin.site.register(StudentProfile)
admin.site.register(Interest)
admin.site.register(StudentInterest)
admin.site.register(StudentTestAttempt)
