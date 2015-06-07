__author__ = 'christopher'


def format_coor(coor):
    x = coor.split()[0]
    y = coor.split()[2]
    z = coor.split()[1]

    if float(x) > 0:
        x = x.replace("-", "") + " E"
    else:
         x = x.replace("-", "") + " W"
    if float(y) > 0:
        y =  y.replace("-", "") + " N"
    else:
        y = y.replace("-", "") + " S"

    formatted = y + " / " + x
    return formatted



def in_radius(obj1,obj2,radius):
    obj1x = obj1.split(" ")[0]
    obj1y = obj1.split(" ")[3]
    obj2x = obj2.split(" ")[0]
    obj2y = obj2.split(" ")[3]
    if float(obj2x)-radius <= float(obj1x) <= float(obj2x)+radius and float(obj2y)-radius <= float(obj1y) <= float(obj2y)+radius:
        return True
    else:
        return  False

