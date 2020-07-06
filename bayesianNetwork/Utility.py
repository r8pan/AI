import itertools, numpy, copy

class Variable:
    "name is a String, and values is a String list, with prob be the probability of each value"

    def __init__(self, name, values, prob=[]):
        self.name = name
        self.values = values
        self.probabilities = prob

    
class Factor:
    "variableList as defined above, and probability a float list is as it sounds"

    def __init__(self, variableList, probabilities=[]):
        self.variableList = variableList
        # print (probabilities)
        if probabilities:
            self.probabilities = probabilities
        else:			
            self.probabilities = variableList[0].probabilities
            for i in range(len(variableList)-1):
                self.probabilities = list(itertools.product(self.probabilities, variableList[i+1].probabilities))
            # print(self.probabilities)
            for i in range(len(self.probabilities)):
                x = 1
                fct = self.probabilities[i]
                for j in fct:
                    x *= j
                self.probabilities[i] = x

def restrict(factor, variable, value):
    "restrict the factor with certain variables given values"

    varInd = 0
    valInd = 0
	
    for ind, val in enumerate(factor.variableList):
        #print("val.name = " + val.name)
        if val.name == variable.name:
            varInd = ind
            for inds, vals in enumerate(val.values):
                #print(vals)
                if vals == value:
                    valInd = inds
                    break					
            break
    #print(varInd, valInd)
    varLen = len(factor.variableList[varInd].values)
    probabilities = factor.probabilities
    returnProbabilities = []
    numSection = 1
    i = 0
    while i < varInd:
        numSection *= len(factor.variableList[i].values)
        i += 1
    # print(numSection)
    sectionLen = len(probabilities)/numSection
    i = 0
    # print (probabilities)
    # print (type(probabilities))
    while i < len(probabilities):
        # print(int(i+sectionLen/varLen*valInd), int(i+sectionLen/varLen*(valInd+1)-1))
        # print (probabilities[int(i+sectionLen/varLen*valInd)])
        for j in range(int(i+sectionLen/varLen*valInd), int(i+sectionLen/varLen*(valInd+1))):
            returnProbabilities.append(probabilities[j])
        i += sectionLen
    #print (returnProbabilities)
    del factor.variableList[varInd]
    returnVariableList = factor.variableList
    # print (returnVariableList)
    return Factor(returnVariableList, returnProbabilities)
    
def multiply(factor1, factor2):
    returnVariableList = []
    returnProbabilities = []
    
    returnVariableList = list(factor1.variableList)
    diffElem = list(x for x in factor2.variableList if x.name not in (f.name for f in factor1.variableList))
    returnVariableList.extend(diffElem)
    
    # get multiplier list for new list
    multiplier = []
    varNames = []
    for i in returnVariableList:
        varNames.append(i.name)
        multiplier.append(len(i.values))
    prod = numpy.product(multiplier)
    multiplier[0] = int(prod/multiplier[0])
    for i, j in enumerate(multiplier):
        if i == 0:
            continue
        multiplier[i] = int(multiplier[i-1]/multiplier[i])

    # get multiplier list for f1
    multiplierf1 = []
    for i in factor1.variableList:
        multiplierf1.append(len(i.values))
    prodf1 = numpy.product(multiplierf1)
    multiplierf1[0] = int(prodf1/multiplierf1[0])
    for i, j in enumerate(multiplierf1):
        if i == 0:
            continue
        multiplierf1[i] = int(multiplierf1[i-1]/multiplierf1[i])
    #print(multiplierf1)
    
    # get multiplier list for f2
    multiplierf2 = []
    for i in factor2.variableList:
        multiplierf2.append(len(i.values))
    prodf2 = numpy.product(multiplierf2)
    multiplierf2[0] = int(prodf2/multiplierf2[0])
    for i, j in enumerate(multiplierf2):
        if i == 0:
            continue
        multiplierf2[i] = int(multiplierf2[i-1]/multiplierf2[i])
    #print(multiplierf2)
         
    print("prod: ", prod)
    for i in range(prod):
        row = i
        varVals = []
        for j, k in enumerate(multiplier):
            varVals.append(int(row/k))
            row = row%k
        dictionary = dict(zip(varNames, varVals))
        print(dictionary)
        indf1 = 0
        indf2 = 0
        for j in dictionary:
            for k in range(len(factor1.variableList)):
                if factor1.variableList[k].name == j:
                    indf1 += dictionary[j]*multiplierf1[k]
        for j in dictionary:
            for k in range(len(factor2.variableList)):
                if factor2.variableList[k].name == j:
                    indf2 += dictionary[j]*multiplierf2[k]
        # print(indf1, indf2)
        returnProbabilities.append(factor1.probabilities[indf1]*factor2.probabilities[indf2])
    #print(returnProbabilities)
    return Factor(returnVariableList, returnProbabilities)
    
def sumout(factor, variable):
    returnVariableList = []
    returnProbabilities = []
    for i in variable.values:
        fctr = copy.deepcopy(factor)
        #print(i)
        #print(list(x.name for x in fctr.variableList))
        tempFactor = restrict(fctr, variable, i)
        #print(returnProbabilities)
        #print(tempFactor.probabilities)
        if not returnProbabilities:
            returnProbabilities = tempFactor.probabilities
        else:
            returnProbabilities = list(sum(x) for x in zip(returnProbabilities, tempFactor.probabilities))
    print("after sumout:", returnProbabilities)    
    return Factor(returnVariableList, returnProbabilities)
    
def normalize(factor):
    returnVariableList = factor.variableList
    returnProbabilities = []
    sumProb = sum(factor.probabilities)
    for i in factor.probabilities:
        returnProbabilities.append(i/sumProb)
    return Factor(returnVariableList, returnProbabilities)

def inference(factorList, queryVariables, orderedListOfHiddenVariables, evidenceList): # Factor list, String, Variable list, dictionary of evidences
    print("restrict phase")

    if evidenceList:
        print("evidenceList is not empty")
        for i in factorList:
            for j in i.variableList:
                if evidenceList[j.name]:
                    i = restrict(i, j, evidenceList[i.name])
    
    for i in orderedListOfHiddenVariables:
        relatedFactors = []
        for j in factorList:
            for k in j.variableList:
                if k.name == i.name or k.name == x.name for x in queryVariables:
                    print(k.name)
                    relatedFactors.append(j)
                    factorList.remove(j)
        # print(related)
        # print("relatedFactors: ", list(y.name for y in x.variableList for x in relatedFactors))
        tempFactor = relatedFactors[0]
        # print("relatedFactors:", list(x.name for x in y.))
        print("multiplying...")
        for j in range(len(relatedFactors)-1):
            tempFactor = multiply(tempFactor, relatedFactors[j+1])
        print("after multiplying: ", tempFactor.probabilities)
        print("summing out")
        tempFactor = sumout(tempFactor, i)
        factorList.append(tempFactor)
    print(factorList)
    #return normalize(factorList)
    

# test 1
coin = Variable("coin", ["head", "tail"], [0.1, 0.9])
direction = Variable("direction", ["left", "right"], [0.6, 0.4])
testFactor = Factor([coin, direction])

# test 2
x = Variable("X", [True, False])
y = Variable("Y", [True, False])
z = Variable("Z", [True, False])
tf = Factor([x, y, z], [0.1, 0.9, 0.2, 0.8, 0.4, 0.6, 0.3, 0.7])
#tf1 = restrict(tf, x, True)
#tf2 = restrict(tf1, z, False)
#tf3 = restrict(tf2, y, False)

# test for multiply
testFactor1 = Factor([Variable("A", [True, False]), Variable("B", [True, False])], [0.1, 0.9, 0.2, 0.8])
testFactor2 = Factor([Variable("B", [True, False]), Variable("C", [True, False])], [0.3, 0.7, 0.6, 0.4])
#resultFactor = multiply(testFactor1, testFactor2)

# test for sumout
testFactor = Factor([Variable("A", [True, False]), Variable("B", [True, False]), Variable("C", [True, False])], [0.03, 0.07, 0.54, 0.36, 0.06, 0.14, 0.48, 0.32])
#resultFactot = sumout(testFactor, Variable("B", [True, False]))

#test for normalize
testFactor = Factor([Variable("A", [True, False])], [0.24, 0.32])
#resultFactor = normalize(testFactor)
#print(resultFactor.probabilities)