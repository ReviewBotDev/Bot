# some helpers utils
def ERROR(value):
    print '[ERROR] {0}'.format(value)

def WARNING(value):
    print '[WARNING] {0}'.format(value)

def INFO(value):
    print '[INFO] {0}'.format(value)

def LOG_CURRENT_EXCEPTION():
    from traceback import print_exc
    print_exc()

# loaded content
# start
__INSERT__PAYLOAD__
# end