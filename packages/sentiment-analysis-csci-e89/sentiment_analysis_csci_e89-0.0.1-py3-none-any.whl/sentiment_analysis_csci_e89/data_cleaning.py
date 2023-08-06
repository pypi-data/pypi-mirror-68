import os
import string
import re
import pandas as pd


class data_cleaning:
    """
    The purpose of this class is to lay forth methods that can be used to clean the raw text data for a few sample data sets.
    The cleaning of the data should preceed the processing of the data. Cleaning as we define it here, is concerned with making
    sure the text data does not contain any suspicious characters, and that the data is shaped in a specific structure. The other modules
    require a specifc shape of the raw text data. If you plan on using the modules in the package on data sets not supported by this class,
    (that is the hope) we recommend that you perform whatever cleaning tasks you feel appropriate a priori with your own custom written class.
    We ask that you finish by structuring the data as follows: \n  
    Delimited tabular dataset (our recommendation but any other seperator is supported) with three columns: text_id,text,label.

    Instance variables to pass during instantiation:
    :param project: The name of the project you are using the class for.
    :type project: string

    Documentation on our methods can be found below: \n    
    """
    def __init__(self, project):
        self.project = project
        print('Thank you for using the data cleaning class for:', self.project)

    def remove_words_from_samples(self, remove_words, samples):
        """
        Method to remove a list of words from our text (samples). The method accepts text to remove in a list.  

        :param remove_words: words to remove from our raw text
        :type remove_words: list

        :param samples: our raw text data (each sample is a unit of analysis. Could be a sentence or a paragraph. Some body of text). \n
        The method assumes that our samples are stored in a list. samples =['This book is great','The product is terrible']. \n
        :type samples: list

        :returns: samples devoid of the words we requested to remove
        :rtype: list 
        """
        remove_words = set(remove_words)

        #code to remove set of keywords for list of text
        samples_final = [
            ' '.join(w for w in text.split() if w not in remove_words)
            for text in samples
        ]

        return (samples_final)

    def text_processing(self, string_to_clean):
        """
        Generic method for superficial string processing. This helper method is used by many other methods to clean text in a very superficial way.
        All non printable characters (anything that isn't a number, letter or punctutation) are removed. All characters are changed to lower.

        :param string_to_clean: string of characters we want to clear
        :type string_to_clean: string
        
        :returns: a cleaned string devoid of non printable characters.
        :rtype: string

        """
        printable = set(string.printable)
        cleaned_string = ''.join(
            filter(lambda x: x in printable, string_to_clean))
        cleaned_string = re.sub('\n', '', cleaned_string)
        cleaned_string = cleaned_string.lower()
        #let's remove redundant white space
        cleaned_string = re.sub(' +', ' ', cleaned_string)
        #remove trailing and leading white space
        cleaned_string = cleaned_string.strip()

        return (cleaned_string)

    def rotten_tomato_reshape_train(self, data_file_path_train, output_path):
        """
        Method to clean and restructure the rotten tomato train dataset. Turns out the data was provided in a peculiar format and we need
        to do some prep work to make it usable for our tasks. Original Data was retrieved from here: \n
        https://www.kaggle.com/c/sentiment-analysis-on-movie-reviews/data \n
        Once this method is called an output file will be generated contaning data that can be immediately processed by the methods in 
        our pre_processing module.

        :param data_file_path_train: file path of train.tsv file downloaded from link above.
        :type data-file_path_train: string

        :param output_path: directory path of where cleaned train data should be written to.
        :type output_path: string
        """
        text_ID_train = []
        text_train = []
        label_train = []

        with open(data_file_path_train) as train:
            counter_ = 0
            for line in train:
                #split line by tab delimiter
                line_split = line.split('\t')
                text_ID_str = line_split[1]
                text_str = line_split[2]
                label_str = line_split[3]
                if counter_ == 1:
                    text_ID_train.append(text_ID_str)
                    text_train.append(text_str)
                    label_train.append(label_str)
                elif counter_ > 1 and text_ID_str == text_ID_train[-1]:
                    pass
                elif counter_ > 1 and text_ID_str != text_ID_train[-1]:
                    text_ID_train.append(text_ID_str)
                    text_train.append(text_str)
                    label_train.append(label_str)
                counter_ += 1

        #will make all text lower
        text_train = [x.lower() for x in text_train]
        #noticed somethng funky in text data. everytime a ' is present the test is fromated as such : word 'X. I will fix this

        text_train_mod = []
        count_ = 0
        for x in text_train:
            search_res = re.search(r' \'[a-z]*', x)
            if not search_res:
                text_train_mod.append(x)
            else:
                count_ += 1
                res = search_res.group()
                res_strip = res.strip()
                x = re.sub(res, res_strip, x)
                text_train_mod.append(x)

        #second problem pattern won't appears as wo n't. Will fix this
        text_train_mod2 = []
        for x in text_train_mod:
            search_res = re.search(r' n\'[a-z]*', x)
            if not search_res:
                text_train_mod2.append(x)
            else:
                res = search_res.group()
                res_strip = res.strip()
                x = re.sub(res, res_strip, x)
                text_train_mod2.append(x)

        #some problematic patterns we should remove:
        remove_words = {'--', '-rrb-', '-lrb-'}
        text_train_final = self.remove_words_from_samples(
            remove_words, text_train_mod2)
        #code to remove redunant whitespaces
        text_train_final2 = []
        for y in text_train_final:
            y_prime = y.strip()
            y_prime = re.sub(' +', ' ', y_prime)
            text_train_final2.append(y_prime)
        #let's clean out all non printable characters
        text_train_final2 = [
            self.text_processing(x) for x in text_train_final2
        ]

        #let's remove empty elements
        empty_elements_index = []
        for i in range(len(text_train_final2)):
            if not (text_train_final2[i]):
                empty_elements_index.append(i)
        for j in empty_elements_index:
            text_train_final2.pop(j)
            text_ID_train.pop(j)
            label_train.pop(j)
        #we can now write this out to a file
        with open(os.path.join(output_path, 'train_cleaned.tsv'),
                  'w') as train_output:
            for i in range(len(text_train_final2)):
                if i == 0:
                    train_output.write('text_id' + '\t' + 'text' + '\t' +
                                       'label' + '\n')
                    train_output.write(text_ID_train[i] + '\t' +
                                       text_train_final2[i] + '\t' +
                                       label_train[i])
                else:
                    train_output.write(text_ID_train[i] + '\t' +
                                       text_train_final2[i] + '\t' +
                                       label_train[i])

    def rotten_tomato_reshape_test(self, data_file_path_test, output_path):
        """
        Method to clean and restructure the rotten tomato test dataset. Turns out the data was provided in a peculiar format and we need
        to do some prep work to make it usable for our tasks. Original Data was retrieved from here: \n
        https://www.kaggle.com/c/sentiment-analysis-on-movie-reviews/data \n
        Once this method is called an output file will be generated contaning data that can be immediately processed by the methods in 
        our pre_processing module.

        :param data_file_path_train: file path of test.tsv file downloaded from link above.
        :type data-file_path_train: string

        :param output_path: directory path of where cleaned test data should be written to.
        :type output_path: string
        """
        text_ID_test = []
        text_test = []

        with open(data_file_path_test) as test:
            counter_ = 0
            for line in test:
                #split line by tab delimiter
                line_split = line.split('\t')
                text_ID_str = line_split[1]
                text_str = line_split[2]
                if counter_ == 1:
                    text_ID_test.append(text_ID_str)
                    text_test.append(text_str)
                elif counter_ > 1 and text_ID_str == text_ID_test[-1]:
                    pass
                elif counter_ > 1 and text_ID_str != text_ID_test[-1]:
                    text_ID_test.append(text_ID_str)
                    text_test.append(text_str)
                counter_ += 1

        #will make all text lower
        text_test = [x.lower() for x in text_test]
        #noticed somethng funky in text data. everytime a ' is present the test is fromated as such : word 'X. I will fix this

        text_test_mod = []
        count_ = 0
        for x in text_test:
            search_res = re.search(r' \'[a-z]*', x)
            if not search_res:
                text_test_mod.append(x)
            else:
                count_ += 1
                res = search_res.group()
                res_strip = res.strip()
                x = re.sub(res, res_strip, x)
                text_test_mod.append(x)

        #second problem pattern won't appears as wo n't. Will fix this
        text_test_mod2 = []
        for x in text_test_mod:
            search_res = re.search(r' n\'[a-z]*', x)
            if not search_res:
                text_test_mod2.append(x)
            else:
                res = search_res.group()
                res_strip = res.strip()
                x = re.sub(res, res_strip, x)
                text_test_mod2.append(x)

        #some problematic patterns we should remove:
        remove_words = {'--', '-rrb-', '-lrb'}

        #code to remove set of keywords for list of text
        text_test_final = self.remove_words_from_samples(
            remove_words, text_test_mod2)
        #code to remove redunant whitespaces
        text_test_final2 = []
        for y in text_test_final:
            y_prime = y.strip()
            y_prime = re.sub(' +', ' ', y_prime)
            text_test_final2.append(y_prime)

        #let's remove empty elements
        empty_elements_index = []
        for i in range(len(text_test_final2)):
            if not (text_test_final2[i]):
                empty_elements_index.append(i)
        for j in empty_elements_index:
            text_test_final2.pop(j)
            text_ID_test.pop(j)

        #we can now write this out to a file
        with open(os.path.join(output_path, 'test_cleaned.tsv'),
                  'w') as test_output:
            for i in range(len(text_test_final2)):
                if i == 0:
                    test_output.write('text_id' + '\t' + 'text' + '\t' + '\n')
                    test_output.write(text_ID_test[i] + '\t' +
                                      text_test_final2[i] + '\n')
                else:
                    test_output.write(text_ID_test[i] + '\t' +
                                      text_test_final2[i] + '\n')

    def imdb_reshape_data(self, data_file_path, output_path, file_output_name):
        """
        Method to clean and restructure the imdb datasets. The raw data can be downloaded here: \n
        https://ai.stanford.edu/~amaas/data/sentiment/ \n
        After you download and unzip the data you will notice it has been provided in an interesting way. Each individual 
        review is provided as a file, and the sentiment of the review is encoded in the file name. Some work is required
        to structure our data in the format our subsequent modules require. This  method abstracts all of that away and returns 
        two files containing our training and test data that are ready for subsequent processing. Please note this method must be
        called twice to process both the train and test data. In the first pass we can clean and structure our train data
        by indicating the aclImdb/train path in the data_file_path argument. In the second pass we can clean and structure the test
        data by indicating the aclImdb/test path in the data_file_path argument.

        :param data_file_path: file path of the aclImdb directory that we wish to process. train or test.
        :type data_file_path: string

        :param output_path: directory path of where cleaned/structured data should be written to.
        :type output_path: string

        :param file_output_name: name of output file.
        :type file_output_name: string
        """
        imdb_train_cleaned = os.path.join(output_path, file_output_name)
        #we will also at the same time create a file that repsets the response variable as binatu (0,1)
        name_, ext = imdb_train_cleaned.split('.')
        imdb_train_cleaned_binary = name_ + '_binary.' + ext
        #lets ge tthe list of files with negative reviews
        list_of_files_neg = os.listdir(os.path.join(data_file_path, 'neg'))
        #lets get the list of files with positive reviews
        list_of_files_pos = os.listdir(os.path.join(data_file_path, 'pos'))
        #let's write the header first
        with open(imdb_train_cleaned, 'w', encoding='utf-8') as train, open(
                imdb_train_cleaned_binary, 'w',
                encoding='utf-8') as train_binary:
            train.write('text_id' + '\t' + 'text' + '\t' + 'label' + '\n')
            train_binary.write('text_id' + '\t' + 'text' + '\t' + 'label' +
                               '\n')
        #let's write all negative and positive reviews
        with open(imdb_train_cleaned, 'a+', encoding='utf-8') as train, open(
                imdb_train_cleaned_binary, 'a+',
                encoding='utf-8') as train_binary:
            for file in list_of_files_neg:
                id, score = file.split('_')
                score = re.sub('.txt', '', score)
                review_data = []
                with open(os.path.join(data_file_path, 'neg', file),
                          'r',
                          encoding='utf-8') as temp_file:
                    for line in temp_file:
                        #let's drop come funny patterns I saw
                        line = re.sub(r'\t', ' ', line)
                        line = re.sub(r'<br /><br />', ' ', line)
                        #let's apply come cleaning
                        line = self.text_processing(line)
                        review_data.append(line)
                for text in review_data:
                    train.write(id + '\t' + text + '\t' + score + '\n')
                    #logic to write binary score to train binary file
                    if int(score) > 0 and int(score) < 5:
                        score = 0
                        train_binary.write(id + '\t' + text + '\t' +
                                           str(score) + '\n')
                    elif score > 5 and score < 10:
                        score = 1
                        train_binary.write(id + '\t' + text + '\t' +
                                           str(score) + '\n')
            #let's write positive reviews to our structured file
            for file in list_of_files_pos:
                id, score = file.split('_')
                score = re.sub('.txt', '', score)
                review_data = []
                with open(os.path.join(data_file_path, 'pos', file),
                          'r',
                          encoding='utf-8') as temp_file:
                    for line in temp_file:
                        #let's drop come funny patterns I saw
                        line = re.sub(r'\t', ' ', line)
                        line = re.sub(r'<br /><br />', ' ', line)
                        #let's apply come cleaning
                        line = self.text_processing(line)
                        review_data.append(line)
                for text in review_data:
                    train.write(id + '\t' + text + '\t' + score + '\n')
                    #logic to write binary score to train binary file
                    if int(score) > 0 and int(score) < 5:
                        score = 0
                        train_binary.write(id + '\t' + text + '\t' +
                                           str(score) + '\n')
                    elif int(score) > 5 and int(score) < 10:
                        score = 1
                        train_binary.write(id + '\t' + text + '\t' +
                                           str(score) + '\n')
