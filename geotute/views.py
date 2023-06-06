from django.shortcuts import render
from geotute import settings
from geotute.roi import Rois
import json
from django.http import HttpResponse

def grain(request):
    return render(request, "grain.html")

grain01_rois = Rois(settings.STATIC_ROOT / "tutorial" / "Grain01" / "RoiSet.zip")

def result(request):
    picked = grain01_rois.pick(
        float(request.GET['x']),
        float(request.GET['y'])
    )
    if request.accepts("text/html"):
        return render(
            request,
            "result.html",
            context={
                'picked': picked
            }
        )
    elif request.accepts("application/json"):
        return HttpResponse(
            json.dumps({
                'picked': picked
            }),
            content_type="application/json"
        )
