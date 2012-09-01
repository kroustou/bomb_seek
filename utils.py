def neighbours((x, y), including_self=False):
    if including_self:
        return [(x + 1, y), (x, y + 1), (x - 1, y), (x, y - 1)]
    else:
        return [(x + 1, y), (x, y + 1), (x - 1, y), (x, y - 1), (x, y)]
