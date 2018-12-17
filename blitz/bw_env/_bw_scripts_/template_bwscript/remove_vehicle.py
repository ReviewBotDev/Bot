def do(account):
    l = %(vehicles_list)s
    for v in l:
        removeVehicle(account, v[0], v[1])