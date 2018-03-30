from stringutils import *
class TransactionOutput:
    def __init__(self, receiver, value, parent_transaction_id):
        self.receiver = receiver
        self.value = value
        self.parent_transaction_id = parent_transaction_id
        self.id = StringUtils.apply_sha256(
            StringUtils.get_string_from_key(receiver.exportKey('PEM'))
            + str(value) 
            + parent_transaction_id)
    
    def is_mine(self, public_key):
        return (public_key == self.receiver)
