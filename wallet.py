import rsa
from blockchain import *
from transaction_input import *
from transaction import *
class Wallet:
    def __init__(self):
        self.private_key = ''
        self.public_key = ''
        self.UTXOs_local = {}
        self.generate_key_pair()
    

    def generate_key_pair(self):
        (self.public_key, self.private_key) = rsa.newkeys(2048)

    def get_balance(self):
        total = 0
        for u,v in UTXOs.iteritems():
            if v.is_mine(self.public_key):
                self.UTXOs_local[v.id] = v
                total += v.value
        return total
    
    def send_funds(self, _receiver, value):
        if self.get_balance() < value:
            print "#Not enough funds to create this transaction"
            return None
        inputs = []
        total = 0
        for u,v in self.UTXOs_local.iteritems():
            total += v.value
            inputs.append(TransactionInput(v.id))
            if total > value:
                break

        new_transaction = Transaction(self.public_key, _receiver, value, inputs)
        new_transaction.generate_signature(self.private_key)
        for i in inputs:
            self.UTXOs_local.pop(i.transaction_output_id)
        return new_transaction