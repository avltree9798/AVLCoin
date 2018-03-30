class StringUtils:
    @staticmethod
    def apply_sha256(input):
        import hashlib
        return hashlib.sha512(input.encode()).hexdigest()

    @staticmethod
    def get_string_from_key(input):
        import base64
        return base64.b64encode(input)
    
    @staticmethod
    def get_merkle_root(transactions):
        count = len(transactions)
        previous_tree_layer = []
        for t in transactions:
            previous_tree_layer.append(t.transaction_id)
        tree_layer = previous_tree_layer
        while count > 1:
            tree_layer = []
            size = count(previous_tree_layer)
            index = 1
            while index < size:
                tree_layer.append(StringUtils.apply_sha256(
                    previous_tree_layer[index-1] + previous_tree_layer[index]
                ))
                index += 1
            size = count(previous_tree_layer)
            previous_tree_layer = tree_layer
        merkle_root = tree_layer[0] if (count(tree_layer) == 1) else''
        return merkle_root
