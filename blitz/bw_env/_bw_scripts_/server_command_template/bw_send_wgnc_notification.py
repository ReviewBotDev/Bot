def do(account):
    n = '%(notification)s'
    account._getClientMailbox().receiveNotification(n)