def do(account):
    import time
    pdata = account.bp['pdata']
    invVehId = account._inventory.getVehicleInvID(%(compDescr)s)
    if invVehId:
        if invVehId in pdata['inventory'][1]['birthdays']:
            INFO(pdata['inventory'][1]['birthdays'][invVehId])
        else:
            INFO('Bithday didnt defined')
        pdata['inventory'][1]['birthdays'][invVehId] = int(time.time() - 7948800)
        INFO(pdata['inventory'][1]['birthdays'][invVehId])
    else:
        ERROR('Vehicle is\'t in inventory')