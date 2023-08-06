# Python packages
import os

# Third party packages
import requests
from . import validate


class APIConfiguration():
    def __init__(self, certificate_path, auth1, auth2, connString=None, dbHost=None, dbPswd=None):
        self.certificate_path = certificate_path
        self.auth1 = auth1
        self.auth2 = auth2

        # only set these if you are using datavault
        self.db_host = dbHost 
        self.db_password = dbPswd
        self.connection_string = connString


class AzulAPI():

    def __init__(self, config, environment='dev', dataVault=False):
        '''
        :param config (type APIConfigutation)
        :param environment (string, defaults 'dev' can also be set to 'prod')
        :param dataVault (boolean, you must configurate database credentials for this)
        '''
        self.config = config
        self.dataVault = dataVault
        self.ENVIRONMENT = environment
        self.TEST_URL = 'https://pruebas.azul.com.do/webservices/JSON/Default.aspx'
        self.PRODUCTION_URL = 'https://pagos.azul.com.do/webservices/JSON/Default.aspx'
        self.ALT_PRODUCTION_URL = 'https://contpagos.azul.com.do/Webservices/JSON/default.aspx'
        

    def azul_request(self, transaction_type, **kwargs):
        if self.ENVIRONMENT == 'prod':
            azul_endpoint = self.PRODUCTION_URL
        else:
            azul_endpoint = self.TEST_URL

        try:
            validation_handler = {
                'sale': validate.sale_transaction(kwargs),
                'hold': validate.hold_transaction(kwargs),
                'refund': validate.refund_transaction(kwargs),
                'post': validate.post_sale_transaction(kwargs),
                'verify': validate.verify_transaction(kwargs),
                'nullify': validate.nulify_transaction(kwargs),
                'datavault_create': validate.datavault_create(kwargs),
                'datavault_delete': validate.datavault_delete(kwargs)
            }

            # Validating that kwargs has all required attributes.
            validation_handler.get(transaction_type)

            # Required parameters for all transactions
            parameters = {
                'Channel': kwargs['Channel'],
                'Store': kwargs['Store'],
            }

            if kwargs['Itbis'] and kwargs['Itbis'] == 0:
                parameters.pop('Itbis')

            # Updating parameters with the extra parameters
            parameters.update(kwargs)
        
        except KeyError as missing_key:
            print(
                f'You are missing {missing_key} which is a required parameter for {transaction_type}.')
            return

        cert_path = self.config.certificate_path

        headers = {
            'Content-Type': 'application/json',
            'Auth1': self.config.auth1,
            'Auth2': self.config.auth2
        }
        try:
            response = requests.post(azul_endpoint, json=parameters,
                                     headers=headers, cert=cert_path)
        except:
            try:
                azul_endpoint = ALT_PRODUCTION_URL
                response = requests.post(azul_endpoint, json=parameters,
                                         headers=headers, cert=cert_path)
            except:
                print(
                    {'status': 'error',
                     'message': 'Could not reach Azul Web Service.'})

        return response

    def sale_transaction(self, **kwargs):
        azul_request('sale', kwargs)

    def hold_transaction(self, **kwargs):
        azul_request('hold', kwargs)

    def refund_transaction(self, **kwargs):
        azul_request('refund', kwargs)

    def post_sale_transaction(self, **kwargs):
        azul_request('post', kwargs)

    def verify_transaction(self, **kwargs):
        azul_request('verify', kwargs)
    
    def nulify_transaction(self, **kwargs):
        azul_request('nullify', kwargs)
    
    def datavault_create(self, **kwargs):
        azul_request('datavault_create', kwargs)
    
    def datavault_delete(self, **kwargs):
        azul_request('datavault_delete', kwargs)


if __name__ == '__main__':
    apiConfig = APIConfiguration('server.pem', 'testcert2', 'testcert2')
    pyazul = AzulAPI(apiConfig)
    response = pyazul.sale_transaction(
        Channel='EC',
        Store='39038540035',
        CardNumber='4035874000424977',
        Expiration='202012',
        CVC='977',
        PosInputMode='E-Commerce',
        Amount='1000',
        Itbis='180',
        CurrencyPosCode='$',
        Payments='1',
        Plan='0',
        AcquirerRefData='1',
        RNN='null',
        CustomerServicePhone='809-111-2222',
        OrderNumber='',
        ECommerceUrl='azul.iterativo.do',
        CustomOrderId='ABC123',
        DataVaultToken='',
        ForceNo3DS='1',
        SaveToDataVault='0'
    )
    print(response.text)
