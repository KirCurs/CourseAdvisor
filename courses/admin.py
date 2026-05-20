from django.contrib import admin

from .models import Course, CourseTag, Prerequisite

admin.site.register(Course)
admin.site.register(CourseTag)
admin.site.register(Prerequisite)
