from django.contrib import admin
from accounts.models import *
from dashboard.models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Age)
admin.site.register(Sport)
admin.site.register(Tournament)
admin.site.register(Region)
admin.site.register(District)
admin.site.register(Athlete)
admin.site.register(School)
admin.site.register(City)
admin.site.register(Municipality)
admin.site.register(Classroom)
admin.site.register(school_official)
