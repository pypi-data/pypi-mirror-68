# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT license.

import json
import numpy as np
from encrypted.inference.eibase import EIBase

class EILinearRegressionClient(EIBase):
    def encrypt(self, values):
        '''
        Securely calculate the dot product of the given vector of doubles with the weight
        vector on the server. The values vector is encrypted as one or several ciphertexts
        with Microsoft SEAL and sent to the secure linear inferencing service. The server
        learns neither the contents of the values vector, not the result of the dot product.
        The result ciphertext is finally decrypted locally to obtain the result.
        '''
        _values = np.asarray(values, dtype=float)
        if (len(_values.shape) != 1):
            raise ValueError('`values` has invalid dimension; expected 1 but got ' + len(_values))

        key_id = self.seal_instance.get_secret_key_hash()

        # Get ciphertexts with our data
        self.log("Encrypting input data")
        encrypted_array = self.seal_instance.get_ciphertext_string_array(_values)

        encrypted_length = 0
        for cipher_str in encrypted_array:
            cipher_length = len(cipher_str)
            encrypted_length += cipher_length
        self.log("Input data encrypted: ... {0} ...".format(encrypted_array[0][50:150]))
        self.log("Created {0} ciphertext(s) with a size of {1:.3f} KB".format(len(encrypted_array), encrypted_length / 1024))

        return encrypted_array

    def decrypt(self, response: list):
        self.log('Received encrypted response of size {}'.format(len(response)))

        result = np.ndarray(len(response), dtype=float)
        for m in range(0, len(response)):
            result[m] = self.seal_instance.decrypt_result(response[m])

        self.log("Encrypted inference request completed")
        return result
