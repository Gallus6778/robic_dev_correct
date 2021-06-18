import requests
import sys
import string

##########################################################################
#   IMPORT MODULE WHERE MSISDN IS REPLACED INTO XML FILE TO SEND TO HLR  #
from complaints_call.replace_msisdn import Replace_msisdn_in_xml_class

#-------------------------------------------------------------------------
# import xml.etree.cElementTree as ET

class Soap_class:
    def __init__(self, msisdn):
        self.msisdn = msisdn

    def main(self):
        try:
            url = "http://10.124.192.138:10081/ProvisioningGateway/services/SPMLHlrSubscriber45Service"
            # Modifier le fichier Request_by_MSISDN
            file_with_msisdn = Replace_msisdn_in_xml_class(self.msisdn)
            filename = file_with_msisdn.main()

            payload = filename
            headers = {'Content-Type': 'text/xml', 'charset': 'UTF-8', 'SOAPAction': 'http://10.124.192.138:10081/ProvisioningGateway/services/SPMLHlrSubscriber45Service'}

            with open(payload) as fd:
                r = requests.post(url, data=fd.read().replace("\n",""), headers=headers)
                response = 'None'
                response = r.content
                file = open('complaints_call/storage_xml/xml_received_from_hlr.xml', 'w')
                file.write(response.decode('utf-8'))
                file.close()
            return 'complaints_call/storage_xml/xml_received_from_hlr.xml'
        except:
            return "defaut de connexion avec la HLR"

if __name__ == "__main__":
    nbr = 237669595858
    msisdn = Soap_class(str(nbr))
    msisdn.main()