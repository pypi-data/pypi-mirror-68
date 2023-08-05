from py3nvml.py3nvml import *


class AIZGPU_NVIDIA:
    def __init__(self, device_id):
        self.device = device_id

        self.name = nvmlDeviceGetName(self.device)
        self.MAX_SAMPLES = 100
        self.gpu_usage = [0] * 100
        self.vram_usage = [0] * self.MAX_SAMPLES
        self.vram_total = nvmlDeviceGetMemoryInfo(self.device).total
        self.pcie_bw = [0] * self.MAX_SAMPLES
        self.pcie_gen = nvmlDeviceGetMaxPcieLinkGeneration(self.device)
        self.pcie_width = nvmlDeviceGetMaxPcieLinkWidth(self.device)
        self.perf = 0
        self.Sample()

    def Sample(self):
        nv_util = nvmlDeviceGetUtilizationRates(self.device)
        self.gpu_usage.append(int(nv_util.gpu))
        self.gpu_usage = self.gpu_usage[1:len(self.gpu_usage)]

        self.vram_usage.append(nvmlDeviceGetMemoryInfo(self.device).used / float(self.vram_total) * 100)
        self.vram_usage = self.vram_usage[1:len(self.vram_usage)]

        pcie_usage = nvmlDeviceGetPcieThroughput(self.device, NVML_PCIE_UTIL_TX_BYTES) + nvmlDeviceGetPcieThroughput(self.device, NVML_PCIE_UTIL_RX_BYTES)
        pcie_usage = pcie_usage / (1024.0)
        #print(pcie_tx_usage)
        self.pcie_bw.append(pcie_usage)
        self.pcie_bw = self.pcie_bw[1:len(self.pcie_bw)]



def ListNVIDIAGPUDevices():

    try:
        nvmlInit()
        num_gpus = nvmlDeviceGetCount()
        gpus = []
        for i in range(0, num_gpus):
            gpus.append(AIZGPU_NVIDIA(nvmlDeviceGetHandleByIndex(i)))
    except:
        gpus = []
        
    return gpus
