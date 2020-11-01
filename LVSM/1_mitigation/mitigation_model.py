'''
# Equipment Failure Mitigation Multi-Label Classification

# Purpose
This Linear Support Vector Machine (LSVM) classifier categorizes failure mitigation strategies of of electric plant equipment.

# Stack
- Numpy for data manipulation
- Linear Support Vector Machine (LVSM) from sklearn
- Stopword dictionary from Natural Language Toolkit (NLTK)
- Pandas, matplotlib, and seaborn for plotting

# Author
@ Al Miller

# License
MIT License 2020
'''

# Natural language processing (NLP) imports
import re
import nltk
from collections import Counter
from nltk.corpus import stopwords
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC
from sklearn.multiclass import OneVsRestClassifier

# Metrics
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import confusion_matrix
from sklearn.metrics import plot_confusion_matrix

# Plotting
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt


class NLPModel():

    def __init__(self, df):
        '''
        Configure dataframe as CSV file of plant equipment
        '''
        self.df = df

    def makePlots(self):
        '''
        Make preliminary plots of equipment CSV
        '''

        # Plot frequency distribution of 'Mitigation' strategy categories
        df = self.df
        dfMitigation = df.drop(['Fleet', 'Station', 'Unit', 'UNID', 'Status', 'Function', 'System', 'Component', 'ComponentDesc', 'Subcomponent',
                                'SubcomponentDesc', 'SPVType', 'Derate%', 'Basis', 'Mitigation', 'Elimination', 'Classification', 'Manufacturer',
                                'ModelPartNo', 'Template', 'CausedTrip', 'CorrectiveActions', 'Comments',
                                'Cycle', 'Loops', 'NSSSType', 'PlantDesign', 'TurbineType', 'TurbineCount',
                                'SPVID', 'general_maintenance', 'heavy_maintenance',
                                'replacement', 'visual_inspection', 'time_base_replacement', 'component_overhaul',
                                'periodic_cycling', 'no_action_required', 'unknown_maintenance', 'train_set_1',
                                'validate_set_1', 'apply_set_1', 'train_set_2', 'validate_set_2', 'apply_set_2',
                                'NewComponent', 'NewSystem'], axis=1)
        numberOfOccurrences = []
        categories = list(dfMitigation.columns.values)
        for category in categories:
            numberOfOccurrences.append(
                (category, dfMitigation[category].sum()))
        dfStats = pd.DataFrame(
            numberOfOccurrences, columns=['Mitigation Strategy Category', 'Number of Occurrences in Train/Validate Set'])
        dfStats.plot(x='Mitigation Strategy Category', y='Number of Occurrences in Train/Validate Set',
                     kind='bar', legend=False, grid=True, figsize=(8, 5))
        plt.title("Mitigation Strategy Frequency in Train/Validate Set")
        plt.ylabel('Number of Occurrences in Train/Validate Set', fontsize=12)
        plt.xlabel('Mitigation Strategy Category', fontsize=12)

        # Plot distribution of the number of 'Mitigation' categories per record
        rowsums = df.iloc[:, 2:].sum(axis=1)
        x = rowsums.value_counts()
        plt.figure(figsize=(8, 5))
        plt.title(
            "Mitigation Strategies with Multiple Categories in Train/Validate Set")
        plt.ylabel('Number of Occurrences in Train Set', fontsize=12)
        plt.xlabel('Number of Categories', fontsize=12)
        plt.show()

        # Print count of the most frequent words in 'Mitigation' field
        print(Counter(" ".join(df["Mitigation"]).split()).most_common(100))

    def runModel(self, sampleIndex, sampleSize):
        '''
        Run the model on the given dataset (train/validate/apply) for the 'Mitigation' field
        '''
        df = self.df

        # Clean text for mitigation
        df['Mitigation'] = df['Mitigation'].map(
            lambda Mit: self.cleanText(Mit))
        '''
        Split data into a training, validation and "application" sets
        
        train_set has 3,569 records, taken uniformly (every 20th record) from data population
        '''
        train, test = train_test_split(
            df, random_state=1, test_size=sampleSize, train_size=3569, shuffle=False)
        X_train = train.Mitigation
        X_test = test.Mitigation
        print('\nSize of Train Set\tSize of Validation Set\n{}\t\t{}'.format(
            X_train.shape, X_test.shape))

        # Vectorize text, remove stopwords
        stop_words = set(stopwords.words('english'))
        SVC_pipeline = Pipeline([
            ('tfidf', TfidfVectorizer(stop_words=stop_words)),
            ('clf', OneVsRestClassifier(LinearSVC(), n_jobs=1)),
        ])

        # Make 'Mitigation' category predictions
        categories = ['maintenance', 'operational', 'physical_barrier',
                      'design_and_engineering', 'supply_chain', 'unknown_mitigation']
        predictions = []
        # Print metrics if first pass (train and validation), not for application set
        if(sampleIndex == 0):
            print('\nCategory\tAccuracy\n')
            for index, category in enumerate(categories):
                SVC_pipeline.fit(X_train, train[category])
                predictions.append(SVC_pipeline.predict(X_test))
                if(sampleIndex == 0):
                    print('{}\t\t{:.4}\t{:.4}\t{:.4}\t{:.4}'.format(category, accuracy_score(test[category], predictions[index]), precision_score(
                        test[category], predictions[index]), recall_score(test[category], predictions[index]), f1_score(test[category], predictions[index])))
                    confusion_matrix(test[category], predictions[index])
                    plot_confusion_matrix(test[category], predictions[index])
                    plt.show()
        if(sampleIndex == 1):
            df = pd.DataFrame({'maintenance': predictions[0], 'operational': predictions[1], 'physical_barrier': predictions[2],
                               'design_and_engineering': predictions[3], 'supply_chain': predictions[4], 'unknown_mitigation': predictions[5]})
            df.to_csv('./out/predictions.csv')


    def cleanText(self, text):
        '''
        Clean 'Mitigation' field text.

        Text cleaning simply taken from medium.com article
        '''
        text = text.lower()
        text = re.sub(r"what's", "what is ", text)
        text = re.sub(r"\'s", " ", text)
        text = re.sub(r"\'ve", " have ", text)
        text = re.sub(r"can't", "can not ", text)
        text = re.sub(r"n't", " not ", text)
        text = re.sub(r"i'm", "i am ", text)
        text = re.sub(r"\'re", " are ", text)
        text = re.sub(r"\'d", " would ", text)
        text = re.sub(r"\'ll", " will ", text)
        text = re.sub(r"\'scuse", " excuse ", text)
        text = re.sub('\W', ' ', text)
        text = re.sub('\s+', ' ', text)
        text = text.strip(' ')
        return text

if __name__ == "__main__":
    '''
    Validate and then apply the model to predict 'Mitigation' field categories for entire dataset
    First train/validate, then application sets
    '''
    sampleSizes = [3569, 67822]
    for sampleIndex, sampleSize in enumerate(sampleSizes):
        df = pd.read_csv(
            "./in/equipment_data_for_mitigation.csv", encoding="ISO-8859-1")
        Model = NLPModel(df)
        Model.makePlots()
        Model.runModel(sampleIndex, sampleSize)
