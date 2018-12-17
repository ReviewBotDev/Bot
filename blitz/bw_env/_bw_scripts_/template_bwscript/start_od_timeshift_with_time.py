def do(account):
    compDescr = %(compDescr)s
    slotLevel = %(slotLevel)s
    slotGroup = %(slotGroup)s
    seconds = %(seconds)s
    from account_helpers.VehiclesTimeShift import TIME_SHIFT_TYPE
    from account_helpers.OptionalDevicesSlots import SLOT_GROUP
    vehInvId = getVehInvID(account, compDescr)
    print vehInvId
    if not vehInvId > 0:
        WARNING('Can\'t change :( ')
        return
    account._inventory._vehTimeShifts.start(vehInvId=vehInvId, type=TIME_SHIFT_TYPE.DEVICE_SLOT, seconds=seconds, data = (slotLevel, slotGroup), price=('credits', 10))