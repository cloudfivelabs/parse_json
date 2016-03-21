# get filename to parse or use default
filename = raw_input("CSV file to parse [text1.csv]:") or "text1.csv"

# the list to incremntally build the JSON object
json_list = [ "[" ]

# the CSV header row used to lookup the column names
header_list = None

# keep track of which CSV colum we are parsing
number_of_csv_columns = None

# whether to print lots of debug statements
debug = False

# function to build the JSON list (called from the parse loop)
def build_json( column_index, value, is_end_of_file ):

    # get the correct column header and remove any whitespace
    column_string = ( header_list[column_index] ).strip()
    if debug: print "calling write_json with column: {}  and value: {}".format( column_index, column_string )

    # dont add a comma to the end of the JSON when we are parsing the last item
    last_character = ','
    if is_end_of_file:
        last_character = ''
    if column_index == 0:
        begin = '{'
        end = ','
    elif column_index == number_of_csv_columns-1:
        begin = ''
        end = '}' + last_character
    else:
        begin = ''
        end = ','

    # create the JSON token, remembering to treat numbers differently in JSON
    token = ''
    if value.isdigit():
      token += begin + "\"" + column_string + "\": " + value + end
    else:
      token += begin + "\"" + column_string + "\": \"" + value + "\"" + end

    json_list.append(token)
    return None

# shortcut to find the number of columns in the CSV file
with open( filename, 'r') as file:
  # read each line into a list of lines
  list_of_lines = file.readlines()
  # get the first 'header' line and divide it into JSON keys
  header_list = ( list_of_lines.pop(0) ).split(",")
  # get the number of keys to determine the number of expected tokens per line
  number_of_csv_columns = len( header_list )
  # convert the rest of the file to a string for parsing
  file_string = ''.join(list_of_lines)

# function to keep track of which column we are on in the file
def increment_column( column ):
    column += 1
    if column == number_of_csv_columns:
        column = 0
    return column

# get the first line (header) of the file
# tokenize the header to get the number of values
# read the whole file in as a string

# read each character to tokenize the string
# the number of tokens depends on the number of CSV columns
# do not split on commas inside quotes
# preserve newlines inside quotes

# if the character is a number, continue until a non number is found
#     add the number string to the json list unquoted
#
# if the character is not a number:
#     if character is a quote, set flag
#     if character is a newline set flag
#
#     if character is a comma and the quote flag is not set,
#       add the string up to that counter as next token to the list
#     if character is a newline and the quote flag is not set, return
#     if character is a newline and the quote flag is set, escape the newline

current_column = 0

digit_started = False
quote_started = False
is_end_of_file = False

number_string = ''
token_string = ''

# get each character in the CSV file string
for idx, character_value in enumerate( file_string ):

    #if debug: print "{} : {}".format( idx, len( file_string ) )

    # check to see if we are on the last character of the file
    if idx + 1 == len( file_string ):
        is_end_of_file = True

    # start to parse chracters as a digit
    if character_value.isdigit():
        digit_started = True
        number_string += character_value

    # check to see if digit parsing is done
    elif digit_started and not character_value.isdigit():
        digit_started = False
        build_json( current_column, number_string, is_end_of_file)
        number_string = ''
        current_column = increment_column( current_column )

    # handle SPACES
    elif character_value == ' ':
        if quote_started:
            if debug: print "space inside quotes"
            token_string += character_value
        else:
            if debug: print "space outside quotes: ", token_string
            continue

    # handle NEWLINES
    elif character_value == '\n':
        if quote_started:
            if debug: print "newline inside quotes"
            token_string += '\\n'
        else:
            if debug: print "newline ended token", token_string
            build_json( current_column, token_string, is_end_of_file )
            token_string = ''
            current_column = 0

    # handle QUOTES
    elif character_value == '"':
        if not quote_started:
            if debug: print "started quote"
            # escape the quote for the JSON string
            token_string += '\\"'
            quote_started = True
        else:
            if debug: print "ended quote"
            # escape the quote for the JSON string
            token_string += '\\"'
            quote_started = False

    # handle COMMAS
    elif character_value == ",":
        if quote_started:
            if debug: print "found comma inside quotes"
            token_string += character_value
        else:
            if debug: print "ended token",token_string
            build_json( current_column, token_string, is_end_of_file )
            current_column = increment_column( current_column )
            token_string = ''

    # handle everything else
    else:
        token_string += character_value

json_list.append( "]" );
print ''
print ''.join(json_list)

with open ("output.json", "w") as output_file:
    for item in json_list:
        output_file.write("%s\n" % "".join(item))
