# The model is based off this tutorial : https://medium.com/tensorflow/a-transformer-chatbot-tutorial-with-tensorflow-2-0-88bf59e66fe2
# More information is available here: https://colab.research.google.com/github/tensorflow/examples/blob/master/community/en/transformer_chatbot.ipynb#scrollTo=eDUX7Oa8Xudj
import slidingWindow
from sklearn.model_selection import train_test_split
from model import Model
import numpy as np

if __name__ == '__main__':
    filepath = "..\Classification\Acquisition\Data\Dataset_avec_angles_tester"
    saved_model_path = "model"

    # Format the data
    with open(filepath + '/dataset_emg_angles.npz', 'rb') as file:
        data = np.load(file, allow_pickle=True)
        emg_data = data["emg_data"]
        angle_data = data["angle_data"]

    print("EMG dataset size:", emg_data.shape)
    print("Angle size:", angle_data.shape)


    # x_train = emg_data
    x_train, x_test, y_train, y_test = train_test_split(
        emg_data, angle_data, test_size=0.10, random_state=40
    )

    n_timesteps = 30
    average_window = 10

    x_train, y_train = slidingWindow.create_time_serie(x_train, y_train, n_timesteps, average_window)
    x_test, y_test = slidingWindow.create_time_serie(x_test, y_test, n_timesteps, average_window)

    # parameter for the model
    n_layers = 3
    d_model = x_train.shape[2]
    n_heads = 7
    units = 1024
    dropout = 0.1
    time_steps = x_train.shape[1]
    epochs = 10

    model = Model(time_steps, n_layers, units, d_model, n_heads, dropout)

    model.train_model(x_train, y_train, x_test, y_test, epochs, saved_model_path)


