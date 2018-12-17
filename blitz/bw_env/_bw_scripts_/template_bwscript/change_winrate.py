def do(account):
    import dossiers3.utils
    a7x7_wins = %(a7x7_wins)s
    a7x7_battles = %(a7x7_battles)s
    rating_wins = %(rating_wins)s
    rating_battles = %(rating_battles)s
    tourn_wins = %(tourn_wins)s
    tourn_battles = %(tourn_battles)s
    dossier = dossiers3.utils.create(account._stats['dossier'])
    if a7x7_battles is not None:
        dossier.a7x7.battlesCount = a7x7_battles
    if a7x7_wins is not None:
        dossier.a7x7.wins = a7x7_wins
    if rating_wins is not None:
        dossier.ratingBattles.battlesCount = rating_battles
    if rating_battles is not None:
        dossier.ratingBattles.wins = rating_wins
    if tourn_battles is not None:
        dossier.tournament.battlesCount = tourn_battles
    if tourn_wins is not None:
        dossier.tournament.wins = tourn_wins
    account._stats.setAccountDossier(dossier)
    account.exportToWeb()