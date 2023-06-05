import read_roi

def isInPolygon(roi, x, y):
    xs = roi['x']
    ys = roi['y']
    count = min(len(xs), len(ys))
    if count == 0:
        return False
    n = 0
    lastx = xs[count - 1]
    lasty = ys[count - 1]
    for i in range(count):
        xi = xs[i]
        yi = ys[i]
        if lastx < xi:
            if lastx < x and x <= xi:
                t = (x - lastx) / (xi - lastx)
                yt = lasty + t * (yi - lasty)
                if y < yt:
                    n += 1
        elif xi < lastx:
            if xi < x and x <= lastx:
                t = (x - xi) / (lastx -xi)
                yt = yi + t * (lasty - yi)
                if y < yt:
                    n += 1
        lastx = xi
        lasty = yi
    return n % 2 == 1

def isInRect(roi, x, y):
    xmin = roi['left']
    xmax = xmin + roi['width']
    ymin = roi['top']
    ymax = ymin + roi['height']
    return xmin <= x and x <= xmax and ymin <= y and y <= ymax

def isInOval(roi, x, y):
    xd = (x - roi['left']) / roi['width'] - 0.5
    yd = (y - roi['top']) / roi['height'] - 0.5
    r2 = xd * xd + yd * yd
    if r2 <= 0.25:
        print('oval')
        return True
    return False

def isInFreeline(roi, x, y):
    print("don't know how to calculate freeline")
    return False

def isInPolyline(roi, x, y):
    print("don't know how to calculate polyline")
    return False

def isInFreehand(roi, x, y):
    if 'aspect_ratio' in roi:
        print("don't know how to calculate ellipse")
        # roi['ex1'], roi['ey1'], roi['ex2'], roi['ey2']
        # are these the largest extents of the ellipse?
        return False
    print("don't know how to calculate freehand that isn't an ellipse")
    return False

def isInTraced(roi, x, y):
    print("don't know how to calculate traced")
    return False

def belowCubicSegment(x, y, x0, y0, x1, y1, x2, y2, x3, y3):
    print("Cannot calculate cubic segments")
    return False

def belowQuadSegment(x, y, x0, y0, x1, y1, x2, y2):
    print("Cannot calculate quad segments")
    return False

def belowLinearSegment(x, y, x0, y0, x1, y1):
    if x0 == x1:
        return False
    elif x1 < x0:
        (x0, y0, x1, y1) = (x1, y1, x0, y0)
    if x < x0 or x1 <= x:
        return False
    t = (x - x0) / (x1 - x0)
    yt = y0 + t * (y1 - y0)
    return y <= yt

def belowLineSegment(x, y, lastx, lasty, seg):
    type = len(seg)
    if type == 2:
        return belowLinearSegment(x, y, lastx, lasty, *seg)
    elif type == 4:
        return belowQuadSegment(x, y, lastx, lasty, *seg)
    elif type == 6:
        return belowCubicSegment(x, y, lastx, lasty, *seg)
    print("did not understand path segment ({0})".format(seg))
    return False

def isInComposite(roi, x, y):
    if not isInRect(roi, x, y):
        return False
    paths = [p for p in roi['paths'] if 3 < len(p)]
    if len(paths) == 0:
        return False
    for path in paths:
        count = 0
        lastx = path[-1][-2]
        lasty = path[-1][-1]
        for segment in path:
            if belowLineSegment(x, y, lastx, lasty, segment):
                count += 1
            lastx = segment[-2]
            lasty = segment[-1]
        print(count)
        if count % 2 == 1:
            return True
    return False

isInFns = {
    'polygon': isInPolygon,
    'rectangle': isInRect,
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
