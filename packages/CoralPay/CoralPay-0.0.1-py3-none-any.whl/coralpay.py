from pretty_bad_protocol import gnupg
import binascii
import requests


"""
#/v2/gpx/users/lookup
#/v2/secureauth/lookup
Steps

1. install Gnupg
2. pip install pretty_bad_protocol
3  generate the your public and private key https://www.igolder.com/pgp/generate-key/
4. gpg --import coralpay.public.txt
5. gpg --import your_privatekey.txt

"""

class CoralPay:
    def __init__(self, homedir='/path/to/home/directory', key_id=None):
        # gnupg.GPG(homedir=homedir,  keyring='pubring.gpg', secring='secring.gpg')
        self.gpg = gnupg.GPG(binary='/usr/bin/gpg', homedir=homedir,
                             keyring='pubring.gpg', secring='secring.gpg')
        self.key_id = key_id

    def coral_encrypt(self, message, hex=True):
        """
        :param message:
        :param key_id:
        :param hex:
        :return:
        """
        app_request = str(self.gpg.encrypt(str(message), self.key_id))
        if hex:
            app_request = app_request.encode("latin-1").hex()
        return str(app_request)

    def coral_decrypt(self, message, passphrase=None, always_trust=True, hex=True):
        """
        :message is the response from coralpay
        :param message:
        :param passphrase:
        :return:
        """
        if hex:
            binary_response = binascii.unhexlify(message)
        response = (self.gpg.decrypt(binary_response, always_trust=always_trust, passphrase=passphrase,
                                     output=None))
        return str(response)

    def call_coray_pay(self, endpoint, message, verify_ssl=True):
        """

        :param endpoint:
        :param message:
        :return:
        : configure the enpoint on your UI config
        """
        #URL = "https://testdev.coralpay.com/cgateproxy/api/invokereference"
        head = {'Content-Type': 'text/plain'}
        coral_callback_response = requests.post(endpoint, message, headers=head, verify=verify_ssl)
        return coral_callback_response.text

    def process_callback(self, message, passphrase=None):
        """
        :param message:
        :return:
        """
        callback_response = gpg.coral_decrypt(message, passphrase=passphrase, always_trust=True, hex=True)
        return str(callback_response)
        

if __name__ == '__main__':
    message = {
        "RequestHeader": {
            "Username": "****",
            "Password": "******"},
        "RequestDetails": {
            "TerminalId": "*****",
            "Channel": "USSD",
            "Amount": 50.0,
            "MerchantId": "*****",
            "TransactionType": "0",
            "SubMerchantName": "******",
            "TraceID": ""
        }
    }

    # Initiate
    gpg = CoralPay(homedir='/Users/oluwasemilore/.gnupg',
                   key_id="CORALPAY_FINGERPRINT")
    data = gpg.coral_encrypt(message, hex=True)
    URL = "CORALPAY_ENDPOINT"
    res = gpg.call_coray_pay(URL, data)
    coral_response = gpg.coral_decrypt(
        res, passphrase="YOUR PUBLIC KEY", always_trust=True, hex=True)
    print(coral_response)
