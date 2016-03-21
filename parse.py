# get filename to parse or use default
filename = raw_input("CSV file to parse:") or "text1.csv"

json_list = [ "[" ]
header_list = None
number_of_csv_columns = None
debug = True

def build_json( column_index, value, is_end_of_file ):

    # get the correct column header and remove any whitespace
    column_string = ( header_list[column_index] ).strip()
    if debug: print "calling write_json with column: {}  and value: {}".format(column_index,value)

    # dont add a comma to the end of the JSON
    last_character = ','
    if is_end_of_file:
        last_character = ''

    if column_index == 0:
        begin = '{'
        end = ','
    elif column_index == 3:
        begin = ''
        end = '}' + last_character
    else:
        begin = ''
        end = ','

    # treat numbers differently in JSON
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
  # get the number of keys to determine
  number_of_csv_columns = len( header_list )
  #print number_of_csv_columns
  file_string = ''.join(list_of_lines)

def increment_column( column ):
    column += 1
    if column == number_of_csv_columns:
        column = 0
    return column

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

    print "{} : {}".format( idx,len( file_string ) )
    if idx + 1 == len( file_string ):
        is_end_of_file = True

    # start to parse a digit
    if character_value.isdigit():
        digit_started = True
        number_string += character_value

    # check to see if digit parsing is done
    elif digit_started and not character_value.isdigit():
        digit_started = False
        build_json( current_column, number_string, is_end_of_file)
        number_string = ''
        current_column = increment_column( current_column )

    # SPACES
    elif character_value == ' ':
        if quote_started:
            if debug: print "space inside quotes"
            token_string += character_value
        else:
            if debug: print "space outside quotes: ", token_string
            continue

    # NEWLINES
    elif character_value == '\n':
        if quote_started:
            if debug: print "newline inside quotes"
            token_string += '\\n'
        else:
            if debug: print "newline ended token", token_string
            build_json( current_column, token_string, is_end_of_file )
            token_string = ''
            current_column = 0

    # QUOTES
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

    # COMMAS
    elif character_value == ",":
        if quote_started:
            if debug: print "found comma inside quotes"
            token_string += character_value
        else:
            if debug: print "ended token",token_string
            build_json( current_column, token_string, is_end_of_file )
            current_column = increment_column( current_column )
            token_string = ''

    # anything else
    else:
        token_string += character_value

json_list.append( "]" );
print ''.join(json_list)

with open ("output.json", "w") as output_file:
    for item in json_list:
        output_file.write("%s\n" % "".join(item))
