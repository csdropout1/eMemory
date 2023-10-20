To run the apriori algorithm follow these steps:

Start by initiating a venv state on your desired python complier.
(If you are doing this on terminal, you can try using the command "source ./venv/bin/activate")

next use "python hw3.py iris.data *change this to any minimum support* *change this to any file name for output*"
here is an example of how the command might look like

(venv) reaper@macs-air CS470 % python hw3.py iris.data 500 prettyiris.txt
(venv) reaper@macs-air CS470 % 

##### NOTE: DUE TO THE NATURE OF CATEGORICAL DATA CLEANING, IF YOU WANT TO TEST THIS PROGRAM ON A DIFFERENT DATASET,
ADJUSTMENTS WILL HAVE TO BE MADE IN THE CODE!!!

*For example, I tested my program with the abalone.data file, and I cleaned it by removing the first letter and the last value that was greater than 1. Edit the line (10) using df.drop!

When you are doing this, make sure that iris.data (or which ever dataset you are using), hw3.py, and a venv file is present
in the directory that terminal (or cmd) is opened.

If you have pycharm installed, feel free to edit the code or rename the file to main to run the code.
If for some reason you do not know how to run a python file using system arguments, also feel free to manually change the "sys.argv[n]" appropriately with sys.argv[1] being the file name, sys.argv[2] being k in k means, and sys.argv[3] being the output file name.