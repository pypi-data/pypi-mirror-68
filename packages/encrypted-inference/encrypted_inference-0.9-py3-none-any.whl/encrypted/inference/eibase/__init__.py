# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT license.

import random
import string
from abc import ABC, abstractmethod
from encrypted.inference.internal.einative import SEALClientInstance

class EIBase(ABC):
    def __init__(self, secret_key: str = None, session_id: str = None, verbose = False):
        self.verbose = verbose
        self.seal_instance = SEALClientInstance(secret_key)
        if (session_id == None):
            self.session_id = self.__generate_id()
        else:
            self.session_id = session_id
        self.key_id = self.seal_instance.get_secret_key_hash()[0:32]
        self.log("Session ID: {0}".format(self.session_id))
        self.log("Secret key: {0}".format(self.secret_key()))
        self.log("Public keys ID: {0}".format(self.key_id))

    def __del__(self):
        self.log("Cleaning up native resources")
        self.seal_instance = None

    def secret_key(self):
        return self.seal_instance.get_secret_key()

    def secret_key_hash(self):
        return self.seal_instance.get_secret_key_hash()

    def get_public_keys(self):
        '''
        Get the public keys data
        '''
        self.log("Generating public keys")
        public_keys, pk_size = self.seal_instance.get_public_keys()
        self.log("Public keys generated: {0:.3f} MB".format(pk_size / (1024 * 1024)))
        return self.key_id, public_keys

    def log(self, msg: str):
        if (self.verbose):
            print(msg)

    def __generate_id(self):
        '''
        Generate a random string
        '''
        letters = string.ascii_lowercase + string.digits
        result = ''.join(random.choice(letters) for i in range(32))
        return result

    @abstractmethod
    def encrypt(self, values: list):
        pass

    @abstractmethod
    def decrypt(self, response: dict):
        pass
