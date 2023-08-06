# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT license.

def handle_error(error):
    '''
    Handle an error from a Native method
    '''
    if (error != 0):
        raise OSError('Failed to call native method. Result: %s' %hex(error))

