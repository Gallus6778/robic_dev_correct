#!/usr/bin/python

from datetime import datetime
import asyncio, telnetlib3
import os
# from threading import Thread, Event
from multiprocessing import Process
import time

class Telnet_mss:

    """ Module pour l'extraction des informations de la SGSN """

    def __init__(self, msisdn, mss_ip):

        self.mss_ip = mss_ip
        self.username = "MSCBOT"
        self.password = "741852963"
        self.MSISDN = msisdn
        self.ZMVO = "ZMVO:MSISDN="
        self.Z = "Z;"
        self.ZZ = "ZZ;"
        self.mss_log_file = "complaints_call/storage_log/" + self.mss_ip +".txt"

        f1 = open(self.mss_log_file, "w")
        f1.close()

    @asyncio.coroutine
    def shell(self, reader, writer):
        while True:
            outp = yield from reader.read(65536)
            if not outp:
                break
            elif 'ENTER USERNAME' in outp:
                writer.write(self.username)
                writer.write('\n\r' + self.password + '\n\r'
                             + self.ZMVO + self.MSISDN + ':;\n\r'
                             + self.Z +'\n\r'
                             + self.ZZ + '\n\r')
            f1 = open(self.mss_log_file, "a")
            f1.write(outp)
            f1.close()

    def main(self):
        loop = None
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError as ex:
            if "There is no current event loop in thread" in str(ex):
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)

        coro = telnetlib3.open_connection(self.mss_ip, 23, shell=self.shell)
        reader, writer = loop.run_until_complete(coro)
        print('debut-fin')

        loop.run_until_complete(writer.protocol.waiter_closed)
        file_name = self.mss_log_file
        return file_name

if __name__ == '__main__':
    ip = "10.124.206.68"
    zmmi_zmmo_zmms = Telnet_mss('237663744490', mss_ip=ip)
    zmmi_zmmo_zmms.main()
    print("fin")