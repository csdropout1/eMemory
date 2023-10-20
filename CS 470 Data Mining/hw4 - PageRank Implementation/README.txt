To run the pageRank algorithm follow these steps:

Start by initiating a venv state on your desired python complier.
(If you are doing this on terminal, you can try using the command "source ./venv/bin/activate")

next use "python hw4.py input.dot output.csv" *change the file names accordingly.

here is an example of how the command might look like

(venv) reaper@macs-air CS470 % python hw4.py graph3.dot pagerank3.csv
(venv) reaper@macs-air CS470 % 

When you are doing this, make sure that graph1.dot (or which ever dot file you are using), hw4.py, and a venv file is present in the directory that terminal (or cmd) is opened.

If you have pycharm installed, feel free to edit the code or rename the file to main to run the code.
If for some reason you do not know how to run a python file using system arguments, also feel free to manually change the "sys.argv[x]" appropriately with sys.argv[1] being the file name and sys.argv[2]  being the output file name.