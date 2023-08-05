import os
import re
import numpy as np
from math import sin, pi
import sys
from aiz.gpu_amd import ListAMDGPUDevices
from aiz.gpu_nvidia import ListNVIDIAGPUDevices
from aiz.cpu import GetCPUDevice
from sparklines import sparklines


gpuDevices = []
cpuDevice = None

def DetectHardware():
    print('Detecting Hardware...')
    global gpuDevices
    global cpuDevice
    #GPU devices
    gpuDevices = ListAMDGPUDevices(False)
    gpuDevices.extend(ListNVIDIAGPUDevices())
    cpuDevice = GetCPUDevice()



# TODO Add more info
def PrintHardwareInfo():
    print('=======================================')
    num_gpus = len(gpuDevices)
    print('NUM_GPUS:' + str(num_gpus))
    for i in range(0,num_gpus):
        print('Name:%s' % gpuDevices[i].name)
        print('Vram:%5.2f MB' % (float(gpuDevices[i].vram_total) / (1024.0 * 1024.0)))
        print('Fan Usage:%f %%' % gpuDevices[i].fan)

    print('=======================================')
    print('CPU:%s' % cpuDevice.name)
    print('Cores:%d' % cpuDevice.num_cores)
    print('Threads:%d' % cpuDevice.num_threads)
    print('Mem:%5f MB' % cpuDevice.memory)


def DrawGraph(title, y_data):
    win.addch('\n')
    win.addstr(title)
    y=gpuDevices[i].gpu_usage
    line = sparklines(y,num_lines=2, minimum=0, maximum=100)
    win.addstr(line[0])
    win.addch('\n')
    win.addstr('%3d %%  ' % gpuDevices[i].gpu_usage[index])
    win.addstr(line[1])

def DisplayStats(win, curses):



    # Draw GPU Info
    for i in range(0, len(gpuDevices)):
        index = gpuDevices[i].MAX_SAMPLES-1
        gpuDevices[i].Sample()

        
        win.addstr('%s  TEMP:%3.0f C FAN: %2.0f %%' % (gpuDevices[i].name, gpuDevices[i].temp, gpuDevices[i].fan))
        
        
        #gpu usage
        win.addch('\n')
        win.addstr('USAGE  ')
        y=gpuDevices[i].gpu_usage
        line = sparklines(y,num_lines=2, minimum=0, maximum=100)
        win.addstr(line[0], curses.color_pair(1))
        win.addch('\n')
        win.addstr('%3d %%  ' % gpuDevices[i].gpu_usage[index])
        win.addstr(line[1], curses.color_pair(1))

        #vram usage
        #vram_size = 8 * 1024 * 1024 * 1024
        win.addch('\n')
        win.addch('\n')
        win.addstr('VRAM   ')
        y=gpuDevices[i].vram_usage
        line = sparklines(y,num_lines=2, minimum=0, maximum=100)
        win.addstr(line[0], curses.color_pair(1))
        win.addch('\n')
        win.addstr('%3d %%  ' % gpuDevices[i].vram_usage[index])
        win.addstr(line[1], curses.color_pair(1))
 
        
        #pcie bandwidth
        win.addch('\n')
        win.addch('\n')
        win.addstr('PCIE    ')
        y=gpuDevices[i].pcie_bw
        line = sparklines(y,num_lines=2, minimum=0, maximum=100)
        win.addstr(line[0], curses.color_pair(1))
        win.addch('\n')
        win.addstr('%3d MB/s' % gpuDevices[i].pcie_bw[index])
        win.addstr(line[1], curses.color_pair(1))

        win.addch('\n')
        
    #Draw CPU stats
    win.addch('\n')
    win.addch('\n')
    win.addstr('%s' % cpuDevice.name)
    win.addch('\n')
    cpuDevice.Sample()

    index = cpuDevice.MAX_SAMPLES-1
        
    #cpu usage
    win.addstr('USAGE  ')
    y=cpuDevice.cpu_usage
    line = sparklines(y,num_lines=2, minimum=0, maximum=100)
    win.addstr(line[0], curses.color_pair(1))
    win.addch('\n')
    win.addstr('%3d %%  ' % cpuDevice.cpu_usage[index])
    win.addstr(line[1], curses.color_pair(1))
    

    
