# Basics
import pandas as pd
import numpy as np

# NLP
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords

stop = stopwords.words('english')

def clean_name_col(df, 
                   name_col, 
                   remove_digits = True, 
                   remove_punctuation = True, 
                   remove_stop = True
                  ):
    
    """Function to clean up name column before vectorizer"""

    # All lower case
    df[name_col] = df[name_col].astype(str)
    name_vector = df[name_col].str.lower()

    if remove_digits == True:
        # Remove digits
        name_vector = name_vector.str.replace('\d+', '')

    if remove_punctuation == True:
        # Remove punctuation
        name_vector = name_vector.str.replace('[^\w\s]','')
        name_vector = name_vector.str.replace('_','')

    if remove_stop == True:
        # Remove stopwords
        name_vector = name_vector.apply(lambda x: ' '.join([word for word in x.split() if word not in (stop)]))

    # Clean up all spaces there may be
    name_vector = name_vector.str.replace('\s+', ' ')
    
    return name_vector


def tfidf_fit_transform(name_vector, 
                         min_df, 
                         max_df, 
                         df_prep, 
                         stop_words = 'english'
                        ):

    # Before tf-idf vectorizer, let's clean the text column
    corpus = name_vector
    vectorizer = TfidfVectorizer(min_df = min_df,  # To speed up processing time
                                 max_df = max_df, # Remove terms that are too common
                                 stop_words = stop_words) # To make sure we haven't missed any

    # TD-IDF Matrix
    X = vectorizer.fit_transform(corpus)

    # extracting feature names
    tfidf_tokens = vectorizer.get_feature_names_out()
    result = pd.DataFrame(
        data = X.toarray(), 
        index = df_prep.index, 
        columns = tfidf_tokens
    )

    # Speed up processing
    result = result.astype('float32')

    # Ensure we differentiate the tf-idf columns when they are all merged
    result.columns = [str('word_' + col) for col in result.columns]
    
    return vectorizer, result

def tfidf_transform(name_vector,
                    vectorizer, 
                    df_prep, 
                    ):
    
    corpus = name_vector

    # TD-IDF Matrix
    X = vectorizer.transform(corpus)

    # extracting feature names
    tfidf_tokens = vectorizer.get_feature_names_out()
    result = pd.DataFrame(
        data = X.toarray(), 
        index = df_prep.index, 
        columns = tfidf_tokens
    )

    # Speed up processing
    result = result.astype('float32')

    # Ensure we differentiate the tf-idf columns when they are all merged
    result.columns = [str('word_' + col) for col in result.columns]
    
    return result