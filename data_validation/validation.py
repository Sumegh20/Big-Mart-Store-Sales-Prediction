import json
import os
import glob
import numpy as np

from logging_details.custom_logging import ApplicationLogging
log = ApplicationLogging()

class DataValidation:
    def __init__(self):
        self.schema = 'dataset_schema.json'

    def deletePreviousInputFiles(self):
        """
        It deletes the previous csv files from Prediction_Files, if exist
        :return: Nothing
        """
        try:
            if len(os.listdir('Prediction_Files/')):
                filelist = glob.glob('Prediction_Files/*.csv')
                for file in filelist:
                    os.remove(file)
        except Exception as e:
            log.Error("(deletePreviousInputFiles) ::" + str(e))

    def getSchemaValues(self, columnName):
        """
        It opens the (dataset_schema.json) file and return the required information
        :param columnName: str :: Enter column name in double quotation
        :return: required information about the dataset
        """
        try:
            with open(self.schema, 'r') as f:
                dic = json.load(f)
                f.close()

            information = dic[columnName]

            return information
        except Exception as e:
            log.Error("(getSchemaValues) ::" + str(e))

    def checkingInputData(self, data):
        """
        It checks the input dataset. That at least it contains all required columns(features) for the prediction
        :param data: Pandas DataFrame: User input dataset
        :return: two variable : One Flag variable and One list of missing columns(features)
        """
        try:
            inputColumnNames = data.columns
            requiredColumnNames = self.getSchemaValues("columnNames")

            isColumnMissing = False
            missingColumns = []
            for columnName in requiredColumnNames:
                if not columnName in inputColumnNames:
                    missingColumns.append(columnName)
                    isColumnMissing = True

            return isColumnMissing, missingColumns
        except Exception as e:
            log.Error("(checkingInputData) ::" + str(e))

    @staticmethod
    def getUnessentialFeature(list1, list2):
        """
        It is a static method. to identify extra columns and store them into a list
        :param list1: python list : list of required features(columns) for prediction
        :param list2: python list : list of features coming from user input data
        :return: python list : list of unimportant(unessential) features for prediction
        """
        try:
            extraElement=[]
            for element in list2:
                if not element in list1:
                    extraElement.append(element)

            return extraElement
        except Exception as e:
            log.Error("(getUnessentialFeature) ::"+str(e))

    def deleteUnessentialColumns(self, data):
        """
        It delete the unimportant(unessential) features from the dataset.
        :param data: pandas DataFrame : User given dataset
        :return: pandas DataFrame : After removing the unimportant(unessential) features
        """
        try:
            requiredColumnNumber = self.getSchemaValues("columnNumber")
            requiredColumnNames = self.getSchemaValues("columnNames")

            inputColumnNames = data.columns
            inputColumnNumbers = len(inputColumnNames)

            if inputColumnNumbers > requiredColumnNumber:
                # collect the unimportant(unessential) features
                unessentialFeature = self.getUnessentialFeature(requiredColumnNames, inputColumnNames)

                # deleting unimportant(unessential) features from DataFrame
                data.drop(labels=unessentialFeature, axis=1, inplace=True)

            return data
        except Exception as e:
            log.Error("(deleteUnessentialColumns) ::"+str(e))

    def convertValuesIntoLowerCase(self, data):
        """
        It converts the categorical features elements into lower case letter. And save the file into it's location
        :param data: pandas DataFrame: User input dataset
        :return: pandas DataFrame : After convert the values of categorical columns in to lower case
        """
        try:
            data = data.applymap(lambda s: s.lower() if type(s) == str else s)
            #data.to_csv('Prediction_Files/input_data.csv', index=False)
            return data
        except Exception as e:
            log.Error("(convertValuesIntoLowerCase) ::" + str(e))

    def isFloatable(self, string):
        """
        It checks that can we convert the string into a float
        :param string: python string:
        :return: bool :
        """
        try:
            float(string)
            return True
        except Exception as e:
            return False

    def stringToFloatConversion(self, s):
        """
        It typecast the string data in to float
        :param s:
        :return:
        """
        try:
            if type(s) in [str, int, float]:
                if type(s) == str:
                    if self.isFloatable(s):
                        return float(s)
                    else:
                        return np.nan
                else:
                    return s
            else:
                return np.nan
        except Exception as e:
            log.Error("(stringToFloatConversion) ::"+str(e))

    def checkingNumericalColumn(self, data):
        """
        It checks the numerical columns of the data.
        :param data: pandas DataFrame: User input dataset.
        :return: pandas DataFrame: After the validation of numerical columns.
        """
        try:
            NumericalColumns = self.getSchemaValues("NumericalColumns")

            for i in NumericalColumns:
                data[[i]] = data[[i]].applymap(lambda s: self.stringToFloatConversion(s))

            return data
        except Exception as e:
            log.Error("(checkingNumericalColumn) ::"+str(e))

    def checkingCategoricalColumns(self, data):
        """
        It deals with the unknown category of all categorical columns
        :param data: pandas DataFrame: User input dataset.
        :return: pandas DataFrame: After checking and transforming the columns
        """
        try:
            CategoricalColumns = self.getSchemaValues("CategoricalColumns")
            for i in CategoricalColumns:
                checklist = self.getSchemaValues(i)
                for count, element in enumerate(data[i]):
                    if not element in checklist:
                        data[i][count] = np.nan
            return data
        except Exception as e:
            log.Error("(checkingCategoricalColumns) ::"+str(e))

    def getValidatedInputData(self, data):
        """
        It is the main method of this class. We call only use this method to validate our dataset.
        :param data: pandas DataFrame: User input dataset.
        :return: pandas DataFrame: Gives the final validate data
        """
        log.Info("(getValidatedInputData) :: Input dataset validation started")
        try:
            # Delete the unimportant(unessential) features from the dataset.
            importantColumnsData = self.deleteUnessentialColumns(data)
            log.Info("(getValidatedInputData) :: Unessential columns are deleted")

            # Convert the elements in to lower case
            lowerCaseData = self.convertValuesIntoLowerCase(importantColumnsData)
            log.Info("(getValidatedInputData) :: Convert the elements of string columns into lowercase letter")

            # Checking the Numerical columns
            NumericalData = self.checkingNumericalColumn(lowerCaseData)
            log.Info("(getValidatedInputData) :: Numerical columns are checked")

            # Checking Categorical Columns
            FinalData = self.checkingCategoricalColumns(NumericalData)
            log.Info("(getValidatedInputData) :: Categorical columns are checked")

            return FinalData
        except Exception as e:
            log.Error("(getValidatedInputData) ::"+str(e))

