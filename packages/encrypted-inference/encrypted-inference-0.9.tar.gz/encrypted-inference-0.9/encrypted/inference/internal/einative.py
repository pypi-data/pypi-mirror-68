# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT license.

import ctypes
import os
import platform
import base64
import json
import numpy as np
import struct
from encrypted.inference.internal import eiutils, _version

def __load_einative():
    '''
    Load the native library
    '''
    osname = platform.system();

    if (osname == 'Windows'):
        einative_pre = ''
        einative_ext = 'dll'
    elif (osname == 'Linux'):
        einative_pre = 'lib'
        einative_ext = 'so'
    elif (osname == 'Darwin'):
        einative_pre = 'lib'
        einative_ext = 'dylib'
    else:
        raise OSError('Current OS is not supported: %s' %osname)

    einative_name = einative_pre + 'eisdk.' + einative_ext

    folder = os.path.dirname(os.path.abspath(__file__))
    dll_path = os.path.join(folder, einative_name)
    dll = ctypes.CDLL(dll_path)
    return dll

_einative = __load_einative()

# Argument definitions
_einative.GetSecretKey.argtypes = [ ctypes.c_void_p, ctypes.POINTER(ctypes.c_uint64) ]
_einative.GetSecretKeyHash.argtypes = [ ctypes.c_void_p, ctypes.POINTER(ctypes.c_uint64) ]
_einative.GetPublicKeys.argtypes = [ ctypes.c_void_p, ctypes.POINTER(ctypes.c_uint64), ctypes.POINTER(ctypes.c_byte) ]
_einative.EncryptList.argtypes = [ ctypes.c_void_p, ctypes.c_uint64, ctypes.POINTER(ctypes.c_double), ctypes.c_uint64, ctypes.POINTER(ctypes.c_uint64), ctypes.POINTER(ctypes.c_byte) ]
_einative.DecryptResult.argtypes = [ ctypes.c_void_p, ctypes.c_uint64, ctypes.POINTER(ctypes.c_byte), ctypes.POINTER(ctypes.c_double) ]
_einative.CreateSEALClientInstance.argtypes = [ ctypes.POINTER(ctypes.c_void_p), ctypes.POINTER(ctypes.c_uint64) ]
_einative.DestroySEALClientInstance.argtypes = [ ctypes.c_void_p ]
_einative.GetServerSlotCount.argtypes = [ ctypes.c_void_p, ctypes.POINTER(ctypes.c_uint64) ]
_einative.GetClientSlotCount.argtypes = [ ctypes.c_void_p, ctypes.POINTER(ctypes.c_uint64) ]
_einative.CreateSEALServerInstance.argtypes = [ ctypes.c_uint64, ctypes.c_uint64, ctypes.POINTER(ctypes.c_int32), ctypes.c_double, ctypes.POINTER(ctypes.c_void_p) ]
_einative.DestroySEALServerInstance.argtypes = [ ctypes.c_void_p ]
_einative.GetCiphertextBufferSize.argtypes = [ ctypes.POINTER(ctypes.c_uint64) ]
_einative.ComputeDotProduct.argtypes = [ ctypes.c_void_p, ctypes.c_uint64, ctypes.POINTER(ctypes.c_double), ctypes.c_double, ctypes.c_uint64, ctypes.POINTER(ctypes.c_byte), ctypes.c_uint64, ctypes.POINTER(ctypes.c_byte), ctypes.POINTER(ctypes.c_uint64), ctypes.POINTER(ctypes.c_byte) ]

class NativeObject(object):
    '''
    Class that represents a native object
    '''
    native_ptr = ctypes.c_void_p()
    owned = True

    def __init__(self, native_ptr_value, owned_val):
        self.native_ptr = native_ptr_value
        self.owned = owned_val

    def destroy_native(self):
        raise NotImplementedError()

    def __del__(self):
        if (self.native_ptr.value != None and self.owned):
            self.destroy_native()

class SEALClientInstance(NativeObject):
    '''
    Class that represents a native instance of an Encrypted Inference Client
    '''
    def __init__(self, secret_key: str = None, native_ptr_value = None, owned_val = True):
        if (native_ptr_value is None):
            ptr = ctypes.c_void_p()
            secret_key_bytes = None
            secret_key_ptr = None
            if (secret_key is not None):
                secret_key_bytes = base64.b64decode(secret_key)
                if (len(secret_key_bytes) != 64):
                    raise ValueError('The given secret key is invalid')
                secret_key_ptr = ctypes.cast(secret_key_bytes, ctypes.POINTER(ctypes.c_uint64))

            error = _einative.CreateSEALClientInstance(ctypes.byref(ptr), secret_key_ptr)
            eiutils.handle_error(error)
            super().__init__(ptr, owned_val)
        else:
            super().__init__(native_ptr_value, owned_val)

    def destroy_native(self):
        _einative.DestroySEALClientInstance(self.native_ptr)

    def get_secret_key(self):
        '''
        Return a base64-encoded secret key.
        '''
        secret_key_arr = (ctypes.c_uint64 * 8)()
        error = _einative.GetSecretKey(self.native_ptr, secret_key_arr)
        eiutils.handle_error(error)

        b64key = base64.b64encode(secret_key_arr)
        return str(b64key, encoding='UTF-8')

    def get_secret_key_hash(self):
        '''
        Return a base32-encoded hash of the secret key.
        '''
        secret_key_hash_arr = (ctypes.c_uint64 * 4)()
        error = _einative.GetSecretKeyHash(self.native_ptr, secret_key_hash_arr)
        eiutils.handle_error(error)

        b32hash = base64.b32encode(secret_key_hash_arr)
        return str(b32hash, encoding='UTF-8').lower().strip('=')

    def get_public_keys(self):
        '''
        Get a byte array with the public keys
        '''
        # First get size
        pk_size = ctypes.c_uint64()
        error = _einative.GetPublicKeys(self.native_ptr, ctypes.byref(pk_size), None)
        eiutils.handle_error(error)

        # Create destination buffers
        pk_bin = (ctypes.c_byte * pk_size.value)()

        error = _einative.GetPublicKeys(self.native_ptr, ctypes.byref(pk_size), pk_bin)
        eiutils.handle_error(error)

        pk_array = np.array(pk_bin[:pk_size.value], dtype = ctypes.c_byte)
        int_size = int(pk_size.value)
        return bytes(pk_array), int_size

    def get_ciphertext_string_array(self, values: np.ndarray):
        '''
        Get an array of Ciphertexts encoded as base64 strings
        '''
        values_array = (ctypes.c_double * len(values))(*values)
        cipher_idx = ctypes.c_uint64(0)
        error = 0
        result = []
        values_count = ctypes.c_uint64(len(values))

        while (error == 0):
            cipher_size = ctypes.c_uint64()

            # Get size of ciphertext
            error = _einative.EncryptList(self.native_ptr, values_count, values_array, cipher_idx, ctypes.byref(cipher_size), None)
            if (error == 0):
                cipher_bin = (ctypes.c_byte * cipher_size.value)()

                error = _einative.EncryptList(self.native_ptr, values_count, values_array, cipher_idx, ctypes.byref(cipher_size), cipher_bin)
                eiutils.handle_error(error)

                cipher_bin_actual = np.array(cipher_bin[:cipher_size.value], dtype = ctypes.c_byte)
                b64 = base64.b64encode(cipher_bin_actual)
                result.append(str(b64, encoding='ASCII'))

            cipher_idx = ctypes.c_uint64(cipher_idx.value + 1)

        return result

    def decrypt_result(self, b64ciphertext: bytes):
        '''
        Decrypt a Ciphertext encoded as a base 64 string
        '''
        cipher_bytes = base64.b64decode(b64ciphertext)
        cipher_arr = (ctypes.c_byte * len(cipher_bytes))(*cipher_bytes)
        cipher_size = ctypes.c_uint64(len(cipher_bytes))
        result_ct = ctypes.c_double()

        error = _einative.DecryptResult(self.native_ptr, cipher_size, cipher_arr, ctypes.byref(result_ct))
        eiutils.handle_error(error)
        return float(result_ct.value)


class SEALServerInstance(NativeObject):
    '''
    Class that represents a native instance of an Encrypted Inference Server
    '''
    def __init__(self, native_ptr_value = None, owned_val = True):
        if (native_ptr_value is None):
            # Read parameters
            folder = os.path.dirname(os.path.abspath(__file__))
            parameters_path = os.path.join(folder, 'parameters.json')
            parameters_file = open(parameters_path)
            parameters = json.load(parameters_file)

            coeff_mod_list = parameters['CoeffModulus']
            coeff_mod_array = (ctypes.c_int32 * len(coeff_mod_list))(*coeff_mod_list)
            coeff_mod_array_count = ctypes.c_uint64(len(coeff_mod_list))
            initial_scale = ctypes.c_double(parameters['InitialScale'])
            poly_modulus_degree = ctypes.c_uint64(parameters['PolyModulusDegree'])
            ptr = ctypes.c_void_p()

            error = _einative.CreateSEALServerInstance(poly_modulus_degree, coeff_mod_array_count, coeff_mod_array, initial_scale, ctypes.byref(ptr))
            eiutils.handle_error(error)
            super().__init__(ptr, owned_val)
        else:
            super().__init__(native_ptr_value, owned_val)

    def destroy_native(self):
        _einative.DestroySEALServerInstance(self.native_ptr)

    def get_ciphertext_buffer_size(self):
        '''
        Get the size of the buffer that is necessary to store a Ciphertext
        '''
        ciphertext_buffer_size = ctypes.c_uint64(0)
        error = _einative.GetCiphertextBufferSize(ctypes.byref(ciphertext_buffer_size))
        eiutils.handle_error(error)
        return int(ciphertext_buffer_size.value)

    def compute_dot_product(self, weights: np.ndarray, intercept: float, ciphertexts: list, public_keys: bytes):
        '''
        Compute dot product of the given weights and ciphertexts
        '''
        slot_count = ctypes.c_uint64();

        weights_array = (ctypes.c_double * len(weights))(*weights)
        _intercept = ctypes.c_double(intercept)
        dimension = ctypes.c_uint64(len(weights))

        cipher_bytes = bytes()
        for cipher in ciphertexts:
            cipher_bytes += base64.b64decode(cipher);

        cipher_arr = (ctypes.c_byte * len(cipher_bytes))(*cipher_bytes)
        cipher_size = ctypes.c_uint64(len(cipher_bytes))

        # We assume public keys are already a byte array
        pk_arr = (ctypes.c_byte * len(public_keys))(*public_keys)
        pk_size = ctypes.c_uint64(len(public_keys))

        # How many ciphertexts do we expect at most?
        _einative.GetServerSlotCount(self.native_ptr, ctypes.byref(slot_count));
        cipher_count = (dimension.value + slot_count.value - 1) // slot_count.value

        # Total expected buffer needed for the ciphertexts
        cipher_size = self.get_ciphertext_buffer_size() * cipher_count
        result_arr = (ctypes.c_byte * cipher_size)()
        result_size = ctypes.c_uint64(cipher_size)

        error = _einative.ComputeDotProduct(self.native_ptr, dimension, weights_array, _intercept, cipher_size, cipher_arr, pk_size, pk_arr, ctypes.byref(result_size), result_arr)
        eiutils.handle_error(error)

        result_bin_actual = np.array(result_arr[:result_size.value], dtype = ctypes.c_byte)
        b64 = base64.b64encode(result_bin_actual)
        return b64
