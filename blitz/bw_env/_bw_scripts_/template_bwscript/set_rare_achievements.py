def do(account):
    import dossiers3.utils
    ids = %(ids)s
    dossier = dossiers3.utils.create(account._stats['dossier'])
    dossier.ClearField("rareAchievements")
    unique_ids = list(set(ids))
    dossier.rareAchievements.extend(unique_ids)
    try:
        dossier.ClearField('templateAchievements')
        for i in unique_ids:
            dossier.templateAchievements[i] = ids.count(i)
    except Exception as e:
        INFO('Old version, templateAchievements is not found')
    account._stats.setAccountDossier(dossier)
    account.exportToWeb()