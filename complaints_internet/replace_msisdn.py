import xml.etree.cElementTree as ET

class Replace_msisdn_in_xml_class:
    """
    Class for writing msisdn in xml request_by_msisdn file
    
    It returns output.xml file"""

    def __init__(self, msisdn):
        self.msisdn = msisdn
        self.filename = 'complaints_internet/storage_xml/xml_request_by_msisdn.xml'

# ------------ Method which modify msisdn in xml request_by_msisdn file and save it into 'output.xml' file -----------
    def main(self):
        tree = ET.ElementTree(file=self.filename)
        root = tree.getroot()

        for alias in root.findall('.//alias'):
            alias.set('value', self.msisdn)
        tree.write('complaints_internet/storage_xml/xml_to_send_to_hlr.xml')
        return 'complaints_internet/storage_xml/xml_to_send_to_hlr.xml'

if __name__=="__main__":
    msisdn = Replace_msisdn_in_xml_class('237669592850')
    msisdn.main()