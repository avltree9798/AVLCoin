class Block:
    def __init__(self, previous_hash):
        import time
        self.merkle_root = ''
        self.previous_hash = previous_hash
        self.time_stamp = time.time() 
        self.nonce = 0
        self.hash = self.calculate_hash()
        self.transactions = []

    def calculate_hash(self):
        import stringutils
        calculated_hash = stringutils.StringUtils.apply_sha256(
            repr(self.previous_hash) + repr(self.time_stamp) +
            repr(self.nonce) + self.merkle_root
        )
        return calculated_hash
    

    def mining(self, difficulty):
        target = '0'*difficulty    
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
        
        print "Block Mined!!! : " +self.hash
    
    def add_transaction(self, transaction):
        if transaction is None:
            return False
        if self.previous_hash != "0":
            if not transaction.process_transaction():
                print "#Transaction failed to process"
        
        self.transactions.append(transaction)
        print "#Transaction successfully added to Blockchain"
        return True
    

    
