from block import *
from wallet import *
from stringutils import *
from transaction import *
from blockchain import *
import json
import jsonpickle

w = None
b = None
difficulty = 5
genesis_transaction = None
def __init__():
    global w
    global b
    global UTXOs
    global difficulty
    global genesis_transaction
    w = Wallet()
    b = Wallet()
    coinbase = Wallet()
    genesis_transaction = Transaction(coinbase.public_key, w.public_key, 21000000, None)
    genesis_transaction.generate_signature(coinbase.private_key)
    genesis_transaction.transaction_id = "0"
    genesis_transaction.outputs.append(TransactionOutput(genesis_transaction.receiver, genesis_transaction.value, genesis_transaction.transaction_id))
    UTXOs[genesis_transaction.outputs[0].id] = genesis_transaction.outputs[0]
    print "Creating and Mining Genesis Block"
    genesis = Block("0")
    genesis.add_transaction(genesis_transaction)
    add_block(genesis)

    exodus = Block(genesis.hash)
    print "Wallet A balance is: "+str(w.get_balance())
    print "Wallet B balance is: " + str(b.get_balance())
    print "Wallet A attempt to send funds(40) to Wallet B..."
    exodus.add_transaction(w.send_funds(b.public_key, 40))
    add_block(exodus)
    print "Wallet A balance is: " + str(w.get_balance())
    print "Wallet B balance is: " + str(b.get_balance())

    leveticus = Block(exodus.hash)
    print "Wallet B attempt to send funds(500) to Wallet A..."
    leveticus.add_transaction(b.send_funds(w.public_key, 500))
    add_block(leveticus)
    print "Wallet A balance is: " + str(w.get_balance())
    print "Wallet B balance is: " + str(b.get_balance())


    numbers = Block(leveticus.hash)
    print "Wallet B attempt to send funds(0.00000000002323523) to Wallet A..."
    numbers.add_transaction(b.send_funds(w.public_key, 0.00000000002323523))
    add_block(numbers)
    print "Wallet A balance is: " + str(w.get_balance())
    print "Wallet B balance is: " + str(b.get_balance())

    print "Is valid blockchain? : "+str(is_valid_chain())
    print "#The Blockchain"
    block = json.dumps([jsonpickle.encode(b, unpicklable=False)
                        for b in blockchain])
    print block
    file = open("blockchain.txt","w+")
    file.write(block)
    file.close()

    
def add_block(block):
    global difficulty
    block.mining(difficulty)
    blockchain.append(block)


def is_valid_chain():
    global blockchain
    global difficulty
    global genesis_transaction
    current_block = None
    previous_block = None
    i = 1
    target = '0' * difficulty
    tempUTXOs = {}
    tempUTXOs[genesis_transaction.outputs[0].id] = genesis_transaction.outputs[0]
    while i < len(blockchain):
        current_block = blockchain[i]
        previous_block = blockchain[i-1]
        if current_block.hash != current_block.calculate_hash():
            print "#Current Hashes not equal"
            return False
        
        if previous_block.hash != previous_block.calculate_hash():
            print "#Previous Hashes not equal"
            return False
        
        if current_block.hash[:difficulty] != target:
            print "#This block hasn't been mined"
            return False
        temp_transaction_output = None
        index = 0
        for current_transaction in current_block.transactions:
            if not current_transaction.verify_signature():
                print "#Signature on transaction "+str(index)+" is invalid"
                return False
            if current_transaction.get_inputs_value() != current_transaction.get_outputs_value():
                print "#Input and output are not equals on transaction "+str(index)
            for transaction_input in current_transaction.inputs:
                temp_output = tempUTXOs[transaction_input.transaction_output_id]
                if temp_output is None:
                    print "#Reference on transaction "+str(index)+" is missing"
                    return False
                if temp_output.value != transaction_input.UTXO.value:
                    print "#Reference input transaction "+str(index)+" is invalid"
                    return False
                tempUTXOs.pop(transaction_input.transaction_output_id)
            for output in current_transaction.outputs:
                tempUTXOs[output.id] = output
            if current_transaction.outputs[0].receiver != current_transaction.receiver:
                print "#Transaction("+str(index)+") output receiver is not who it should be"
                return False
            if current_transaction.outputs[1].receiver != current_transaction.sender:
                print "#Transaction(" + str(index) + ") output 'change' is not sender"
                return False
            index += 1
        i += 1
    
    return True

__init__()
