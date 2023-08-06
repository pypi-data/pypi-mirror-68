import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score, roc_auc_score, auc, roc_curve, confusion_matrix
from sklearn.model_selection import train_test_split, cross_val_score

# Aliases
from typing import List, Dict
from pandas.core.series import Series
from pandas.core.frame import DataFrame
from numpy import ndarray
np.random.seed(10000)

class Classify_ML(object):
    """
    This class is Generic helper classfiersn class
    """

    def __init__(self, clf, clf_name: str, feature_matrix: DataFrame, response_vector: Series, **param_args):
        """
        Once instaniated, this class will fit and split the training and testing data
        :clf: given the classfier
        :clf_name: given the classfier name
        :feature_matrix: given the independent variables
        :response_vector: given the dependent variable
        :param_args: given arbitrary arguments of kwargs optional parameters
        """

        # intantiates arguments
        self.param_args: Dict = param_args
        self.feature_matrix: DataFrame = feature_matrix
        self.response_vector: Series = response_vector
        self.clf = None
        self.feature_names_combinations: List[str] = []
        self.auto_accuracy: List[Dict] = []
        self.df: DataFrame = None

        if not clf and not clf_name and not feature_matrix and not response_vector:
            raise AttributeError("ERROR: clf, clf_name, feature_matrix, response_vector are required.")

        self.default_clf: List[str] = ['logreg', 'knn',
                                       'dtree']  # TODO: create and call utils/constants.py to check this
        if clf_name not in self.default_clf:
            raise ValueError(f"ERROR: available classfier for now {self.default_clf}")

        # split training and testing data here
        train_test: Dict = self.train_test()

        self.X_train = train_test.get("X_train")
        self.X_test = train_test.get("X_test")
        self.y_train = train_test.get("y_train")
        self.y_test = train_test.get("y_test")

        self.clf = clf.fit(self.X_train, self.y_train)
        self.clf_original = clf

    def get_clf_name(self) -> str:
        """
        This function will return the classifier name
        :return: a string of classifier name
        """
        return self.clf_name

    def get_dimensions(self, vector: ndarray) -> tuple:
        """
        Helper function to check the dimension of the given vectors and return the mxn dimension
        :vector: given mxn vector
        :return: a tuple of mxn object
        """
        if not type(vector) in [Series, DataFrame, ndarray]:  # Todo: put this in utils/constants.py
            raise TypeError("Error: Must be type of ndarray, Series, DataFrame")

        return vector.shape

    def get_prediction_class(self) -> ndarray:
        """
        This function will return the prediction class from the given classfier
        :return: numpy array of the prediction class
        """
        return self.clf.predict(self.X_test)

    def get_predict_probability(self) -> ndarray:
        """
        This function will return all the prediction probabilites
        :return: numpy array of the prediction probabilities
        """
        return self.clf.predict_proba(self.X_test)

    def get_roc_auc_score(self, k_fold: int = np.random.randint(10, 15)) -> float:
        """
        This function calculate the roc_auc score, using cross validations technique.
        With a random kfolds from 10 to 15
        :k_fold: an optional k_fold parameter with an initial value of 10 - 15 k_fold
        :return: a roc_auc score in decimal points
        """
        if not self.is_binary():
            return TypeError("True values must be in binary formats ")
        return cross_val_score(self.clf,
                               self.X_train,
                               self.y_train, cv=k_fold,
                               scoring="roc_auc").mean()  # Random K-folds 10-15

    def get_prediction_accuracy(self) -> float:
        """
        This function will return the prediction accuracy in decimal points
        :return the prediction accuracy in decimal points
        """
        return accuracy_score(self.get_prediction_class(), self.y_test)

    def get_null_accuracy(self) -> float:
        """
        This function will return the null accuracy from the true value vector
        :y_test: given the true value vector
        :return: the null accuracy from response vector
        """
        if self.param_args.get('binary_clf'):
            return max(self.y_test.mean(), 1 - self.y_test.mean())

        return float(self.y_test.value_counts().head(1) / len(self.y_test))

    def get_roc_curve(self) -> tuple:
        """
        This function will compute the ROC curve
        :return: a tuple that contains True postive, False postive rates and Thresholds
        """

        if not self.is_binary():
            return TypeError("True values must be in binary formats ")

        fpr, tpr, threshold = roc_curve(self.y_test, self.get_predict_probability()[:, 1])
        return (fpr, tpr, threshold)

    def get_random_features(self) -> List[str]:
        """
        This function will return random feature names
        :return: a list of random feature names
        """
        if not self.param_args.get('feature_names') and not self.feature:
            raise Warning("Must set future_engineering to True")

        feature_names: List[str] = self.param_args.get('feature_names')
        if not feature_names:
            raise ValueError("ERROR: feature names cannot be empty")

        lower_bound: int = np.random.randint(0, round(len(feature_names) + 1 / 2))
        upper_bound: int = np.random.randint(lower_bound, len(feature_names) + 1)
        return feature_names[lower_bound:upper_bound]

    def get_best_features(self) -> DataFrame:
        """
        This function will attempt to find the best featrue_matrix based on the given dataset
        :return: a dataframe that contains the best scores for all combinations of feature matrix
        """
        if not self.param_args.get('feature_enginering'):
            raise Warning("Must set feature_engineering to True")

        if self.df.empty:
            raise Warning("Must run clf.get_auto_accuracy first.")

        return self.df[(self.df['accuracy'] > 0.5) & (self.df['sensitivity'] > 0.5) & (self.df['specificity'] > 0.5)]

    def get_auto_accuracy(self, iteration: int = 1000) -> DataFrame:
        """
        This function will attempt to automatically tune feature matrix and find the best accuracy
        :iteration: an optional parameter with default iteration of 1000
        :return: pandas dataframe
        """

        for i in range(iteration):
            self.feature_names_combinations.append(self.get_random_features())

        for feature in self.unique_feature_names():
            X_train, X_test, y_train, y_test = train_test_split(self.feature_matrix, self.response_vector,
                                                                random_state=np.random.randint(100, 150))
            y_pred_class = self.clf_original.fit(X_train, y_train).predict(X_test)
            results: Dict = self.calculate_cm(cm=confusion_matrix(y_test, y_pred_class), is_cm=True)
            results['features'] = feature
            self.auto_accuracy.append(results)

        self.df = pd.DataFrame.from_dict(self.auto_accuracy)
        return self.df

    def unique_feature_names(self) -> List[List]:
        """
        This function will return unique feature names
        :return: a list of list of unique feature names
        """
        if not self.feature_names_combinations:
            return []

        combination_feature_names: List[str] = sorted(set(list(filter(lambda column_name:
                                                                      column_name if len(column_name) else None,
                                                                      map(lambda features: ','.join(sorted(features)),
                                                                          self.feature_names_combinations)
                                                                      )
                                                               )
                                                          )
                                                      )

        return list(map(lambda feature: feature.split(','), combination_feature_names))

    def train_test(self, random_state: int = np.random.randint(100, 150)) -> Dict:
        """
        Helper function to create to split given feature matrix and response vectors into training and testing data
        :random_state: an optional param with random state from 100 to 150
        :return: a dictionary that contains testing and training data attributes
        """

        if not self.get_dimensions(vector=self.feature_matrix) and not self.get_dimensions(vector=self.response_vector):
            # Todo: raise
            raise ValueError(
                f"ERROR Mismatch Dimensions Feature Matrix: {self.feature_matrix.shape} must equals Response Vector: {self.response_vector.shape}")

        X_train, X_test, y_train, y_test = train_test_split(self.feature_matrix, self.response_vector,
                                                            random_state=random_state)

        return {
            "X_train": X_train,
            "X_test": X_test,
            "y_train": y_train,
            "y_test": y_test

        }

    def is_binary(self) -> bool:
        """
        Helpler function to check, if the true values contains binary response
        :return: a boolean value
        """
        return [0, 1] == sorted(pd.unique(self.y_test.tolist()).tolist())

    def calculate_cm(self, cm: ndarray = None, is_cm: bool = False) -> Dict:
        """
        This function will calculate the following confusion matrix attributes:
        - True Positive
        - True Negative
        - False Positive
        - False Negative
        - Sensitivity
        - Specificity
        - Accuracy
        - Error Rate
        - False Positive Rate
        :cm: an optional confusion matrix parameter, default is None
        :is_cm: an optional flag, set to True. If confusion matrix is provided
        :return: a dictionary of confusion matrix attributes
        """

        if not is_cm:
            cm = confusion_matrix(self.y_test, self.get_prediction_class())
        tp = cm[1][1]
        tn = cm[0][0]
        fp = cm[0][1]
        fn = cm[1][0]

        total: int = tp + tn + fp + fn
        actual_no: int = tn + fp
        actual_yes: int = fn + fp

        return {
            "accuracy": (tp + tn) / total,
            "error_rate": (fp + fn) / total,
            "sensitivity": tp / float(actual_yes),
            "specificity": tn / float(actual_no),
            "false_positve_rate": fp / float(actual_no)
        }
