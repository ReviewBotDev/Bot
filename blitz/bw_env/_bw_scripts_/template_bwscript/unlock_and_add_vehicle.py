def do(account):
    l = %(nation_vehicle_list)s
    for p in l:
        INFO('Try add vehicle {}'.format(p))
        # nation_id, vehicle_id, name
        unlockAndAddVehicleNew(account, p[0], p[1], p[2])