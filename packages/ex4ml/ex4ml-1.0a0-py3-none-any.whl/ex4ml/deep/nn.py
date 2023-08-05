"""Contains functions to create commonly used neural networks."""

from tensorflow.keras.layers import Dense, Input, Dropout
from tensorflow.keras.models import Model, Sequential


def create_ffnn(input_size, layer_list, sequential=True):
    """
    Create a Feed-Forward Neural Network keras model of a specified size.

    Args:
        input_size (int or tuple): The shape of the input layer.
        layer_list (list[dict]): List of dictionaries each having the form:

            ::

                {
                    'size': size,               # (int)
                    'fn': activation_function,  # (str)
                    'droput': dropout,          # (bool, optional)
                    'regularizer': regularizer  # (keras.regularizer, optional)
                }

        sequential (bool, optional): Whether the model should be a ``keras.models.Sequential`` model. Defaults to
            ``True``.

    Returns:
        keras.Model: The Feed-Forward Neural Network keras model.
    """

    # Create input layer to network
    network_input = Input(input_size)
    network = network_input

    # Construct NN layer by layer.
    for layer in layer_list:
        # Set regularizer default.
        if 'regularizer' not in layer:
            layer['regularizer'] = None

        # Create next dense layer.
        network = Dense(layer['size'], activation=layer['fn'],
                        kernel_regularizer=layer['regularizer'])(network)

        # Add dropout layer if requested.
        if 'dropout' in layer:
            network = Dropout(layer['dropout'])(network)

    # Make sure to return sequential model if requested.
    model = Model(inputs=network_input, outputs=network)
    if sequential:
        model = Sequential.from_config(model.get_config())
    return model


def create_autoencoder(input_size, encode_layer_list, decode_layer_list, sequential=True):
    """
    Create an auto-encoder (encoder and decoder).

    Args:
        input_size (int or tuple): The shape of the input layer.
        encode_layer_list (list[dict]): List of dictionaries each having the form:

            ::

                {
                    'size': size,               # (int)
                    'fn': activation_function,  # (str)
                    'droput': dropout,          # (bool, optional)
                    'regularizer': regularizer  # (keras.regularizer, optional)
                }

        decode_layer_list (list[dict]): List of dictionaries each having the form:

            ::

                {
                    'size': size,               # (int)
                    'fn': activation_function,  # (str)
                    'droput': dropout,          # (bool, optional)
                    'regularizer': regularizer  # (keras.regularizer, optional)
                }

        sequential (bool, optional): Whether the model should be a ``keras.models.Sequential`` model. Defaults to
            ``True``.


    Returns:
        dict: The models for each part of the auto-encoder.

        ::

            {
                'autoencoder':  # (keras.Model),
                'encoder':      # (keras.Model),
                'decoder':      # (keras.Model)
            }
    """

    # Figure out the encoding size.
    if encode_layer_list:
        code_size = encode_layer_list[-1]['size']
    else:
        code_size = input_size

    # Create encoder and decoder models separately.
    encoder = create_ffnn(input_size, encode_layer_list, sequential=sequential)
    decoder = create_ffnn(code_size, decode_layer_list, sequential=sequential)

    # Link encoder and decoder to form autoencoder.
    autoencoder_input = Input(input_size)
    encoded = encoder(autoencoder_input)
    decoded = decoder(encoded)
    autoencoder = Model(inputs=autoencoder_input, outputs=decoded)

    # Make sure to return sequential model if requested.
    if sequential:
        autoencoder = Sequential.from_config(autoencoder.get_config())

    return {
        'encoder': encoder,
        'decoder': decoder,
        'autoencoder': autoencoder
    }


def create_symmetric_autoencoder(input_size, encode_layer_list, sequential=True):
    """
    Create a symmetric auto-encoder (encoder and decoder).

    Args:
        input_size (int or tuple): The shape of the input layer.
        encode_layer_list (list[dict]): Only include layers for the encoder. List of dictionaries each having the form:

            ::

                {
                    'size': size,               # (int)
                    'fn': activation_function,  # (str)
                    'droput': dropout,          # (bool, optional)
                    'regularizer': regularizer  # (keras.regularizer, optional)
                }

        sequential (bool, optional): Whether the model should be a ``keras.models.Sequential`` model. Defaults to
            ``True``.

    Returns:
        dict: The models for each part of the auto-encoder.

        ::

            {
                'autoencoder':  # (keras.Model),
                'encoder':      # (keras.Model),
                'decoder':      # (keras.Model)
            }
    """

    # Determine the decoder layers.
    decode_layer_list = []
    for k in range(1, len(encode_layer_list)):
        decode_layer_list.append(encode_layer_list[-(k + 1)])
    decode_layer_list.append({
        'size': input_size,
        'fn': None
    })

    return create_autoencoder(input_size, encode_layer_list, decode_layer_list, sequential=sequential)
