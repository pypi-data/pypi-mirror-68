import os
import keras
import datetime
from collections import Counter
from keras import models
from keras import layers
from keras import optimizers
from keras import regularizers
from keras.layers import Embedding, Flatten, Dense, LSTM, Bidirectional, Dropout
import time
import matplotlib.pyplot as plt
import pickle
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report

from pandas_confusion import ConfusionMatrix
import matplotlib.pyplot as plt
import numpy as np
import traceback


from sentiment_analysis_csci_e89.pretrained_embeddings import pretrained_embeddings


class modeling:
    """
    The purpose of this class is to lay forth methods that can be used to model our data.
    Note this module is intended for neural architectures designed to process text data given that the data is processed a priori.
    The pre_processor module handles the data preperation; please use those methods to prepare the inputs to the various model
    architectures provided herewithin.
    It should be noted that the methods to train the networks were not written to allow on the fly changes to the underlying architecture.
    Instead, we only provide paramatization of important necessary arguments and some hyperparamaters. Feel free to augment this class
    by adding additional architectures orby modifying the ones that are provided. 

    Instance variables to pass during instantiation:

    :param project: The name of the project you are using the class for
    :type project: string

    :param models_output_path: file path of where trained models will be written to as hd5 objects.
    :type models_output_path: string

    :param error_log_dir: directory path of where errors should be logged to
    :type error_log_dir: string
    
    Documentation on our methods can be found below: \n
    """
    def __init__(self, project, models_output_path, error_log_dir):
        self.project = project
        self.models_output_path = models_output_path
        self.error_log_dir = error_log_dir
        print('Thank you for using the modeling class for:', self.project)

    def error_logger(self, exception_error, error_log_dir, file_name=''):
        """Generic method for error logging. This helper method is used by many other methods to log exception errors as they occur throughout our application.
         
        :type exception_error: string
        :param exception_error: this is the error identified by the interpreter at run time. This detail will be written to the error log to help future debugging

        :type error_log_dir: string
        :param error_log_dir: file path of where we wish to write our error log file 

        :type file_name: string
        :param file_name: Defaults to null. Can be intialized for method calls that deal with input files. If initialized information on the file where the error occured will be logged
        """
        error_log_file_name = "Error_Log.log"
        if not os.path.isdir(error_log_dir):
            os.mkdir(error_log_dir)
        else:
            pass

        with open(os.path.join(error_log_dir, error_log_file_name),
                  "a+") as el:
            el.write(
                str(exception_error) + "," + file_name + ',' +
                str(datetime.datetime.now()) + "\n")
        print("Error !", "Error Message:", str(exception_error))
        print('#########################')

    def zero_classsifier_predicitons(self, val_labels):
        """
        Method to compute zero rule classifier predictions to use as baseline comparison ofr each of our models.

        :param val_labels: list or numpy array containing actual labels we want to measure our model against
        :type val_lables: list or numpy array
        """
        error_log_dir = self.error_log_dir
        try:
            if not (isinstance(val_labels, (list, np.ndarray))):
                print('val_lables should be of type numpy array or list!')
            #let's compute class distributions of validation labels
            class_distribution = Counter(val_labels)
            #let's find the most occuring class.
            key_max_freq = max(class_distribution.keys(),
                               key=(lambda k: class_distribution[k]))
            N = len(val_labels)
            zero_rule_predictions = [key_max_freq for x in range(N)]
            return (zero_rule_predictions)

        except Exception:
            e = traceback.format_exc()
            self.error_logger(exception_error=e, error_log_dir=error_log_dir)

    def get_zero_classsifier_performance(self, val_labels, show_plot=False):
        """
        Metod to compute statistics on how well a the zero classifier model performed.

        :param val_labels: list or numpy array containing actual labels we want to measure our model against. One hot labels
         can be provided in the case of multi level response varaibles. otherwise 1 dimensional response variable encodings can be passed.
         List or numpy array types are suported. We strictly advise that the response labels be encoded according the following
         simple scheme:[0,1,..N] where N is the number of classes. Said differently: if we are modeling a phenomenon with 5
         classes, the response variable should be labelled as follows : 0,1,2,3,4. You can create a dictionary mapping the integer
         encodings to whatever the 'original' class names may be a priori before the modeling efforts. Example: {0:'Negative',1:'Positive'}. 
         To train the models using the neural architectures in this module a one hot encoding of the labels is required anyways.That
         representation can be easily mapped to the type we are asking of you here.        
        :type val_labels: list or numpy array

        :param show_plot: Flag to display plot of consusion matrix. Defaults to False.
        :type show_plot: boolean
        """
        error_log_dir = self.error_log_dir
        try:
            #Let's get the zero classifier predictions.
            class_predictions = self.zero_classsifier_predicitons(
                val_labels=val_labels)
            # we apply the logic to convert val_labels to class labels. Can handle one hot encoded class labels/
            try:
                output_dim = val_labels.shape[1]
            except:
                if isinstance(val_labels, list):
                    val_labels = np.asarray(val_labels)
                    #let's try again to get the shape
                    try:
                        output_dim = prediction.shape[1]
                    except:
                        #would fail if output is a one dimensional array.
                        output_dim = 1
                else:
                    #would fail if output is a one dimensional array
                    output_dim = 1

            if output_dim == 1:
                #we make the probability scores a prediction. This is a binary classification problem
                actuals = list(val_labels)
                # we can now build out the confusion matrix
            else:
                #code to create class predictions for multi level case
                actuals = [x.argmax() for x in val_labels]

            cm = confusion_matrix(actuals, class_predictions)
            print('#######################################')
            print('Let\'s study the performance of the zero classifier :)')
            print(cm)
            print('Summry Statistics:')
            print('\n')
            print('\n')
            print('Accuracy:')
            print(accuracy_score(actuals, class_predictions))
            print('\n')
            print('Classification report:')
            print(classification_report(actuals, class_predictions))
            if show_plot:
                print('Here is a plot of the confusion Matrix:')
                cm.plot()
                plt.show()
            print('#######################################')

        except Exception:
            e = traceback.format_exc()
            self.error_logger(exception_error=e, error_log_dir=error_log_dir)

    def get_classifier_performance(self,
                                   model,
                                   val_data,
                                   val_labels,
                                   cutoff=0.5,
                                   show_plot=False):
        """
        Method to compute statistics on how well a classification model performed.

        :param model: model that was used to train classifier. Model expects keras model object but others will work.
        :type model: model object
        
        :param val_data: validation data tensor (multidimensional numpy array of same shape and type as one provided in training)
        :type val_data: list or numpy array

        :param val_labels: list or numpy array containing actual labels we want to measure our model against. One hot labels
         can be provided in the case of multi level response varaibles. otherwise 1 dimensional response variable encodings can be passed.
         List or numpy array types are suported. We strictly advise that the response labels be encoded according the following
         simple scheme:[0,1,..N] where N is the number of classes. Said differently: if we are modeling a phenomenon with 5
         classes, the response variable should be labelled as follows : 0,1,2,3,4. You can create a dictionary mapping the integer
         encodings to whatever the 'original' class names may be a priori before the modeling efforts. Example: {0:'Negative',1:'Positive'}. 
         To train the models using the neural architectures in this module a one hot encoding of the labels is required anyways.That
         representation can be easily mapped to the type we are asking of you here.        
        :type val_labels: list or numpy array

        :param cutoff: threshold to determine predicted class in case of binary classification problems.
         This implicitly assumes that, in the case of nerual architectures, our output layer ended with softmax or sigmoid activations or
         at least that the predictions are probabilities between 0 and 1.
        :type cutoff: float

        :param show_plot: Flag to display plot of consusion matrix. Defaults to False.
        :type show_plot: boolean
        """
        error_log_dir = self.error_log_dir
        try:
            prediction = model.predict(val_data)
            #logic to convert model probabilities to class labels.
            try:
                output_dim = prediction.shape[1]
            except:
                if isinstance(prediction, list):
                    print('Expecting predictions to be a numpy array and not a list. Please Covnert: np.array(list)'\
                        'in future workflows. We will attempt coercion to array now.')
                    prediction = np.asarray(prediction)
                    #let's try again to get the shape
                    try:
                        output_dim = prediction.shape[1]
                    except:
                        #would fail if output is a one dimensional array.
                        output_dim = 1
                else:
                    #would fail if output is a one dimensional array
                    output_dim = 1

            if output_dim == 1:
                #we make the probability scores a prediction. This is a binary classification problem
                class_predictions = [
                    0 if x < cutoff else 1 for x in prediction
                ]
                # we can now build out the confusion matrix
            else:
                #code to create class predictions for multi level case
                class_predictions = [x.argmax() for x in prediction]

            # we apply the same logic to the provided actual labels : val_labels

            try:
                output_dim = val_labels.shape[1]
            except:
                if isinstance(val_labels, list):
                    val_labels = np.asarray(val_labels)
                    #let's try again to get the shape
                    try:
                        output_dim = prediction.shape[1]
                    except:
                        #would fail if output is a one dimensional array.
                        output_dim = 1
                else:
                    #would fail if output is a one dimensional array
                    output_dim = 1

            if output_dim == 1:
                #we make the probability scores a prediction. This is a binary classification problem
                actuals = list(val_labels)
                # we can now build out the confusion matrix
            else:
                #code to create class predictions for multi level case
                actuals = [x.argmax() for x in val_labels]

            cm = ConfusionMatrix(actuals, class_predictions)
            print('#######################################')
            print(
                'Let\'s study the performance of our classifier more closely:)'
            )
            print(cm)
            print('Summry Statistics:')
            print('\n')
            print('\n')
            print('Accuracy:')
            print(accuracy_score(actuals, class_predictions))
            print('\n')
            print('Classification report:')
            print(classification_report(actuals, class_predictions))
            if show_plot:
                print('Here is a plot of the confusion Matrix:')
                cm.plot()
                plt.show()
            print('#######################################')

        except Exception:
            e = traceback.format_exc()
            self.error_logger(exception_error=e, error_log_dir=error_log_dir)

    def plot_training_graph(self, training_metric, validation_metric,
                            metric_name):
        """
        Method to display the evolution of important training metrics over epoch time.

        :param training_metric:list of metrics like loss,accuracy (or some custom metric) for each epoch. Metric measured against known training labels
        :type training_metric list:

        :param validation_metric:list of metrics like loss,accuracy (or some custom metric) for each epoch. Metric measured against validation labels not part of training process
        :type validation_metric list:

        :param metric_name: name of metric (loss, accuracy..etc)
        :type metric_name: string

        """
        error_log_dir = self.error_log_dir
        try:
            trainin_metric = training_metric
            validation_metric = validation_metric

            epochs = range(1, len(trainin_metric) + 1)

            plt.plot(epochs,
                     trainin_metric,
                     'bo',
                     label='Training ' + metric_name)
            plt.plot(epochs,
                     validation_metric,
                     'r',
                     label='Validation loss ' + metric_name)
            plt.title('Training and validation ' + metric_name)
            plt.xlabel('Epochs')
            plt.ylabel(metric_name)
            plt.legend()
            plt.show()

        except Exception:
            e = traceback.format_exc()
            self.error_logger(exception_error=e, error_log_dir=error_log_dir)

    def nn_dense_layers(self,
                        train_data,
                        train_labels,
                        val_data,
                        val_labels,
                        num_epochs,
                        batch_size,
                        model_name,
                        models_output_path=''):
        """
        Method to train a neural network wth denseley connected layers. Network has following archtecture: \n
         3 layers with 16 neurons each \n
         Relu as non linear activation for each layer \n
         softmax (for mult level classification) or sigmoid (binary) activation on final output layer. \n

        :param train_data: processed training data
        :type train_data: numpy array

        :param train_labels: processed training labels (one hot encoded for multi level classification problems)
        :type train_labels: numpy array

        :param val_data: processed validation data
        :type val_data: numpy array

        :param val_labels: processed validation labels (one hot encoded for multi level classification problems)
        :type val_labels: numpy array

        :param num_epochs: Desired number of epochs to train our network
        :type num_epochs: int

        :param batch_size: Number of training samples to use in forward and backward propagation before making paramater updates.If we have 1000 samples and batch size of 100 then we will make 10 paramater updates for each epoch (SGD). For reasons beyond the scope of this documentation we should try to pick the batch size as numbers that are solutions to x=2^n for n in [4..K]
        :type batch_size: int  

        :param model_name: name of our model. This is important as our models will be saved by default.
        :type model_name: string

        :param models_output_path: directory of where we want to store our models. This is passed during class instatiation and can be overwritten here.
        :type models_output_path: string 
        """
        error_log_dir = self.error_log_dir

        try:
            if not models_output_path:
                models_output_path = self.models_output_path
            #some logic here to handle different cases
            try:
                num_classes = train_labels.shape[1]
            except:
                num_classes = 2
            if num_classes > 2:
                activation_ = 'softmax'
                loss_ = 'categorical_crossentropy'
                num_output_units = train_labels.shape[1]
            else:
                activation_ = 'sigmoid'
                loss_ = 'binary_crossentropy'
                num_output_units = 1
            print('activation:', activation_, 'AND loss:', loss_)
            model = models.Sequential()
            model.add(
                layers.Dense(16,
                             activation='relu',
                             input_shape=(train_data.shape[1], )))
            model.add(layers.Dense(16, activation='relu'))
            model.add(layers.Dense(16, activation='relu'))
            model.add(layers.Dense(num_output_units, activation=activation_))
            print('Here is a summary of the model')
            model.summary()

            model.compile(optimizer=optimizers.RMSprop(lr=0.001),
                          loss=loss_,
                          metrics=['accuracy'])
            start_time = time.time()
            history = model.fit(train_data,
                                train_labels,
                                epochs=num_epochs,
                                batch_size=batch_size,
                                validation_data=(val_data, val_labels))
            end_time = time.time()
            total_run_time = end_time - start_time
            history_name = model_name + '_history.json'
            model_name = model_name + '.h5'
            model.save(os.path.join(models_output_path, model_name))
            with open(os.path.join(models_output_path, history_name),
                      'wb') as history_dict:
                pickle.dump(history.history, history_dict)
            print('#######################')
            print('Our network trained in:', total_run_time, 'Seconds')

            print('We can display the training efforts graphically...')
            self.plot_training_graph(
                training_metric=history.history['loss'],
                validation_metric=history.history['val_loss'],
                metric_name='loss')

            self.plot_training_graph(
                training_metric=history.history['accuracy'],
                validation_metric=history.history['val_accuracy'],
                metric_name='accuracy')
            #we will now produce a more detailed view of the models performance:
            self.get_classifier_performance(model=model,
                                            val_data=val_data,
                                            val_labels=val_labels)
            print(
                'WE NOW COMPARE OUR MODEL TO THE ZERO CLASSIFER AS THE BASELINE'
            )
            self.get_zero_classsifier_performance(val_labels=val_labels,
                                                  show_plot=False)
        except Exception:
            e = traceback.format_exc()
            self.error_logger(exception_error=e, error_log_dir=error_log_dir)

    def nn_dense_layers_penalized(self,
                                  train_data,
                                  train_labels,
                                  val_data,
                                  val_labels,
                                  num_epochs,
                                  batch_size,
                                  model_name,
                                  lambda_hyper=0.001,
                                  models_output_path=''):
        """
        Method to train a neural network wth densley connected layers with l1 (Lasso) regularizer at each layer.Network has following archtecture: \n
         3 layers with 16 neurons each \n
         Relu as non linear activation for each layer \n
         L1 Kernel regularizer at each layer \n
         softmax (for mult level classification) or sigmoid (binary) activation on final output layer. \n

        :param train_data: processed training data
        :type train_data: numpy array

        :param train_labels: processed training labels (one hot encoded for multi level classification problems)
        :type train_labels: numpy array

        :param val_data: processed validation data
        :type val_data: numpy array

        :param val_labels: processed validation labels (one hot encoded for multi level classification problems)
        :type val_labels: numpy array

        :param num_epochs: Desired number of epochs to train our network
        :type num_epochs: int

        :param batch_size: Number of training samples to use in forward and backward propagation before making paramater updates.If we have 1000 samples and batch size of 100 then we will make 10 paramater updates for each epoch (SGD). For reasons beyond the scope of this documentation we should try to pick the batch size as numbers that are solutions to x=2^n for n in [4..K]
        :type batch_size: int  

        :param model_name: name of our model. This is important as our models will be saved by default.
        :type model_name: string

        :param lambda_hyper: value for lambda hyperparamater. Defaults set at 0.001
        :type lambda_hyper: float

        :param models_output_path: directory of where we want to store our models. This is passed during class instatiation and can be overwritten here.
        :type models_output_path: string 
        """
        error_log_dir = self.error_log_dir
        if not models_output_path:
            models_output_path = self.models_output_path
        #some logic here to handle different cases
        try:
            try:
                num_classes = train_labels.shape[1]
            except:
                num_classes = 2
            if num_classes > 2:
                activation_ = 'softmax'
                loss_ = 'categorical_crossentropy'
                num_output_units = train_labels.shape[1]
            else:
                activation_ = 'sigmoid'
                loss_ = 'binary_crossentropy'
                num_output_units = 1
            print('activation:', activation_, 'AND loss:', loss_)
            model = models.Sequential()
            model.add(
                layers.Dense(16,
                             kernel_regularizer=regularizers.l1(lambda_hyper),
                             activation='relu',
                             input_shape=(train_data.shape[1], )))
            model.add(
                layers.Dense(16,
                             kernel_regularizer=regularizers.l1(lambda_hyper),
                             activation='relu'))
            model.add(
                layers.Dense(16,
                             kernel_regularizer=regularizers.l1(lambda_hyper),
                             activation='relu'))
            model.add(layers.Dense(num_output_units, activation=activation_))
            print('Here is a summary of the model')
            model.summary()

            model.compile(optimizer=optimizers.RMSprop(lr=0.001),
                          loss=loss_,
                          metrics=['accuracy'])
            start_time = time.time()
            history = model.fit(train_data,
                                train_labels,
                                epochs=num_epochs,
                                batch_size=batch_size,
                                validation_data=(val_data, val_labels))
            end_time = time.time()
            total_run_time = end_time - start_time
            history_name = model_name + '_history.json'
            model_name = model_name + '.h5'
            model.save(os.path.join(models_output_path, model_name))
            with open(os.path.join(models_output_path, history_name),
                      'wb') as history_dict:
                pickle.dump(history.history, history_dict)
            print('#######################')
            print('Our network trained in:', total_run_time, 'Seconds')

            print('We can display the training efforts graphically...')
            self.plot_training_graph(
                training_metric=history.history['loss'],
                validation_metric=history.history['val_loss'],
                metric_name='loss')

            self.plot_training_graph(
                training_metric=history.history['accuracy'],
                validation_metric=history.history['val_accuracy'],
                metric_name='accuracy')
            #we will now produce a more detailed view of the models performance:
            self.get_classifier_performance(model=model,
                                            val_data=val_data,
                                            val_labels=val_labels)
            print(
                'WE NOW COMPARE OUR MODEL TO THE ZERO CLASSIFER AS THE BASELINE'
            )
            self.get_zero_classsifier_performance(val_labels=val_labels,
                                                  show_plot=False)
        except Exception:
            e = traceback.format_exc()
            self.error_logger(exception_error=e, error_log_dir=error_log_dir)

    def nn_dense_embedding(self,
                           train_data,
                           train_labels,
                           val_data,
                           val_labels,
                           max_words,
                           embedding_dimension,
                           num_epochs,
                           batch_size,
                           model_name,
                           lambda_hyper,
                           models_output_path=''):
        """
         Method to train a neural network wth learned embeddings + densley connected layers.Network has following archtecture: \n
         Embedding layer. Dimension of embedding matrix depends on size of input (vocab) and size of word embeddings \n
         L1 kernel regularizer at each dense layer (not on output layer) \n
         First dense layer with 24 neurons and relu activation (layer connected to the flattened embedding layer) \n
         Second dense layer with 16 neurons and relu activation \n
         Third dense layer with 8 neurons and relu activation  \n
         Output layer with softmax (for mult level classification) or sigmoid (binary) activation. \n

        :param train_data: processed training data
        :type train_data: numpy array

        :param train_labels: processed training labels (one hot encoded for multi level classification problems)
        :type train_labels: numpy array

        :param val_data: processed validation data
        :type val_data: numpy array

        :param val_labels: processed validation labels (one hot encoded for multi level classification problems)
        :type val_labels: numpy array

        :param max_words: max words = top N words were in vocabulary were considered
        :type max_words: int

        :param embedding_dimension: dimnesion of word embeddings we wish to learn.
        :type embedding dimension: int

        :param num_epochs: Desired number of epochs to train our network
        :type num_epochs: int

        :param batch_size: Number of training samples to use in forward and backward propagation before making paramater updates.If we have 1000 samples and batch size of 100 then we will make 10 paramater updates for each epoch (SGD). For reasons beyond the scope of this documentation we should try to pick the batch size as numbers that are solutions to x=2^n for n in [4..K]
        :type batch_size: int

        :param model_name: name of our model. This is important as our models will be saved by default.
        :type model_name: string

        :param lambda_hyper: value for lambda hyperparamater. Defaults set at 0.001
        :type lambda_hyper: float

        :param models_output_path: directory of where we want to store our models. This is passed during class instatiation and can be overwritten here.
        :type models_output_path: string 

        """
        error_log_dir = self.error_log_dir
        if not models_output_path:
            models_output_path = self.models_output_path

        try:
            max_len = train_data.shape[1]
            #some logic here to handle different cases
            try:
                num_classes = train_labels.shape[1]
            except:
                num_classes = 2
            if num_classes > 2:
                activation_ = 'softmax'
                loss_ = 'categorical_crossentropy'
                num_output_units = train_labels.shape[1]
            else:
                activation_ = 'sigmoid'
                loss_ = 'binary_crossentropy'
                num_output_units = 1
            print('activation:', activation_, 'AND loss:', loss_)
            model = models.Sequential()
            model.add(
                Embedding(max_words, embedding_dimension,
                          input_length=max_len))
            model.add(Flatten())
            model.add(
                layers.Dense(24,
                             kernel_regularizer=regularizers.l1(lambda_hyper),
                             activation='relu'))
            model.add(
                layers.Dense(16,
                             kernel_regularizer=regularizers.l1(lambda_hyper),
                             activation='relu'))
            model.add(
                layers.Dense(8,
                             kernel_regularizer=regularizers.l1(lambda_hyper),
                             activation='relu'))
            model.add(Dense(
                num_output_units,
                activation=activation_,
            ))
            print('Here is a summary of the model')
            model.summary()

            model.compile(optimizer=optimizers.RMSprop(lr=0.001),
                          loss=loss_,
                          metrics=['accuracy'])
            start_time = time.time()
            history = model.fit(train_data,
                                train_labels,
                                epochs=num_epochs,
                                batch_size=batch_size,
                                validation_data=(val_data, val_labels))
            end_time = time.time()
            total_run_time = end_time - start_time
            history_name = model_name + '_history.json'
            model_name = model_name + '.h5'
            model.save(os.path.join(models_output_path, model_name))
            with open(os.path.join(models_output_path, history_name),
                      'wb') as history_dict:
                pickle.dump(history.history, history_dict)
            print('#######################')
            print('Our network trained in:', total_run_time, 'Seconds')

            print('We can display the training efforts graphically...')
            self.plot_training_graph(
                training_metric=history.history['loss'],
                validation_metric=history.history['val_loss'],
                metric_name='loss')

            self.plot_training_graph(
                training_metric=history.history['accuracy'],
                validation_metric=history.history['val_accuracy'],
                metric_name='accuracy')
            #we will now produce a more detailed view of the models performance:
            self.get_classifier_performance(model=model,
                                            val_data=val_data,
                                            val_labels=val_labels)
            print(
                'WE NOW COMPARE OUR MODEL TO THE ZERO CLASSIFER AS THE BASELINE'
            )
            self.get_zero_classsifier_performance(val_labels=val_labels,
                                                  show_plot=False)
        except Exception:
            e = traceback.format_exc()
            self.error_logger(exception_error=e, error_log_dir=error_log_dir)

    def nn_dense_embedding_pretrained(self,
                                      train_data,
                                      train_labels,
                                      val_data,
                                      val_labels,
                                      max_words,
                                      embeddings_to_use,
                                      embedding_dimension,
                                      word_index,
                                      num_epochs,
                                      batch_size,
                                      model_name,
                                      embeddings_directory_path,
                                      lambda_hyper=0.001,
                                      models_output_path=''):
        """
         Method to train a neural network with pretrained embeddings + densley connected layers.Network has following archtecture: \n
         Embedding layer. Dimension of embedding matrix depends on size of input (vocab) and size of word embeddings \n
         L1 kernel regularizer at each dense layer (not on output layer) \n
         First dense layer with 32 neurons and relu activation (layer connected to the flattened embedding layer) \n
         Second dense layer with 24 neurons and relu activation \n
         Third dense layer with 16 neurons and relu activation  \n
         Fourth dense layer with 8 neurons and relu activation  \n
         Fifth dense layer with 4 neurons and relu activation  \n
         Output layer with softmax (for mult level classification) or sigmoid (binary) activation. \n

        :param train_data: processed training data
        :type train_data: numpy array

        :param train_labels: processed training labels (one hot encoded for multi level classification problems)
        :type train_labels: numpy array

        :param val_data: processed validation data
        :type val_data: numpy array

        :param val_labels: processed validation labels (one hot encoded for multi level classification problems)
        :type val_labels: numpy array

        :param max_words: max words = top N words were in vocabulary were considered
        :type max_words: int

        :param embeddings_to_use: choice of pretrained word embeddings to use. GloVe and word2vec are supported. For GloVe please pass GloVe. For word2vec please pass word2vec,
        :type embeddings_to_use: string

        :param embedding_dimension: dimnesion of word embeddings we wish to use in training. GloVe supports 50,100,200 and 300 dimensional word embeddings. word2vec supports 300 
        :type embedding dimension: int

        :param word_index: dictionary mapping integers to each word contained in our vocabulary. This dictionary depends on our training data and should be retrived by accessing the .word_index attribute from the pre_processing object that was used to pre-process the training data.
        :type word_index: dictionary
        
        :param num_epochs: Desired number of epochs to train our network
        :type num_epochs: int

        :param batch_size: Number of training samples to use in forward and backward propagation before making paramater updates.If we have 1000 samples and batch size of 100 then we will make 10 paramater updates for each epoch (SGD). For reasons beyond the scope of this documentation we should try to pick the batch size as numbers that are solutions to x=2^n for n in [4..K]
        :type batch_size: int

        :param model_name: name of our model. This is important as our models will be saved by default.
        :type model_name: string

        :param lambda_hyper: value for lambda hyperparamater. Defaults set at 0.001
        :type lambda_hyper: float

        :param embeddings_directory_path: file path of where word raw word embedding files live
        :type embeddings_directory_path: string

        :param models_output_path: directory of where we want to store our models. This is passed during class instatiation and can be overwritten here.
        :type models_output_path: string 
        """
        error_log_dir = self.error_log_dir
        try:
            #we frist retrieve the pretrained embeddings. We will use the pretrained_embeddings class
            embedding = pretrained_embeddings(
                project='NLP',
                embeddings_directory_path=embeddings_directory_path,
                error_log_dir=error_log_dir)

            if embeddings_to_use not in ('GloVe', 'word2vec'):
                print(
                    'You did not pass a recognized pretrained wordembedding. We are defaulting to GloVe.'
                )
                embeddings_to_use = 'GloVe'

            if embeddings_to_use == 'GloVe' and embedding_dimension not in (
                    50, 100, 200, 300):
                print('Dimension of embedding not supported for GloVe vectors. 50,100,200,300 are supported. If you want something else ' \
                    'you will have to train them yourself or learn embeddings from the data. We have a method available for this. ' \
                    'We will default to using 100d word vectors.')
                embedding_dimension = 100

            if embeddings_to_use == 'word2vec' and embedding_dimension != 300:
                print('Dimension of embedding not supported for word2vec vectors. Only 300 simensionla vectors are supported. If you want something else ' \
                    'you will have to train them yourself or learn embeddings from the data. We have a method available for this. ' \
                    'We will default to using 300d word vectors.')
                embedding_dimension = 300

            #we retrive the processed word embeddings.
            if embeddings_to_use == 'GloVe':
                embedding_index = embedding.get_glove_vecs(embedding_dimension)
            elif embeddings_to_use == 'word2vec':
                embedding_index = embedding.get_word2vec_vecs()

            #we prepare the word-embeddings matrix
            embedding_matrix = np.zeros((max_words, embedding_dimension))
            for word, i in word_index.items():
                if i < max_words:
                    embedding_vector = embedding_index.get(word)
                    if embedding_vector is not None:
                        embedding_matrix[i] = embedding_vector
            #now we can define the model architecture
            if not models_output_path:
                models_output_path = self.models_output_path
            max_len = train_data.shape[1]
            #some logic here to handle different cases
            try:
                num_classes = train_labels.shape[1]
            except:
                num_classes = 2
            if num_classes > 2:
                activation_ = 'softmax'
                loss_ = 'categorical_crossentropy'
                num_output_units = train_labels.shape[1]
            else:
                activation_ = 'sigmoid'
                loss_ = 'binary_crossentropy'
                num_output_units = 1
            print('activation:', activation_, 'AND loss:', loss_)
            model = models.Sequential()
            model.add(
                Embedding(max_words, embedding_dimension,
                          input_length=max_len))
            model.add(Flatten())
            model.add(
                Dense(32,
                      kernel_regularizer=regularizers.l1(lambda_hyper),
                      activation='relu'))
            model.add(
                Dense(24,
                      kernel_regularizer=regularizers.l1(lambda_hyper),
                      activation='relu'))
            model.add(
                Dense(16,
                      kernel_regularizer=regularizers.l1(lambda_hyper),
                      activation='relu'))
            model.add(
                Dense(8,
                      kernel_regularizer=regularizers.l1(lambda_hyper),
                      activation='relu'))
            model.add(
                Dense(4,
                      kernel_regularizer=regularizers.l1(lambda_hyper),
                      activation='relu'))
            model.add(Dense(num_output_units, activation=activation_))
            print('Here is a summary of the model')

            #we now load the pretrained word embeddings into the Embedding_layer
            model.layers[0].set_weights([embedding_matrix])
            model.layers[
                0].trainable = False  #we must freeze the embedding layer as we don't want to update these in training.
            model.summary()

            model.compile(optimizer=optimizers.RMSprop(lr=0.001),
                          loss=loss_,
                          metrics=['accuracy'])
            start_time = time.time()
            history = model.fit(train_data,
                                train_labels,
                                epochs=num_epochs,
                                batch_size=batch_size,
                                validation_data=(val_data, val_labels))
            end_time = time.time()
            total_run_time = end_time - start_time
            history_name = model_name + '_history.json'
            model_name = model_name + '.h5'
            model.save(os.path.join(models_output_path, model_name))
            with open(os.path.join(models_output_path, history_name),
                      'wb') as history_dict:
                pickle.dump(history.history, history_dict)
            print('#######################')
            print('Our network trained in:', total_run_time, 'Seconds')

            print('We can display the training efforts graphically...')
            self.plot_training_graph(
                training_metric=history.history['loss'],
                validation_metric=history.history['val_loss'],
                metric_name='loss')

            self.plot_training_graph(
                training_metric=history.history['accuracy'],
                validation_metric=history.history['val_accuracy'],
                metric_name='accuracy')
            #we will now produce a more detailed view of the models performance:
            self.get_classifier_performance(model=model,
                                            val_data=val_data,
                                            val_labels=val_labels)
            print(
                'WE NOW COMPARE OUR MODEL TO THE ZERO CLASSIFER AS THE BASELINE'
            )
            self.get_zero_classsifier_performance(val_labels=val_labels,
                                                  show_plot=False)
        except Exception:
            e = traceback.format_exc()
            self.error_logger(exception_error=e, error_log_dir=error_log_dir)

    def nn_dense_embedding_pretrained_lstm(self,
                                           train_data,
                                           train_labels,
                                           val_data,
                                           val_labels,
                                           max_words,
                                           embeddings_to_use,
                                           embedding_dimension,
                                           word_index,
                                           num_epochs,
                                           batch_size,
                                           model_name,
                                           embeddings_directory_path,
                                           models_output_path=''):
        """
         Method to train a neural network with pretrained embeddings + densley connected layers.Network has following archtecture: \n
         Embedding layer. Dimension of embedding matrix depends on size of input (vocab) and size of word embeddings \n
         First LSTM layer with 16 neurons and relu activation (layer connected to the flattened embedding layer) \n
         Second LSTM layer with 8 neurons and relu activation \n
         Third LSTM layer with 8 neurons and relu activation  \n
         Fourth LSTM layer with 4 neurons and relu activation  \n
        Output layer with softmax (for mult level classification) or sigmoid (binary) activation. \n

        :param train_data: processed training data
        :type train_data: numpy array

        :param train_labels: processed training labels (one hot encoded for multi level classification problems)
        :type train_labels: numpy array

        :param val_data: processed validation data
        :type val_data: numpy array

        :param val_labels: processed validation labels (one hot encoded for multi level classification problems)
        :type val_labels: numpy array

        :param max_words: max words = top N words were in vocabulary were considered
        :type max_words: int

        :param embeddings_to_use: choice of pretrained word embeddings to use. GloVe and word2vec are supported. For GloVe please pass GloVe. For word2vec please pass word2vec,
        :type embeddings_to_use: string

        :param embedding_dimension: dimnesion of word embeddings we wish to use in training. GloVe supports 50,100,200 and 300 dimensional word embeddings. word2vec supports 300 
        :type embedding dimension: int

        :param word_index: dictionary mapping integers to each word contained in our vocabulary. This dictionary depends on our training data and should be retrived by accessing the .word_index attribute from the pre_processing object that was used to pre-process the training data.
        :type word_index: dictionary
        
        :param num_epochs: Desired number of epochs to train our network
        :type num_epochs: int

        :param batch_size: Number of training samples to use in forward and backward propagation before making paramater updates.If we have 1000 samples and batch size of 100 then we will make 10 paramater updates for each epoch (SGD). For reasons beyond the scope of this documentation we should try to pick the batch size as numbers that are solutions to x=2^n for n in [4..K]
        :type batch_size: int

        :param model_name: name of our model. This is important as our models will be saved by default.
        :type model_name: string

        :param embeddings_directory_path: file path of where word raw word embedding files live
        :type embeddings_directory_path: string

        :param models_output_path: directory of where we want to store our models. This is passed during class instatiation and can be overwritten here.
        :type models_output_path: string 
        """
        #we frist retrieve the pretrained embeddings. We will use the pretrained_embeddings class
        error_log_dir = self.error_log_dir
        try:
            embedding = pretrained_embeddings(
                project='NLP',
                embeddings_directory_path=embeddings_directory_path,
                error_log_dir=error_log_dir)

            if embeddings_to_use not in ('GloVe', 'word2vec'):
                print(
                    'You did not pass a recognized pretrained wordembedding. We are defaulting to GloVe.'
                )
                embeddings_to_use = 'GloVe'

            if embeddings_to_use == 'GloVe' and embedding_dimension not in (
                    50, 100, 200, 300):
                print('Dimension of embedding not supported for GloVe vectors. 50,100,200,300 are supported. If you want something else ' \
                    'you will have to train them yourself or learn embeddings from the data. We have a method available for this. ' \
                    'We will default to using 100d word vectors.')
                embedding_dimension = 100

            if embeddings_to_use == 'word2vec' and embedding_dimension != 300:
                print('Dimension of embedding not supported for word2vec vectors. Only 300 simensionla vectors are supported. If you want something else ' \
                    'you will have to train them yourself or learn embeddings from the data. We have a method available for this. ' \
                    'We will default to using 300d word vectors.')
                embedding_dimension = 300

            #we retrive the processed word embeddings.
            if embeddings_to_use == 'GloVe':
                embedding_index = embedding.get_glove_vecs(embedding_dimension)
            elif embeddings_to_use == 'word2vec':
                embedding_index = embedding.get_word2vec_vecs()

            #we prepare the word-embeddings matrix
            embedding_matrix = np.zeros((max_words, embedding_dimension))
            for word, i in word_index.items():
                if i < max_words:
                    embedding_vector = embedding_index.get(word)
                    if embedding_vector is not None:
                        embedding_matrix[i] = embedding_vector
            #now we can define the model architecture
            if not models_output_path:
                models_output_path = self.models_output_path
            max_len = train_data.shape[1]
            #some logic here to handle different cases
            try:
                num_classes = train_labels.shape[1]
            except:
                num_classes = 2
            if num_classes > 2:
                activation_ = 'softmax'
                loss_ = 'categorical_crossentropy'
                num_output_units = train_labels.shape[1]
            else:
                activation_ = 'sigmoid'
                loss_ = 'binary_crossentropy'
                num_output_units = 1
            print('activation:', activation_, 'AND loss:', loss_)
            model = models.Sequential()
            model.add(
                Embedding(max_words, embedding_dimension,
                          input_length=max_len))
            model.add(LSTM(units=16, return_sequences=True))
            model.add(Dropout(0.3))
            model.add(LSTM(units=8, return_sequences=True))
            model.add(Dropout(0.3))
            model.add(LSTM(units=8, return_sequences=True))
            model.add(Dropout(0.3))
            model.add(LSTM(units=4))
            model.add(Dense(num_output_units, activation=activation_))
            print('Here is a summary of the model')

            #we now load the pretrained word embeddings into the Embedding_layer
            model.layers[0].set_weights([embedding_matrix])
            model.layers[
                0].trainable = False  #we must freeze the embedding layer as we don't want to update these in training.
            model.summary()

            model.compile(optimizer=optimizers.RMSprop(lr=0.001),
                          loss=loss_,
                          metrics=['accuracy'])
            start_time = time.time()
            history = model.fit(train_data,
                                train_labels,
                                epochs=num_epochs,
                                batch_size=batch_size,
                                validation_data=(val_data, val_labels))
            end_time = time.time()
            total_run_time = end_time - start_time
            history_name = model_name + '_history.json'
            model_name = model_name + '.h5'
            model.save(os.path.join(models_output_path, model_name))
            with open(os.path.join(models_output_path, history_name),
                      'wb') as history_dict:
                pickle.dump(history.history, history_dict)
            print('#######################')
            print('Our network trained in:', total_run_time, 'Seconds')

            print('We can display the training efforts graphically...')
            self.plot_training_graph(
                training_metric=history.history['loss'],
                validation_metric=history.history['val_loss'],
                metric_name='loss')

            self.plot_training_graph(
                training_metric=history.history['accuracy'],
                validation_metric=history.history['val_accuracy'],
                metric_name='accuracy')
            #we will now produce a more detailed view of the models performance:
            self.get_classifier_performance(model=model,
                                            val_data=val_data,
                                            val_labels=val_labels)
            print(
                'WE NOW COMPARE OUR MODEL TO THE ZERO CLASSIFER AS THE BASELINE'
            )
            self.get_zero_classsifier_performance(val_labels=val_labels,
                                                  show_plot=False)
        except Exception:
            e = traceback.format_exc()
            self.error_logger(exception_error=e, error_log_dir=error_log_dir)

    def nn_1dcovnet_learned_embeddings(self,
                                       train_data,
                                       train_labels,
                                       val_data,
                                       val_labels,
                                       max_words,
                                       embedding_dimension,
                                       num_epochs,
                                       batch_size,
                                       model_name,
                                       dropout_rate,
                                       lambda_hyper,
                                       models_output_path=''):
        """
         Method to train a neural network wth learned embeddings + Conv1d and dense layers.Network has following archtecture: \n
         Embedding layer. Dimension of embedding matrix depends on size of input (vocab) and size of word embeddings \n
         L1 kernel regularizer at each dense layer (not on output layer) \n
         First conv layer: 32 filters and a kernel of size 9 \n
         dropout layer \n
         Second conv layer with 16 filters and kernel of size 9 \n
         dropout layer \n
         Third conv layer with 8 filters and kernel of size 7 \n
         MaxPooling Layer --this will reduce dimensionalioty -- \n
         Fourth conv layer with 8 filters and kernel size of 5 \n
         Flattened layer
         Dense Layer with 8 neurons and non linear relu activation \n
         Dense Layer with 4 neurons and non linear relu activation \n
         Output layer with softmax (for mult level classification) or sigmoid (binary) activation. \n

        :param train_data: processed training data
        :type train_data: numpy array

        :param train_labels: processed training labels (one hot encoded for multi level classification problems)
        :type train_labels: numpy array

        :param val_data: processed validation data
        :type val_data: numpy array

        :param val_labels: processed validation labels (one hot encoded for multi level classification problems)
        :type val_labels: numpy array

        :param max_words: max words = top N words were in vocabulary were considered
        :type max_words: int

        :param embedding_dimension: dimnesion of word embeddings we wish to learn.
        :type embedding dimension: int

        :param num_epochs: Desired number of epochs to train our network
        :type num_epochs: int

        :param batch_size: Number of training samples to use in forward and backward propagation before making paramater updates.If we have 1000 samples and batch size of 100 then we will make 10 paramater updates for each epoch (SGD). For reasons beyond the scope of this documentation we should try to pick the batch size as numbers that are solutions to x=2^n for n in [4..K]
        :type batch_size: int

        :param model_name: name of our model. This is important as our models will be saved by default.
        :type model_name: string

        :param lambda_hyper: value for lambda hyperparamater. Defaults set at 0.001
        :type lambda_hyper: float

        :param models_output_path: directory of where we want to store our models. This is passed during class instatiation and can be overwritten here.
        :type models_output_path: string 

        """
        error_log_dir = self.error_log_dir
        if not models_output_path:
            models_output_path = self.models_output_path

        try:
            max_len = train_data.shape[1]
            #some logic here to handle different cases
            try:
                num_classes = train_labels.shape[1]
            except:
                num_classes = 2
            if num_classes > 2:
                activation_ = 'softmax'
                loss_ = 'categorical_crossentropy'
                num_output_units = train_labels.shape[1]
            else:
                activation_ = 'sigmoid'
                loss_ = 'binary_crossentropy'
                num_output_units = 1
            print('activation:', activation_, 'AND loss:', loss_)
            model = models.Sequential()
            model.add(
                Embedding(max_words, embedding_dimension,
                          input_length=max_len))
            model.add(layers.Conv1D(32, 9, activation='relu'))
            model.add(layers.Dropout(dropout_rate))
            model.add(layers.Conv1D(16, 9, activation='relu'))
            model.add(layers.Dropout(dropout_rate))
            model.add(layers.Conv1D(8, 7, activation='relu'))
            model.add(layers.MaxPooling1D(4))
            model.add(layers.Conv1D(8, 5, activation='relu'))
            model.add(Flatten())
            model.add(
                Dense(8,
                      kernel_regularizer=regularizers.l1(lambda_hyper),
                      activation='relu'))
            model.add(
                Dense(4,
                      kernel_regularizer=regularizers.l1(lambda_hyper),
                      activation='relu'))
            model.add(Dense(
                num_output_units,
                activation=activation_,
            ))
            print('Here is a summary of the model')
            model.summary()

            model.compile(optimizer=optimizers.RMSprop(lr=0.001),
                          loss=loss_,
                          metrics=['accuracy'])
            start_time = time.time()
            history = model.fit(train_data,
                                train_labels,
                                epochs=num_epochs,
                                batch_size=batch_size,
                                validation_data=(val_data, val_labels))
            end_time = time.time()
            total_run_time = end_time - start_time
            history_name = model_name + '_history.json'
            model_name = model_name + '.h5'
            model.save(os.path.join(models_output_path, model_name))
            with open(os.path.join(models_output_path, history_name),
                      'wb') as history_dict:
                pickle.dump(history.history, history_dict)
            print('#######################')
            print('Our network trained in:', total_run_time, 'Seconds')

            print('We can display the training efforts graphically...')
            self.plot_training_graph(
                training_metric=history.history['loss'],
                validation_metric=history.history['val_loss'],
                metric_name='loss')

            self.plot_training_graph(
                training_metric=history.history['accuracy'],
                validation_metric=history.history['val_accuracy'],
                metric_name='accuracy')
            #we will now produce a more detailed view of the models performance:
            self.get_classifier_performance(model=model,
                                            val_data=val_data,
                                            val_labels=val_labels)
            print(
                'WE NOW COMPARE OUR MODEL TO THE ZERO CLASSIFER AS THE BASELINE'
            )
            self.get_zero_classsifier_performance(val_labels=val_labels,
                                                  show_plot=False)
        except Exception:
            e = traceback.format_exc()
            self.error_logger(exception_error=e, error_log_dir=error_log_dir)