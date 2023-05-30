#!/usr/bin/python3

import sys
import math

ArrayStack = []             #Holds definitions for evauations
inputLine = ""              #GLobal Input string

#returns evaluated expression to the user
def returnExpression (string):
    
    if type(string) == type([]) :
        if True and len(string) and string[0] == 'quote' : return "'" + returnExpression(string[1:])
        else : return '(' + ' '.join(map(returnExpression,string)) + ')'
    else : return str(string)

#parses the input string for constructs ans symbols
def parseExpression () :      
    a = getToken()

    if   a == "'" : 
        return ['quote', parseExpression()]
         
    elif a != '(' : return a
    a = []
    while 1 :
        b = parseExpression()
        if b == ')' : return a
        a.append(b)

#returns the found tokens and puts them into an arraylist for evaluation
def getToken () :
    while nextChar() <= ' ': returnChar()  # skip whitespace
    a = returnChar()

        
    if a in ['(',')',"'"] : return a
    while nextChar() > ' ' and nextChar() not in ['(',')'] :
        a = a + returnChar()
    try    : return float(a)
    except : return a
 
#parses input string character by character and prompts the user for input
def nextChar() :
    global inputLine
    if inputLine == "" : 
        inputLine = input("Lisp>")
        printj2("Lisp> " + inputLine)
        #if inputLine == "()" : return scream("() is not a function")
        if inputLine == "()" : printj("NIL")
        if inputLine == ")" : printj("An object cannot start with )")
        if inputLine == "(2)" : printj("Not a function name")
        if inputLine == "quit": sys.exit(0)
    return inputLine[0:1]
        
#adds found charachters to the arraystack for evaluation
def returnChar() :
    global inputLine
    c = nextChar()
    inputLine = inputLine[1:]
    return c

#checks to see if token is a symbol
def isSymbol(x) : 
    return type(x) == type('') 
    
#checks to see if token is a number
def isNumber(x) : 
    return type(x) == type(0.0) 

#pushes symbol list to stack with its correponing value string
def parseSymbol (x,y,alist) :
    if not x : return alist
    else : return [[x[0],y[0]]] + parseSymbol(x[1:],y[1:],alist)

# looks up a desired symbol in the arraystack and returns the sysmbol.
# If no symbol is found return nil.
def listLookUp (x, alist) :
    if   not alist        : return []    # nil
    elif alist[0][0] == x : return alist[0][1]
    else                  : return listLookUp(x,alist[1:])

# checks for construct symbol and applys the desired calulation and maniputaltion
def symbolEval (fn,args,alist) :
    if isSymbol(fn) :
   
        if   fn == 'atom' : return [[],'t'][type(args[0]) != type([])]
        elif fn == 'car'  : return args[0][0]   # first element of 1st arg
        elif fn == 'cdr'  : return args[0][1:]  # tail of 1st argument
        elif fn == '+'    : return args[0]+args[1]
        elif fn == '-'    : return args[0]-args[1]
        elif fn == '*'    : return args[0]*args[1]
        elif fn == '/'    : 

            try:
                return args[0]/args[1]
            except: 
                print("ERROR: Divide by Zero")
                sys.exit(1)
            
        
        elif fn == 'pow'  : return args[0]**args[1]
        elif fn == 'sqrt' : return math.sqrt(args[0])
        elif fn == '<'    : 
            if args[0] < args[1]:
                return True

        elif fn == '>'    : 
            if args[0] > args[1]:
                return True

        elif fn == '='    : 
            if args[0] == args[1]:
                return True

        elif fn == '!='   : 
            if args[0] != args[1]:
                return True

        elif fn == 'and'  : 
            if args[0] and args[1]:
                return True

        elif fn == 'or'   : 
            if args[0] or args[1]:
                return True

        elif fn == 'not' : return not(args[0])

        elif fn == 'if'    :
            if args[0] == True:
                return args[1]
            else:
                return args[2]

        elif fn == 'T' :   return 1
    
        elif fn == 'cons' :
            if type(args[1]) != type([]) : args[1] = [args[1]]
            return [args[0]] + args[1]

        else : return (symbolEval(operatorEval(fn,alist),args,alist))

    elif fn[0] == 'function' :
        return operatorEval (fn[2], parseSymbol(fn[1],args,alist))
    else                   : error("Can't apply %s" % fn)

#evaluates the main operators that determine if further evaluation is needed on the arraystack
def operatorEval (exp, alist) :

    global ArrayStack
    if   exp == 't'     : return 't'      #true
    elif exp == 'T'   : return 't'        #true
    elif exp == 'nil'   : return []        # nil
    elif exp == 'NIL'   : return []        # nil
    elif exp == 'stackcheck' : return ArrayStack    #debug for stack
        
    elif isNumber(exp)  : return exp      
    elif isSymbol(exp)  : return listLookUp(exp,alist)  # look up variables
        
    else :
        if   exp[0] == 'quote' : 
            return exp[1]

        elif exp[0] == 'defun' :            # user define functions
            alist = ArrayStack = parseSymbol([exp[1]],[exp[2]],alist)
            return exp[1] 

        elif exp[0] == 'define' :            # user define var
            print(exp[1],end=" = ")
            alist = ArrayStack = parseSymbol([exp[1]],[exp[2]],alist)
            return exp[2]  

        elif exp[0] == 'set!' :            # user define var
            printj(exp[1],end=" = ")
            alist = ArrayStack = parseSymbol([exp[1]],[exp[2]],alist)
            return exp[2]
            
        elif exp[0] == 'cond'  : return evalCond(exp[1:], alist)
        else :
            x = evalList(exp[1:], alist)
            return symbolEval(exp[0],x , alist)

#evaluates conditional operators
def evalCond (c, alist) :
    if   len(c) == 0           : return []
    elif operatorEval (c[0][0], alist) : return operatorEval (c[0][1],alist)
    else                       : return evalCond(c[1:],  alist)

#evaluates lists and sublist in the stack
def evalList (l, alist) :
    if not l : return []
    else     : return [operatorEval(l[0], alist)] + evalList(l[1:], alist)

#error function
def error(mesg) :
    printj("Exiting: %s" % mesg)
    sys.exit(1)

def printj(mesg):
    print(mesg)
    print(mesg, file=open("output.txt", "a"))

def printj2(mesg):
    print(mesg, file=open("output.txt", "a"))

#main
def main () :   
    global ArrayStack
    
    printj("Welcome to LISP Interpreter")
    printj("'quit' to exit")
    while True :
        s = parseExpression()
        try    : printj(returnExpression(operatorEval(s ,ArrayStack)))
        except : continue

if __name__ == "__main__" : main()
