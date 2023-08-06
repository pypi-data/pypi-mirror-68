import os
import numpy as np
import re
import datetime
import pandas as pd
from collections import Counter
from math import log
from keras.preprocessing.text import Tokenizer
import random
import traceback


class predict_newdata:
    """The purpose of this class is to lay forth methods that can be used to prepare incoming live data for our language modeling tasks.
    Specifically we must have a pipeline that can accept new raw text data and prepare it in such a way that we can use
    our trained models to make predictions.
    In the class constructor we have logic to ensure that the data_file_path instance variable leads to a delimited tabular dataset with
    two columns: text_id,text. Please prepare your test data in the same way to use this class. NOTE: there is no label column here. 
    This is because in a model deployment setting the labels are unknown...
    Please note you will also need to provide to tokenizer object from the instance of the pre_processing class you utilized to prepare
    your train data. It can be accessed via the attribute object.tokenizer \n

    Instance variables to pass during instantiation:

    :param project: The name of the project you are using the class for
    :type project: string

    :param data_file_path: file path of where samples to predict on live. Data must be structured in tabular format: text_id,text columns.
    :type data_file_path: string

    :param seperator: delimiter used in training data file
    :type seperator: string

    :param tokenizer_object: tokenizer object that was used to fit data that model we want to predict with was trained on. The pre_processing module by default saves the tokenizer object to a pickle file. Read it in please.
    :type tokenizer_object: dict

    :param predictions_output_path: file path of where predicted sentiment should be written to \n
    :type predictions_output_path: string

    :param error_log_dir: file path of where our error log files should be written to
    :type error_log_dir: string

    Documentation on our methods can be found below: \n
    """
    def __init__(self, project, data_file_path, seperator, tokenizer_object,
                 predictions_output_path, error_log_dir):
        self.project = project
        self.data_file_path = data_file_path
        #seperator used in our raw data file
        self.seperator = seperator
        self.predictions_output_path = predictions_output_path
        self.error_log_dir = error_log_dir
        #data frame of our data
        self.text_data = pd.read_csv(data_file_path, sep=seperator)
        try:
            self.text_id = list(self.text_data['text_id'])
            self.text = list(self.text_data['text'])
        except:
            print(
                'Input data does not follow specified format... Please make sure the following columns are present: text_id,text.'
            )
            print(
                'Please check input data and instantiate and instance of the class again.Do so until the error above disappers.'
            )
        #will rearrange dataframe so that consistent ordering of columns is preserved. Might seem unimportant but I want this for
        #ease of downstream coding
        self.text_data = pd.DataFrame({
            'text_id': self.text_id,
            'text': self.text,
        })

        self.tokenizer = tokenizer_object
        # I will set the word_index as an attribute as well
        self.word_index = self.tokenizer.word_index
        # I will attach the sequences as an attribute as well
        self.sequences = np.array(self.tokenizer.texts_to_sequences(self.text))

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

    def to_one_hot_ecoding(self):
        """
        Method to create one hot encoded vectors of our data. Method does not accept arguments. This will operate on the samples that are stored as an attribute during the instantiation of the class.
        
        :returns: one hot encodded vectors of our samples
        :rtype: 2D numpy array
        """
        error_log_dir = self.error_log_dir
        try:
            one_hot_results = self.tokenizer.texts_to_matrix(self.text,
                                                             mode='binary')
            return (one_hot_results)

        except Exception:
            e = traceback.format_exc()
            self.error_logger(exception_error=e, error_log_dir=error_log_dir)

    def to_tfidf_ecoding(self):
        """
        Method to compute the tf-idf vectors of our samples. Method does not accept arguments. This will operate on the samples that are stored as an attribute during the instantiation of the class.
        
        :returns: tf-idf vectors of our samples
        :rtype: 2D numpy array

        """
        error_log_dir = self.error_log_dir
        try:
            tfidf_results = self.tokenizer.texts_to_matrix(self.text,
                                                           mode='tfidf')
            return (tfidf_results)

        except Exception:
            e = traceback.format_exc()
            self.error_logger(exception_error=e, error_log_dir=error_log_dir)

    def make_predictions(self,
                         model,
                         processed_data,
                         cutoff=0.5,
                         output_file_name=None):
        """
        Method to make predictions on unseen new data. By default the method will return predictions but also write them to a file if a file name is provided.

        :param model: model object we want to use to make the predictionss
        :type model: model object

        :param processed_data: data to predict on processed and shaped in the format the model expects
        :type processed_data: numpy array

        :param cutoff: in the case of binary predictions this cutoff will be used to assign class labels. Defaults to 0.5
        :type cutoff: float

        :returns class_predictions: predicted classes
        :rtype class_predictions: list

        :returns predictions: probability distribution of all class labels
        :rtype predictions: numpy array

        """
        error_log_dir = self.error_log_dir
        try:
            prediction = model.predict(processed_data)
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

            if output_file_name is not None:
                output_file_name = os.path.join(self.predictions_output_path,
                                                output_file_name)
                print('writing predictions to disk...', output_file_name)
                with open(output_file_name, 'w') as of:
                    for x, y, z in zip(self.text_id, self.text,
                                       class_predictions):
                        of.write(str(x) + '\t' + str(y) + '\t' + str(z) + '\n')
            else:
                print(
                    'Not writing predictions to disk... add a name to the output_file_name argument if you wish to have results written to disk.'
                )
            return (class_predictions, prediction)

        except Exception:
            e = traceback.format_exc()
            self.error_logger(exception_error=e, error_log_dir=error_log_dir)
