#!/usr/bin/env python

import os
import json
import subprocess


class Scanner():

    formats = ['pnm','tiff','png','jpeg']
    devices = {}
    active_device = ""
    file_format = ""
    file_path = ""

    def available_devices(self, *args, **kwargs):
        with open('.devices.json', 'r+') as f:
            try:
                self.devices = json.load(f)
            except json.JSONDecodeError:
                print("DUPA")
                devices_list = []
                devices_list.append(subprocess.check_output('scanimage -f %d', shell=True).decode('ascii'))
                self.devices = { str(i + 1) : devices_list[i] for i in range(0, len(devices_list)) }
                json.dump(self.devices, f)
            f.close()

    def print_devices(self, *args, **kwargs):
        for number, device in self.devices.items():
            print(f"  {number}. {device}\n")

    def scan(self, *args, **kwargs):
        os.system(f'scanimage -d {self.active_device} --format={self.file_format} -o {self.file_path} -p')

    def menu(self, *args, **kwargs):
        self.available_devices()
        print(f"Wybierz urzadzenie z listy:")
        self.print_devices()
        self.active_device = self.devices.get(input())
        print(f"Podaj format pliku do zapisania (dostepne formaty: {self.formats}:")
        self.file_format = input()
        print(f"Podaj sciezke pliku do zapisu:")
        self.file_path = input()
        if not self.file_path.endswith(tuple(self.formats)):
            self.file_path += "." + self.file_format
        self.scan()

scan = Scanner()
scan.menu()