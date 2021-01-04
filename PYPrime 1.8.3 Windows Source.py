import math
import platform
import subprocess
import time
import os
import xml.etree.ElementTree as ET
import datetime
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import pyautogui

Runs = []


class UI:
    Title = f"{89 * '-'}\n{35 * ' '}PYPrime 1.8.3 HWBOT{35 * ' '}\n{89 * '-'}\n\n"
    Description = '\nThis is a strictly single core benchmark. Please close all applications in the background to get a reliable result\n'
    UserInput = f'{30 * "*"}\nPress ENTER to start benchmark'
    ExitPrompt = 'Press ENTER to exit'
    SubmitToHwbot = "To submit the score upload the .hwbot file located in the same folder as the benchmark,\nyou will find there a screenshot, upload that too if you want\n"

    def __init__(self, t):
        self.t = t
        self.score = round(self.t, 3)

    def Score(self):
        ScoreText = f"Average completion time: {self.score} s"
        hashes = "\n" + len(ScoreText) * "#" + "\n"
        print(hashes + ScoreText + hashes)

    def seconds(self):
        return self.score

    def __str__(self):
        return


memorytype = {
    0: 'DDR4 SDRAM',
    1: 'Other',
    2: 'DRAM',
    3: 'Synchronous DRAM',
    4: 'Cache DRAM',
    5: 'EDO RAM',
    6: 'EDRAM',
    7: 'VRAM',
    8: 'SRAM',
    9: 'RAM',
    10: 'ROM',
    11: 'Flash',
    12: 'EEPROM',
    13: 'FEPROM',
    14: 'EPROM',
    15: 'CDRAM',
    16: '3DRAM',
    17: 'SDRAM',
    18: 'SGRAM',
    19: 'RDRAM',
    20: 'DDR SD-RAM',
    21: 'DDR2 SDRAM',
    22: 'DDR2 FB-DIMM',
    24: 'DDR3 SDRAM',
    25: 'FBD2'
}

pr = 8000000

print(UI.Title)


def SocketCount():
    n = 0
    for i in subprocess.check_output('wmic cpu get "DeviceID" /format:list').strip().decode().split("\n"):
        if any(char.isdigit() for char in i):
            n += 1
    return n


def MemoryType():
    ram = int(subprocess.check_output("wmic memorychip get MemoryType /format:list").strip().decode().split('\r')[0][11:])
    if ram in memorytype:
        return memorytype[ram]


def Benchmark(limit):
    P = [2, 3]
    sieve = [False] * (limit + 1)
    for x in range(1, int(math.sqrt(limit)) + 1):
        for y in range(1, int(math.sqrt(limit)) + 1):
            n = 4 * x ** 2 + y ** 2
            if n <= limit and (n % 12 == 1 or n % 12 == 5): sieve[n] = not sieve[n]
            n = 3 * x ** 2 + y ** 2
            if n <= limit and n % 12 == 7: sieve[n] = not sieve[n]
            n = 3 * x ** 2 - y ** 2
            if x > y and n <= limit and n % 12 == 11: sieve[n] = not sieve[n]
    for x in range(5, int(math.sqrt(limit))):
        if sieve[x]:
            for y in range(x ** 2, limit + 1, x ** 2):
                sieve[y] = False
    for p in range(5, limit):
        if sieve[p]: P.append(p)

# Genetrate XML and encrypt it


def datafile(second):
    time = datetime.datetime.now()
    submission = ET.Element('submission')
    application = ET.Element('application')
    name = ET.Element('name')
    version = ET.Element('version')
    score = ET.Element('score')
    points = ET.Element('points')
    timestamp = ET.Element('timestamp')
    hardware = ET.Element('hardware')
    processor = ET.Element('processor')
    cname = ET.Element('name')
    count = ET.Element('amount')
    memory = ET.Element('memory')
    totalSize = ET.Element('totalSize')
    videocard = ET.Element('videocard')
    gname = ET.Element('name')
    motherboard = ET.Element('motherboard')
    mname = ET.Element('name')
    vendor = ET.Element('vendor')
    mvendor = ET.Element('vendor')
    # speed = ET.Element('speed')
    mtype = ET.Element('type')

    name.text = 'PYPrime'
    version.text = '1.7.3'
    points.text = str(second)
    timestamp.text = str(time)
    submission.set('xmlns:xsi', "http://www.w3.org/2001/XMLSchema-instance")
    submission.set('xmlns', "http://hwbot.org/submit/api?client=pyprime&clientVersion=[1.4.1, 1.5.2]")
    cname.text = str(subprocess.check_output('wmic cpu get name /format:list').strip().decode()[5:])
    count.text = str(SocketCount())
    totalSize.text = str(round(float(subprocess.check_output('wmic OS get TotalVisibleMemorySize /Value').strip().decode()[23:]) / 1048576, 1)) + 'GB'
    gname.text = str(subprocess.check_output("wmic path win32_VideoController get name /format:list").strip().decode().split('\r')[0][5:])
    mname.text = str(subprocess.check_output('wmic baseboard get product | MORE +1', shell=True).strip().decode())
    vendor.text = str(subprocess.check_output('wmic baseboard get Manufacturer | MORE +1', shell=True).strip().decode())
    mvendor.text = str(subprocess.check_output("wmic memorychip get Manufacturer /format:list").strip().decode().split('\r')[0][13:])
    # speed.text = str(subprocess.check_output("wmic memorychip get speed /format:list").strip().decode().split('\r')[0][6:])
    mtype.text = MemoryType()

    submission.append(application)
    application.append(name)
    application.append(version)
    submission.append(score)
    score.append(points)
    submission.append(timestamp)
    submission.append(hardware)
    hardware.append(processor)
    processor.append(cname)
    hardware.append(memory)
    memory.append(totalSize)
    hardware.append(videocard)
    videocard.append(gname)
    hardware.append(motherboard)
    motherboard.append(mname)
    motherboard.append(vendor)
    memory.append(mvendor)
    # memory.append(speed)
    memory.append(mtype)
    processor.append(count)

    file = open("Submission.hwbot", 'wb')

    key = b'16byelongkey'

    iv = b'16bytelongiv'

    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    file.write(cipher.encrypt(pad(ET.tostring(submission, xml_declaration=True), 16)))
    file.close()


def main():
    Start = time.perf_counter()
    Benchmark(pr)
    End = time.perf_counter()
    Runs.append(End - Start)


print(f'OS: {platform.system()} {platform.release()}, Build {platform.version()}\n')
print(f"CPU: {str(subprocess.check_output('wmic cpu get name /format:list').strip().decode()[5:])}\n")
print(f"Base CPU Clock Speed: {float(subprocess.check_output('wmic cpu get currentclockspeed').strip().decode()[22:]) / 1000} GHz\n")
print(f"Total RAM installed: {round(float(subprocess.check_output('wmic OS get TotalVisibleMemorySize /Value').strip().decode()[23:]) / 1048576, 1)} GB\n")

print(UI.Description)

input(UI.UserInput)

print(f"Calculating prime numbers up to {pr}\nThe time required is generally between 10 and 40 seconds...\n")

time.sleep(2)

for i in range(5):
    main()
    print(f"Completed run {i + 1}/5")

CurrentScore = UI(sum(Runs) / len(Runs))
CurrentScore.Score()
datafile(CurrentScore.seconds())

im = pyautogui.screenshot()
im.save('Screenshot.png')

print(UI.SubmitToHwbot)
input(UI.ExitPrompt)
