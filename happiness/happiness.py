from math import sqrt

def h1(v, D=128):
    # v: 0 -> 1
    xv = []
    yv = []
    r = D/3 - 2*v*D/3 # D/3 -> -D/3
    x0 = D/2
    y0 = D/2 - D*v/1.5
    for x in range(128):
        if abs(x - x0) <= abs(r):
            xv.append(x)
            dx2 =(x - x0)*(x - x0)
            y = round(sqrt(r*r - dx2) + y0)
            if v > 0.5:
                y = -y
            yv.append(y)
    return xv, yv