# -*- coding: utf-8 -*-
"""Classification Analysis  - Shola Ayeotan

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1MSmvmCJrttuaTWOUZSRr_cm90p8mDTn4
"""

# Importing the neccessary libraries

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sklearn as sk
import seaborn as sns

"""#### **Loading the Dataset**"""

bank_marketing = pd.read_csv("/content/bank-full.csv", sep=';')

bank_marketing.shape

bank_marketing.head()

bank_marketing.tail()

bank_marketing.info()

bank_marketing.describe().transpose()

bank_marketing.describe(include='object').transpose()

"""#### **Data Preprocessing**"""

# Renaming the target variable for better clarity

bank_marketing = bank_marketing.rename(columns={'y': 'subscribed'})

# Checking for missing values

bank_marketing.isnull().sum()

# Fetching unique values

bank_marketing.marital.unique()

# Checking for frequency

bank_marketing.marital.value_counts()

# Fetching unique values

bank_marketing.job.unique()

# Checking for frequency

bank_marketing.job.value_counts()

# Fetching unique values

bank_marketing.education.unique()

# Checking for subscription counts

bank_marketing.subscribed.value_counts()

"""### **Visual Exploration**"""

# Visualizing Age Distribution

plt.figure(figsize=(10, 6))
sns.histplot(bank_marketing['age'], bins=20, kde=True, color='skyblue')
plt.title('Age Distribution of Customers')
plt.xlabel('Age')
plt.ylabel('Frequency')
plt.show()

# Visualizing the different types of customer jobs

plt.figure(figsize=(8, 6))

job_counts = bank_marketing['job'].value_counts()
colors = sns.color_palette('hls', len(job_counts))
job_counts.plot(kind='bar', color=colors)

plt.title('Job Distribution')
plt.xlabel('Job')
plt.ylabel('Count')
plt.show()

# Visualizing the distribution of marital status

plt.figure(figsize=(6, 6))

marital_counts = bank_marketing['marital'].value_counts()
plt.bar(marital_counts.index, marital_counts.values, color='orange')

plt.title('Marital Status Distribution')
plt.xlabel('Marital Status')
plt.ylabel('Count')
plt.show()

# Visualizing the distribution of Subscription Status

plt.figure(figsize=(6, 6))

subscription_status = bank_marketing['subscribed'].value_counts()
plt.bar(subscription_status.index, subscription_status.values, color='skyblue')

plt.title('Subscription Status Distribution')
plt.xlabel('Subscription Status')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.show()

# Exploring the distribution of jobs and corresponding subscription statuses

pd.crosstab(bank_marketing.subscribed, bank_marketing.job)

# Visualizing the distribution of subscriptions based on Job Type

plt.figure(figsize=(15, 6))

sns.countplot(x='job', hue='subscribed', data=bank_marketing, palette='Set2')

plt.title('Subscription Rate by Job Type')
plt.xlabel('Job Types', fontsize=12)
plt.ylabel('Subscription Counts', fontsize=12)
plt.show()

# Assuming 'bank_marketing' is your DataFrame
education_subscription_counts = bank_marketing.groupby(['education', 'subscribed']).size().unstack(fill_value=0)

print("Subscription Counts by Educational Qualification:")
print(education_subscription_counts)

# Visualzing the distribution of subscriptions based on educational status

sns.countplot(x='education', hue='subscribed', data=bank_marketing, palette='Set1')

plt.title('Subscription to Term Deposit by Educational Qualification')
plt.xlabel('Educational Qualification', fontsize=12)
plt.ylabel('Subscription Counts', fontsize=12)
plt.xticks(rotation=45)
plt.show()

# Visualzing the distribution of subscriptions based on marital status

plt.figure(figsize=(8, 6))

marital_dist = bank_marketing.groupby(['marital', 'subscribed']).size().unstack()
marital_dist.plot(kind='bar', stacked=True, colormap='viridis')

plt.title('Subscription by Marital Status')
plt.xlabel('Marital Status', fontsize=12 )
plt.ylabel('Subscription Counts', fontsize=12)
plt.show()

# Visualizing the distribution of subscriptions for each month

month_order = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']

plt.figure(figsize=(12, 6))
sns.countplot(x='month', hue='subscribed', data=bank_marketing, order=month_order, palette='Set2')
plt.title('Campaign Outcome Trends Over Months')
plt.xlabel('Month')
plt.ylabel('Count')
plt.show()

# Visualizing Previous Campaign Outcomes

plt.figure(figsize=(10, 6))
sns.countplot(x='poutcome', hue='subscribed', data=bank_marketing)
plt.title('Previous Campaign Outcomes and Subscription')
plt.xlabel('Previous Outcome')
plt.ylabel('Count')
plt.legend(title='Subscribed', loc='upper right')
plt.show()

# Visualizing the distribution of contact mediums used during the campaign

plt.figure(figsize=(10,5))

plt.pie(bank_marketing.contact.value_counts().values,labels=bank_marketing.contact.value_counts().index, autopct='%.2f')

plt.title('Distrubtion Of Contact Mediums',fontsize=14)
plt.show()

# Visualzing contact methods and subscription outcomes

  plt.figure(figsize=(10, 6))
  sns.countplot(x='contact', hue='subscribed', data=bank_marketing)
  plt.title('Contact Methods and Subscription Outcome')
  plt.xlabel('Contact Method')
  plt.ylabel('Count')
  plt.legend(title='Subscribed', loc='upper right')
  plt.show()

"""#### Correlation Analysis"""

# Checking for correlation between the variables

plt.figure(figsize=(12, 8))
sns.heatmap(bank_marketing.corr(), annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Correlation Heatmap')
plt.show()

"""### **Further Preprocessing**

**Encoding the categorical and target variables**
"""

from sklearn import preprocessing
from sklearn.preprocessing import LabelEncoder

# Converting some variables using Label Encoder

Label = LabelEncoder()

categorical_var = ['default', 'housing', 'loan', 'subscribed']

for i in categorical_var:
    bank_marketing[i]=Label.fit_transform(bank_marketing[i])

# Converting the remaining variables using One Hot Encoding

enc = preprocessing.OneHotEncoder(drop = 'first')
onehots = enc.fit_transform(bank_marketing[['job', 'marital', 'education', 'contact', 'month', 'poutcome']]).toarray()

# Retrieving the feature names after encoding
feature_names = enc.get_feature_names_out(input_features=['job', 'marital', 'education', 'contact', 'month', 'poutcome'])

onehot_df = pd.DataFrame(onehots, columns=feature_names)
bank_marketing = pd.concat([bank_marketing, onehot_df], axis=1)

# Dropping the original columns that were encoded
bank_marketing.drop(['job', 'marital', 'education', 'contact', 'month', 'poutcome'], axis=1, inplace = True)

bank_marketing.head()

"""**Splitting the dataset**"""

from sklearn.model_selection import train_test_split

X = bank_marketing.drop(columns=['subscribed'])
y = bank_marketing['subscribed']

# Splitting the data into 80% train and 20% test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

"""**Standardizing the dataset**"""

from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

"""**Addressing Class Imbalance**"""

from imblearn.over_sampling import SMOTE

# Applying SMOTE to balance the dataset

smote = SMOTE(random_state=42)
X_train_sm, y_train_sm = smote.fit_resample(X_train, y_train)

sns.countplot(x=y_train_sm)

"""**Feature Selection and Engineering**"""

from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import RFECV

# Initialising the RandomForestClassifier
rf = RandomForestClassifier(random_state=0)

rfecv = RFECV(rf, cv=3, step=5)

# Fitting the RFECV on the training data
X_train_fs = rfecv.fit_transform(X_train_sm, y_train_sm)
X_test_fs = rfecv.transform(X_test)

# Printing the number of remaining features following the selection
print(f"Number of remaining features: {X_train_fs.shape[1]}")

# Visualizing the result of the selection

plt.figure( figsize=(15, 6))

plt.title('Number of Features Included vs Accuracy')
plt.xlabel('Number of Features Included')
plt.ylabel('Model Accuracy')
plt.plot(np.linspace(0,50,10), rfecv.cv_results_['mean_test_score'])
plt.show()

"""## **Model Development, Training and Evaluation**"""

!pip install xgboost

from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier

from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score, recall_score, precision_score
from sklearn.metrics import roc_curve, auc

# Creating a dictionary for storing the performance metrics of each model
model_comparison={}

"""#### **DECISION TREE**"""

# Initializing the Decision Tree model
dtModel = DecisionTreeClassifier(random_state=42)

# Fitting the model on the training data
dtModel.fit(X_train_fs, y_train_sm)

# Running predictions on the test set
dtPred = dtModel.predict(X_test_fs)

# Generating the confusion matrix heatmap
print(f"Accuracy Score: {accuracy_score(y_test,dtPred)*100:.2f}%")

cm = confusion_matrix(y_test,dtPred)
ax = sns.heatmap(cm, cmap='flare',annot=True, fmt='d')

plt.xlabel("Predicted Class",fontsize=12)
plt.ylabel("True Class",fontsize=12)
plt.title("Confusion Matrix",fontsize=12)
plt.show()


# Generating the classification report
print("Classification Report:")
print(classification_report(y_test, dtPred))

# Updating the model comparison dictionary with this model's performance
model_comparison['Decision Tree']=[accuracy_score(dtPred,y_test),f1_score(dtPred,y_test,average='weighted'),
                                   precision_score(y_test, dtPred),recall_score(y_test, dtPred)]

# Predicting the probabilities of the positive class
dtROC = dtModel.predict_proba(X_test_fs)[:, 1]

# Computing the ROC curve
dtFPR, dtTPR, dtThresholds = roc_curve(y_test, dtROC)

# Calculating the Area Under the Curve (AUC)
dtAUC = auc(dtFPR, dtTPR)

# Plotting the ROC curve
plt.figure(figsize=(8, 8))
plt.plot(dtFPR, dtTPR, color='darkorange', lw=2, label=f'Decision Tree ROC curve (AUC = {dtAUC:.2f})')
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--', label='Random')
plt.xlabel('False Positive Rate (FPR)')
plt.ylabel('True Positive Rate (TPR)')
plt.title('Receiver Operating Characteristic (ROC) Curve - Decision Tree')
plt.legend()
plt.show()

"""##### **Hyperparemeter tuning**"""

from sklearn.model_selection import GridSearchCV

# Defining a parameter grid
param_grid = {'max_depth': [None, 10, 20, 30],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]}

# Creating a grid search
grid_search = GridSearchCV(
    DecisionTreeClassifier(random_state=42),
    param_grid,
    cv=5,
    scoring='accuracy')

grid_search.fit(X_train_fs, y_train_sm)

# Retrieving the best parameters
best_params = grid_search.best_params_
print("Best Hyperparameters:", best_params)

# Creating a new model with the best hyperparameters

tunedDtModel = DecisionTreeClassifier(
    max_depth=20, min_samples_leaf=1, min_samples_split=2, random_state=42)

tunedDtModel.fit(X_train_fs, y_train_sm)

dtPred2 = tunedDtModel.predict(X_test_fs)

# Generating the confusion matrix heatmap

print(f"Accuracy Score: {accuracy_score(y_test,dtPred2)*100:.2f}%")

cm = confusion_matrix(y_test,dtPred2)
ax = sns.heatmap(cm, cmap='flare',annot=True, fmt='d')

plt.xlabel("Predicted Class",fontsize=12)
plt.ylabel("True Class",fontsize=12)
plt.title("Confusion Matrix",fontsize=12)
plt.show()

# Generating the classification report
print("Classification Report:")
print(classification_report(y_test, dtPred2))

# Updating the model comparison dictionary with this model's performance
model_comparison['Decision Tree']=[accuracy_score(dtPred2,y_test),f1_score(dtPred2,y_test,average='weighted'),
                                   precision_score(y_test, dtPred2),recall_score(y_test, dtPred2)]

# Plotting the ROC curve

dtROC2 = tunedDtModel.predict_proba(X_test_fs)[:, 1]

dtFPR, dtTPR, dtThresholds = roc_curve(y_test, dtROC2)

dtAUC = auc(dtFPR, dtTPR)

plt.figure(figsize=(8, 8))
plt.plot(dtFPR, dtTPR, color='darkorange', lw=2, label=f'Decision Tree ROC curve (AUC = {dtAUC:.2f})')
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--', label='Random')
plt.xlabel('False Positive Rate (FPR)')
plt.ylabel('True Positive Rate (TPR)')
plt.title('Receiver Operating Characteristic (ROC) Curve - Decision Tree')
plt.legend()
plt.show()

"""#### **LOGISTIC REGRESSION**"""

# Initializing the Logistic Regression model
logModel = LogisticRegression()

# Training the Logistic Regression model
logModel.fit(X_train_fs, y_train_sm)

# Making predictions on the test set
logPred = logModel.predict(X_test_fs)

# Generating the confusion matrix heatmap

print(f"Accuracy Score: {accuracy_score(y_test,logPred)*100:.2f}%")

cm = confusion_matrix(y_test,logPred)
ax = sns.heatmap(cm, cmap='flare',annot=True, fmt='d')

plt.xlabel("Predicted Class",fontsize=12)
plt.ylabel("True Class",fontsize=12)
plt.title("Confusion Matrix",fontsize=12)
plt.show()


# Generating the classification report
print("Classification Report for the Logistic Model:")
print(classification_report(y_test, logPred))

# Updating the model comparison dictionary
model_comparison['Logistic Regression']=[accuracy_score(logPred,y_test),f1_score(logPred,y_test,average='weighted'),
                                   precision_score(y_test, logPred),recall_score(y_test, logPred)]

# Plotting the ROC curve for Logistic Regression

logROC = logModel.predict_proba(X_test_fs)[:, 1]

logFPR, logTPR, logThresholds = roc_curve(y_test, logROC)

logAUC = auc(logFPR, logTPR)

plt.figure(figsize=(8, 8))
plt.plot(logFPR, logTPR, color='green', lw=2, label=f'Logistic Regression ROC curve (AUC = {logAUC:.2f})')
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--', label='Random')
plt.xlabel('False Positive Rate (FPR)')
plt.ylabel('True Positive Rate (TPR)')
plt.title('Receiver Operating Characteristic (ROC) Curve - Logistic Regression')
plt.legend()
plt.show()

"""### ENSEMBLE LEARNING

#### **RANDOM FOREST**
"""

# Initializing the Random Forest model
rfModel = RandomForestClassifier(n_estimators=10)

# Fitting the model on the training data
rfModel.fit(X_train_fs, y_train_sm)

# Running predictions on the test set
rfPred = rfModel.predict(X_test_fs)

# Generating the confusion matrix heatmap

print(f"Accuracy Score: {accuracy_score(y_test,rfPred)*100:.2f}%")

cm = confusion_matrix(y_test,rfPred)
ax = sns.heatmap(cm, cmap='flare',annot=True, fmt='d')

plt.xlabel("Predicted Class",fontsize=12)
plt.ylabel("True Class",fontsize=12)
plt.title("Confusion Matrix",fontsize=12)
plt.show()


# Generating the classification report
print("Classification Report for Random Forest Model:")
print(classification_report(y_test, rfPred))

# Updating the model comparison dictionary
model_comparison['Random Forest']=[accuracy_score(rfPred,y_test),f1_score(rfPred,y_test,average='weighted'),
                                   precision_score(y_test, rfPred),recall_score(y_test, rfPred)]

# Plotting the ROC curve for Random Forest

rfROC = rfModel.predict_proba(X_test_fs)[:, 1]

rfFPR, rfTPR, rfThresholds = roc_curve(y_test, rfROC)

rfAUC = auc(rfFPR, rfTPR)

plt.figure(figsize=(8, 8))
plt.plot(rfFPR, rfTPR, color='blue', lw=2, label=f'Random Forest ROC curve (AUC = {rfAUC:.2f})')
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--', label='Random')
plt.xlabel('False Positive Rate (FPR)')
plt.ylabel('True Positive Rate (TPR)')
plt.title('Receiver Operating Characteristic (ROC) Curve - Random Forest')
plt.legend()
plt.show()

"""#### **XG BOOST**"""

# Initializing the XGBoost Classifier
xgbModel = XGBClassifier(random_state=42)

# Training the model
xgbModel.fit(X_train_fs, y_train_sm)

# Making predictions on the test set
xgbPred = xgbModel.predict(X_test_fs)

# Generating the confusion matrix heatmap

print(f"Accuracy Score: {accuracy_score(y_test,xgbPred)*100:.2f}%")

cm = confusion_matrix(y_test,xgbPred)
ax = sns.heatmap(cm, cmap='flare',annot=True, fmt='d')

plt.xlabel("Predicted Class",fontsize=12)
plt.ylabel("True Class",fontsize=12)
plt.title("Confusion Matrix",fontsize=12)
plt.show()



# Generating the classification report
print("Classification Report for XG Boost Model:")
print(classification_report(y_test, xgbPred))

# Updating the model comparison dictionary
model_comparison['XGBoost']=[accuracy_score(xgbPred,y_test),f1_score(xgbPred,y_test,average='weighted'),
                                   precision_score(y_test, xgbPred),recall_score(y_test, xgbPred)]

# Plotting the ROC curve for XGBoost

xgbROC = xgbModel.predict_proba(X_test_fs)[:, 1]

xgbFPR, xgbTPR, xgbThreshold = roc_curve(y_test, xgbROC)

xgbAUC = auc(xgbFPR, xgbTPR)

plt.figure(figsize=(8, 8))
plt.plot(xgbFPR, xgbTPR, color='red', lw=2, label=f'XGBoost ROC curve (AUC = {xgbAUC:.2f})')
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--', label='Random')
plt.xlabel('False Positive Rate (FPR)')
plt.ylabel('True Positive Rate (TPR)')
plt.title('Receiver Operating Characteristic (ROC) Curve - XGBoost')
plt.legend()
plt.show()

"""### **Comparative Analysis**"""

# Constructing a new dataframe and transposing it
Model_comparisons = pd.DataFrame(model_comparison).T

# Naming the columns appropriately
Model_comparisons.columns = ['Model Accuracy','Model F1-Score', 'Precision', 'Recall']

# Sorting the dataframe based on the F1-Scores
Model_comparisons = Model_comparisons.sort_values(by='Model F1-Score',ascending=False)

# Formating for better visualization
Model_comparisons.style.format("{:.2%}").background_gradient(cmap='Blues')

# Highlighting the highest performance score in each column

Model_comparisons.style.highlight_max().format("{:.2%}")

# Highlighting the lowest performance score in each column

Model_comparisons.style.highlight_min().format("{:.2%}")

# Visualizing the performance of each model based on Precision Scores

plt.figure(figsize=(8, 6))

models = list(Model_comparisons.index)
precision_scores = list(Model_comparisons['Precision'])

plt.bar(models, precision_scores)
plt.title(" Model Performances by Precision Values", fontsize=18)
plt.xlabel("Supervised Learning Models", fontsize=14)
plt.ylabel("Precision", fontsize=14)
plt.xticks(rotation=45)

plt.show()

# Visualizing the performance of each model based on Recall Scores

plt.figure(figsize=(8, 6))

models = list(Model_comparisons.index)
recall_scores = list(Model_comparisons['Recall'])

plt.bar(models, recall_scores)
plt.title(" Model Performances by Recall Scores", fontsize=18)
plt.xlabel("Supervised Learning Models", fontsize=14)
plt.ylabel("Recall", fontsize=14)
plt.xticks(rotation=45)

plt.show()

# Comparing ROC Curves of Logistic Regression and XGB Boost Models

plt.plot(logFPR, logTPR, color='darkorange', lw=2, label='Logistic Regression ROC curve (AUC = {:.2f})'.format(logAUC))
plt.plot(xgbFPR, xgbTPR, color='blue', lw=2, label='XG Boost ROC curve (AUC = {:.2f})'.format(xgbAUC))