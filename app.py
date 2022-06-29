from flask import Flask, render_template, request, send_file
from flask_cors import cross_origin
import pandas as pd
import os
import glob
from werkzeug.utils import secure_filename

from logging_details.custom_logging import ApplicationLogging
from data_validation.validation import DataValidation
from data_preprocessing.preprocessing import DataPreprocessor
from data_prediction.prediction import DataPrediction

log = ApplicationLogging()
# Creating Data Validation Object
dataValidationObject = DataValidation()
ALLOWED_EXTENSIONS = {'csv'}

app = Flask(__name__)


@app.route("/", methods=['POST', 'GET'])
@cross_origin()
def homePage():
    """
    It deletes the previous input and predicted data from Prediction_Files
    :return: web page : Home page of the program
    """
    try:
        dataValidationObject.deletePreviousInputFiles()

        return render_template('input.html', data={"massage": "Upload Your csv file or give the data manually",
                                                   "isError": False})
    except Exception as e:
        log.Error("(homePage) ::" + str(e))
        return render_template('error.html', massage="Something Went Wrong Try Again !!!")


@app.route("/manualDataEntry", methods=['POST', 'GET'])
@cross_origin()
def manualDataInput():
    """
    It is responsible for take data manually from the user.
    It also validates the input data (basically it converts the text into lowercase letter)
    :return:
    """
    log.Info("(manualDataInput) :: User give the data manually")
    try:
        # checking files in Prediction_Files folder
        if os.path.exists('Prediction_Files/*.csv') or len(os.listdir('Prediction_Files/')):
            dataValidationObject.deletePreviousInputFiles()

        if not os.path.isdir('prediction_Files/'):
            os.mkdir(f'prediction_Files/')
            
        if request.method == 'POST':
            # Take the data from HTML page
            manualData = request.form.to_dict(flat=False)
            pd.DataFrame.from_dict(manualData).to_csv('Prediction_Files/input_data.csv', index=False)
            data = pd.read_csv('Prediction_Files/input_data.csv')

            data1 = dataValidationObject.convertValuesIntoLowerCase(data)
            data1.to_csv('Prediction_Files/Validated_Input_Data.csv', index=False)

        return render_template('input.html', data={"massage": "You give data manually. The data is uploaded. "
                                                              "Ready for Prediction", "isError": False})
    except Exception as e:
        log.Error("(manualDataInput) ::" + str(e))
        return render_template('input.html', data={"massage": "Something went wrong in your input data. "
                                                              "Enter your data again !!!", "isError": True})


def checkingFileExtension(filename):
    """
    It checking the file extensions of the input file
    :param filename: str : path of the file
    :return:
    """
    return '.' in filename and filename.split('.')[1].lower() in ALLOWED_EXTENSIONS


@app.route("/uploadFile", methods=['POST', 'GET'])
@cross_origin()
def uploadCSVfile():
    """
    It is responsible for take csv file from the user.
    It also validates the csv file
    :return:
    """
    log.Info("(uploadCSVfile) :: User chose to upload data by csv file")
    try:
        # checking files in Prediction_Files folder
        if os.path.exists('Prediction_Files/*.csv') or len(os.listdir('Prediction_Files/')):
            dataValidationObject.deletePreviousInputFiles()
            
        if not os.path.isdir('prediction_Files/'):
            os.mkdir(f'prediction_Files/')

        if request.method == 'POST':
            if request.files['file'] is not None:
                file = request.files['file']

                # Checking the file extension
                if checkingFileExtension(file.filename):
                    file.save(os.path.join('Prediction_Files/', secure_filename(file.filename)))
                    inputFilelist = glob.glob('Prediction_Files/*.csv')
                    inputdata = pd.read_csv(inputFilelist[0])

                    isMissingColumn, missingColumns = dataValidationObject.checkingInputData(inputdata)

                    # if there is a missing column we go to the homePage
                    if isMissingColumn:
                        return render_template('input.html', data={"massage": f"There are some missing columns \n\t "
                                                                              f"Column names are{missingColumns}",
                                                                   "isError": True})
                    else:
                        # We validate the elements of input csv file
                        validatedInputData = dataValidationObject.getValidatedInputData(inputdata)
                        validatedInputData.to_csv('Prediction_Files/Validated_Input_Data.csv', index=False)
                else:
                    return render_template('input.html',
                                           data={"massage": "File extension is not csv. Please enter a csv file ",
                                                 "isError": True})
            else:
                return render_template('input.html', data={"massage": "Chose the file first", "isError": True})

        return render_template('input.html',
                               data={"massage": "Your data is uploaded. Ready for prediction", "isError": False})
    except Exception as e:
        log.Error("(uploadCSVfile) ::" + str(e))
        return render_template('input.html',
                               data={"massage": "Something went wrong in your input data. Enter your data again !!!",
                                     "isError": True})


@app.route('/predict', methods=['GET', 'POST'])
@cross_origin()
def predict():
    """
    It predicts the target column from the user input data
    :return:
    """
    try:
        # Read the input csv file
        df = pd.read_csv('Prediction_Files/Validated_Input_Data.csv')

        # Creating PreProcessing Object
        preprocessingObject = DataPreprocessor()
        preprossedData = preprocessingObject.getPreprocessedData(df)

        # Creating Prediction Object
        predictionObject = DataPrediction()
        predictionData, predictionDataColumns = predictionObject.getPrediction(preprossedData)

        log.Info("(predict) :: Result is shown in HTML file")
        return render_template('prediction.html', result=[enumerate(predictionData), predictionDataColumns])
    except Exception as e:
        log.Error("(predict) ::" + str(e))
        return render_template('error.html', massage="Something went wrong. Go to the home page and Try Again !!!")


@app.route('/download', methods=['GET', 'POST'])
@cross_origin()
def download():
    """
    It helps us to download the result csv
    :return:
    """
    try:
        log.Info("(download) :: Result is downloaded")
        return send_file(os.path.join('Prediction_Files/') + 'Result.csv', as_attachment=True)
    except Exception as e:
        log.Error("(download) ::" + str(e))
        return render_template('error.html', massage="Can't Download the result. Something went wrong. Try Again !!!")


if __name__ == '__main__':
    log.Info("(app) :: $=============== Application started ===============$")
    app.run()
