from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
import keras.layers as layers
from tensorflow import keras
import data_processing as d
import numpy as np

class keras_CNN():
    def __init__(self, kernel_size, epochs):
        self.EPOCHS = epochs
        self.KERNEL_SIZE = kernel_size
        self.FILTERS = 32
        self.DROPOUT_RATE = 0.3
           
    def getModel(self):
        return keras.Sequential(
            [
                layers.Conv1D(self.FILTERS, self.KERNEL_SIZE, padding='same', activation='relu', name="layer1"),
                layers.LeakyReLU(),
                layers.Dropout(self.DROPOUT_RATE),
                layers.Conv1D(self.FILTERS, 5, padding='same', activation='relu', name="layer2"),
                layers.LeakyReLU(),
                layers.Dropout(self.DROPOUT_RATE),
                # layers.Conv1D(self.FILTERS / 4, self.KERNEL_SIZE, padding='same', activation='relu', name="layer3"),
                # layers.LeakyReLU(),
                # layers.Dropout(self.DROPOUT_RATE),
                layers.Dense(13, activation='softmax', name='output_layer')
            ])

    def plot(self, history, epochs, metric):
        loss_train = history[metric]
        epochs = range(1,epochs + 1)
        plt.plot(epochs, loss_train, 'g', label=metric)
        plt.title(metric)
        plt.xlabel('Epochs')
        plt.ylabel(metric)
        plt.legend()
        plt.show()
        
    def reshape_and_chng_type(self, X_train, X_test, y_train, y_test):
        new_X_train = X_train.reshape(1, X_train.shape[0], X_train.shape[1])
        new_y_train = y_train.reshape(1, y_train.shape[0], y_train.shape[1])
        new_X_test = X_test.reshape(1, X_test.shape[0], X_test.shape[1])
        new_y_test = y_test.reshape(1, y_test.shape[0], y_test.shape[1])
        
        new_X_train = new_X_train.astype(np.float32)
        new_y_train = new_y_train.astype(np.float32)
        new_X_test = new_X_test.astype(np.float32)
        new_y_test = new_y_test.astype(np.float32)
        return new_X_train, new_X_test, new_y_train, new_y_test

    def main(self):        
        model = self.getModel()
        optimizer = keras.optimizers.Nadam(learning_rate=1e-3, decay=5e-4)
    
        model.compile(optimizer, 'mse', metrics=[keras.metrics.Accuracy()])

        # model.build()
        # model.summary()
        history = model.fit(
            self.X_train,
            self.y_train,
            batch_size=32,
            epochs=self.EPOCHS
        )
    
        for metric in history.history:
            self.plot(history.history, self.EPOCHS, metric, "Training")
    
        print("Evaluate on test data")
        results = model.predict(self.X_test, batch_size=32)
        print("test loss, test acc:", accuracy_score(results, self.y_test))
