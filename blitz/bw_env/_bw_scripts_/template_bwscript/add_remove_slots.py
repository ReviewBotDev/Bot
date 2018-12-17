def do(account):
    slots = %(slots)s
    pdata = account.bp['pdata']
    busy_slots = len(pdata['inventory'][1]['serialized'].keys())
    if slots < 0 and (account._stats.getSlotsCount() - busy_slots) < abs(slots):
        ERROR("Not enough slots to deduct")
    else:
        account._stats.addSlot(slots)