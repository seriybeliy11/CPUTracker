import psutil
from time import sleep
from threading import Thread, Lock
import platform

CPU_COUNT = psutil.cpu_count()
pc_info = f'{platform.processor()}'
cpu_freq = f'{psutil.cpu_freq(percpu=True)}'
cpu_qnt = f'{CPU_COUNT} cores'
memory = f'{psutil.virtual_memory()}'
disk_info = f'{psutil.disk_partitions()}'
sent_packs = f'{psutil.net_io_counters(pernic=False, nowrap=True).packets_sent} packets'


cpu = [[None]*100 for _ in range(CPU_COUNT)]
ram = [[None]*100 for _ in range(2)]
disks = [[None]*100 for _ in range(2)]
net_stat = [[None]*100 for _ in range(2)]


def update_msts():
    _cpu = psutil.cpu_percent(percpu=True)

    for i in range(CPU_COUNT):
        cpu[i][:-1] = cpu[i][1:]
        cpu[i][-1] = _cpu[i]

    _ram = psutil.virtual_memory().percent
    _swap = psutil.swap_memory().percent
    disk_r = psutil.disk_io_counters(perdisk=True)['PhysicalDrive0'].read_bytes
    disk_w = psutil.disk_io_counters(perdisk=True)['PhysicalDrive0'].write_bytes
    net_sent = psutil.net_io_counters(pernic=False, nowrap=True).bytes_sent
    net_recv = psutil.net_io_counters(pernic=False, nowrap=True).bytes_recv
    
    ram[0][:-1] = ram[0][1:]
    ram[0][-1] = _ram  
    ram[1][:-1] = ram[1][1:]    
    ram[1][-1] = _swap 

    disks[0][:-1] = disks[0][1:]
    disks[0][-1] = disk_r
    disks[1][:-1] = disks[1][1:]
    disks[1][-1] = disk_w
   
    net_stat[0][:-1] = net_stat[0][1:]
    net_stat[0][-1] = net_sent  
    net_stat[1][:-1] = net_stat[1][1:]    
    net_stat[1][-1] = net_recv








    