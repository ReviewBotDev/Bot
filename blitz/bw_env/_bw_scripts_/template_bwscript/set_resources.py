def do(account):
    gold = %(gold)s
    credits = %(credits)s
    freeXP = %(freeXP)s
    if gold is not None:
        account._syncData.statsW['gold'] = gold
    if credits is not None:
        account._syncData.statsW['credits'] = credits
    if freeXP is not None:
        account._syncData.statsW['freeXP'] = freeXP