def do(account):
    compDescr = %(compDescr)s
    experience = %(experience)s
    account._syncData.statsW['vehTypeXP'][compDescr] = experience