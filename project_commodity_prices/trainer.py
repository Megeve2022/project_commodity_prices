import numpy as np
import joblib
from random import randint
from termcolor import colored
from tensorflow.keras import models
from tensorflow.keras import layers
from tensorflow.keras import optimizers, metrics
from tensorflow.keras.layers.experimental.preprocessing import Normalization
from tensorflow.keras.callbacks import EarlyStopping
from project_commodity_prices.data import get_data
from project_commodity_prices.data import get_train_test_df
from google.cloud import storage
from project_commodity_prices.params import *


def init_model():
    '''LSTM Layers'''
    metric = metrics.MAPE
    opt = optimizers.RMSprop(learning_rate=0.01)

    normalizer = Normalization()
    normalizer.adapt(np.asarray(X_train))

    model = models.Sequential()
    model.add(normalizer)
    model.add(layers.LSTM(30,input_shape=(252,5), return_sequences = False, activation='tanh'))
    model.add(layers.Dense(10, activation='relu'))
    model.add(layers.Dense(12, activation='linear'))

    model.compile(loss='mse',
                  optimizer=opt,
                  metrics=[metric])

    es = EarlyStopping(monitor='val_loss', verbose=1, patience=10, restore_best_weights=True)
    history = model.fit(X_train, y_train,validation_split=0.2,epochs=100, batch_size=1,callbacks=[es], verbose=1)

    return history,model


def save_model(model, path="model.joblib"):
    """Save the model into a .joblib format"""
    joblib.dump(model, path)
    print("model.joblib saved locally", "green")


def save_model_to_gcp(model, local_model_name="model.joblib"):
    """Save the model into a .joblib and upload it on Google Storage /models folder
    HINTS : use sklearn.joblib (or jbolib) libraries and google-cloud-storage"""
    # saving the trained model to disk (which does not really make sense
    # if we are running this code on GCP, because then this file cannot be accessed once the code finished its execution)
    save_model(model, path=local_model_name)
    client = storage.Client().bucket(BUCKET_NAME)
    storage_location = f"models/{MODEL_NAME}/{MODEL_VERSION}/{local_model_name}"
    blob = client.blob(storage_location)
    blob.upload_from_filename(local_model_name)
    print("uploaded model.joblib to gcp cloud storage under \n => {}".format)


if __name__ == '__main__':
    # Get initial data frame
    df = get_data()
    # Get X_train, y_train, X_test and y_test data frames
    X_train, y_train, X_test, y_test = get_train_test_df(df)
    # Initializate model
    history,model = init_model()
    # Show test metrics
    res = model.evaluate(X_test, y_test, verbose=0)
    print(f'MAPE on the test set : {res[1]:.0f} %')
    # Save model to Google Cloud Platform
    save_model_to_gcp(model)
