echo [$(date)]: "START"
echo [$(date)]: "Creating conda env with python 3.11.7"
conda create --prefix ./big_env python==3.11.7 -y
echo [$(date)]: "Activate the conda env"
source activate ./big_env
echo [$(date)]: "installing dev requirements"
pip install -r requirements.txt
echo [$(date)]: "END"

# Run the file by following command in the terminal
# bash init_setup.sh