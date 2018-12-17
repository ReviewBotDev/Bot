def do(account):
    stuffs = %(stuffs)s
    for name, quantity in stuffs:
        account._inventory.addStuff(name, quantity)