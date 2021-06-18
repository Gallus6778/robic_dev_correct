#!/usr/bin/python

from datetime import datetime
import asyncio, telnetlib3
import os

class Telnet_sgsn:

    def __init__(self, msisdn):
        self.server_ip = "10.124.206.68"
        self.user = "CHATBO"
        self.password = "1234567890"
        self.MSISDN = msisdn
        self.ZMMI = "ZMMI:MSISDN="
        self.ZMMO = "ZMMO:MSISDN="
        self.ZMMS = "ZMMS:MSISDN="
        r = str(datetime.now())
        r = r.replace(':', '-')
        self.sgsn_log_file = "complaints_internet/storage_log/" + self.server_ip + "-" + r + ".txt"

        f1 = open(self.sgsn_log_file, "w")
        f1.close()

    def msisdn_to_send(self, msisdn):
        return msisdn

    @asyncio.coroutine
    def shell(self, reader, writer):
        # MSISDN = msisdn_to_send()
        while True:
            outp = yield from reader.read(65536)
            if not outp:
                break
            elif 'ENTER USERNAME' in outp:
                writer.write(self.user)
                writer.write('\n\r' + self.password + '\n\r'
                             + self.ZMMI + self.MSISDN + ':;\n\r'
                             + self.ZMMO + self.MSISDN + ':;\n\r'
                             + self.ZMMS + self.MSISDN + ':;\n\r'
                             + 'Z;\n\r'
                             + 'ZZ;\n\r')
            f1 = open(self.sgsn_log_file, "a")  # server_ip + "_" + str(datetime.now()) +
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

        coro = telnetlib3.open_connection(self.server_ip, 23, shell=self.shell)
        reader, writer = loop.run_until_complete(coro)
        loop.run_until_complete(writer.protocol.waiter_closed)

        return self.sgsn_log_file

if __name__ == '__main__':
    zmmi_zmmo_zmms = Telnet_sgsn('237663744490')
    zmmi_zmmo_zmms.main()
    print("fin")