def do(account):
    camo_id = %(camo_id)s
    unlocks = account._syncData.unlocksW['fullUnlocks']
    unlocks.add(camo_id)