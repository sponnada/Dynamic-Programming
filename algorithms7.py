#Sri Ponnada
#Algorithms

from operator import itemgetter


#this function checks two intervals to see if there is a conflict
#intervals are in the format [x, y]

def conflict(a, b):
    if (b[0] == a[0]) or (b[0] < a[1] and b[1] > a[0]) or (b[0] > a[0] and b[1] < a[1]):
        return True
    
    else:
        return False
    

#this function makes a dictionary of all the substrings in the target
#with each substring as a key and the indices of its string slice 
#as values in the format [x, y]

def makedicts(source, target):
    td = {}
    x = 0
    #go through each element in the target
    while x < len(target):
        y = x + 1
        #get every possible substring starting with the element
        while y <= len(target):
            td[target[x:y]] = [x,y]
            y = y + 1
        x = x + 1
    
    return td


#this function returns a list of tuples with each tuple containing a substring
#and the number of letters it would put into the right place if flipped
#the list of tuples is sorted in descending order of calculated weights of each substring

def getWeights(source, target):
    weights = []
    substrings = makedicts(source, target)
    for element in substrings.keys():
        #go through each substring of the target and get the string slice
        indices = substrings[element]
        #get the corresponding slice from the source string
        a = source[indices[0]:indices[1]]
        #reverse the target substring
        temp = element[::-1]
        counter = 0
        x = 0
        #check how many characters the target slice would put in the right
        #place by comparing each character in the source slice to the
        #character in the corresponding position in the target slice
        while x < len(temp):
            if temp[x] == a[x]:
                counter = counter + 1
                x = x + 1
            else:
                x = x + 1
        #add the target substring and the number of letters put in the right place
        #to a list
        weights.append((element, counter))
        
    old = sorted(weights, key= itemgetter(1), reverse = True)
    
    
    #go through list of weights and remove substrings that only put one character
    #in place or zero characters in place
    #also remove palindromes
    new = []
    i = 0
    while i < len(old):
        if old[i][1] == 0 or old[i][1] == 1:
            i = i + 1
            
        elif old[i][0] == old[i][0][::-1]:
            i = i + 1
        else:
            new.append(old[i])
            i = i + 1
            
    
    #go through each element in the new list of weights and calculate the "real weight"
    #which is the length of the element minus the number of characters put in the right place
    #divided by the number of characters put in the right place
    wd = []
    for element in new:
        realweight = (len(element[0]) - element[1])/float(element[1])
        #add the element and its real weight to the list
        wd.append((element, realweight))
    
    #sort this list in ascending order (based on the weights) to have the elements 
    #with the most desirable weights first in the list
    wd = sorted(wd, key = itemgetter(1))
    #print wd
    toreturn = []
    
    #add only the substring and # of characters in right position tuples to the
    #list to be returned
    for element in wd:
        toreturn.append(element[0])
        
    return toreturn
            
            

#this function returns a list of intervals that minimize the number of flips

def checker(source, target):
    #get the dictionary of substrings
    substrings = makedicts(source, target)
    #get the list of substrings ordered based on real weight
    toflip = getWeights(source, target)
    
    #create a list of the slice values for each substring in the list of
    #substrings ordered based on real weight
    data = []
    i = 0
    while i < len(toflip):
        inds = substrings[toflip[i][0]]
        data.append(inds)
        i = i + 1
        
    
    #this is the list of intervals to be flipped
    theflip = []
    x = 0
    while x < len(data):
        if x == 0:
            #always add the first element of data since that has the most weight
            theflip.append(data[x])
            x = x + 1
            
        else:
            boolean = True
            #check every other interval with all the elements that are in the
            #list of intervals to be flipped for conflicts
            for element in theflip:
                con = conflict(data[x], element)
                if con == True:
                    #print "didn't pass", data[x], element
                    boolean = False
            
            #if there is a conflict, move to next interval        
            if boolean == False:
                x = x + 1
                
            #if there is no conflict, add the interval to list of intervals
            #to be flipped
            else:
                theflip.append(data[x])
                x = x + 1
            
    
    return theflip



#this function performs the flips and substitutions necessary to transform
#the target string to the source string
def changes(source, target):
    substrings = makedicts(source, target)
    #get the list of intervals to flip
    toflip = checker(source, target)
    
    print "STARTING TRANSFORMATION"
    print "***********************"
    print "THIS IS THE TARGET: ", target
    
    #flip each interval in the list of intervals to be flipped
    for element in toflip:
        sub = target[element[0]:element[1]]
        new = sub[::-1] #simply reverse the substring
        target = target.replace(sub, new) #replace the substring in the target with the flipped version
        print target, "(a flip)"
        
    
    #make a list of the characters in the target and source to allow manipulation
    #at this point, all the possible flips have been done
    t = list(target)
    s = list(source)
    x = 0
    #go through each element of the source list
    while x < len(s):
        #if the element at index x in source doesn't match the element at index x in
        #the target string, then substitute
        if s[x] != t[x]:
            t[x] = s[x]
            print "".join(t), "(a substitution)"
            x = x + 1
            
        else:
            x = x + 1
    
    #Join the target list together to be a string        
    target = "".join(t)
    
    print "***********************"
    print "TRANSFORMATION FINISHED"
                  
    return target


#this function takes as input a file containing two input strings and
#prints out a minimum length sequence of transformations from the
#target to the source

def minChanges(filename):
    #open file
    f = open(filename, "r")
    #make a list to contain the source and target strings
    words = []
    for line in f:
        a = line.strip("\n")
        strings = a.split()
        #check to see if it is a line containing a string
        if len(strings) == 2:
            words.append(strings[1])
    
    return changes(words[0], words[1])


