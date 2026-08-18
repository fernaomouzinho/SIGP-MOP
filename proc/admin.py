from django.contrib import admin
from .models import *

admin.site.register(Proc)
admin.site.register(ProcComp)
admin.site.register(ProcReqTrack)
admin.site.register(ProcResTrack)
admin.site.register(ProcTrack)
admin.site.register(LetTo)
admin.site.register(ProcLet)
admin.site.register(ProcFiles)