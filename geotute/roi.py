import read_roi

def isInPolygon(roi, x, y):
    print('polygon: not implemented')
    return False

def isInRect(roi, x, y):
    xmin = roi['left']
    xmax = xmin + roi['width']
    ymin = roi['top']
    ymax = ymin + roi['height']
    return xmin <= x and x <= xmax and ymin <= y and y <= ymax

def isInOval(roi, x, y):
    xd = (x - roi['left']) / roi['width'] - 0.5
    yd = (y - roi['top']) / roi['height'] - 0.5
    print('oval: {0}, {1}'.format(xd, yd))
    r2 = xd * xd + yd * yd
    return r2 <= 0.25

def isInFreeline(roi, x, y):
    print("don't know how to calculate freeline")
    return False

def isInPolyline(roi, x, y):
    print("don't know how to calculate polyline")
    return False

def isInFreehand(roi, x, y):
    print("don't know how to calculate freehand")
    return False

def isInTraced(roi, x, y):
    print("don't know how to calculate traced")
    return False

def belowCubicSegment(x, y, p0, p1, p2, p3, p4, p5):
    print("Cannot calculate cubic segments")
    return False

def belowQuadSegment(x, y, p0, p1, p2, p3):
    print("Cannot calculate quad segments")
    return False

def belowLinearSegment(x, y, p0, p1):
    [x0, y0] = p0
    [x1, y1] = p1
    if x0 == x1:
        return False
    elif x1 < x0:
        [x0, y0] = p0
        [x1, y1] = p1
    if x < x0 or x1 <= x:
        return False
    t = (x - x0) / (x1 - x0)
    yt = y0 + t * (y1 - y0)
    return y <= yt

def belowLineSegment(seg, x, y):
    type = len(seg)
    if type == 2:
        return belowLinearSegment(x, y, *seg)
    elif type == 4:
        return belowQuadSegment(x, y, *seg)
    elif type == 6:
        return belowCubicSegment(x, y, *seg)
    print("did not understand path segment")
    return False

def isInComposite(roi, x, y):
    if not isInRect(roi, x, y):
        return False
    count = 0
    for segment in roi['paths']:
        if belowLineSegment(segment, x, y):
            count += 1
    return count % 2 == 1

isInFns = {
    'polygon': isInPolygon,
    'rect': isInRect,
    'oval': isInOval,
    'line': isInFreeline,
    'polyline': isInPolyline,
    'freehand': isInFreehand,
    'traced': isInTraced,
    'composite': isInComposite,
}

class Rois:
    def __init__(self, filename) -> None:
        self.name2roi = read_roi.read_roi_zip(filename)
    def pick(self, x, y):
        rs = []
        for name, roi in self.name2roi.items():
            isIn = isInFns.get(roi['type'])
            if isIn is None:
                print("ROI type '{0}' not understood".format(roi['type']))
            elif isIn(roi, x, y):
                rs.append(name)
        return rs
