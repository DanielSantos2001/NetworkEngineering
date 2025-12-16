#!/usr/bin/env python3
from netmiko import ConnectHandler
import csv
import sys

devices_file = sys.argv[1] if len(sys.argv) > 1 else 'devices_list.txt'

def read_devices(path):
    devs = []
    with open(path) as f:
        for line in f:
            if line.strip() and not line.startswith('#'):
                host,ip,username,password,device_type = line.strip().split(',')
                devs.append({
                    'host': host,
                    'ip': ip,
                    'username': username,
                    'password': password,
                    'device_type': device_type
                })
    return devs

def get_interfaces(dev):
    conn = ConnectHandler(host=dev['ip'], username=dev['username'],
                          password=dev['password'], device_type=dev['device_type'])
    output = conn.send_command('show interfaces status')
    conn.disconnect()
    return output

def parse_and_write(dev, output):
    # simple CSV write, adapt parsing per vendor
    with open(f"{dev['host']}_interfaces.csv","w",newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['raw_output'])
        writer.writerow([output])

if __name__ == '__main__':
    devices = read_devices(devices_file)
    for d in devices:
        out = get_interfaces(d)
        parse_and_write(d,out)
