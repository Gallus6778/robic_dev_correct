from complaints_correction.hlr_module import Soap_class

class Obic:
    def __init__(self, msisdn):
        self.msisdn = msisdn
        self.path_to_file = 'complaints_correction/storage_xml/obic.xml'

    def main(self):
        msisdn_to_correct = Soap_class(msisdn=self.msisdn, path_to_file=self.path_to_file).main()