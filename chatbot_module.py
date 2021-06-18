#!/usr/bin/env python
# importation du module qui fera l'extraction du xml depuis la HLR pour les Complaints_internet
from Complaints_internet.soap_module import Soap_class
# importation du module qui fera le tri de donnees du xml pour l'ajouter dans le dataset
import Complaints_internet.dataset_enrichment as read_xml
# importation du module qui fera l'extraction du log depuis la SGSN pour les Complaints_internet
from Complaints_internet import sgsn_info_module
# importation du module qui identifiera et corrigera depuis la SGSN et la HLR les Complaints_internet
from Complaints_internet.correct_complaints_module import Info_hlr

# msisdn_info_results = {'imsi' : 'None',
#                            'encKey' : 'None',
#                            'algoId' : 'None',
#                            'kdbId' : 'None',
#                            'acsub' : 'None',
#                            'imsiActive' : 'None',
#                            'accTypeGSM' : 'None',
#                            'accTypeGERAN' : 'None',
#                            'accTypeUTRAN' : 'None',
#                            'odboc' : 'None',
#                            'odbic' : 'None',
#                            'odbr' : 'None',
#                            'odboprc' : 'None',
#                            'odbssm' : 'None',
#                            'odbgprs' : 'None',
#                            'odbsci' : 'None',
#                            'isActiveIMSI' : 'None',
#                            'msisdn' : 'None',
#                            'actIMSIGprs' : 'None',
#                            'obGprs' : 'None',
#                            'qosProfile' : 'None',
#                            'refPdpContextName' : 'None',
#                            'imeisv' : 'None',
#                            'ldapResponse' : 'None'}

class Pas_internet:
    def __init__(self, msisdn):
        self.msisdn = msisdn
        self.msisdn_info_results = {'imsi': 'None',
                               'encKey': 'None',
                               'algoId': 'None',
                               'kdbId': 'None',
                               'acsub': 'None',
                               'imsiActive': 'None',
                               'accTypeGSM': 'None',
                               'accTypeGERAN': 'None',
                               'accTypeUTRAN': 'None',
                               'odboc': 'None',
                               'odbic': 'None',
                               'odbr': 'None',
                               'odboprc': 'None',
                               'odbssm': 'None',
                               'odbgprs': 'None',
                               'odbsci': 'None',
                               'isActiveIMSI': 'None',
                               'msisdn': 'None',
                               'actIMSIGprs': 'None',
                               'obGprs': 'None',
                               'qosProfile': 'None',
                               'refPdpContextName': 'None',
                               'imeisv': 'None',
                               'ldapResponse': 'None'}

    def main(self):
        msisdn = Soap_class(msisdn=self.msisdn)
        soap_xml_filename = msisdn.main()

        # sgsn_info_module.main(msisdn_form)

        # Enrichissement du dataset avec des inforamtions de l'abonne dans la Complaints_internet (ce dernier modifiera le contenu du dictionnaire )
        try:
            # read_xml.put_data_in_dataset(soap_thread(msisdn_form), msisdn_info_results)
            read_xml.put_data_in_dataset(soap_xml_filename, self.msisdn_info_results)
        except:
            messageErreur = 'Error -> file not closed:-) You must first closed the "dataset_internet.xlsx" file !'
            return messageErreur

        # Recuperation des inforamtions de l'abonne dans la SGSN pour Complaints_internet
        # zmmi_command = zmmi_zmmo_zmms_class(msisdn)
        # zmmi_command.main()

        # ============================= Correction du probleme ===========================
        subscriber_info = Info_hlr()
        info_parameter = subscriber_info.main()

        message_ack = ''
        for keys, values in info_parameter.items():
            message_ack = message_ack + keys + ":" + values + ";"

        # return info_parameter
        return message_ack