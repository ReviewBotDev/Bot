def do(account):
    from items import ITEM_TYPES
    from items import vehicles
    stuff = account.bp['pdata']['inventory'][ITEM_TYPES.STUFF]
    stuff_with_name = {}
    for key, quantity in stuff.iteritems():
        name = vehicles.g_cache.stuff[key].name
        stuff_with_name[name] = quantity
    for name, quantity in stuff_with_name.iteritems():
        INFO('Remove {} - {}'.format(name, quantity))
        account._inventory.addStuff(name, -quantity)
