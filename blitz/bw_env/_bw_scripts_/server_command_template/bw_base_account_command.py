# Check, where we are executing script
PROCESS_ID = "%(process_id)s"
dbids_list = %(dbid_list)s
mailbox_dict = {}
dbids_on_another = []

def _onAccountCreated(_account, databaseID, wasActive):
    global mailbox
    if _account is not None:
        mailbox_dict[databaseID] = _account

# loaded content
# start
__INSERT__PAYLOAD__
# end

INFO('Create acc from DB... {}'.format(dbids_list))
for dbid in dbids_list:
    # call there because global mailbox is not working if this function calls inside other functions
    BigWorld.createBaseLocallyFromDBID('Account', dbid, _onAccountCreated)

INFO('Mailbox dict {}'.format(mailbox_dict))
not_loaded = set(dbids_list) - set(mailbox_dict.keys())
if not_loaded:
    ERROR('Following account can\'t be loaded {}. Maybe they are corrupted?'.format(not_loaded))

account_dict = {}
if mailbox_dict:
    for dbid, mailbox in mailbox_dict.items():
        try:
            account_dict[dbid] = BigWorld.entities[mailbox.id]
        except Exception as e:
            dbids_on_another.append(dbid)

INFO('Account dict {}'.format(account_dict))
for dbid, account in account_dict.items():
    try:
        do(account)
    except Exception as e:
        ERROR('[DO] {}'.format(e))

if dbids_on_another:
    INFO('[ENTITY NOT FOUND] Entity cannot be loaded {}, possible, it is on another base app. Current {}'.format(dbids_on_another, PROCESS_ID))
    INFO('[MISSED ENTITY] >{}<'.format(dbids_on_another))