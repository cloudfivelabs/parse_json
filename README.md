The goal of this excercise is to create a CSV to JSON converter using any helpful tools or libraries, with the exception of those designed to handle CSV parsing.

The input should be valid CSV and the output should be valid JSON. 

* The CSV file will consist of multiple rows. 
* The rows are newline-delimited and columns are comma-separated.  
* The first row will always be a header row. 
* All rows will have the same number of columns.
* Entries can optionally be enclosed in double quotation marks, with quotation marks in the data denoted as "" inside of a quoted field (For example """This is a great idea,"" he said.").  
* Any ascii characters, including newlines, can appear inside of quotations.

The data will be transformed into a JSON output that consists of an array of objects.  Each object will be composed of fields with the names of the headers and values from the corresponding row. Numbers should translate to JSON numbers while anything else is a string.

Example input CSV file:

```
ID, Name, Age, Favorite Color
1, Bob, 23, Red
2, Samuel, 99, Turquoise
3, "Doe, John", 44, Orange
4, Jimmy, 16, "bold, Bold, BOLD,
BOOOOLDDD Blue"
```

Example output valid JSON file:

```
[
  {
    "ID": 1,
    "Name": "Bob",
    "Age": 23,
    "Favorite Color": "Red"
  },
  {
    "ID": 2,
    "Name": "Samuel",
    "Age": 99,
    "Favorite Color": "Turquoise"
  },
  {
    "ID": 3,
    "Name": "\"Doe, John\"",
    "Age": 44,
    "Favorite Color": "Orange"
  },
  {
    "ID": 4,
    "Name": "Jimmy",
    "Age": 16,
    "Favorite Color": "\"bold, Bold, BOLD,\nBOOOOLDDD Blue\""
  }
]
```

Solution:

This solution uses Python 2.7.11 and is coded in the file: `parse.py`

Two sample json files are included:

`text1.csv`

`text2.csv`

Running the code:

`> python parse.py`

The user will be propmpted to enter the CSV file to parse. 

`CSV file to parse [text1.csv]:`

Hitting enter/return will use the default file: `text1.csv`

The output JSON file is printed to standard out, and also to a file called 'output.json'

NOTES:

* The most common way to read in a file from Python is probably not going to work well here.
* Proper escaping of newlines and quotes is very important
* Parsing is hard to do with Python lists.

FURTHER IMPROVEMENTS:

* Improved error handling
* Additional command line arguments
* Input file validation (check and handle CSV format problems)
* Improved JSON formatting
* Improved modularity (split file reading / writing into own functions)
* Ability to specify other output formats
* Import other helpful utility libraries (command line args, logging, etc.)



