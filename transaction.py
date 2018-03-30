from stringutils import *
import rsa
from blockchain import *
from transaction_output import *
class Transaction:
    def __init__(self, sender, receiver, value, inputs):
        self.sender = sender
        self.receiver = receiver
        self.value = value
        self.inputs = inputs
        self.transaction_id = ''
        self.signature = ''
        self.outputs = []
        self.sequence = 0
    
    def calculate_hash(self):
        self.sequence += 1
        return StringUtils.apply_sha256(
            StringUtils.get_string_from_key(self.sender.exportKey('PEM')) +
            StringUtils.get_string_from_key(self.receiver.exportKey('PEM')) +
        repr(self.value) + str(self.sequence)
        )
    
    def generate_signature(self, private_key):
        data = StringUtils.get_string_from_key(
            self.sender.exportKey('PEM')) + StringUtils.get_string_from_key(self.receiver.exportKey('PEM')) + str(self.value)
        self.signature = rsa.b64encode(rsa.sign(data, private_key, "SHA-512"))
    

    def verify_signature(self):
        data = StringUtils.get_string_from_key(
            self.sender.exportKey('PEM')) + StringUtils.get_string_from_key(self.receiver.exportKey('PEM')) + str(self.value)
        return rsa.verify(data, rsa.b64decode(self.signature), self.sender)

    def process_transaction(self):
        if not self.verify_signature():
            print "#Transaction signature failed to verify"
            return False

        for i in self.inputs:
            i.UTXO = UTXOs[i.transaction_output_id]

        if self.get_inputs_value() < minimum_transaction:
            print "#Transaction is too small"
            return False

        left_over = self.get_inputs_value() - self.value
        self.transaction_id = self.calculate_hash()
        self.outputs.append(TransactionOutput(
            self.receiver, self.value, self.transaction_id))
        self.outputs.append(TransactionOutput(
            self.sender, left_over, self.transaction_id
        ))

        for o in self.outputs:
            UTXOs[o.id] = o
        
        for i in self.inputs:
            if i.UTXO == None:
                pass
            else:
                UTXOs.pop(i.UTXO.id)

        return True
    
    def get_inputs_value(self):
        total = 0
        for i in self.inputs:
            if i.UTXO == None: 
                pass
            else:
                total += i.UTXO.value
        return total

    def get_outputs_value(self):
        total = 0
        for o in self.outputs:
                total += o.value
        return total
