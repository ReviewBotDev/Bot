def do(account):
    import time
    import datetime
    is_zero = int(%(total_seconds)s) == 0
    endTime = 0 if is_zero else int(time.time() + %(total_seconds)s)
    account._activatePremium(endTime, int(%(total_seconds)s))
