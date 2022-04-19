


def setUpGolfers(file):
    menu = readMenu(file)
    for key,val in menu:
        Golfer


def readMenu(getMenu):
    menu = {}
    if len(getMenu) <4:
        for line in getMenu:
            itemCode, description, price = line.strip().split(",")
            menu[itemCode] = [description, float(price)]
    return menu