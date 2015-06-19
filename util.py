__author__ = 'christopher'


def format_coor(coor):      #used to go from 100 64 100 format to 100 S / 100 N format
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

def convert_coor(coor):  #used to go from 100 S / 100 E format to 100 54 100 format
    split_coor = coor.split()
    x = split_coor[3]
    y = split_coor[0]

    if split_coor[1] == "S":
        y = "-" + y

    if split_coor[4] == "W":
        x + "-" + x
    converted = x + " " + "64" + " " + y
    return converted




def in_radius(obj1,obj2,radius):
    if is_coor_formatted(obj1):
        obj1 = convert_coor(obj1)
    if is_coor_formatted(obj2):
        obj2 = convert_coor(obj2)
    print obj2
    obj1x = obj1.split(" ")[0]
    obj1y = obj1.split(" ")[2]
    obj2x = obj2.split(" ")[0]
    obj2y = obj2.split(" ")[2]
    if float(obj2x) - int(radius) <= float(obj1x) <= float(obj2x) + int(radius) and float(obj2y) - int(radius) <= float(obj1y) <= float(obj2y)+ int(radius):
        return True
    else:
        return  False

def is_coor_formatted(coor):
    if "/" in coor:
        return True
    else:
        return False