To run the apriori algorithm follow these steps:

Start by initiating a venv state on your desired python complier.
(If you are doing this on terminal, you can try using the command "source ./venv/bin/activate")

next use "python hw2.py data.txt *change this to any minimum support* *change this to any file name for output*"
here is an example of how the command might look like

(venv) reaper@macs-air CS470 % python hw2.py data.txt 500 result500.txt
(venv) reaper@macs-air CS470 % 

When you are doing this, make sure that data.txt (or which ever dataset you are using), hw2.py, and a venv file is present
in the directory that terminal (or cmd) is opened.

If you have pycharm installed, feel free to edit the code or rename the file to main to run the code.
If for some reason you do not know how to run a python file using system arguments, also feel free to manually change the "sys.argv[3]" appropriately with sys.argv[1] being the file name, sys.argv[2] being the minimum support, and sys.argv[3] being the output file name.