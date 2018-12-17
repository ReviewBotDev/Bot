def do(account):
    import dossiers3.utils
    mmr = %(mmr)s
    previousMMR = %(previousMMR)s
    clearMMR = %(clearMMR)s
    dossier = dossiers3.utils.create(account._stats['dossier'])
    dossier.ratingBattles.mmr = mmr
    dossier.ratingBattles.prevMmr = previousMMR
    if clearMMR:
        dossier.ClearField('ratingBattles')
    account._stats.setAccountDossier(dossier)
    account.exportToWeb()