#=============================================
# Functions copied or adapted from rocm-smi
# https://github.com/RadeonOpenCompute/ROC-smi
# Copyright (c) 2014-2019 Advanced Micro Devices, Inc. All rights reserved.
#=============================================

import os
import re
import logging




drmprefix = '/sys/class/drm'
hwmonprefix = '/sys/class/hwmon'
debugprefix = '/sys/kernel/debug/dri'
moduleprefix = '/sys/module'
kfdprefix = '/sys/class/kfd/kfd'


# Supported firmware blocks
validFwBlocks = {'vce', 'uvd', 'mc', 'me', 'pfp',
'ce', 'rlc', 'rlc_srlc', 'rlc_srlg', 'rlc_srls',
'mec', 'mec2', 'sos', 'asd', 'ta_ras', 'ta_xgmi',
'smc', 'sdma', 'sdma2', 'vcn', 'dmcu'}

valuePaths = {
    'id' : {'prefix' : drmprefix, 'filepath' : 'device', 'needsparse' : True},
    'sub_id' : {'prefix' : drmprefix, 'filepath' : 'subsystem_device', 'needsparse' : False},
    'vbios' : {'prefix' : drmprefix, 'filepath' : 'vbios_version', 'needsparse' : False},
    'perf' : {'prefix' : drmprefix, 'filepath' : 'power_dpm_force_performance_level', 'needsparse' : False},
    'sclk_od' : {'prefix' : drmprefix, 'filepath' : 'pp_sclk_od', 'needsparse' : False},
    'mclk_od' : {'prefix' : drmprefix, 'filepath' : 'pp_mclk_od', 'needsparse' : False},
    'dcefclk' : {'prefix' : drmprefix, 'filepath' : 'pp_dpm_dcefclk', 'needsparse' : False},
    'fclk' : {'prefix' : drmprefix, 'filepath' : 'pp_dpm_fclk', 'needsparse' : False},
    'mclk' : {'prefix' : drmprefix, 'filepath' : 'pp_dpm_mclk', 'needsparse' : False},
    'pcie' : {'prefix' : drmprefix, 'filepath' : 'pp_dpm_pcie', 'needsparse' : False},
    'sclk' : {'prefix' : drmprefix, 'filepath' : 'pp_dpm_sclk', 'needsparse' : False},
    'socclk' : {'prefix' : drmprefix, 'filepath' : 'pp_dpm_socclk', 'needsparse' : False},
    'clk_voltage' : {'prefix' : drmprefix, 'filepath' : 'pp_od_clk_voltage', 'needsparse' : False},
    'voltage' : {'prefix' : hwmonprefix, 'filepath' : 'in0_input', 'needsparse' : False},
    'profile' : {'prefix' : drmprefix, 'filepath' : 'pp_power_profile_mode', 'needsparse' : False},
    'use' : {'prefix' : drmprefix, 'filepath' : 'gpu_busy_percent', 'needsparse' : False},
    'use_mem' : {'prefix' : drmprefix, 'filepath' : 'mem_busy_percent', 'needsparse' : False},
    'pcie_bw' : {'prefix' : drmprefix, 'filepath' : 'pcie_bw', 'needsparse' : False},
    'replay_count' : {'prefix' : drmprefix, 'filepath' : 'pcie_replay_count', 'needsparse' : False},
    'unique_id' : {'prefix' : drmprefix, 'filepath' : 'unique_id', 'needsparse' : False},
    'serial' : {'prefix' : drmprefix, 'filepath' : 'serial_number', 'needsparse' : False},
    'vendor' : {'prefix' : drmprefix, 'filepath' : 'vendor', 'needsparse' : False},
    'sub_vendor' : {'prefix' : drmprefix, 'filepath' : 'subsystem_vendor', 'needsparse' : False},
    'fan' : {'prefix' : hwmonprefix, 'filepath' : 'pwm1', 'needsparse' : False},
    'fanmax' : {'prefix' : hwmonprefix, 'filepath' : 'pwm1_max', 'needsparse' : False},
    'fanmode' : {'prefix' : hwmonprefix, 'filepath' : 'pwm1_enable', 'needsparse' : False},
    'temp1' : {'prefix' : hwmonprefix, 'filepath' : 'temp1_input', 'needsparse' : True},
    'temp1_label' : {'prefix' : hwmonprefix, 'filepath' : 'temp1_label', 'needsparse' : False},
    'temp2' : {'prefix' : hwmonprefix, 'filepath' : 'temp2_input', 'needsparse' : True},
    'temp2_label' : {'prefix' : hwmonprefix, 'filepath' : 'temp2_label', 'needsparse' : False},
    'temp3' : {'prefix' : hwmonprefix, 'filepath' : 'temp3_input', 'needsparse' : True},
    'temp3_label' : {'prefix' : hwmonprefix, 'filepath' : 'temp3_label', 'needsparse' : False},
    'power' : {'prefix' : hwmonprefix, 'filepath' : 'power1_average', 'needsparse' : True},
    'power_cap' : {'prefix' : hwmonprefix, 'filepath' : 'power1_cap', 'needsparse' : False},
    'power_cap_max' : {'prefix' : hwmonprefix, 'filepath' : 'power1_cap_max', 'needsparse' : False},
    'power_cap_min' : {'prefix' : hwmonprefix, 'filepath' : 'power1_cap_min', 'needsparse' : False},
    'dpm_state' : {'prefix' : drmprefix, 'filepath' : 'power_dpm_state', 'needsparse' : False},
    'vram_used' : {'prefix' : drmprefix, 'filepath' : 'mem_info_vram_used', 'needsparse' : False},
    'vram_total' : {'prefix' : drmprefix, 'filepath' : 'mem_info_vram_total', 'needsparse' : False},
    'vis_vram_used' : {'prefix' : drmprefix, 'filepath' : 'mem_info_vis_vram_used', 'needsparse' : False},
    'vis_vram_total' : {'prefix' : drmprefix, 'filepath' : 'mem_info_vis_vram_total', 'needsparse' : False},
    'vram_vendor' : {'prefix' : drmprefix, 'filepath' : 'mem_info_vram_vendor', 'needsparse' : False},
    'gtt_used' : {'prefix' : drmprefix, 'filepath' : 'mem_info_gtt_used', 'needsparse' : False},
    'gtt_total' : {'prefix' : drmprefix, 'filepath' : 'mem_info_gtt_total', 'needsparse' : False},
    'ras_gfx' : {'prefix' : drmprefix, 'filepath' : 'ras/gfx_err_count', 'needsparse' : False},
    'ras_sdma' : {'prefix' : drmprefix, 'filepath' : 'ras/sdma_err_count', 'needsparse' : False},
    'ras_umc' : {'prefix' : drmprefix, 'filepath' : 'ras/umc_err_count', 'needsparse' : False},
    'ras_mmhub' : {'prefix' : drmprefix, 'filepath' : 'ras/mmhub_err_count', 'needsparse' : False},
    'ras_athub' : {'prefix' : drmprefix, 'filepath' : 'ras/athub_err_count', 'needsparse' : False},
    'ras_sdma' : {'prefix' : drmprefix, 'filepath' : 'ras/sdma_err_count', 'needsparse' : False},
    'ras_pcie_bif' : {'prefix' : drmprefix, 'filepath' : 'ras/pcie_bif_err_count', 'needsparse' : False},
    'ras_hdp' : {'prefix' : drmprefix, 'filepath' : 'ras/hdp_err_count', 'needsparse' : False},
    'ras_xgmi_wafl' : {'prefix' : drmprefix, 'filepath' : 'ras/xgmi_wafl_err_count', 'needsparse' : False},
    'ras_df' : {'prefix' : drmprefix, 'filepath' : 'ras/df_err_count', 'needsparse' : False},
    'ras_smn' : {'prefix' : drmprefix, 'filepath' : 'ras/smn_err_count', 'needsparse' : False},
    'ras_sem' : {'prefix' : drmprefix, 'filepath' : 'ras/sem_err_count', 'needsparse' : False},
    'ras_mp0' : {'prefix' : drmprefix, 'filepath' : 'ras/mp0_err_count', 'needsparse' : False},
    'ras_mp1' : {'prefix' : drmprefix, 'filepath' : 'ras/mp1_err_count', 'needsparse' : False},
    'ras_fuse' : {'prefix' : drmprefix, 'filepath' : 'ras/fuse_err_count', 'needsparse' : False},

    'xgmi_err' : {'prefix' : drmprefix, 'filepath' : 'xgmi_error', 'needsparse' : False},
    'ras_features' : {'prefix' : drmprefix, 'filepath' : 'ras/features', 'needsparse' : True},
    'bad_pages' : {'prefix' : drmprefix, 'filepath' : 'ras/gpu_vram_bad_pages', 'needsparse' : False},
    'ras_ctrl' : {'prefix' : debugprefix, 'filepath' : 'ras/ras_ctrl', 'needsparse' : False},
    'gpu_reset' : {'prefix' : debugprefix, 'filepath' : 'amdgpu_gpu_recover', 'needsparse' : False},
    'driver' : {'prefix' : moduleprefix, 'filepath' : 'amdgpu/version', 'needsparse' : False}
}

# These are the valid memory info types that are currently supported
# vram
# vis_vram (Visible VRAM)
# gtt
validMemTypes = ['vram', 'vis_vram', 'gtt']

for block in validFwBlocks:
    valuePaths['%s_fw_version' % block] = {'prefix' : drmprefix, 'filepath' : 'fw_version/%s_fw_version' % block, 'needsparse' : False}
#SMC has different formatting for its version
valuePaths['smc_fw_version']['needsparse'] = True

def listAmdHwMons():
    """Return a list of AMD HW Monitors."""
    hwmons = []

    for mon in os.listdir(hwmonprefix):
        tempname = os.path.join(hwmonprefix, mon, 'name')
        if os.path.isfile(tempname):
            with open(tempname, 'r') as tempmon:
                drivername = tempmon.read().rstrip('\n')
                if drivername in ['radeon', 'amdgpu']:
                    hwmons.append(os.path.join(hwmonprefix, mon))
    return hwmons

def getHwmonFromDevice(device):
    """ Return the corresponding HW Monitor for a specified GPU device.

    Parameters:
    device -- DRM device identifier
    """
    drmdev = os.path.realpath(os.path.join(drmprefix, device, 'device'))
    for hwmon in listAmdHwMons():
        if os.path.realpath(os.path.join(hwmon, 'device')) == drmdev:
            return hwmon
    return None

def getFilePath(device, key):
    """ Return the filepath for a specific device and key

    Parameters:
    device -- Device whose filepath will be returned
    key -- [$valuePaths.keys()] The sysfs path to return
    """
    if key not in valuePaths.keys():
        print('Cannot get file path for key %s' % key)
        logging.debug('Key %s not present in valuePaths map' % key)
        return None
    pathDict = valuePaths[key]
    fileValue = ''

    if pathDict['prefix'] == hwmonprefix:
        # HW Monitor values have a different path structure
        if not getHwmonFromDevice(device):
            logging.warning('GPU[%s]\t: No corresponding HW Monitor found', parseDeviceName(device))
            return None
        filePath = os.path.join(getHwmonFromDevice(device), pathDict['filepath'])
    elif pathDict['prefix'] == debugprefix:
        # Kernel DebugFS values have a different path structure
        filePath = os.path.join(pathDict['prefix'], parseDeviceName(device), pathDict['filepath'])
    elif pathDict['prefix'] == drmprefix:
        filePath = os.path.join(pathDict['prefix'], device, 'device', pathDict['filepath'])
    else:
        # Otherwise, just join the 2 fields without any parsing
        filePath = os.path.join(pathDict['prefix'], pathDict['filepath'])

    if not os.path.isfile(filePath):
        return None
    return filePath

def getSysfsValue(device, key):
    """ Return the desired SysFS value for a specified device

    Parameters:
    device -- DRM device identifier
    key -- [$valuePaths.keys()] Key referencing desired SysFS file
    """
    filePath = getFilePath(device, key)
    pathDict = valuePaths[key]

    if not filePath:
        return None
    # Use try since some sysfs files like power1_average will throw -EINVAL
    # instead of giving something useful.
    try:
        with open(filePath, 'r') as fileContents:
            fileValue = fileContents.read().rstrip('\n')
    except:
        logging.warning('GPU[%s]\t: Unable to read %s', parseDeviceName(device), filePath)
        return None

    # Some sysfs files aren't a single line of text
    if pathDict['needsparse']:
        fileValue = parseSysfsValue(key, fileValue)

    if fileValue == '':
        logging.debug('GPU[%s]\t: Empty SysFS value: %s', parseDeviceName(device), key)

    return fileValue

def parseSysfsValue(key, value):
    """ Parse the sysfs value string
    Parameters:
    key -- [$valuePaths.keys()] Key referencing desired SysFS file
    value -- SysFS value to parse
    Some SysFS files aren't a single line/string, so we need to parse it
    to get the desired value
    """
    if key == 'id':
        # Strip the 0x prefix
        return value[2:]
    if re.match(r'temp[0-9]+', key):
        # Convert from millidegrees
        return int(value) / 1000
    if key == 'power':
        # power1_average returns the value in microwatts. However, if power is not
        # available, it will return "Invalid Argument"
        if value.isdigit():
            return float(value) / 1000 / 1000
    # ras_reatures has "feature mask: 0x%x" as the first line, so get the bitfield out
    if key == 'ras_features':
        return int((value.split('\n')[0]).split(' ')[-1], 16)
    # The smc_fw_version sysfs file stores the version as a hex value like 0x12345678
    # but is parsed as int(0x12).int(0x34).int(0x56).int(0x78)
    if key == 'smc_fw_version':
        return (str('%02d' % int((value[2:4]), 16)) + '.' + str('%02d' % int((value[4:6]), 16)) + '.' +
                str('%02d' % int((value[6:8]), 16)) + '.' + str('%02d' % int((value[8:10]), 16)))

    return ''


def parseDeviceNumber(deviceNum):
    """ Parse the device number, returning the format of card#
    Parameters:
    deviceNum -- DRM device number to parse
    """
    return 'card' + str(deviceNum)


def parseDeviceName(deviceName):
    """ Parse the device name, which is of the format card#.
    Parameters:
    deviceName -- DRM device name to parse
    """
    return deviceName[4:]

def isAmdDevice(device):
    """ Return whether the specified device is an AMD device or not
    Parameters:
    device -- DRM device identifier
    """
    vid = getSysfsValue(device, 'vendor')
    if vid == '0x1002':
        return True
    return False

def getMemInfo(device, memType):
    """ Return the specified memory usage for the specified device

    Parameters:
    device -- DRM device identifier
    type -- [vram|vis_vram|gtt] Memory type to return
    """
    if memType not in validMemTypes:
        logging.error('Invalid memory type %s', memType)
        return (None, None)
    memUsed = getSysfsValue(device, '%s_used' % memType)
    memTotal = getSysfsValue(device, '%s_total' % memType)
    if memUsed == None:
        logging.debug('Unable to get %s_used' % memType)
    elif memTotal == None:
        logging.debug('Unable to get %s_total' % memType)
    return (memUsed, memTotal)


class AIZGPU_AMD:
    def __init__(self, device_id):
        self.device = device_id
        self.id = getSysfsValue(self.device, 'id')
        self.name = device_id # TODO FIX name
        self.MAX_SAMPLES = 100
        self.gpu_usage = [0] * self.MAX_SAMPLES
        self.vram_usage = [0] * self.MAX_SAMPLES
        self.vram_total = 0
        self.pcie_bw = [0] * self.MAX_SAMPLES
        self.perf = 0
        self.fan = 0
        self.fanmax = 0
        self.temp = 0
        self.Sample()

    def GetName(self):
        return self.name

    def Sample(self):
        self.perf = getSysfsValue(self.device, 'perf')
        self.fan = getSysfsValue(self.device, 'fan')
        self.temp = getSysfsValue(self.device, 'fan')

        # GPU usage
        self.gpu_usage.append(int(getSysfsValue(self.device, 'use')))
        self.gpu_usage = self.gpu_usage[1:len(self.gpu_usage)]

        # VRAM usage
        memInfo = getMemInfo(self.device, 'vram')
        mem_use = '% 3.0f' % (100*(float(memInfo[0])/float(memInfo[1])))
        self.vram_total = memInfo[1]
        self.vram_usage.append(int(mem_use))
        self.vram_usage = self.vram_usage[1:len(self.vram_usage)]

        # PCIE usage
        fsvals = getSysfsValue(self.device, 'pcie_bw')
        # The sysfs file returns 3 integers: bytes-received, bytes-sent, maxsize
        # Multiply the number of packets by the maxsize to estimate the PCIe usage
        received = int(fsvals.split()[0])
        sent = int(fsvals.split()[1])
        mps = int(fsvals.split()[2])
        # Use 1024.0 to ensure that the result is a float and not integer division
        bw = ((received + sent) * mps) / 1024.0 / 1024.0
        self.pcie_bw.append(float(bw))
        self.pcie_bw = self.pcie_bw[1:len(self.pcie_bw)]

        # Fan speed %
        fanLevel = getSysfsValue(self.device, 'fan')
        self.fanMax = getSysfsValue(self.device, 'fanmax')
        if fanLevel and self.fanMax:
            self.fan = (float(fanLevel) / float(self.fanMax)) * 100
            #self.fan = fanLevel

        # Temperature
        self.temp = getSysfsValue(self.device, 'temp1')


def ListAMDGPUDevices(showall):
    """ Return a list of GPU devices.
    Parameters:
    showall -- [True|False] Show all devices, not just AMD devices
    """

    if not os.path.isdir(drmprefix) or not os.listdir(drmprefix):
        print('Unable to get devices, /sys/class/drm is empty or missing')
        return None

    devicelist = [device for device in os.listdir(drmprefix) if re.match(r'^card\d+$', device) and (isAmdDevice(device) or showall)]
    devicelist_sorted = sorted(devicelist, key=lambda x: int(x.partition('card')[2]))

    gpus = []
    for i in range(0, len(devicelist_sorted)):
        gpus.append(AIZGPU_AMD(devicelist_sorted[i]))

    return gpus




    

        