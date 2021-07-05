#!/usr/bin/env python

import re, openpyxl
# -------------------------COMPLAINTS INTERNET------------------------------------------------------
#   IMPORT MODULE WHICH WILL SEND AND RETURN XML FILE RESPONSE OF HLR   #

from complaints_internet.hlr_module import Soap_class

#   IMPORT MODULE WHICH WILL READ XML FILE RESPONSE OF HLR   #
from complaints_internet.read_xml_module import Read_request_by_msisdn

#   IMPORT MODULE WHICH WILL CHECK HLR AND PROVIDE DECISIONS   #
from complaints_internet.corrections_module import Check_hlr_info_and_provide_decision as provide_decision

#   IMPORT MODULE WHICH WILL SEND AND RETURN LOG FILE RESPONSE OF SGSN   #
from complaints_internet.sgsn_module import Telnet_sgsn

#   IMPORT MODULE WHICH WILL SEND AND RETURN LOG FILE RESPONSE OF SGSN   #
from complaints_internet.read_log_module import Read_sgsn_log

class Pas_internet:
    def __init__(self, msisdn):
        self.msisdn = msisdn
        self.msisdn_info_results = {'imsi': 'None', 'encKey': 'None', 'algoId': 'None', 'kdbId': 'None', 'acsub': 'None',
                               'imsiActive': 'None', 'accTypeGSM': 'None', 'accTypeGERAN': 'None',
                               'accTypeUTRAN': 'None', 'odboc': 'None', 'odbic': 'None', 'odbr': 'None',
                               'odboprc': 'None', 'odbssm': 'None', 'odbgprs': 'None', 'odbsci': 'None',
                               'isActiveIMSI': 'None', 'msisdn': 'None', 'actIMSIGprs': 'None', 'obGprs': 'None',
                               'qosProfile': 'None', 'refPdpContextName': 'None', 'imeisv': 'None',
                               'ldapResponse': 'None'}

    def main(self):
        if re.match('^[0-9]*$', self.msisdn):
            # Recuperation des inforamtions de l'abonne dans la HLR pour Complaints_internet
            msisdn = Soap_class(msisdn=self.msisdn)
            xml_reveived_from_hlr = msisdn.main()

            # Recuperation des inforamtions de l'abonne dans la SGSN pour Complaints_internet
            log_from_sgsn = Telnet_sgsn(msisdn=self.msisdn).main()
            xlsx_sgsn_info = Read_sgsn_log(sgsn_log_file=log_from_sgsn)
            xlsx_sgsn_info.txt_reader()
            xlsx_sgsn_info = xlsx_sgsn_info.xlsx_writter()
            workbook = openpyxl.load_workbook(filename=xlsx_sgsn_info)

            sheet = workbook.active
            dict = {}

            radio_access_type = sheet['C2'].value
            pdp_state = sheet["D2"].value
            terminal_type = sheet["E2"].value
            lac = sheet["F2"].value
            ci = sheet["G2"].value

            # Enrichissement du dataset avec des inforamtions de l'abonne dans la Complaints_internet (ce dernier modifiera le contenu du dictionnaire )
            try:
                Read_request_by_msisdn(xml_reveive_from_hlr=xml_reveived_from_hlr,
                                       msisdn_info_results=self.msisdn_info_results).put_data_in_dataset()
            except:
                messageErreur = 'Error -> file not closed:-) You must first closed the "dataset_internet.xlsx" file !'
                return messageErreur

            # ============================= Correction du probleme ===========================
            subscriber_info = provide_decision()
            info_parameter = subscriber_info.main()

            message_ack = ''
            for keys, values in info_parameter.items():
                message_ack = message_ack + keys + ":" + values + ";"

            # return info_parameter
            return message_ack

        else:
            error = "Sorry, the msisdn should be a number only !!!"
            return error


