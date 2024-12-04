# Alphabets = v, [, n, ], ;, =, {, }, i, f, s, ,
# Variables = P (Program), D (Declare), S (Assign), C (Access), T (Type), N (NumList)


# Split into Decl, Assign, Access

class Grammar:
    def __init__(self, variables, terminals, start, productions):
        self.variables = variables
        self.terminals = terminals
        self.currentProduction = start
        self.productions = productions

#        for variable in productions[start]: # Checking D S C
#            if production in productions[variable]:

    def checkProgram(self, P):
        instructions = P.split('; ', 2)

        if len(instructions) != 3:
            return False
        else:
            D = instructions[0] + ';'
            S = instructions[1] + ';'
            C = instructions[2]

            if g.checkD(D) and g.checkS(S) and g.checkC(C):
                return True
            else:
                return False

    # Check for Declaration
    def checkD(self, D):
        currInd = -1
        tempS = D

        if "[" not in tempS or "]" not in tempS or ";" not in tempS:
            return False

        arrInd = tempS[tempS.index("[") + 1:tempS.index("]")]
        if arrInd.isnumeric():
            tempS = tempS.replace(arrInd, "")
        else:
            return False

        for x in productions['D']:
            if x in productions:
                if not self.checkT(tempS[0:tempS.index(" ")]):
                    return False
                tempS = tempS[tempS.index(" ") + 1:]
            if x == 'num':
                continue
            if tempS.find(x) < currInd:
                return False
            else:
                currInd = tempS.find(x)
                if x == 'var':
                    varName = tempS[0: tempS.index("[")]
                    if varName.isalnum():
                        tempS = tempS[tempS.index("["):]
                    else:
                        return False
                else:
                    tempS = tempS.replace(x, "", 1)

        tempS.replace(" ", "")
        return tempS == ""

    # Check for Assign
    def checkS(self, S):
        currInd = -1
        tempS = S.replace(" ", "")

        if "{" not in tempS or "}" not in tempS or "=" not in tempS or ";" not in tempS:
            return False

        for x in productions['S']:
            if x in productions:
                if self.checkN(tempS):
                    tempS = tempS[tempS.index("}"):]
                    continue
            if tempS.find(x) < currInd:
                return False
            else:
                currInd = tempS.find(x)
                if x == 'var':
                     varName = tempS[0:tempS.index("=")]
                     if varName.isalnum():
                        tempS = tempS[tempS.index("="):]
                     else:
                        return False
                else:
                     tempS = tempS.replace(x, "", 1)
        return tempS == ""

    # Check for Type
    def checkT(self, T):
        if "int" == T or "float" == T or "string" == T:
            return True
        else:
            return False

    # Check for NumList
    def checkN(self, tempS):
        if(tempS.find(",,") > -1) or (tempS.find(",}") > -1) or not (tempS[0].isnumeric()):
            return False
        tempS = tempS.replace(",", "")
        numbers = tempS[0:tempS.index("}")]
        if not numbers.isnumeric():
            return False
        return True

    # Check for Access
    def checkC(self, C): # SO SCUFFED
        currInd = -1
        tempS = C.replace(" ", "") # Removing White Space

        if "[" not in tempS or "]" not in tempS or "=" not in tempS or ";" not in tempS:
            return False

        arrInd = tempS[tempS.index("[")+1:tempS.index("]")]
        indAssign = tempS[tempS.index("=")+1:tempS.index(";")]

        if arrInd.isnumeric():
            tempS = tempS.replace(arrInd, "")
        else:
            return False
        if indAssign.isnumeric():
            tempS = tempS.replace(indAssign, "")
        else:
            return False

        for x in productions['C']:
            if x == 'num':
                continue
            if tempS.find(x) < currInd:
                return False
            else:
                currInd = tempS.find(x)
                if x == 'var':
                    varName = tempS[0: tempS.index("[")]
                    if varName.isalnum():
                        tempS = tempS[tempS.index("["):]
                    else:
                        return False
                else:
                    tempS = tempS.replace(x, "", 1)
        return tempS == ""


if __name__ == "__main__":

    # Initialize Grammar
    variables = {'P', 'D', 'S', 'C', 'T', 'N'} # (P = Program, D = ArrayDecl, S = ArrayAssign, C = ArrayAccess, T = Type, N = NumList)
    terminals = {'[', ']', ';', '=', '{', '}', 'int', 'float', 'string', ',', 'num', 'var'}
    start = 'P'
    productions = {'P': ['D', 'S', 'C'],
                   'D': ['T', 'var', '[', 'num', ']', ';'],
                   'S': ['var', '=', '{', 'N', '}', ';'],
                   'C': ['var', '[', 'num', ']', '=', 'num', ';'],
                   'T': ['int', 'float', 'string'],
                   'N': ['num', 'N, num']}

    g = Grammar(variables, terminals, start, productions)

    print("Please declare an array, populate the array, then change the value of a random index")
    string = input("NOTE: Please separate instructions by a semi-colon and a space, (ex. int arr[2]; arr[0] = 0): ")

    print("Generated by Grammar: " + str(g.checkProgram(string)))


    # TESTCASES:
    # int arr[5]; arr = {1, 2, 3, 4, 5}; arr[2] = 10;                           # TRUE
    # float fArray[9]; iArray = {11231234,2,3}; randomArray[2] = 9;             # TRUE
    # string sArray[1231432]; iArray = {231, 4332, 534}; randomArr[3123] = 2;   # TRUE
    # int array[2]; brokenArray = {3,5,,}; array[1] = 4;                        # FALSE
    # string brokenArray[]; array = {1, 3, 4}; array[1] = 2;                    # FALSE
    # int array[9]; array = {3, 4, 6, 2, 3}; brokenArray][ 2;                   # FALSE