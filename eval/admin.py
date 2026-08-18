from django.contrib import admin
from .models import *

admin.site.register(Eval)
admin.site.register(EvalFile)
admin.site.register(EvalTrack)
admin.site.register(EvalFITrack)
admin.site.register(LetTo)
admin.site.register(EvalLet)
admin.site.register(EvalLetAdnBack)
admin.site.register(EvalLetCNABack)