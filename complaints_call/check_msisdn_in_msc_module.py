from complaints_call.mss_module import Telnet_mss
from complaints_call.read_log_module import Read_mss_log

class Check_msisdn:
    def __init__(self, msisdn):
        self.msisdn = msisdn
        self.msisdn_in = {'YAMS01':'KNOWN SUBSCRIBER', 'YAMS02':'KNOWN SUBSCRIBER', 'DOMS01':'KNOWN SUBSCRIBER', 'DOMS02':'KNOWN SUBSCRIBER'}

    def main(self):
        log_in_YAMS01 = Telnet_mss(msisdn=self.msisdn, mss_ip='10.124.208.1').main()
        self.msisdn_in['YAMS01'] = Read_mss_log(mss_log_file=log_in_YAMS01).txt_reader()

        log_in_YAMS02 = Telnet_mss(msisdn=self.msisdn, mss_ip='10.124.208.81').main()
        self.msisdn_in['YAMS02'] = Read_mss_log(mss_log_file=log_in_YAMS02).txt_reader()

        log_in_DOMS01 = Telnet_mss(msisdn=self.msisdn, mss_ip='10.124.140.1').main()
        self.msisdn_in['DOMS01'] = Read_mss_log(mss_log_file=log_in_DOMS01).txt_reader()

        log_in_DOMS02 = Telnet_mss(msisdn=self.msisdn, mss_ip='10.124.148.4').main()
        self.msisdn_in['DOMS02'] = Read_mss_log(mss_log_file=log_in_DOMS02).txt_reader()

        return self.msisdn_in