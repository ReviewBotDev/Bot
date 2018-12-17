class NewVersionException(Exception):
    pass

def getVehInvID(account, compDescr):
    try:
        return account._inventory.getVehicleInvID(compDescr)
    except Exception as e:
        INFO(e)
        return -1

def unlockAndAddVehicleNew(account, nationID, vehID, vehicleName):
    try:
        import items
        from items import vehicles, avatar
        from AccountCommands import VEHICLE_SETTINGS_FLAG
        asTuple = (nationID, vehID)
        inv = account._inventory
        # Add slot and vehicle.
        account._syncData.statsW['slots'] = account._stats['slots'] + 1
        vehInvID, _ = inv.addVehicle(vehData=items.VehicleData(typeID=asTuple), withModules=True, crewLevel=avatar.MAX_MASTERY_LEVEL)
        vehData = account._inventory.getVehicleData(vehInvID)
        if vehData is None:
            INFO('Already exist {0}:{1} - {2}'.format(nationID, vehID, vehicleName))
            return
        serializedVehType = items.dumps(vehData.type)
        account._stats.unlock(serializedVehType)
        # Enable auto-repair, auto-load and auto-equip.
        setting = VEHICLE_SETTINGS_FLAG.DEFAULT_MASK
        inv.changeVehicleSetting(vehInvID, setting, True)
        return vehInvID
    except KeyError as e:
        ERROR('Vehicle {} can\'t be added '.format(vehicleName))
    except Exception as e:
        LOG_CURRENT_EXCEPTION()
        ERROR('Can\'t add vehicle {}. Error {}'.format(vehicleName, e))
        return -1

def removeVehicle(account, compDescr, name=None):
    try:
        vehInvId = getVehInvID(account, compDescr)
        if vehInvId > 0:
            INFO('Delete {0} (name {1})'.format(compDescr, name))
            account._inventory.removeVehicle( vehInvId )
    except Exception as e:
        INFO(e)
        return -1

