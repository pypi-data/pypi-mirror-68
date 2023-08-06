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
import pickle


class pre_processing:
    """The purpose of this class is to lay forth methods that can be used to prepare text data for language modeling tasks. Specifically we 
    will provide funcionality to convert raw text to numeric vector representations (vectorizing text) in some vector space in R^n.
    Different methods will be made available to prepare the data for different modeling approaches. 
    In the class constructor we have logic to ensure that the data_file_path instance variable leads to a delimited tabular 
    dataset with three columns: text_id,text,label. Please prepare your training data in the same way to use this class.
    Below are the different vector representations that this module currently supports: \n
    1. One hot encoded vectors  
    2. Tf-idf weighted vectors
    3. Dense vectors \n 
    This class was designed with the idea of providing the user flexibility in his/her modellng efforts. To achieve this end
    I believe it is appropriate to make the user aware of the attributes that are attached to each instance of this class upon instantiation. \n
    1. self.text_data : pandas dataframe containing our text_data
    2. self.text_id : list of ids identifying unique samples in our data
    3. self.text : list of our text samples
    4. self.label : list of our training labels
    5. self.dict_count : dictionary mapping each word in our corpus to its frequency
    6. self.number_distinct_words : int storing number of distinct words in our corpus
    7. self.max_words : Top N words that will be considered in our modeling. max_words sets this threshold. If not passed in class instantitation logic will be triggered to compute a reasonable value 
    8. self.tokenizer : tokenizer object used to fit our data and generate our vectors. This object is important.
    9. self.word_index : dictionary mapping each word (that was retained as dictated by the max_words parameter) in our corpus to an integer. These integers, organized in sequences, are what will be used by some of our networks.
    10. self.sequences : 2D numpy array storing each sample as an array of integer sequences
    11. self.class_distribution : dictionary mapping each class label to its frequency. In the case of binary data it would look something like {0:M,1:N} where M,N are some integers
    12. self.data_balance_stat : float representing a level of balance of our dataset. Shannon entropy is used to compute this metric.\n
    
    Instance variables to pass during instantiation:

    :param project: The name of the project you are using the class for
    :type project: string

    :param data_file_path: file path of training data
    :type data_file_path: string

    :param seperator: delimiter used in training data file
    :type seperator: string

    :param error_log_dir: file path of where our error log files should be written to
    :type error_log_dir: string

    :param tokenizer_dir: file path of where our tokenizer object should be written to. This will be needed if these models need to be used ot make predictions on future data
    :type tokenizer_dir: string

    :param max_words: Top N words that will be considered in our modeling. max_words sets this threshold.
    :type max_words: int

    Documentation on our methods can be found below: \n
    """
    def __init__(self,
                 project,
                 data_file_path,
                 seperator,
                 error_log_dir,
                 tokenizer_dir,
                 max_words=''):

        self.project = project
        self.data_file_path = data_file_path
        #seperator used in our raw data file
        self.seperator = seperator
        self.error_log_dir = error_log_dir
        self.tokenizer_dir = tokenizer_dir
        #data frame of our data
        self.text_data = pd.read_csv(data_file_path, sep=seperator)
        try:
            self.text_id = list(self.text_data['text_id'])
            self.text = list(self.text_data['text'])
            self.label = list(self.text_data['label'])
        except:
            print(
                'Input data does not follow specified format... Please make sure the following columns are present: text_id,text,label.'
            )
            print(
                'Please check input data and instantiate and instance of the class again.Do so until the error above disappers.'
            )
        #will rearrange dataframe so that consistent ordering of columns is preserved. Might seem unimportant but I want this for
        #ease of downstream coding
        self.text_data = pd.DataFrame({
            'text_id': self.text_id,
            'text': self.text,
            'label': self.label
        })

        #attribute that stores word frequencies. We use this to set default behavior for our to_one_hot_ecoding & to_tfidf_ecoding
        #methods. These methods require that a user specify dimensionality of their vector space (i.e the number of unique words to
        # preserve in the vocabulary). This is hard to do intellignelty without knowing how big the vacabulary space is. This
        #atrribute allows for users to check that on the fly after class instantiation.
        self.dict_count = {}
        for x in list(self.text):
            try:
                words = x.split(' ')
                for word in words:
                    if word in self.dict_count:
                        #increment count of word by 1
                        self.dict_count[word] = self.dict_count[word] + 1
                    else:
                        #add word to dictionary with count of 1
                        self.dict_count[word] = 1
            except:
                pass
        #we extract this from the dict above created above.
        self.number_distinct_words = len(self.dict_count)
        #here we set the max_words if it is not passed. Max words is indicating that the TOP N words in teh corpus will
        #be included in our vocabulary
        if not max_words:
            self.max_words = int(self.number_distinct_words * .75)
        else:
            self.max_words = max_words
        # I will now vectorizer the corpus. I do this here so i can attach the tokenizer object as an attribute of the class
        tokenizer = Tokenizer(num_words=self.max_words)
        tokenizer.fit_on_texts(self.text)
        self.tokenizer = tokenizer
        #we will save the tokenizer to disk. Users may need to make prediction on live test data in the future
        #they will need the tokenizer object to do this. By saving it to disk they will always have it available
        tokenizer_file = os.path.join(tokenizer_dir,
                                      'tokenizer_object_' + project + '.pkl')
        with open(tokenizer_file, 'wb') as tk:
            pickle.dump(tokenizer, tk, pickle.HIGHEST_PROTOCOL)
        print('Tokenizer object written to:', tokenizer_file)
        print('To load in the future use the following code:', '\n',
              'with open(path_to_pkl file) as tk:', '\n',
              '     tokenizer=pickle.load(tk)')
        # I will set the word_index as an attribute as well
        self.word_index = self.tokenizer.word_index
        # I will attach the sequences as an attribute as well
        self.sequences = np.array(self.tokenizer.texts_to_sequences(self.text))
        #attribute that holds the class distribution. We will use this in a method of this class to provide some hedge against
        #over/under sampling when creating train/val datasets. Users will be able to turn 'off' this behavior and can opt for
        #random paritioning if they so choose
        self.class_distribution = Counter(self.label)
        self.data_balance_stat = self.shannon_entropy(self.class_distribution)
        if len(self.class_distribution) == 2:
            try:
                self.labels_as_array = np.asarray(self.label).astype('float')
            except:
                print(
                    'Is you binary response variable coded as type float or int? If not we would recommend making it of type int or float.'
                )
                print(
                    'If you make that change you will be able to acces the labels_as_array_attribute which you need to create your tensors'
                )
        print('Thank you for using the pre_processing class for your:',
              self.project, 'project.')
        print(
            'We have done some quick data exploration and calculated the dimensions of your vacabulary space.'
        )
        print(
            'You have', self.number_distinct_words,
            'unique words in your text. Depending on your approach you may want to '\
            'remove words (stop words etc..). There is a built in method (remove_words_from_samples) '\
            'in the data_cleaning class to help with this.'
        )

        if self.number_distinct_words > 5000:
            print(
                'You may want to explore using dense lower dimensional word embeddings learned from you data'\
                '(or pre-trained from elsewhere) for this task..\nWe have methods in this package available to '\
                'you to build out models of this nature.')

        print(
            'Level of balance of our dataset (measured using shannon entropy):',
            self.data_balance_stat)

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

    def shannon_entropy(self, dict_dist):
        """
        Method to compute statistic that we can use as a measure of balance of a dataset.
        values close to 0 indicate an unbalanced dataset whereas values close to 1 indicatae a balanced dataset.

        :param dict_dist: a dictionary mapping each value of the response variable to it's frequency. This is a dictionary that holds the distribution information of our data
        :type dict_dist: dictionary

        :returns balance: a measure of balance of our data set
        :rtype balance: float

        """
        error_log_dir = self.error_log_dir
        try:
            k = len(dict_dist)  #number of classes
            n = 0  #we compute number of observations by iterating through our dicrionary
            for key in dict_dist:
                n += dict_dist[key]
            H = 0
            for key in dict_dist:
                ci = dict_dist[key]
                H_i = (ci / n) * log(ci / n)
                H += H_i
            H = -1 * H
            balance = H / log(k)
            return (balance)

        except Exception:
            e = traceback.format_exc()
            self.error_logger(exception_error=e, error_log_dir=error_log_dir)

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

    def to_one_hot_labels(self):
        """
        Method to convert our labels to one_hot vectors. Example: if we have a classification task where the response variable can
        be one of thre classes A,B,C the one hot represenatation of one of these responses would be: [1,0,0],[0,1,0],[0,0,1]. Our
        neural architectures ask for our labels to be structured in this way. For binary classification this is not necessary.
        Method does not accept arguments. This will operate on the samples that are stored as an attribute during the instantiation
        of the class.

        :returns: array of one hot encoded resposes labels
        :rtype: 2D array
        """
        #we compute the number of unique classes --> this will be the dimension of each of our one hot encoded vectors
        error_log_dir = self.error_log_dir
        try:
            labels = self.label
            dimension = len(set(labels))
            results = np.zeros((len(labels), dimension))
            for i, label in enumerate(labels):
                results[i, label] = 1
            return (results)

        except Exception:
            e = traceback.format_exc()
            self.error_logger(exception_error=e, error_log_dir=error_log_dir)

    def train_split(self,
                    train,
                    labels,
                    train_split_proportion=.80,
                    return_original_label=True,
                    balance=True):
        """
        Method to split our data in train and validation. Logic is built in to catch potential imbalances in the data
        set. If triggered an algorithm that will select the train samples more carefully as to preserve uniformity across class
        distribution will be implemented. The algorithm (very naive at this point) will be triggered if and only if the data set is perceived to lack balance
        (shannon entropy used to determine this) AND if the balance flag is enabled AND if the selection algortihm won't cannibilize 
        our training set. If either one of those three conditions is not satisfied, then the data will be split according to the proportion
        indicated by the user.

        :param train: samples we wish to split.
        :type train: 2D numpy array

        :param labels: sample labels
        :type labels: numpy array

        :param train_split_proportion: Proportion of samples to be used for training. Defaults to .80
        :type train_split_proportion: float (0,1)

        :param balance: Flag to indicate whether the data balancing algorithm should be initiated (if appropriate conditions are met). Defaults to true.The algorithm will ensure that training data will be assmebled by putting a constraint on the number of samples to be selected from each class.
        :type balance: boolean

        """
        error_log_dir = self.error_log_dir

        try:
            class_distribution = self.class_distribution
            orig_labels = self.label.copy()

            #let's compute the frequency of the smallest class
            key_min_freq = min(class_distribution.keys(),
                               key=(lambda k: class_distribution[k]))
            min_freq = class_distribution[key_min_freq]
            #key_max_freq = max(class_distribution.keys(),
            #key=(lambda k: class_distribution[k]))
            #max_freq = class_distribution[key_max_freq]
            #number of classes
            nclasses = len(class_distribution)
            #number of samples
            N = len(labels)
            #total number of samples in the case of selection algorithm being delpoyed
            max_samples_min_class = int(train_split_proportion * min_freq)
            N_prime = max_samples_min_class * nclasses
            #computation of number of samples lost in training to balance the data
            loss_samples = N - N_prime
            percent_loss = loss_samples / N  #if we lose more than 60 percent and have fewer than 4000 samples of data then we won't activate the algorithm
            if balance and self.data_balance_stat < .98 and percent_loss < .60 and (
                    N - loss_samples > 4000):
                #balance logic is enabled and shannon entropy score is below a threshold (.98) that I determined
                #this is hard and the choice is somewhat arbitrary. Warning messages will be displayed here to notify user
                #about this nehavior. Option can be disabled.
                print('Sample selection algorithm initiated to generate a balnced train set. If this behavior is not wanted '\
                    'please turn balance flag to false.')
                #we need to map each response value to a list of indices. We will store this in a dictionary
                list_of_values = [x for x in class_distribution]
                index_dict = {}
                for val in list_of_values:
                    #let's get all indices for a particular value
                    index_vals = [
                        i for i in range(len(orig_labels))
                        if orig_labels[i] == val
                    ]
                    index_dict.update({val: index_vals})
                #now we need get train and validation indices for each class
                random_index_dict = {}
                for val in list_of_values:
                    #will shuffle list of indices from index_dict
                    random_index = random.sample(index_dict[val],
                                                 len(index_dict[val]))
                    random_index_dict.update({val: random_index})

                val_indices_dict = {}
                train_indices_dict = {}
                for val in list_of_values:
                    sample_candidates = random_index_dict[val]
                    train_indices = sample_candidates[0:max_samples_min_class]
                    val_indices = sample_candidates[max_samples_min_class:]
                    train_indices_dict.update({val: train_indices})
                    val_indices_dict.update({val: val_indices})

                # extract list of trand and val indices
                train_index_list = list(train_indices_dict.values())
                train_index_list = [
                    item for sublist in train_index_list for item in sublist
                ]
                #let's shuffle so it doesn't appear strange
                #now validation list
                train_index_list = random.sample(train_index_list,
                                                 len(train_index_list))
                val_index_list = list(val_indices_dict.values())
                val_index_list = [
                    item for sublist in val_index_list for item in sublist
                ]
                #let's shuffle so it doesn't appear strange
                val_index_list = random.sample(val_index_list,
                                               len(val_index_list))
                train_data = train[train_index_list]
                val_data = train[val_index_list]
                train_labels = labels[train_index_list]
                val_labels = labels[val_index_list]
                if return_original_label:
                    #will return original labels as well as one hot encoded labels so that also linear classifier can be trained
                    #train_original_labels = orig_labels[train_index_list]
                    train_original_labels = [
                        orig_labels[i] for i in train_index_list
                    ]
                    #val_original_labels = orig_labels[val_index_list]
                    val_original_labels = [
                        orig_labels[j] for j in val_index_list
                    ]
                    return (train_data, train_labels, train_original_labels,
                            val_data, val_labels, val_original_labels)
                else:
                    return (train_data, train_labels, val_data, val_labels)
            else:
                #balance logic is enabled. If shannon entropy score is below a threshold (.97)
                #balance logic shut off.. proceeed to split data according to proportion indicated
                #number of samples
                N = len(labels)
                #number of train samples
                N_t = int(train_split_proportion * N)
                #number of validation samples
                #N_v = 1 - N_t
                #random indices for train data
                random_indices = random.sample(range(0, N), N)
                indices_train = random_indices[0:N_t]
                indices_val = random_indices[N_t:]

                train_data = train[indices_train]
                val_data = train[indices_val]
                train_labels = labels[indices_train]
                val_labels = labels[indices_val]
                if return_original_label:
                    #will return original labels as well as one hot encoded labels so that also linear classifier can be trained
                    #train_original_labels = orig_labels[indices_train]
                    train_original_labels = [
                        orig_labels[i] for i in indices_train
                    ]
                    #val_original_labels = orig_labels[indices_val]
                    val_original_labels = [orig_labels[j] for j in indices_val]
                    return (train_data, train_labels, train_original_labels,
                            val_data, val_labels, val_original_labels)
                else:
                    return (train_data, train_labels, val_data, val_labels)

        except Exception:
            e = traceback.format_exc()
            self.error_logger(exception_error=e, error_log_dir=error_log_dir)