
# DISCLAIMER
Particular information regarding utility equipment and maintenance programs has been redacted, rendering this model unusable in its current state.

## Purpose
This text-classification model is documented herein to provide an example of multi-label text classification.

The use case is classification of electric plant (utility) equipment failure mitigation and maintenance strategies into general categories to identify trends and deficiencies.

## Background

This model classifies recods in the free-text 'Mitigation' field of a plant equipment database (71,391 records) into based on 'Mitigation' and 'Maintenance' strategy type. Records are binned into one or multiple of the following classes:

- maintenance	
- operational	
- physical_barrier	
- design_and_engineering	
- supply_chain
- unknown

The NLP classifier applies a Linear Support Vector Classification (SVC) algorithm (https://scikit-learn.org/stable/modules/generated/sklearn.svm.LinearSVC.html).

LVSC was selected based on trials using a number of text-classification algorithms, including:

- Random Forrest
- Naive Bayes
- Linear Regression

Moreover, this classifier applies a multi-label, "One vs Rest" (also known as 'binomial classifiication') strategy, which iteratively applies a seperate LVSM classifier for each label.

## Classifier Setup

1. Clone the repository

`git clone https://github.com/ANMillerIII/LVSM.git`

2. Initialize and activate vitual environment 

`py -m venv venv`

`./venv/Scripts/activate`

3. Install dependencies

`py -m pip install requirements.txt -r`

4. Switch to "LVSM" directory

`cd LVSM`

## Run Classifier

To run the 'Mitigation' classifier

`py ./1_mitigation/mitigation_model.py`

or

`py ./2_maintenance/maintenance_model.py`

Prediction output will be in the respective 'out' directories

## Limitations

1. 'train_set' data set is used based on naive string matching with some oversight. This should be improved by manually going through some 'Mitigation' fields and classifying them by hand.	
2. Accuracy is not a meaningful metric for the 'apply_set' data, since the model is used to make predictions (must spot check manually)
3. Foreign-language entries are somewhat correctly classified, but with low fidelity
4. 'train_set' data (3,569 records) are not classified by NLP, but rather string-matching/manually