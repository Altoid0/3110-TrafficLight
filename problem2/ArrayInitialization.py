# Alphabets = v, [, n, ], ;, =, {, }, i, f, s, ,
# Variables = P (Program), D (Declare), S (Assign), C (Access), T (Type), N (NumList)


# Split into Decl, Assign, Access

import sys

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
            print("Error: Program must have exactly three parts separated by ';'.")
            return False
        else:
            D = instructions[0] + ';'
            S = instructions[1] + ';'
            C = instructions[2]

            if self.checkD(D) and self.checkS(S) and self.checkC(C):
                return True
            else:
                return False

    def checkD(self, D):
        currInd = -1
        tempS = D

        if "[" not in tempS or "]" not in tempS or ";" not in tempS:
            print("Error: Declaration must include '[', ']', and ';'.")
            return False

        arrInd = tempS[tempS.index("[") + 1:tempS.index("]")]
        if arrInd.isnumeric():
            tempS = tempS.replace(arrInd, "")
        else:
            print("Error: Array index must be a numeric value.")
            return False

        for x in self.productions['D']:
            if x in self.productions:
                if not self.checkT(tempS[0:tempS.index(" ")]):
                    print("Error: Invalid type in declaration.")
                    return False
                tempS = tempS[tempS.index(" ") + 1:]
            if x == 'num':
                continue
            if tempS.find(x) < currInd:
                print("Error: Incorrect order in declaration.")
                return False
            else:
                currInd = tempS.find(x)
                if x == 'var':
                    varName = tempS[0: tempS.index("[")]
                    if varName.isalnum():
                        tempS = tempS[tempS.index("["):]
                    else:
                        print("Error: Invalid variable name.")
                        return False
                else:
                    tempS = tempS.replace(x, "", 1)

        tempS = tempS.replace(" ", "")
        return tempS == ""

    def checkS(self, S):
        currInd = -1
        tempS = S.replace(" ", "")

        if "{" not in tempS or "}" not in tempS or "=" not in tempS or ";" not in tempS:
            print("Error: Assignment must include '{', '}', '=', and ';'.")
            return False

        for x in self.productions['S']:
            if x in self.productions:
                if self.checkN(tempS):
                    tempS = tempS[tempS.index("}"):]
                    continue
            if tempS.find(x) < currInd:
                print("Error: Incorrect order in assignment.")
                return False
            else:
                currInd = tempS.find(x)
                if x == 'var':
                    varName = tempS[0:tempS.index("=")]
                    if varName.isalnum():
                        tempS = tempS[tempS.index("="):]
                    else:
                        print("Error: Invalid variable name in assignment.")
                        return False
                else:
                    tempS = tempS.replace(x, "", 1)
        return tempS == ""

    def checkT(self, T):
        return T in {"int", "float", "string"}

    def checkN(self, tempS):
        if (",," in tempS) or (",}" in tempS) or not tempS[0].isnumeric():
            print("Error: Invalid number list.")
            return False
        tempS = tempS.replace(",", "")
        numbers = tempS[0:tempS.index("}")]
        if not numbers.isnumeric():
            print("Error: Number list contains non-numeric characters.")
            return False
        return True

    def checkC(self, C):
        currInd = -1
        tempS = C.replace(" ", "")

        if "[" not in tempS or "]" not in tempS or "=" not in tempS or ";" not in tempS:
            print("Error: Access must include '[', ']', '=', and ';'.")
            return False

        arrInd = tempS[tempS.index("[") + 1:tempS.index("]")]
        indAssign = tempS[tempS.index("=") + 1:tempS.index(";")]

        if arrInd.isnumeric():
            tempS = tempS.replace(arrInd, "")
        else:
            print("Error: Array index must be numeric.")
            return False
        if indAssign.isnumeric():
            tempS = tempS.replace(indAssign, "")
        else:
            print("Error: Assigned value must be numeric.")
            return False

        for x in self.productions['C']:
            if x == 'num':
                continue
            if tempS.find(x) < currInd:
                print("Error: Incorrect order in access.")
                return False
            else:
                currInd = tempS.find(x)
                if x == 'var':
                    varName = tempS[0: tempS.index("[")]
                    if varName.isalnum():
                        tempS = tempS[tempS.index("["):]
                    else:
                        print("Error: Invalid variable name in access.")
                        return False
                else:
                    tempS = tempS.replace(x, "", 1)
        return tempS == ""

if __name__ == "__main__":
    # Initialize Grammar
    variables = {'P', 'D', 'S', 'C', 'T', 'N'}
    terminals = {'[', ']', ';', '=', '{', '}', 'int', 'float', 'string', ',', 'num', 'var'}
    start = 'P'
    productions = {'P': ['D', 'S', 'C'],
                   'D': ['T', 'var', '[', 'num', ']', ';'],
                   'S': ['var', '=', '{', 'N', '}', ';'],
                   'C': ['var', '[', 'num', ']', '=', 'num', ';'],
                   'T': ['int', 'float', 'string'],
                   'N': ['num', 'N, num']}

    g = Grammar(variables, terminals, start, productions)
    while True:
        print("*NOTE* Please separate instructions by a semi-colon and a space (e.g., int arr[2]; arr = {1, 2}; arr[0] = 0).")
        string = input("Please declare an array, populate the array, then change the value of a random index (or type 'exit' to quit): ")

        if string.lower() == "exit":
            print("Exiting the program.")
            break

        if g.checkProgram(string):
            print("\nGenerated by Grammar: " + str(g.checkProgram(string)) + "\n")
        else:
            print("The input program is invalid.")

    # TESTCASES:
    # int arr[5]; arr = {1, 2, 3, 4, 5}; arr[2] = 10;                           # TRUE
    # float fArray[9]; iArray = {11231234,2,3}; randomArray[2] = 9;             # TRUE
    # string sArray[1231432]; iArray = {231, 4332, 534}; randomArr[3123] = 2;   # TRUE
    # int array[2]; brokenArray = {3,5,,}; array[1] = 4;                        # FALSE
    # string brokenArray[]; array = {1, 3, 4}; array[1] = 2;                    # FALSE
    # int array[9]; array = {3, 4, 6, 2, 3}; brokenArray][ 2;                   # FALSE