from django.shortcuts import render
from geotute import settings
from geotute.roi import Rois

def grain(request):
    return render(request, "grain.html")

def result(request):
    rois = Rois(settings.STATIC_ROOT / "tutorial" / "Grain01" / "RoiSet.zip")
    return render(
        request,
        "result.html",
        context={
            'hello': 'hello there',
            'picked': rois.pick(
                float(request.GET['x']),
                float(request.GET['y'])
            )
        }
    )
