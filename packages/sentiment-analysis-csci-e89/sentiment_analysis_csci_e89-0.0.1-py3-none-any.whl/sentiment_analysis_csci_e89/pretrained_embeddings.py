import os
import numpy as np
import traceback
import datetime


class pretrained_embeddings:
    """  
    In this class we will provide helper methods to retrieve pre-trained word embeddings to use
    in your workflow.
    Pretrained word embeddings can be particularly useful on tasks where little training data is available
    (otherwise word embeddings trained on your data are likely going to be more powerful). In order to use pre-trained
    word embeddings some data transformations are required. Stanford GloVe and google's word2vec embeddings are particularly
    popular and useful. 
    The 'raw' word embeddings data can be found here: \n
    1. https://nlp.stanford.edu/projects/glove/ (GloVe) download the glove.6B.zip file and unzip)
    2. https://drive.google.com/file/d/0B7XkCwpI5KDYNlNUTTlSS21pQmM/edit \n

    This module assumes you have downloaded the 'raw' data from the sources listed above. Furthermore we ask that you store 
    the data on your machine using a directory tree like the one shown below: \n
        embeddings_data --> glove.6B (directory) --> unpacked files from the unzipping. 4 files should appear here:
        50d,100d,200d,300d \n
        embeddings_data --> word2vec -->unpacked files from the unzipping. 1 file should appear here: GoogleNews-vectors-negative300.bin

    when instantiating the class you will pass the file path of the embeddings_data directory.

    Some more information on each of the sources supported by this module:
    GloVE Embeddings: \n
    trained on wikipedia 2014 + Gigaword5 (6B tokens, 400K vocab, uncased, 50d, 100d, 200d, & 300d vectors, 822 MB download). \n
    word2vec embeddings: \n
    Pre-trained vectors trained on part of Google News dataset (about 100 billion words). The model contains 300-dimensional 
    vectors for 3 million words and phrases. The link above will download a bin.gz directory. Unzip it somehwere locally using command:gunzip GoogleNews-vectors-negative300.bin.gz \n
    
    Instance variables to pass during instantiation:

    :param project: The name of the project you are using the class for
    :type project: string

    :param  embeddings_directory_path: file path of where the raw word embeddings (downloaded from the sources listed above) live.
    :type  embeddings_directory_path: string

    :param error_log_dir: directory path of where errors should be logged to
    :type error_log_dir: string

    Documentation on our methods can be found below: \n
    """
    def __init__(self, project, embeddings_directory_path, error_log_dir):
        self.project = project
        self.embeddings_directory_path = embeddings_directory_path
        self.error_log_dir = error_log_dir
        print('Thank you fro using the pretrained_embeddings class in your:',
              project, 'project')

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

    def get_glove_vecs(self, dimension):
        """
        Method to parse the raw GloVe vectors file and return a mapping of each word to its corresponding vector.
        
        :param dimension: the dimension of the word embedddings we want to use. We can choose from 50d,100d,200d,300d
        :type dimension: int

        :returns embeddings_index: dictionary mapping each word to its assoiciated dense word vector
        :rtype: dictionary
        """
        error_log_dir = self.error_log_dir
        try:
            embeddings_directory_path = self.embeddings_directory_path
            if dimension not in (50, 100, 200, 300):
                print(
                    'Word embeddings for the dimension you choose do not exist. We will default to loading 100d word embeddings.'
                )
                dimension = 100

            file_path_data = os.path.join(
                embeddings_directory_path, 'glove.6B',
                'glove.6B.' + str(dimension) + 'd.txt')
            if not os.path.exists(file_path_data):
                print('Unable to fnd embedding file. Is the embeddings_directory_path correct? If it is, please ' \
                'make sure that you have stored the GloVe embeddings according to the directory structure outlined in the docs.')
            print('Loading GloVe word vectors... make take a few seconds...')
            embeddings_index = {}
            with open(file_path_data, 'r', encoding='utf-8') as glove_data:
                #the structure of these files is clear once you look into it. each embedding is presented on a line as follows: word vec
                # we can split by white space. the word will appear in the first index of the resulting list and the vector will be comprised
                #of all remaning elements in the list
                for line in glove_data:
                    data_ = line.split()
                    word = data_[0]
                    vector_components = np.asarray(data_[1:], dtype='float32')
                    #we can now update the dictionary
                    embeddings_index[word] = vector_components
            return (embeddings_index)

        except Exception:
            e = traceback.format_exc()
            self.error_logger(exception_error=e, error_log_dir=error_log_dir)

    def get_word2vec_vecs(self):
        """
        Method to parse the raw word2vec vectors file and return a mapping of each word to its corresponding vector.

        :returns word_vecs: dictionary mapping each word to its assoiciated dense word vector
        :rtype: dictionary
        """
        error_log_dir = self.error_log_dir
        try:
            embeddings_directory_path = self.embeddings_directory_path
            fname = os.path.join(embeddings_directory_path, 'word2vec',
                                 'GoogleNews-vectors-negative300.bin')
            if not os.path.exists(fname):
                print('Unable to fnd embedding file. Is the embeddings_directory_path correct? If it is, please ' \
                'make sure that you have stored the GloVe embeddings according to the directory structure outlined in the docs.')
            print(
                'Loading word2vec word evectors... make take a few seconds...')
            word_vecs = {}
            with open(fname, "rb") as f:
                header = f.readline()
                vocab_size, layer1_size = map(int, header.split())
                binary_len = np.dtype('float32').itemsize * layer1_size
                for line in range(vocab_size):
                    word = []
                    while True:
                        ch = f.read(1)
                        if ch == ' ':
                            word = ''.join(word)
                            break
                        if ch != '\n':
                            word.append(ch)
                    word_vecs[word] = np.fromstring(f.read(binary_len),
                                                    dtype='float32')
            return word_vecs
        except Exception:
            e = traceback.format_exc()
            self.error_logger(exception_error=e, error_log_dir=error_log_dir)