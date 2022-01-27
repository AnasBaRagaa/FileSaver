from django.contrib import admin

# Register your models here.
from django.contrib.auth.models import User

from saver_app.models import Data

admin.site.register(Data)