from cpuinfo import get_cpu_info
import psutil


class AIZCPU:
    def __init__(self):
        self.name = 'CPU'
        for key, value in get_cpu_info().items():
            if key == 'brand':
                self.name = value.replace('(R)','')
                self.name = self.name.replace('(TM)','')
                self.name = self.name.replace('CPU','')
                self.name = self.name.replace('  @ ','@')
                #self.cpu.name = self.cpu.name('(TM)','')
                break
        self.num_threads = psutil.cpu_count()
        self.num_cores = self.num_threads / 2
        self.memory = float(psutil.virtual_memory().total) / 1024.0 / 1024.0
        self.MAX_SAMPLES = 100
        self.cpu_usage = [0] * self.MAX_SAMPLES
        self.mem_usage = [0] * self.MAX_SAMPLES

    def Sample(self):
        cpuStat = psutil.cpu_percent()
        self.cpu_usage.append(cpuStat)
        self.cpu_usage = self.cpu_usage[1:len(self.cpu_usage)]


def GetCPUDevice():
    return AIZCPU()
