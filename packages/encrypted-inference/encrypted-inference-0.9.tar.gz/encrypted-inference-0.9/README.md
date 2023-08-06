# Encrypted inference SDK

This package allows calling a remotely deployed inferencing service that operates on encrypted input data.
The data is encrypted using homomorphic encryption with the [Microsoft SEAL](https://GitHub.com/Microsoft/SEAL) library.
This SDK handles calls to Microsoft SEAL to create a secret key and encrypt the input data, returning an encrypted query as a byte array.
The byte array must then be communicated to a server component, where a model is deployed.
The server performs the prediction, obtaining an encrypted result, which can be decrypted by this SDK with the secret key.
In this process, the server is guaranteed to never learn the client's query.
