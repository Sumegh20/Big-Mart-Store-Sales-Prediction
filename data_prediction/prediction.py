import pickle
import pandas as pd

from logging_details.custom_logging import ApplicationLogging
from file_operation.file_handler import FileHandler


log = ApplicationLogging()
file = FileHandler()

class DataPrediction:
    def __init__(self):
        self.model = "models/Gradientboost_model.pickle"

    # As we transfrom our traget data y^0.3
    def tragetColumnTransformation(self, element):
        return round(element**(1/0.3), 4)

    def getPrediction(self, data):
        """
        It loads the model and give us prediction
        :param data: pandas DataFrame : It is the PreProcessed dataset
        :return: pandas DataFrame with the predicted column
        """
        log.Info("(getPrediction) :: Started prediction")
        try:
            # predictModel = pickle.loads(open(self.model, "rb").read())
            predictModel = file.loadModel(self.model)

            # Calculate the prediction
            y_pred = predictModel.predict(data)

            # Store the prediction into the DataFrame after the transformation
            data['SALES_PREDICTION'] = [self.tragetColumnTransformation(i) for i in y_pred]

            # # Create the name of the final csv file
            # inputFilelist = glob.glob('Prediction_Files/*.csv')
            # fileName = inputFilelist[0].split('\\')[1].split('.')[0]

            # # store the data into a csv file in the Prediction_Files folder
            # data.to_csv(f'Prediction_Files/Result.csv')

            # store the data into a csv file in the Prediction_Files folder
            dataframe = pd.read_csv('Prediction_Files/Validated_Input_Data.csv')
            dataframe['SALES_PREDICTION'] = data['SALES_PREDICTION']
            dataframe.to_csv(f'Prediction_Files/Result.csv',index=False)

            # return the prediction column
            return dataframe.to_numpy(), dataframe.columns
        except Exception as e:
            log.Error("(getPrediction) ::"+str(e))