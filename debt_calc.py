import os
from googleapiclient.discovery import build

#####################################################################
# code from stack overflow (with additions and modifications by me) #
#####################################################################

# function to return dict for 'add_data'
# fields is a mask to return only certain values from the spreadsheet
""" 
sheets(data(rowData(values(effectiveFormat/backgroundColor,formattedValue)),startColumn,startRow),properties(sheetId,title))

RETURNS:

SHEETS: data, properties

	DATA: rowData, startColumn, startRow

		ROWDATA: values

			VALUES: effectiveFormat/backgroundColor, formattedValue

				effectiveFormat/backgroundColor

				formattedValue

		startColumn

		startRow

	PROPERTIES: sheetID, title
		
		sheetID

		title
		
In other words, it returns only these attributes:
effectiveFormat/backgroundColor, formattedValue, startColumn, startRow, sheetID, title
"""

def get_sheet_colors(service, wbId: str, ranges: list):
    params = {'spreadsheetId': wbId,
              'ranges': ranges,
              'fields': 'sheets(data(rowData(values(effectiveFormat/backgroundColor,formattedValue)),startColumn,startRow),properties(sheetId,title))'}
    return service.spreadsheets().get(**params).execute()

def get_info_arrs():
    # declaration of service object
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="E:\\VSCode\\discord-bot-project\\discord-bot-352004-95d1d5f53a9d.json"
    service_obj = build('sheets', 'v4')
    sheet_id = '1cWEmMLPJBN803RNeucffQcJglPTY9DS54wrYPCHcHE0'

    desiredA1NotationRanges = []
    all_data = get_sheet_colors(service_obj, sheet_id, desiredA1NotationRanges)

    # close the service object
    service_obj.close()
    # all_data is a dict with keys determined by the fields in the request
    # (i.e. "sheets") and the output of the API method used (aka consult your API reference)

    dataset = []
    default_bg = {'red': 1, 'green': 1, 'blue': 1}
    # all_data['sheets'] is a list of sheet resources (per the API spec.)
    for sheet in all_data['sheets']:
        # The sheet resource is a dict with keys determined by what we requested in fields
        # (i.e. properties (->sheetId, ->title), data)
        print('Sheet name is {title} with grid id {sheetId}'.format_map(sheet["properties"]))
        # each range in data will only contain startRow and/or startColumn if they are not 0
        # (i.e. if you grab A1:___, you won't have startRow or startColumn)
        for range in sheet['data']:
            rowData = range.get('rowData', [])
            if not rowData:
                continue
            offsets = {'row': range.get('startRow', 0),
                    'col': range.get('startColumn', 0)}
            rangeBGs = [default_bg] * offsets['row']
            rangeValues = [''] * offsets['row']
            for row in rowData:
                # sentinel value to see if row is empty or not, becomes true if a single valid value is inserted
                sentinel = False
                colData = row['values']
                newBGs = [default_bg] * offsets['col']
                newVals = [''] * offsets['col']
                for col in colData:
                    try:
                        newBGs.append(col['effectiveFormat']['backgroundColor'])
                    except KeyError:
                        newBGs.append(default_bg) # Shouldn't get called (all cells have a background)
                    try:
                        newVals.append(col['formattedValue']) # Always a string if present.
                    except KeyError:
                        newVals.append('') # Not all cells have a value.
                    else:
                        sentinel = True # sets sentinel to true if the row contains at least one value
                # as long as the row has at least one value append bg and value list to dataset
                if sentinel:
                    rangeBGs.append(newBGs)
                    rangeValues.append(newVals)
            dataset.append({'sheetId': sheet['properties']['sheetId'],
                            'sheetName': sheet['properties']['title'],
                            'backgrounds': rangeBGs,
                            'values': rangeValues})

    # BACKGROUND/VALUE [row][column]

    # dataset is now a list with elements that correspond to the requested ranges,
    # and contain 0-base row and column indexed arrays of the backgrounds and values.
    # One could add logic to pop elements from the ranges if the entire row has no values.
    #   ^^ added through the sentinel boolean variable ^^
    # Color in A1 of 1st range:
    return dataset

# print(f'Cell A1 color is {r1["backgrounds"][0][0]} and has value {r1["values"][0][0]}')
# print(f'Cell D2 color is {r1["backgrounds"][1][3]} and has value {r1["values"][1][3]}')
# print(f'Cell A21 has color {r1["backgrounds"][19][0]} with value {r1["values"][19][0]}')

###################################
# END OF CODE FROM STACK OVERFLOW #
###################################


# loop through all rows (debts) and calculate the amount owed per person
# this will be done using a nested dict structure of the style:
# {
# "Parker": {          
#           "Logan": $x
#           .
#           .
#           .
#           "Thomas": $y     
#           }
#
#  "Logan": {
#           }
# .
# .
# .
#
# "Thomas": {
#           }
# }

# calculates and returns the data structure containing all the debt information
def calc_indv_debts():
    # parse the document into information arrays
    r1 = get_info_arrs()[0]
    bgs = r1['backgrounds']
    vals = r1['values']

    # 0 indexed position of the column with the name of the person owed
    owedCol = 2
    # 0 indexted position of the first column with values to add
    startCol = 3
    # number of rows and columns in the sheet
    numRows = len(vals)
    numCols = len(vals[0])
    
    # dictionary of dictionaries to store each person's debts and who they owe
    debts = {}
    for col in range(startCol, numCols):
        # The name of the person whos debt column currently being totaled
        currPer = vals[0][col]
        # initialize the sub dictionary for that person
        debts[currPer]={'Total': 0}
        # go through each row and calculate the total debt owed
        for entry in range(1, numRows):
            # if the cell is green (payed) or 'N/A' then do not consider it
            # 'red' in bgs is used because green squares do not contain a red value while white has
            # red blue and green all set to 1
            if (not vals[entry][col] == 'N/A') and ('red' in bgs[entry][col]):
                # value of the debt to be added
                tempV = float(str(vals[entry][col]).replace("$", ""))
                # updates the amount owed to the given person, if the currPer has yet to accumulate a debt
                # to the given person, creates a new entry for them
                debts[currPer]['Total'] += tempV
                if vals[entry][owedCol] not in debts[currPer]:
                    debts[currPer][vals[entry][owedCol]] = tempV
                else:
                    debts[currPer][vals[entry][owedCol]] += tempV

    # return final dict structure
    return debts

