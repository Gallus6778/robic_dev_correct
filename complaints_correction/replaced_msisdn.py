import xml.etree.cElementTree as ET
import os


class Replaced_msisdn_in_xml_class:
    """
    Class for writing msisdn in xml request_by_msisdn file

    It returns output.xml file"""

    def __init__(self, msisdn, path_to_file):
        self.msisdn = msisdn
        self.filename = path_to_file

    # ------------ Method which modify msisdn in xml request_by_msisdn file and save it into 'output.xml' file -----------
    def main(self):
        with open('complaints_correction/storage_xml/xml_to_send_to_hlr.xml', 'w') as outfile:
            with open(self.filename, 'r') as file:  # contains your records
                a = file.read()
                if "msisdn_to_change" in a:
                    b = a.replace('msisdn_to_change', self.msisdn)
                    # print (b)
                    outfile.write(b)
                else:
                    outfile.write(a)
        return 'complaints_correction/storage_xml/xml_to_send_to_hlr.xml'

if __name__ == "__main__":
    msisdn = Replace_msisdn_in_xml_class('237669592850')
    msisdn.main()