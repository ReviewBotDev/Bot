def do(account):
    import dossiers3.utils
    battles = %(battles)s
    dossier = dossiers3.utils.create(account._stats['dossier'])
    dossier.ratingBattles.calibrationBattlesLeft = battles
    account._stats.setAccountDossier(dossier)
    account.exportToWeb()