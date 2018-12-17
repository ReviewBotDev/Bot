def do(account):
    import time
    import dossiers3.utils
    seconds = %(seconds)s
    recalTime = int(time.time() + seconds)
    dossier = dossiers3.utils.create(account._stats['dossier'])
    if dossier.ratingBattles.calibrationBattlesLeft == 0:
        dossier.ratingBattles.recalibrationStartTime = recalTime
        account._stats.setAccountDossier(dossier)
    else:
        ERROR('Account is not in Calibration/Recalibration state')
