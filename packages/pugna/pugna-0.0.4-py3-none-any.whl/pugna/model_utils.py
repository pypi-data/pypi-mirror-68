import tensorflow as tf


def save_model(model, model_name):
    # serialize model to json
    json_model = model.to_json()
    # save the model architecture to JSON file
    with open(f'{model_name}.json', 'w') as json_file:
        json_file.write(json_model)
    # saving the weights of the model
    model.save_weights(f'{model_name}_weights.h5')


def load_model(model_name):
    # Reading the model from JSON file
    with open(f'{model_name}.json', 'r') as json_file:
        json_savedModel = json_file.read()
    # load the model architecture
    model = tf.keras.models.model_from_json(json_savedModel)
    # model.summary()
    model.load_weights(f'{model_name}_weights.h5')
    return model


def save_model_checkpoint(model, model_name, num, zpad='04'):
    """
    name format: '{model_name}+checkpoint_0001.h5'
    """
    # saving the smodel's architecture, weights, and training configuration in a single file/folder.
    model.save(f'{model_name}_checkpoint_' + format(num, zpad) + '.h5')


def load_model_checkpoint(model_name, num, zpad='04'):
    """
    name format: '{model_name}+checkpoint_0001.h5'
    """
    # loading the model from the HDF5 file
    model = tf.keras.models.load_model(
        f'{model_name}_checkpoint_' + format(num, zpad) + '.h5')
    return model
