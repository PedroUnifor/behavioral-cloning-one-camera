import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.optimizers import Adam
from keras.callbacks import ModelCheckpoint
from keras.layers import Lambda, Conv2D, MaxPooling2D, Dropout, Dense, Flatten
from utils import INPUT_SHAPE, batch_generator
import argparse
import cv2, os
import matplotlib.pyplot as plt

np.random.seed(0)


def load_data(args):
    """
    Load training data and split it into training and validation set
    """
    data_df = pd.read_csv(os.path.join(os.getcwd(), args.data_dir, 'driver_log_02.csv'), names=['center', 'aceleracao', 'rotacao']) #carrega o arquivo CSV para o DataFrame e atribuir os valores de imagens para center, aceleração para aceleração e rotação para rotação

    X = data_df['center'].values #colocar o valor do dataframe center pro X
    y = data_df[['rotacao']].values #colocar o valor do dataframe center pro Y (rotação)

    X_train, X_valid, y_train, y_valid = train_test_split(X, y, test_size=args.test_size, random_state=0) #random_state = pegar as imagens em ordem aleatória
	#test_size = percentual de treino e teste
    print('--------- ESSE E O X TRAIN -------------')
    print(X_train)
    #plt.imshow(X_train[0])
    #plt.show()
    print('--------- ESSE E O X VALID -------------')
    print(X_valid)
    print('--------- ESSE E O Y TRAIN -------------')
    print(y_train)
    print('--------- ESSE E O Y VALID -------------')
    print(y_valid)
    print(args.data_dir)

    return X_train, X_valid, y_train, y_valid


def build_model(args): #criar a rede neural

    model = Sequential() #cria um espaço em branco na memoria para o keras trabalhar
    model.add(Lambda(lambda x: x/127.5-1.0, input_shape=INPUT_SHAPE)) #camada de normalização
    model.add(Conv2D(24, 5, 5, activation='elu', subsample=(2, 2)))
    model.add(Conv2D(36, 5, 5, activation='elu', subsample=(2, 2)))
    model.add(Conv2D(48, 5, 5, activation='elu', subsample=(2, 2)))
    model.add(Conv2D(64, 3, 3, activation='elu'))
    model.add(Conv2D(64, 3, 3, activation='elu'))
    model.add(Dropout(args.keep_prob))
    model.add(Flatten())
    model.add(Dense(100, activation='elu'))
    model.add(Dense(50, activation='elu'))
    model.add(Dense(10, activation='elu'))
    model.add(Dense(1))
    model.summary() #imprime os valores dos layers

    return model


def train_model(model, args, X_train, X_valid, y_train, y_valid): #treinar o modelo
    """
    Train the model
    """
    checkpoint = ModelCheckpoint('model-{epoch:03d}.h5', #procurar ModelCheckpoint no keras
                                 monitor='val_loss',     
                                 verbose=0, 
                                 save_best_only=args.save_best_only, 
                                 mode='auto')

    model.compile(loss='mean_squared_error', optimizer=Adam(lr=args.learning_rate)) #mean_squared_error no youtube

    model.fit_generator(batch_generator(args.data_dir, X_train, y_train, args.batch_size, True),    #treinamento do modelo 
                        args.samples_per_epoch, 
                        args.nb_epoch,
                        max_q_size=1,
                        validation_data=batch_generator(args.data_dir, X_valid, y_valid, args.batch_size, False), #compara o treinamento com os dados validos
                        nb_val_samples=len(X_valid),
                        callbacks=[checkpoint], 
                        verbose=1)


def s2b(s):
    """
    Converts a string to boolean value
    """
    s = s.lower()
    return s == 'true' or s == 'yes' or s == 'y' or s == '1'


def main(): #Parametros do modelo
    """
    Load train/validation data set and train the model
    """
    parser = argparse.ArgumentParser(description='Behavioral Cloning Training Program')
    parser.add_argument('-d', help='data directory',        dest='data_dir',          type=str,   default='Data')
    parser.add_argument('-t', help='test size fraction',    dest='test_size',         type=float, default=0.2)
    parser.add_argument('-k', help='drop out probability',  dest='keep_prob',         type=float, default=0.5)
    parser.add_argument('-n', help='number of epochs',      dest='nb_epoch',          type=int,   default=20)
    parser.add_argument('-s', help='samples per epoch',     dest='samples_per_epoch', type=int,   default=50000)
    parser.add_argument('-b', help='batch size',            dest='batch_size',        type=int,   default=300)
    parser.add_argument('-o', help='save best models only', dest='save_best_only',    type=s2b,   default='True')
    parser.add_argument('-l', help='learning rate',         dest='learning_rate',     type=float, default=1.0e-3)
    args = parser.parse_args() #cria uma váriavel args com com todos os paramentos acima. "dest" será o nome da variável
    print('-' * 30)
    print('Parameters')
    print('-' * 30)
    for key, value in vars(args).items():
        print('{:<20} := {}'.format(key, value))
    print('-' * 30)

    data = load_data(args)
    #print(data)
    model = build_model(args)
    #print(model)
    train_model(model, args, *data)


if __name__ == '__main__':
    main()

