from django.shortcuts import render
from geotute import settings
from geotute.roi import Rois
import json
from django.http import HttpResponse

def viewdata(template_name):
    """
    Produces a view that renders HTML with context given by the
    function's return value if HTML is accepted, or the function's
    return value rendered as a JSON object if JSON is accepted but
    HTML is not.
    """
    def decorator(fn):
        def inner(request):
            if request.accepts("text/html"):
                return render(
                    request,
                    template_name=template_name,
                    context=fn(request)
                )
            elif request.accepts("application/json"):
                return HttpResponse(
                    json.dumps(fn(request)),
                    content_type="application/json"
                )
        return inner
    return decorator

def grain(request):
    return render(request, "grain.html")

grain01_rois = Rois(settings.STATIC_ROOT / "tutorial" / "Grain01" / "RoiSet.zip")

@viewdata("result.html")
def result(request):
    return {
        "picked": grain01_rois.pick(
            float(request.GET['x']),
            float(request.GET['y'])
        )
    }
