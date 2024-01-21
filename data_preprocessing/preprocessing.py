import pandas as pd
import pickle
from datetime import datetime

from logging_details.custom_logging import ApplicationLogging
from file_operation.file_handler import FileHandler

log = ApplicationLogging()
fileObject = FileHandler()

class DataPreprocessor:
    def __init__(self):
        self.OneHot = "models/onehot_encoder_2.pickle" #"models/onehot_encoder.pickle"
        self.MinMax = "models/minmax_transformation_2.pickle"#"models/minmax_transformation.pickle"

    # Feature Engineering
    def YeartoAge(self, data):
        """
        It transforms the Outlet_Establishment_Year to Outlet_Age and drop the Outlet_Establishment_Year.
        :param data: pandas DataFrame : User input dataset.
        :return: pandas DataFrame : After the operations.
        """
        try:
            # Feature Engineering
            # data['Outlet_Age'] = datetime.now().year - int(data['Outlet_Establishment_Year'])
            data['Outlet_Age'] = data['Outlet_Establishment_Year'].apply(lambda x: datetime.now().year - int(x))

            # Drop the Outlet_Establishment_Year
            data.drop(['Outlet_Establishment_Year'], axis=1, inplace=True)

            return data
        except Exception as e:
            log.Error("(YeartoAge) ::"+str(e))

    def getMissingValueColumns(self, data):
        """
        Identification of missing columns
        :param data: pandas DataFrame : User input dataset.
        :return: python list : list of missing columns
        """
        try:
            inputColumnNames = data.columns
            missingColumns = [i for i in inputColumnNames if data[i].isnull().sum()>0]

            return missingColumns
        except Exception as e:
            log.Error("(getMissingValueColumns) ::"+str(e))

    def missingValueImputaion(self, data):
        """
        It imputes the missing columns of the user input data
        :param data: pandas DataFrame : User input dataset.
        :return: pandas DataFrame : DataFrame with no missing value
        """
        try:
            # This contained the replacement values of the missing values of each feature(column)
            # if column == categorical we take it's mode
            # if column == numeric we take it's median

            MissingValueImputerDictionary = {"Item_Type": "others", "Item_Weight": 12.6, "Item_Fat_Content": "low fat",
                                             "Item_MRP": 143.0128, "Outlet_Size": "small", "Outlet_Location_Type": "tier 3",
                                             "Outlet_Type": "supermarket type1", "Outlet_Establishment_Year": datetime.now().year-23}

            missingColumns = self.getMissingValueColumns(data)
            if len(missingColumns) > 0:
                for i in missingColumns:
                    data[i].fillna(value=MissingValueImputerDictionary[i], inplace=True)

            return data
        except Exception as e:
            log.Error("(missingValueImputaion) ::" + str(e))

    def outlierRemover(self, data):
        pass

    def dataTransformation(self, data):
        """
        It transforms the numerical columns
        :param data: pandas DataFrame : User input dataset
        :return: pandas DataFrame : After transform the numerical columns
        """
        try:
            featureList = ['Item_Weight', 'Item_MRP', 'Outlet_Age']
            # load minmax pickle file
            minmax_model = fileObject.loadModel(self.MinMax)
            standard_data = minmax_model.transform(data[featureList])

            for i, feature in enumerate(featureList):
                data[feature] = standard_data[:, i]

            return data
        except Exception as e:
            log.Error("(dataTransformation) ::" + str(e))

    def dataEncoding(self, data):
        """
        It Encodes the Ordinal and Nominal columns of the dataset.
        :param data: pandas DataFrame : User input dataset.
        :return: pandas DataFrame : After encoding the categorical columns.
        """
        # Ordinal Encoding
        Item_Fat_Content_map = {"low fat": "low fat", "lf": "low fat", "regular": "regular", "reg": "regular"}
        data['Item_Fat_Content'] = data['Item_Fat_Content'].map(Item_Fat_Content_map)

        Outlet_Size_map = {'small': 0,  'medium': 1, 'high': 2}
        data['Outlet_Size'] = data['Outlet_Size'].map(Outlet_Size_map)

        Outlet_Location_Type_map = {'tier 1': 2, 'tier1': 2, 'tier 2': 1, 'tier2': 1, 'tier 3': 0, 'tier3': 0}
        data['Outlet_Location_Type'] = data['Outlet_Location_Type'].map(Outlet_Location_Type_map)


        # OneHot Encoding
        # Define the one hot encoded feature(columns)
        featureList = ['Item_Fat_Content', 'Item_Type', 'Outlet_Type']
        # Load the onehot pickle file
        onehot_model = fileObject.loadModel(self.OneHot)
        # Transform the data
        onehot_vector = onehot_model.transform(data[featureList])
        # creating the feature names of the onehot vector after onehot transformation
        cols = ['Item_Fat_Content_regular', 'Item_Type_breads', 'Item_Type_breakfast', 'Item_Type_canned', 'Item_Type_dairy',
                'Item_Type_frozen foods', 'Item_Type_fruits and vegetables', 'Item_Type_hard drinks', 'Item_Type_health and hygiene',
                'Item_Type_household', 'Item_Type_meat', 'Item_Type_others', 'Item_Type_seafood', 'Item_Type_snack foods',
                'Item_Type_soft drinks', 'Item_Type_starchy foods', 'Outlet_Type_supermarket type1', 'Outlet_Type_supermarket type2',
                'Outlet_Type_supermarket type3']
        # creating DataFrame of onehot data
        onehot_dataframe = pd.DataFrame(onehot_vector, columns=cols)
        # concat with original data
        data = pd.concat([data, onehot_dataframe], axis=1)
        # Drop the featureList from original data after onehot transformation
        data.drop(featureList, axis=1, inplace=True)

        return data

    def getPreprocessedData(self, data):
        """
        It is the main method for preprocessing the data. Only call this function to preprocess the entire dataset.
        :param data: pandas DataFrame : User input dataset.
        :return: pandas DataFrame : The preprocessed dataset.
        """
        log.Info("(getPreprocessedData) :: Preprocessing started")
        try:
            # Missing Value Imputation
            df1 = self.missingValueImputaion(data)
            log.Info("(getPreprocessedData) :: Missing Values are imputed")

            # Convert Outlet_Establishment_Year to Outlet_Age
            df2 = self.YeartoAge(df1)
            log.Info("(getPreprocessedData) :: Outlet_Establishment_Year is Converted into Outlet_Age")

            # Transform the Numerical columns
            df3 = self.dataTransformation(df2)
            log.Info("(getPreprocessedData) :: Numerical columns are transformed")

            # Encoding the Categorical Variable
            df4 = self.dataEncoding(df3)
            log.Info("(getPreprocessedData) :: Cetegorical columns are encoded")

            return df4
        except Exception as e:
            log.Error("(getPreprocessedData) ::" + str(e))






