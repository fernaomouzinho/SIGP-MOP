import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from eval.models import Eval, EvalLet, EvalTrack, EvalFITrack,EvalLetCNABack
from eval.forms import EvalLetForm2
from conf.utils import getnewid
from conf.utils import getnewid,write_roman
from users.decorators import allowed_users
from sigp.utils import get_roles

# @login_required
# @allowed_users(allowed_roles=['uivp'])
# def uvipEvalFINext1(request, pk): #to Gab
#     obj = get_object_or_404(EvalLet, pk=pk)
#     obj.is_send = True
#     obj.is_back = False
#     obj.comment = None
#     obj.save()
#     eval = obj.eval
#     track = EvalFITrack.objects.filter(eval=eval).first()
#     track.is_uvip_out_1 = True
#     track.date_uvip_out_1 = datetime.datetime.now()
#     track.stages = "UVIP ba Gabinete"
#     track.percent = 21
#     track.save()
#     messages.success(request, f'UVIP ba Gabinete.')
#     return redirect('uvip-eval-det', hashid=eval.hashed)
# #
# @login_required
# @allowed_users(allowed_roles=['gab'])
# def gabEvalFIIn1(request, pk): #to UVIP
#     obj = get_object_or_404(EvalLet, pk=pk)
#     obj.is_read = True
#     obj.save()
#     eval = obj.eval
#     track = EvalFITrack.objects.filter(eval=eval).first()
#     track.is_gab_in_1 = True
#     track.date_gab_in_1 = datetime.datetime.now()
#     track.stages = "Gab Simu"
#     track.percent = 29
#     track.save()
#     messages.success(request, f'Gab Simu.')
#     return redirect('gab-eval-det', hashid=eval.hashed)
# #

@allowed_users(allowed_roles=['sigp_uivp','sigp_admin'])
def uvipEvalFINext(request, pk): #to GAB
    obj = get_object_or_404(EvalLet, pk=pk)
    obj.is_send = True
    obj.is_back = False
    obj.comment = None
    obj.save()
    eval = obj.eval
    track = EvalFITrack.objects.filter(eval=eval).first()
    track.is_uvip_out_1 = True
    track.date_uvip_out_1 = datetime.datetime.now()
    track.stages = "UIVP ba ADN"
    track.percent = 16
    track.save()
    messages.success(request, f'UIVP ba ADN.')
    return redirect('uvip-eval-det', hashid=eval.hashed)


@allowed_users(allowed_roles=['sigp_uivp','sigp_admin'])
def uvipEvalFIIn3(request, pk): #from ADN
    eval = get_object_or_404(Eval, pk=pk)
    track = EvalFITrack.objects.filter(eval=eval).first()
    track.is_uvip_in_2 = True
    track.date_uvip_in_2 = datetime.datetime.now()
    track.stages = "UIVP ba ADN"
    track.percent = 21
    #track.percent = 50
    track.save()
    messages.success(request, f'ADN fila mai UIVP.')
    return redirect('uvip-eval-det', hashid=eval.hashed)

@allowed_users(allowed_roles=['sigp_uivp','sigp_admin'])
def uvipEvalFINext1(request, pk): #to GAB
    obj = get_object_or_404(EvalLet, pk=pk)
    obj.is_send = True
    obj.is_back = False
    obj.comment = None
    obj.save()
    eval = obj.eval
    track = EvalFITrack.objects.filter(eval=eval).first()
    track.is_uvip_out_2 = True
    track.date_uvip_out_2 = datetime.datetime.now()
    track.stages = "UIVP ba GAB"
    track.percent = 25
    track.save()
    messages.success(request, f'UIVP ba GAB.')
    return redirect('uvip-eval-det', hashid=eval.hashed)

#
@allowed_users(allowed_roles=['sigp_gabm','sigp_admin'])
def gabEvalFIIn1(request, pk): #From UVIP
    obj = get_object_or_404(EvalLet, pk=pk)
    obj.is_read = True
    obj.save()
    eval = obj.eval
    track = EvalFITrack.objects.filter(eval=eval).first()
    track.is_gab_in_1 = True
    track.date_gab_in_1 = datetime.datetime.now()
    track.stages = "Gab Simu"
    track.percent = 30
    track.save()
    messages.success(request, f'Gab Simu.')
    return redirect('gab-eval-det', hashid=eval.hashed)
#

@allowed_users(allowed_roles=['sigp_gabm','sigp_admin'])
def gabEvalFINext1(request, pk): #to SGP-Kafi
    obj = get_object_or_404(EvalLet, pk=pk)
    # obj.is_send = True
    # obj.is_back = False
    obj.comment = None
    obj.save()
    eval = obj.eval
    track = EvalFITrack.objects.filter(eval=eval).first()
    track.is_gab_out_1 = True
    track.date_gab_out_1 = datetime.datetime.now()
    track.stages = "UIVP ba SGP"
    track.percent = 35
    track.save()
    messages.success(request, f'Gabinete Ministro ba KAFI.')
    return redirect('gab-eval-det', hashid=eval.hashed)


@allowed_users(allowed_roles=['sigp_gabm','sigp_admin'])
def gabEvalFIIn2(request, pk): #from Kafi
    obj = get_object_or_404(EvalLet, pk=pk)
    obj.is_read = True
    obj.save()
    eval = obj.eval
    track = EvalFITrack.objects.filter(eval=eval).first()
    track.is_gab_in_2 = True
    track.date_gab_in_2 = datetime.datetime.now()
    track.stages = "KAFI ba GABINETE MINISTRO"
    track.percent = 40
    track.save()
    messages.success(request, f'KAFI ba Gabinete Ministro.')
    return redirect('gab-eval-det', hashid=eval.hashed)

@allowed_users(allowed_roles=['sigp_gabm','sigp_admin'])
def gabEvalFINext2(request, pk): #to UIVP
    obj = get_object_or_404(EvalLet, pk=pk)
    # obj.is_send = True
    # obj.is_back = False
    obj.comment = None
    obj.save()
    eval = obj.eval
    track = EvalFITrack.objects.filter(eval=eval).first()
    track.is_gab_out_2 = True
    track.date_gab_out_2 = datetime.datetime.now()
    track.stages = "GABINETE MINISTRO ba UIVP"
    track.percent = 45
    track.save()
    messages.success(request, f'Gabinete ba UIVP.')
    return redirect('gab-eval-det', hashid=eval.hashed)

@allowed_users(allowed_roles=['sigp_uivp','sigp_admin'])
def uvipEvalFIIn4(request, pk): #from Gab
    obj = get_object_or_404(EvalLet, pk=pk)
    # obj.is_send = True
    # obj.is_back = False
    obj.comment = None
    eval = obj.eval
    track = EvalFITrack.objects.filter(eval=eval).first()
    track.is_uvip_in_3 = True
    track.date_uvip_in_3 = datetime.datetime.now()
    track.stages = "GABINETE MINISTRO  ba UIVP"
    track.percent = 50
    track.save()
    messages.success(request, f'GABINETE MINISTRO  ba UIVP.')
    return redirect('uvip-eval-det', hashid=eval.hashed)

@allowed_users(allowed_roles=['sigp_uivp','sigp_admin'])
def uvipEvalFINext2(request, pk): #to check
    obj = get_object_or_404(EvalLet, pk=pk)
    # obj.is_send = True
    # obj.is_back = False
    obj.comment = None
    obj.save()
    eval = obj.eval
    track = EvalFITrack.objects.filter(eval=eval).first()
    track.is_uvip_check = True
    track.date_uvip_check = datetime.datetime.now()
    track.stages = "UIVP Visto Dokumentu"
    track.percent = 55
    track.save()
    messages.success(request, f'UIVP Visto Dokumentu.')
    return redirect('uvip-eval-det', hashid=eval.hashed)

@allowed_users(allowed_roles=['sigp_uivp','sigp_admin'])
def uvipEvalFINext3(request, pk): #to Gab
    obj = get_object_or_404(EvalLet, pk=pk)
    # obj.is_send = True
    # obj.is_back = False
    obj.comment = None
    obj.save()
    eval = obj.eval
    track = EvalFITrack.objects.filter(eval=eval).first()
    track.is_uvip_out_3 = True
    track.date_uvip_out_3 = datetime.datetime.now()
    track.stages = "UIVP ba GABINETE MINISTRO "
    track.percent = 60
    track.save()
    messages.success(request, f'UIVP ba GABINETE MINISTRO .')
    return redirect('uvip-eval-det', hashid=eval.hashed)

@allowed_users(allowed_roles=['sigp_gabm','sigp_admin'])
def gabEvalFIIn3(request, pk): #from UVIP
    obj = get_object_or_404(EvalLet, pk=pk)
    obj.is_read = True
    obj.save()
    eval = obj.eval
    track = EvalFITrack.objects.filter(eval=eval).first()
    track.is_gab_in_3 = True
    track.date_gab_in_3 = datetime.datetime.now()
    track.stages = "KAFI ba GABINETE MINISTRO "
    track.percent = 65
    track.save()
    messages.success(request, f'KAFI ba GABINETE MINISTRO.')
    return redirect('gab-eval-det', hashid=eval.hashed)

@allowed_users(allowed_roles=['sigp_gabm','sigp_admin'])
def gabEvalFINext3(request, pk): #to Approve
    obj = get_object_or_404(EvalLet, pk=pk)
    # obj.is_send = True
    # obj.is_back = False
    obj.comment = None
    obj.save()
    eval = obj.eval
    track = EvalFITrack.objects.filter(eval=eval).first()
    track.is_let_appr = True
    track.date_let_appr = datetime.datetime.now()
    track.stages = "GABINETE MINISTRO Aprova dileberasaun"
    track.percent = 70
    track.save()
    messages.success(request, f'GABINETE MINISTRO Aprova dileberasaun.')
    return redirect('gab-eval-det', hashid=eval.hashed)

@allowed_users(allowed_roles=['sigp_gabm','sigp_admin'])
def gabEvalFINext4(request, pk): #to Approve
    obj = get_object_or_404(EvalLet, pk=pk)
    # obj.is_send = True
    # obj.is_back = False
    obj.comment = None
    obj.save()
    eval = obj.eval
    track = EvalFITrack.objects.filter(eval=eval).first()
    track.is_gab_out_3 = True
    track.date_gab_out_3 = datetime.datetime.now()
    track.stages = "GABINETE MINISTRO ba CNA"
    track.percent = 75
    track.save()
    messages.success(request, f'GABINETE MINISTRO ba CNA.')
    return redirect('gab-eval-det', hashid=eval.hashed)


@allowed_users(allowed_roles=['sigp_gabm','sigp_admin'])
def gabEvalFIIn4(request, pk): #from UVIP
    obj = get_object_or_404(EvalLet, pk=pk)
    obj.is_read = True
    obj.save()
    eval = obj.eval
    track = EvalFITrack.objects.filter(eval=eval).first()
    track.is_gab_in_4 = True
    track.date_gab_in_4 = datetime.datetime.now()
    track.stages = "GABINETE MINISTRO ba CNA"
    track.percent = 80
    track.save()
    # Save to EvalLetCNABack
    # evalcna, created = EvalLetCNABack.objects.get_or_create(
    #     evallet=obj,
    #     defaults={
    #         "datetime": datetime.datetime.now(),
    #         "subject": "EZULTADU HUSI CNA Mai GABINETE",
    #         "is_return": True,
    #     }
    # )
    
    # newid, new_hashid = getnewid(EvalLetCNABack)

    # # Update even if it already exists
    # evalcna.date_gab_in_4 = datetime.datetime.now()
    # evalcna.stage = "Gabinete Ministro ba CNA"
    # evalcna.status = True
    # evalcna.id = newid
    # evalcna.datetime = datetime.datetime.now()
    # evalcna.user = request.user
    # evalcna.hashed = new_hashid
    # evalcna.save()

    messages.success(request, f'GABINETE MINISTRO ba CNA.')
    return redirect('gab-eval-det', hashid=eval.hashed)

@allowed_users(allowed_roles=['sigp_gabm','sigp_admin'])
def gabEvalFINext5(request, pk): #to UIVP
    obj = get_object_or_404(EvalLet, pk=pk)
    # obj.is_send = True
    # obj.is_back = False
    obj.comment = None
    obj.save()
    eval = obj.eval
    track = EvalFITrack.objects.filter(eval=eval).first()
    track.is_gab_out_4 = True
    track.date_gab_out_4 = datetime.datetime.now()
    track.stages = "GABINETE MINISTRO ba UIVP"
    track.percent = 82
    track.save()
    messages.success(request, f'GAB ba UIV.')
    return redirect('gab-eval-det', hashid=eval.hashed)

@allowed_users(allowed_roles=['sigp_uivp','sigp_admin'])
def uvipEvalFIIn5(request, pk): #from Gab
    obj = get_object_or_404(EvalLet, pk=pk)
    # obj.is_send = True
    # obj.is_back = False
    obj.comment = None
    eval = obj.eval
    track = EvalFITrack.objects.filter(eval=eval).first()
    track.is_uvip_in_4 = True
    track.date_uvip_in_4 = datetime.datetime.now()
    track.stages = "GABINETE MINISTRO ba UIVP"
    track.percent = 84
    track.save()
    messages.success(request, f'GABINETE MINISTRO ba UIVP.')
    return redirect('uvip-eval-det', hashid=eval.hashed)

@allowed_users(allowed_roles=['sigp_uivp','sigp_admin'])
def uvipEvalFINext4(request, pk): #to Sign
    obj = get_object_or_404(EvalLet, pk=pk)
    # obj.is_send = True
    # obj.is_back = False
    obj.comment = None
    obj.save()
    eval = obj.eval
    track = EvalFITrack.objects.filter(eval=eval).first()
    track.is_uvip_sign = True
    track.date_uvip_sign = datetime.datetime.now()
    track.stages = "UIVP Asina"
    track.percent = 86
    track.save()
    messages.success(request, f'UIVP Asina.')
    return redirect('uvip-eval-det', hashid=eval.hashed)

@allowed_users(allowed_roles=['sigp_uivp','sigp_admin'])
def uvipEvalFINext5(request, pk): #to Gab
    obj = get_object_or_404(EvalLet, pk=pk)
    # obj.is_send = True
    # obj.is_back = False
    obj.comment = None
    obj.save()
    eval = obj.eval
    track = EvalFITrack.objects.filter(eval=eval).first()
    track.is_uvip_out_4 = True
    track.date_uvip_out_4 = datetime.datetime.now()
    track.stages = "UIVP ba GABINETE MINISTRO"
    track.percent = 90
    track.save()
    messages.success(request, f'UIVP ba GABINETE MINISTRO.')
    return redirect('uvip-eval-det', hashid=eval.hashed)

@allowed_users(allowed_roles=['sigp_gabm','sigp_admin'])
def gabEvalFIIn5(request, pk): #from UVIP
    obj = get_object_or_404(EvalLet, pk=pk)
    obj.is_read = True
    obj.save()
    eval = obj.eval
    track = EvalFITrack.objects.filter(eval=eval).first()
    track.is_gab_in_5 = True
    track.date_gab_in_5 = datetime.datetime.now()
    track.stages = "GABINETE MINISTRO Simu husi UIVP"
    track.percent = 92
    track.save()
    messages.success(request, f'GAB Simu husi UIVP.')
    return redirect('gab-eval-det', hashid=eval.hashed)

@allowed_users(allowed_roles=['sigp_gabm','sigp_admin'])
def gabEvalFINext6(request, pk): #to sign
    obj = get_object_or_404(EvalLet, pk=pk)
    # obj.is_send = True
    # obj.is_back = False
    obj.comment = None
    obj.save()
    eval = obj.eval
    track = EvalFITrack.objects.filter(eval=eval).first()
    track.is_gab_sign = True
    track.date_gab_sign = datetime.datetime.now()
    track.stages = "GABINETE MINISTRO Asina"
    track.percent = 94
    track.save()
    messages.success(request, f'GABINETE MINISTRO Asina.')
    return redirect('gab-eval-det', hashid=eval.hashed)


@allowed_users(allowed_roles=['sigp_gabm','sigp_admin'])
def gabEvalFINext7(request, pk): #to UIVP
    obj = get_object_or_404(EvalLet, pk=pk)
    # obj.is_send = True
    # obj.is_back = False
    obj.comment = None
    obj.save()
    eval = obj.eval
    track = EvalFITrack.objects.filter(eval=eval).first()
    track.is_gab_out_5 = True
    track.date_gab_out_5 = datetime.datetime.now()
    track.stages = "GABINETE MINISTRO ba UIVP"
    track.percent = 96
    track.save()
    messages.success(request, f'GABINETE MINISTRO ba UIVP.')
    return redirect('gab-eval-det', hashid=eval.hashed)


@allowed_users(allowed_roles=['sigp_uivp','sigp_admin'])
def uvipEvalFIIn6(request, pk): #from Gab
    obj = get_object_or_404(EvalLet, pk=pk)
    # obj.is_send = True
    # obj.is_back = False
    obj.comment = None
    eval = obj.eval
    track = EvalFITrack.objects.filter(eval=eval).first()
    track.is_uvip_in_5 = True
    track.date_uvip_in_5 = datetime.datetime.now()
    track.stages = "UIVP Simu husi GABINETE MINISTRO"
    track.percent = 98
    track.save()
    messages.success(request, f'UIVP Simu husi GABINETE MINISTRO.')
    return redirect('uvip-eval-det', hashid=eval.hashed)


@allowed_users(allowed_roles=['sigp_uivp','sigp_admin'])
def uvipEvalFINext6(request, pk): #to AND-CNA-SGP
    obj = get_object_or_404(EvalLet, pk=pk)
    # obj.is_send = True
    # obj.is_back = False
    obj.comment = None
    obj.save()
    eval = obj.eval
    track = EvalFITrack.objects.filter(eval=eval).first()
    track.is_uvip_out_5 = True
    track.date_uvip_out_5 = datetime.datetime.now()
    track.is_end = True
    track.date_end = datetime.datetime.now()
    track.stages = "UIVP ba ADN-CNA-SGP"
    track.percent = 100
    track.save()
    messages.success(request, f'UIVP ba ADN-CNA-SGP.')
    return redirect('uvip-eval-det', hashid=eval.hashed)