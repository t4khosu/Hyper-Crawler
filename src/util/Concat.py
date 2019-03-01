def dictConcat(dict1, dict2):
    for k in dict2:
        if k not in dict1:
            dict1[k] = dict2[k]
        else:
            dict1[k] = dict1[k].union(dict2[k])
    return dict1