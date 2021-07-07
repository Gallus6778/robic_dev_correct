from complaints_correction.hlr_module import Soap_class

class Apn:
    def __init__(self, msisdn):
        self.msisdn = msisdn
        self.path_to_file = 'complaints_correction/storage_xml/modify_apn_n-internet.xml'

    def main(self):
        msisdn_to_correct = Soap_class(msisdn=self.msisdn, path_to_file=self.path_to_file).main()

if __name__ == "__main__":
    path_to_file = 'complaints_correction/storage_xml/modify_apn_n-internet.xml'
    msisdn = input("msisdn : ")
    msisdn_to_correct = Soap_class(msisdn=msisdn, path_to_file=path_to_file).main()