from django.contrib import admin
from .models import *

admin.site.register(Invoice)
admin.site.register(InvTrack)
admin.site.register(CertPay)
admin.site.register(PayRecom)
admin.site.register(InvLet)
admin.site.register(InvLetAdnBack)
admin.site.register(LetTo)