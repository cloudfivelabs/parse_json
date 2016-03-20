# get filename to parse or use default
filename = raw_input("CSV file to parse:") or "text1.csv"

newline_string = "\n"
json_list = [ "[{" ]
header_list = None
number_of_csv_columns = None

def write_json( column_index, value ):
    # get the correct column header and remove any whitespace
    column_string = ( header_list[column_index] ).strip()

    # treat numbers differently in JSON
    if value.isdigit():
      token =  "\""+column_string+"\": "+value+","
    else:
      token =  "\""+column_string+"\": \""+value+"\","

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

# open the file as a string
with open( filename, 'r') as file:
  #file_string = file.read()

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

  number_string = ''
  token_string = ''

  # get each character in the CSV file string
  for idx, character_value in enumerate( file_string ):

    # we have started parsing digits
    if character_value.isdigit():
        digit_started = True
        number_string += character_value

    # we may have finished parsing digits
    elif not character_value.isdigit() and digit_started:
        digit_started = False
        write_json( current_column, number_string)
        number_string = ''
        current_column = increment_column( current_column )

    # SPACES
    elif character_value == ' ' and quote_started:
        token_string += character_value
        print "space inside quotes"

    elif character_value == ' ' and not quote_started:
        print "space outside quotes: ", token_string
        continue

    # NEWLINES
    elif character_value == '\n' and quote_started:
        token_string += character_value
        print "newline inside quotes"

    elif character_value == '\n' and not quote_started:
        token_string += '}\n{'
        write_json( current_column, token_string)
        current_column = 0
        print "newline ended token", token_string
        token_string = ''

    # QUOTES
    elif character_value == '"' and not quote_started:
        token_string += character_value
        quote_started = True
        print "started quote"

    elif character_value == '"' and quote_started:
        token_string += character_value
        quote_started = False
        print "ended quote"

    # COMMAS
    elif character_value == "," and quote_started:
        token_string += character_value
        print "found comma inside quotes"

    elif character_value == "," and not quote_started:
        write_json( current_column, token_string)
        current_column = increment_column( current_column )
        print "ended token",token_string
        token_string = ''

    else:
        token_string += character_value
        #print "string parsing"

json_list.append( "]" );

print json_list

with open ("output.json", "w") as output_file:
    for item in json_list:
        output_file.write("%s\n" % "".join(item))
