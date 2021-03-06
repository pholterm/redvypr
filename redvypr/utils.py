import sys
import logging

logging.basicConfig(stream=sys.stderr)
logger = logging.getLogger('redvypr')
logger.setLevel(logging.DEBUG)


def addrm_device_as_data_provider(devices,deviceprovider,devicereceiver,remove=False):
    """ Adds or remove deviceprovider as a datasource to devicereceiver
    Arguments:
    devices: list of dictionary including device and dataout lists
    deviceprovider: Device object 
    devicerecevier: Device object
    Returns: None if device could not been found, True for success, False if device was already connected
    """
    funcname = "addrm_device_as_data_provider():"
    logger.debug(funcname)
    # Find the device first in self.devices and save the index
    inddeviceprovider = -1
    inddevicereceiver = -1    
    for i,s in enumerate(devices):
        if(s['device'] == deviceprovider):
            inddeviceprovider = i
        if(s['device'] == devicereceiver):
            inddevicereceiver = i     

    if(inddeviceprovider < 0 or inddevicereceiver < 0):
        logger.debug(funcname + ': Could not find devices, doing nothing')
        return None

    datainqueue       = devices[inddevicereceiver]['device'].datainqueue
    datareceivernames = devices[inddevicereceiver]['device'].data_receiver
    dataoutlist       = devices[inddeviceprovider]['dataout']
    
    if(remove):
        if(datainqueue in dataoutlist):
            logger.debug(funcname + ': Removed device')
            dataoutlist.remove(datainqueue)
            # Remove the receiver name from the list
            devices[inddevicereceiver]['device'].data_receiver.remove(devices[inddeviceprovider]['device'].name)
            devices[inddeviceprovider]['device'].data_provider.remove(devices[inddevicereceiver]['device'].name)
            return True
        else:
            return False
    else:
        if(datainqueue in dataoutlist):
            return False
        else:
            logger.debug('addrm_device_as_data_provider():added device')
            dataoutlist.append(datainqueue)
            # Add the receiver and provider names to the device
            devices[inddevicereceiver]['device'].data_receiver.append(devices[inddeviceprovider]['device'].name)
            devices[inddeviceprovider]['device'].data_provider.append(devices[inddevicereceiver]['device'].name)
            return True


def get_data_receiving_devices(devices,device):
    """ Returns a list of devices that are receiving data from device
    """
    funcname = __name__ + 'get_data_receiving_devices():'
    devicesin = []
    # Find the device first in self.devices and save the index
    inddevice = -1
    for i,s in enumerate(devices):
        if(s['device'] == device):
            inddevice = i

    if(inddevice < 0):
        return None

    # Look if the devices are connected as input to the choosen device
    #  device -> data -> s in self.devices
    try:
        dataout = device.dataqueue
    except Exception as e:
        logger.debug(funcname + 'Device has no dataqueue for data output')
        return devicesin
    
    for dataout in devices[inddevice]['dataout']: # Loop through all dataoutqueues
        for s in devices:
            sen = s['device']
            datain = sen.datainqueue
            if True:
                if(dataout == datain):
                    devicesin.append(s)
            
    return devicesin

def get_data_providing_devices(devices,device):
    """ Returns a list of devices that are providing their data to device, i.e. device.datain is in the 'dataout' list of the device
    devices = list of dictionaries 
    """
    # Find the device first in self.devices and save the index
    inddevice = -1
    for i,s in enumerate(devices):
        if(s['device'] == device):
            inddevice = i

    if(inddevice < 0):
        return None
    
    devicesout = []
    # Look if the devices are connected as input to the chosen device
    # s in self.devices-> data -> device
    datain = device.datainqueue
    for s in devices:
        sen = s['device']
        try:
            for dataout in s['dataout']:
                if(dataout == datain):
                    devicesout.append(s)
        except Exception as e:
            print('dataqueue',s,device,str(e))
            
    return devicesout
