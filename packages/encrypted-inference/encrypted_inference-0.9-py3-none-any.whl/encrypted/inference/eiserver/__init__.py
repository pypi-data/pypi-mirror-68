# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT license.

import json
import os
import errno
import numpy as np
from encrypted.inference.internal import einative

class EIServer(object):
    def __init__(self, coeffs, intercept, verbose = False):
        self.verbose = verbose

        self.intercept = np.asarray(intercept)
        self.coeffs = np.asarray(coeffs)

        if (len(self.coeffs.shape) != 2):
            raise ValueError('`coeffs` has invalid dimension; expected 2 but got ' + len(self.coeffs.shape))
        if (len(self.intercept.shape) != 1):
            raise ValueError('`intercept` has invalid dimension; expected 1 but got ' + len(self.intercept.shape))

        # Which dimension labels the models
        self.coeffs_model_index = 0

        # The number of models must match the intercept size
        if (self.coeffs.shape[self.coeffs_model_index] != len(self.intercept)):
            raise ValueError('Size mismatch')

        self.server_instance = einative.SEALServerInstance()

    def __del__(self):
        self.__log("Cleaning up native resources")
        self.server_instance = None

    def __get_coeffs_for_regressor(self, model_index):
        if (self.coeffs_model_index is 0):
            return self.coeffs[model_index]
        elif (self.coeffs_model_index is 1):
            return self.coeffs[:, model_index]
        else:
            raise RuntimeError('Internal error: coeff_model_index is invalid')

    def predict(self, ciphertexts: list, public_keys: bytes):
        '''
        Securely calculate the dot product of the given vector of doubles with the weight vector.
        '''
        if (ciphertexts is None):
            raise ValueError('No input data given')
        if (public_keys is None):
            raise ValueError('No public keys given')

        self.__log('Received encrypted input consisting of {} ciphertexts'.format(len(ciphertexts)))
        self.__log('Computing dot product on encrypted data')
        result = []
        for m in range(0, self.coeffs.shape[self.coeffs_model_index]):
            b64 = self.server_instance.compute_dot_product(self.__get_coeffs_for_regressor(m), self.intercept[m], ciphertexts, public_keys)
            result.append(str(b64.decode('ASCII')))

        self.__log('Created encrypted result of size {}'.format(len(result)))
        return result

    def __log(self, msg: str):
        '''
        Print log message if necessary
        '''
        if (self.verbose):
            print(msg)

