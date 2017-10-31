"""
    find political donors.py
    require python version >= 2.7
"""

# imports
from __future__ import division
import sys


# data structures
class medianZipUnit:
    ''' a data structure designed for elements in medianvals_by_zip.txt
    '''
    __slots__ = ('recipient', 'zip_code', 'running_median', 'total_number', 'total_amount') # save memory

    def __init__(self, recipient="", zip_code="", running_media=0, total_number=0, total_amount=0):
        self.recipient = recipient
	self.zip_code = zip_code
	self.running_median = running_media
	self.total_number = total_number
	self.total_amount = total_amount

    def isEqual(self, r):
        if self.recipient == r.recipient and self.zip_code == r.zip_code:
	    return True
	else: return False



class medianZipContainer:
    ''' a helper class for organizing entries in medianvals_by_zip.txt

        This calss manipulate medianvals_by_zip.txt
	when pushing an entry to this class, it will open the txt file,
	search the file see if file already has a same entry and update
	the txt file accordingly

        in order to make the program scalable, for each
	push event, this class will open txt file and then close it

	This will make program slower, because of the frequent disk accessing,
	but it will work when processing huge input files, like GB level

	file should be stored in output/medianvals_by_zip.txt
    '''
    __slots__=('path', 'tool') # save memory

    def __init__(self, path = "output/medianvals_by_zip.txt"): # hard code, given that the default structure is fixed
        ''' default initializer
	'''
        self.path = path
	self.tool = unitProcessTool()
        
    def pushEntry(self, push_entry):
        ''' main interface
	    
	    this memeber accepts one entry, push it to txt file
	    this memeber also do usual checks for the entry being pushed in
	'''
	median = 0; total_number = 0; total_amount = 0
        
	try:
            with open(self.path, 'r') as txt:
	        # check if same entry exists
	        for line in txt:
	            _entry = self.tool.parseLine(line)
		    entry = medianZipUnit(_entry[0], _entry[1], int(_entry[2]), int(_entry[3]), int(_entry[4]))
		    if entry.isEqual(push_entry):
		        median = entry.running_median
		        total_number = entry.total_number
		        total_amount = entry.total_amount
        except:
	    pass # place holder

        try:
            with open(self.path, 'a') as txt:
	        # now append to the end of file
	        total_number = total_number + push_entry.total_number
	        total_amount = total_amount + push_entry.total_amount
	        median = int(round(total_amount/total_number))

	        txt.write(push_entry.recipient+'|'+push_entry.zip_code+'|'+str(median)+'|'+str(total_number)+'|'+str(total_amount) + '\n')
	except:
            with open(self.path, 'w') as txt:
	        # if file not exist, then create file
	        total_number = total_number + push_entry.total_number
	        total_amount = total_amount + push_entry.total_amount
	        median = int(round(total_amount/total_number))

	        txt.write(push_entry.recipient+'|'+push_entry.zip_code+'|'+str(median)+'|'+str(total_number)+'|'+str(total_amount) + '\n')

	    

class medianDateUnit:
    ''' a data structure designed for elements in medianvals_by_date.txt
    '''
    __slots__=('recipient', 'date', 'median', 'total_number', 'total_amount') # save memory

    def __init__(self, recipient="", date="", median=0, total_number=0, total_amount=0):
        self.recipient = recipient
	self.date = date
	self.median = median
	self.total_number = total_number
	self.total_amount = total_amount

    def isEqual(self, r):
        if self.recipient == r.recipient and self.date == r.date: return True
	else : return False



class medianDateContainer:
    ''' a helper class for organizing entries in medianvals_by_date.txt

        This calss manipulate medianvals_by_date.txt
	when pushing an entry to this class, it first open the txt file,
	then search the file see if file already had a same entry and then update
	the txt file accordingly

	this class also sort entries alphabetically and chronologically

	in order to make the program scalable, for each
	push event, this class will open txt file and then close it

	considering that this file is significantly smaller, to 
	make sorting easier, it will load the whole txt into memory

	file should be stored in output/medianvals_by_date.txt
    '''

    __slots__=('path', 'tool') # save memory

    def __init__(self, path="output/medianvals_by_date.txt"): # hard code path
        ''' default initializer
	'''
        self.path = path
	self.tool = unitProcessTool();

    def pushEntry(self, push_entry):
	# load txt to memory
        L = []
	try:
	    with open(self.path, 'r') as txt:
                for line in txt:
	            _element = self.tool.parseLine(line)
		    element = medianDateUnit(_element[0], _element[1], int(_element[2]), int(_element[3]), int(_element[4]))
		    L.append(element)
	except:
	    pass # place holder

        # update txt content
	exist = False; index = 0
	for i in L:
	    if i.isEqual(push_entry) and not exist:
	        total_number = i.total_number + push_entry.total_number
		total_amount = i.total_amount + push_entry.total_amount
		median = int(round(total_amount/total_number))
		# update
		i.median = median
		i.total_number = total_number
		i.total_amount = total_amount
		exist = True
		break
	    elif i.recipient < push_entry.recipient: # sorting alphabetically
	        index = index+1
	    elif i.recipient == push_entry.recipient:
	        i_date = i.date 
		p_date = push_entry.date 
	
	        if i_date < push_entry.date:         # sorting chronologically
		    index = index+1
	if not exist:
	    L.insert(index, push_entry)

        # rewrite txt file
	with open(self.path, 'w') as txt:
	    for i in L:
	        txt.write(i.recipient+'|'+i.date + '|' + str(i.median) + '|' + str(i.total_number) + '|' + str(i.total_amount) + '\n')



class unitProcessTool:
    ''' a utility class, for entry (in string format) processing
    '''
    __slots__=() # save memeory

    def __init__(self):
        pass # place holder

    def parseLine(self, line, delimit='|'):
        ''' string parser

            try to minimize 3rd party package dependency (only for this project),
            develop own string parser

            input parameter: a string (a line in a txt file)
	    return value: a string list
        '''
        s_res = []; val = ""
        for i in line:
            if i == delimit:
	        s_res.append(val)
                val = "" # clear
	    else:
	        val += i

        s_res.append(val) # last element in the line

        return s_res

    def interestedField(self, LL):
        ''' extract fields that will be used in this project
            based on field position in the line

	    position  0: CMTE_ID
	    position 10: ZIP_CODE
	    position 13: TRANSACTION_DT
	    position 14: TRANSACTION_AMT
	    position 15: OTHER_ID

	    input parameter: a string list
	    return value: a string list of only interested fields
        '''
	RR = ['', '', '', '', '']
	if len(LL) > 0  and len(LL[0])  > 0 and LL[0]  != '\n' : RR[0] = LL[0]
	if len(LL) > 10 and len(LL[10]) > 0 and LL[10] != '\n' : RR[1] = LL[10]
	if len(LL) > 13 and len(LL[13]) > 0 and LL[13] != '\n' : RR[2] = LL[13]
	if len(LL) > 14 and len(LL[14]) > 0 and LL[14] != '\n' : RR[3] = LL[14]
	if len(LL) > 15 and len(LL[15]) > 0 and LL[15] != '\n' : RR[4] = LL[15]
	return RR
        #return [LL[0], LL[10], LL[13], LL[14], LL[15]]

    def getZipUnit(self, LL):
        ''' pack a string list to medianZipUnit structure
	    string list only contain interstered fileds
	'''
        return medianZipUnit(LL[0], self.zipCode(LL[1]), int(LL[3]), 1, int(LL[3]))

    def getDateUnit(self, LL):
        ''' pack a string list to medianDateUnit structure
	    string list only contain interstered fileds
	'''
        return medianDateUnit(LL[0], LL[2], int(LL[3]), 1, int(LL[3]))

    def zipCode(self, L):
        ''' helper function, reorganize zip code

            input parameter: a string zip code
	    return value:    a 5-digit zip code
        '''

        if len(L) >= 5: return L[0:5] # only use the first 5 digits
        else: return L

    def isGoodDateFormat(self, s):
        ''' check date format, follow MMDDYYYY
	'''
        if len(s) != 8: return False
	mm = s[0:2]
	m = int(mm)
	if m<1 or m>12: return False
	dd = s[2:4]
	d = int(dd)
	if d<1 or d > 31: return False
	yy = s[4:8]
	y = int(yy)
	if y < 1900 or y > 2200: return False
	return True



# main entrance function
def readFile(path, zip_output, date_output):
    ''' read txt file, output line by line
    '''
    tool = unitProcessTool();
    zip_txt = medianZipContainer(zip_output);
    date_txt = medianDateContainer(date_output);

    try:
        with open(path, 'r') as f:
	    for line in f:
	        rres = tool.parseLine(line, '|')
	        res = tool.interestedField(rres)

		# input file considerations
		if len(res[4]) > 0 : continue # OTHER_ID field check
		if len(res[0]) == 0 or not res[3].isdigit() : continue # CMTE_ID, TRANSACTION_AMT check

                zip_unit = tool.getZipUnit(res)

		if tool.isGoodDateFormat(res[2]): # simple date check
	            date_unit = tool.getDateUnit(res)

                if len(res[1]) >= 5: # zip code check
	            zip_txt.pushEntry(zip_unit)
		if tool.isGoodDateFormat(res[2]): # simple date check
	            date_txt.pushEntry(date_unit)
    except IOError:
        print "IOError : Cannot open input file:", path
    except ValueError:
        print "ValueError\n"
    except EOFError:
        print "EOFError\n"
    except:
        print "other error...\n"


if __name__=="__main__":
    path = "input/itcont.txt" # default input file path
    zip_output = "output/medianvals_by_zip.txt" # default output file path, zip
    date_output = "output/medianvals_by_date.txt" # default output file path, date

    if len(sys.argv) == 2:    # pass input file path using cmd line
        path = sys.argv[1]
    if len(sys.argv) == 4:
        path = sys.argv[1]; zip_output = sys.argv[2]; date_output = sys.argv[3]

    readFile(path, zip_output, date_output)
