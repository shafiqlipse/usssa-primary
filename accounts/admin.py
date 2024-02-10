from django.contrib import admin
from accounts.models import *
from dashboard.models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Sport)
admin.site.register(Tournament)
admin.site.register(Region)
admin.site.register(District)
admin.site.register(Athlete)
admin.site.register(School)
admin.site.register(school_official)
