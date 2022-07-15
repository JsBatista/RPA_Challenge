# RPA_Challenge

This project is the execution of a challenge focused on ***Robotic Proccess Automation*** using ***Python***.

## Challenge Guidelines

The process is initiated by accessing the folder 'RPA-Article', there, you must open each file as long as it is a *'.pdf'* file whose name starts with a number. Then, you must open the *'Save as'* window, rename this file as *'Page X - Modified'*, where the file number X must be the same as the original number from its name.

The automation must create a spreadsheet with the name 'Execution Report' with field **'File name'** and **'Status'**. Everytime a file is proccessed by the previous pipeline, you must insert the original file name on the **'File name'** column, and insert *'file modified'* on the **'Status'** column. After finishing everything, remember to close all the windows. The spreadsheet and the new documents must be saved in the original folder.

All the above text was translated from the original text, originally in Portuguese-BR. Any changes to the script regarding localization such as these can be made easily in the ***'constants.py'*** file.

## How To Run It

System Requirements:
  * ***Windows 7*** or above
  * ***Python 3.8.3*** or above
  * ***Pip*** package manager for *Python* 
  * ***Adobe Acrobat Reader***  : [link for download](https://get.adobe.com/br/reader/)


After installing Python, use Pip to install the following libraries:

    pip install pywinauto

    pip install pandas

    pip install pathlib

After all the libraries are installed successfully, head to the main project directory and run:

    python src/main.py

Make sure that you use the right python executable. For instance, you may have to change ***python*** to ***python3***.

You can also insert the directory path directly as a command line argument:

    python src/main.py "C:\Users\YOUR_USER\..."

You can also specify if you want to delete the original files by adding a 'Y' after the directory path.

    python src/main.py "C:\Users\YOUR_USER\..." Y
    
## The RPA Process Flow

For this challenge, was created a diagram that show exaclty what is happening inside the RPA, with all possible branches and exits for the script.

The diagram is available both in English and Portuguese-BR:

* [RPA Flow Diagram (English)](https://drive.google.com/file/d/1LNJwvPVYGafs4S6x7kFgtBjG1kadcpnf/view?usp=sharing)
* [RPA Flow Diagram (Portuguese-BR)](https://drive.google.com/file/d/1o7HKqocmTIz_DPU-EmvcGrV-mnSr5VCp/view?usp=sharing)
