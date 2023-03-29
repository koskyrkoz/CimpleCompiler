import sys
import os
from os import path

class lexToken:
        def __init__(self,token,word,line):
                self.token=token
                self.word=word
                self.line=line


reservedWords={'program':101 ,'declare':102,
                'if':201,'else':202,'while':203,
                'switchcase':301,'incase':302,'forcase':303,'case':304,'default':305,
                'not':401,'and':402,'or':403,
                'procedure':501,'function':502,'call':503,'return':504,'in':505,'inout':506,
                'input':601,'print':602}

def charTokenize(char):
        charTokens={'\t':0,' ':0,'letters':1,'digits':2,'+':3,'-':4,'*':5,'/':6,
        '=':7,'<':8,'>':9,'':10,'invalidSymbol':11,',':12,';':13,
        '(':14,')':15,'[':16,']':17,'{':18,
        '}':19,'\n':20,':':21,'.':22,'#':23}

        if (char in alphabet):
                    return charTokens['letters']
        elif (char in digits):
                    return charTokens['digits']
        elif (char in charTokens):
                    return charTokens[char]
        else:
                    return charTokens['invalidSymbol']

ERROR_NUM_OVERFLOW=-99
ERROR_STRING_OVERFLOW=-98
ERROR_NUM_AFTER_LETTER=-97
ERROR_INVALID_COLON=-96
ERROR_INVALID_SYMBOL=-95
ERROR_INVALID_COMMENT=-94

def lexPrintError(currentState,line):
        global file
        global cFile
        global intFile
        global symbolFile

        if(currentState==ERROR_NUM_OVERFLOW):
                print(">>LEX ERROR_NUM_OVERFLOW near line ("+str(line)+"): Number exceeds given range of [-"+str(pow(2,32))+","+str(pow(2,32))+"]")
        elif(currentState==ERROR_STRING_OVERFLOW):
                print(">>LEX ERROR_STRING_OVERFLOW near line ("+str(line)+"): A word cannot be more than 30 characters long")
        elif(currentState==ERROR_NUM_AFTER_LETTER):
                print(">>LEX ERROR_NUM_AFTER_LETTER near line ("+str(line)+"): Letters cannot come after digits")
        elif(currentState==ERROR_INVALID_COLON):
                print(">>LEX ERROR_INVALID_COLON near line: ("+str(line)+"): A colon (:) must be followed by an equals (=) character")
        elif(currentState==ERROR_INVALID_SYMBOL):
                print(">>LEX ERROR_INVALID_SYMBOL near line: ("+str(line)+"): Invalid symbol used")
        elif(currentState==ERROR_INVALID_COMMENT):
                print(">>LEX ERROR_INVALID_COMMENT near line: ("+str(line)+"): Never ending comment")

        file.close()
        cFile.close()
        intFile.close()
        symbolFile.close()

        os.remove(filename[:-3]+'.int')
        os.remove(filename[:-3]+'.c')
        os.remove(filename[:-3]+'_symbol_table.txt')


token={'digits':30,'idk':31,
            '+':40,'-':41,'*':42,'/':43,
            '=':50,'<>':51,'<=':52,'>=':53,'<':54,'>':55,
            '(':60,')':61,'[':62,']':63,'{':64,'}':65,
            ',':70,';':71,':':72,
            ':=':80,
            '.':90,'EOF':91}


digits=['0','1','2','3','4','5','6','7','8','9']
alphabet =['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z',
                        'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']


state={'start':0,'dig':1,'idk':2,'asgn':3,'smaller':4,'larger':5,'rem':6}

transitionTable=[
        #start:0
        [state['start'],state['idk'],state['dig'],token['+'],token['-'],token['*'], token['/'],
     token['='],state['smaller'],state['larger'],token['EOF'],ERROR_INVALID_SYMBOL,
         token[','],token[';'],token['('],token[')'],token['['],token[']'],token['{'],token['}'],
         state['start'],state['asgn'],token['.'],state['rem']],

        #dig:1
        [token['digits'],ERROR_NUM_AFTER_LETTER, state['dig'],token['digits'],token['digits'],token['digits'],
         token['digits'],token['digits'],token['digits'],token['digits'],token['digits'],ERROR_INVALID_SYMBOL,
         token['digits'],token['digits'],token['digits'],token['digits'],token['digits'],token['digits'],token['digits'],token['digits'],
         token['digits'],token['digits'],token['digits'],token['digits']],

        #idk:2
        [token['idk'],state['idk'],state['idk'],token['idk'],token['idk'],token['idk'],token['idk'],token['idk'],token['idk'],token['idk'],token['idk'],ERROR_INVALID_SYMBOL,
         token['idk'],token['idk'],token['idk'],token['idk'],token['idk'],token['idk'],token['idk'],token['idk'],token['idk'],token['idk'],token['idk'],token['idk']],

        #asgn:3
        [ERROR_INVALID_COLON,ERROR_INVALID_COLON,ERROR_INVALID_COLON,ERROR_INVALID_COLON,ERROR_INVALID_COLON,ERROR_INVALID_COLON,
         ERROR_INVALID_COLON,token[':='],ERROR_INVALID_COLON,ERROR_INVALID_COLON,ERROR_INVALID_COLON,ERROR_INVALID_SYMBOL,
         ERROR_INVALID_COLON,ERROR_INVALID_COLON,ERROR_INVALID_COLON,ERROR_INVALID_COLON,ERROR_INVALID_COLON,ERROR_INVALID_COLON,ERROR_INVALID_COLON,ERROR_INVALID_COLON,
         ERROR_INVALID_COLON,ERROR_INVALID_COLON,ERROR_INVALID_COLON,ERROR_INVALID_COLON],

        #smaller:4
        [token['<'],token['<'],token['<'],token['<'],token['<'],token['<'],
         token['<'],token['<='],token['<'],token['<>'],token['<'],ERROR_INVALID_SYMBOL,
         token['<'],token['<'],token['<'],token['<'],token['<'],token['<'],token['<'],token['<'],
         token['<'],token['<'],token['<'],token['<']],

        #larger:5
        [token['>'],token['>'],token['>'],token['>'],token['>'],token['>'],
         token['>'],token['>='],token['>'],token['>'],token['>'],ERROR_INVALID_SYMBOL,
         token['>'],token['>'],token['>'],token['>'],token['>'],token['>'],token['>'],token['>'],
         token['>'],token['>'],token['>'],token['>']],

        #rem:6
        [state['rem'],state['rem'],state['rem'],state['rem'],state['rem'],state['rem'],
         state['rem'],state['rem'],state['rem'],state['rem'],ERROR_INVALID_COMMENT,state['rem'],
         state['rem'],state['rem'],state['rem'],state['rem'],state['rem'],state['rem'],state['rem'],state['rem'],
         state['rem'],state['rem'],state['rem'],state['start']]]


# Lexical Analysis
global tokenCounter
tokenCounter=0
line=1
def lex():
        global tokenCounter
        global line
        word=''
        lineCounter=line
        currentState=state['start']
        while(0<=currentState<=6):
                char=file.read(1)

                if(char=='\n'):
                        lineCounter+=1
                currentState=transitionTable[currentState][charTokenize(char)]

                if(len(word)<30):
                        if(currentState!=state['start'] and currentState!=state['rem']):
                                word+=char
                else:
                    currentState=ERROR_STRING_OVERFLOW
        if(currentState==token['idk'] or currentState==token['digits'] or currentState==token['<'] or currentState==token['>'] ):
                if(char=='\n'):
                        lineCounter-=1
                char=file.seek(file.tell()-1,0)
                word=word[:-1]
        if (currentState==token['idk']):
                if(word in reservedWords):
                        currentState=reservedWords[word]
        if (currentState==token['digits']):
                if(int(word)>=pow(2,32)):
                        currentState=ERROR_NUM_OVERFLOW
        if (currentState<0):
                lexPrintError(currentState,lineCounter)
                print('\n')
                print('Exiting...')
                print('---------')
                print('**********')
                print('\n')
                exit()
        result=lexToken(currentState,word,lineCounter)
        tokenCounter+=1
        line=lineCounter
        return result

# Int code functions
global cFile
global listOfAllQuads
listOfAllQuads = []
countQuad = 1

def nextQuad():
        global countQuad
        return countQuad

def genQuad(first, second, third, fourth):
        global countQuad
        global listOfAllQuads
        list = []
        list = [nextQuad()]
        list += [first] + [second] + [third] + [fourth]
        countQuad +=1
        listOfAllQuads += [list]
        return list

T_i = 1
listOfTempVariables = []
def newTemp():
        global T_i
        global listOfTempVariables
        list = ['T_']
        list.append(str(T_i))
        tempVariable=''.join(list)
        T_i +=1

        listOfTempVariables += [tempVariable]

        create_entity('TEMP', tempVariable, '')

        return tempVariable

def emptyList():
        pointerList = []
        return pointerList

def makeList(x):
        listThis = [x]
        return listThis

def merge(list1, list2):
        list=[]
        list = list+list1+list2
        return list

def backPatch(list, z):
        global listOfAllQuads
        for i in range(len(list)):
                for j in range(len(listOfAllQuads)):
                        if(list[i]==listOfAllQuads[j][0] and listOfAllQuads[j][4]=='_'):
                                listOfAllQuads[j][4] = z
                                break;
        return

def print_listOfAllQuads():
	for i in range(len(listOfAllQuads)):
            if i<9:
                    print (" "+str(listOfAllQuads[i][0])+". "+str(listOfAllQuads[i][1])+" "+str(listOfAllQuads[i][2])+" "+str(listOfAllQuads[i][3])+" "+str(listOfAllQuads[i][4]))
            else:
                    print (str(listOfAllQuads[i][0])+". "+str(listOfAllQuads[i][1])+" "+str(listOfAllQuads[i][2])+" "+str(listOfAllQuads[i][3])+" "+str(listOfAllQuads[i][4]))

# Symbol table classes
topScope=None
class scope():
        def __init__(self):
                self.name = ''
                self.entityList = []
                self.level = 0
                self.enclosingScope = None

class entity():
        def __init__(self):
                self.name = ''
                self.type = ''
                self.variable = self.variable()
                self.tempVar = self.tempVariable()
                self.subprogram = self.subProgram()
                self.parameter = self.parameter()

        class variable:
                def __init__(self):
                        self.type = 'Int'
        class subProgram:
                def __init__(self):
                        self.type = ''
                        self.argumentList = []

        class parameter:
                def __init__(self):
                        self.mode = ''
        class tempVariable:
                def __init__(self):
                    self.type = 'Int'

class argument():
        def __init__(self):
                self.name = ''
                self.type = 'Int'
                self.parType = ''



# Symbol table functions

def new_scope(name):
        global topScope

        nextScope= scope()
        nextScope.name= name
        nextScope.enclosingScope=topScope

        if(topScope is not None):
                nextScope.level= topScope.level + 1
        else:
                nextScope.level= 0
        topScope = nextScope

def new_entity(object):
        global topScope

        topScope.entityList.append(object)

def new_argument(object):
        global topScope

        topScope.entityList[-1].subprogram.argumentList.append(object)

def create_entity(enttype,entname,entsubprogram):
        ent = entity()
        ent.type = enttype
        ent.name = entname
        if (enttype!='VARIABLE' or enttype!='TEMP'):
                ent.subprogram.type = entsubprogram
        new_entity(ent)

def create_parameter_entity(arg):
        ent = entity()
        ent.name = arg.name
        ent.type = 'PARAMETER'
        ent.parameter.mode = arg.parType
        new_entity(ent)

def create_argument(argname, argparType):
        arg = argument()
        arg.name = argname
        arg.parType= argparType
        new_argument(arg)

def delete_scope():
        global topScope

        tempScope = topScope
        topScope = topScope.enclosingScope

        del tempScope

def add_parameters():
        global topScope

        for arg in topScope.enclosingScope.entityList[-1].subprogram.argumentList:
                create_parameter_entity(arg)

def write_Symbol_Table():
        global topScope
        global symbolFile

        symbolFile.write('')

        currentScope=topScope
        while (currentScope is not None):
                symbolFile.write("(SCOPE)"+"\t name:"+currentScope.name+"\t level:"+str(currentScope.level))
                symbolFile.write("\n\t [ENTITIES]")
                for ent in currentScope.entityList:
                        if(ent.type == 'VARIABLE'):
                                symbolFile.write("\n\t"+" name:"+ent.name+"\t type:"+ent.type+"\t variable-type:"+ent.variable.type)
                        elif(ent.type == 'TEMP'):
                                symbolFile.write("\n\t"+" name:"+ent.name+"\t type:"+ent.type+"\t temp-type:"+ent.tempVar.type)
                        elif(ent.type == 'SUBPROGRAM'):
                            if(ent.subprogram.type == 'function'):
                                    symbolFile.write("\n\t"+" name:"+ent.name+"\t type:"+ent.type+"\t function-type:"+ent.subprogram.type)
                                    symbolFile.write("\n\t\t <ARGUMENTS>")
                                    for arg in ent.subprogram.argumentList:
                                            symbolFile.write("\n\t\t"+" name:"+arg.name+"\t type:"+arg.type+"\t parType:"+arg.parType)
                            elif(ent.subprogram.type == 'procedure'):
                                    symbolFile.write("\n\t"+" name:"+ent.name+"\t type:"+ent.type+"\t procedure-type:"+ent.subprogram.type)
                                    symbolFile.write("\n\t\t <ARGUMENTS>")
                                    for arg in ent.subprogram.argumentList:
                                        symbolFile.write("\n\t\t"+" name:"+arg.name+"\t type:"+arg.type+"\t parType:"+arg.parType)
                        elif(ent.type == 'PARAMETER'):
                                symbolFile.write("\n\t"+" name:"+ent.name+"\t type:"+ent.type+"\t mode:"+ent.parameter.mode)
                symbolFile.write("\n------------------------------------------------------\n")
                currentScope = currentScope.enclosingScope


# Syntax Analysis

def printError(message,line):
        global filename
        global file
        global cFile
        global intFile
        global symbolFile

        print(">>SYNTAX ERROR near line ("+str(line)+"): "+message)
        print('\n')
        print('Exiting...')
        print('---------')
        print('**********')
        print('\n')

        file.close()
        cFile.close()
        intFile.close()
        symbolFile.close()

        os.remove(filename[:-3]+'.int')
        os.remove(filename[:-3]+'.c')
        os.remove(filename[:-3]+'_symbol_table.txt')
        return


def syntax_an():

        global current
        global temp

        current=lex()

        def program():
                global current

                if(current.token == reservedWords['program']):
                        current = lex()


                        if(current.token == token['idk']):
                                name = current.word
                                current = lex()

                                block(name, 1)
                                if(current.token == token['.']):
                                        current = lex()

                                        return
                                else:
                                        printError("All programs must end with a '.' ", current.line)
                                        exit()
                        else:
                                printError("All programs must be named",current.line)
                                exit()
                else:
                         printError("All programs must start with 'program' followed by the program's name ",current.line)
                         exit()

        def block(name, flag):
                new_scope(name)

                declarations()

                subprograms()

                genQuad('begin_block',name,'_','_')

                statements()

                if(flag==1):
                        genQuad('halt','_','_','_')

                genQuad('end_block',name,'_','_')

                write_Symbol_Table()

                delete_scope()


        def declarations():
                global current
                global cFile

                while(current.token == reservedWords['declare']):
                        current = lex()

                        cFile.write("int ")
                        varlist()
                        cFile.write(";\n\t")

                        if(current.token == token[';']):
                                current = lex()


                        else:
                                printError("Semicolon missing ", current.line)
                                exit()
                return


        def varlist():
                global current
                global cFile

                if(current.token == token['idk']):
                        cFile.write(current.word)

                        create_entity('VARIABLE', current.word, '')

                        current = lex()

                        while(current.token == token[',']):
                                cFile.write(current.word)
                                current = lex()


                                if(current.token == token['idk']):
                                        cFile.write(current.word)

                                        create_entity('VARIABLE', current.word, '')

                                        current = lex()

                                else:
                                        printError("All identifiers must be separated by one comma ',' ", current.line)
                                        exit()
                return

        def subprograms():
                global current

                while(current.token == reservedWords['procedure'] or current.token == reservedWords['function'] ):
                        subprogram()
                return


        def subprogram():
                global current

                if(current.token==reservedWords['procedure']):
                        current=lex()


                        if(current.token==token['idk']):
                                id = current.word

                                create_entity('SUBPROGRAM', current.word, 'procedure')

                                current = lex()

                                if(current.token == token['(']):
                                        current = lex()


                                        formalparlist()

                                        if(current.token == token[')']):
                                                current = lex()

                                                block(id,0)

                                                return
                                        else:
                                                printError("Expected closing parenthesis ')' ",current.line)
                                                exit()
                                else:
                                        printError("Expected parenthesis '(' ",current.line)
                                        exit()
                        else:
                                printError("Expected identifier after 'procedure' ", current.line)
                                exit()
                elif(current.token== reservedWords['function']):
                        current = lex()
                        if(current.token==token['idk']):
                                id = current.word

                                create_entity('SUBPROGRAM', current.word, 'function')

                                current = lex()

                                if(current.token == token['(']):
                                        current = lex()

                                        formalparlist()

                                        if(current.token == token[')']):
                                                current = lex()

                                                block(id,0)

                                                return
                                        else:
                                                printError("Expected closing parenthesis ')' ",current.line)
                                                exit()
                                else:
                                        printError("Expected parenthesis '(' ",current.line)
                                        exit()
                        else:
                                printError("Expected identifier after 'function' ", current.line)
                                exit()

        def formalparlist():
                global current

                formalparitem()
                while(current.token == token[',']):
                        current  = lex()

                        formalparitem()
                return


        def formalparitem():
                global current

                if(current.token == reservedWords['in']):
                        current = lex()


                        if(current.token== token['idk']):

                                create_argument(current.word, 'VALUE')

                                current = lex()

                        else:
                                printError("Expected variable name after 'in' ", current.line)
                                exit()
                elif(current.token == reservedWords['inout']):
                        current = lex()


                        if(current.token == token['idk']):

                                create_argument(current.word, 'REFERENCE')

                                current = lex()

                        else:
                                printError("Expected variable name after 'inout' ", current.line)
                                exit()
                else:
                        printError("Expected either 'in' or 'inout' ", current.line)
                        exit()
                return

        def statements():
                global current

                if(current.token == token['{']):
                        current = lex()

                        statement()

                        while(current.token == token[';']):
                                current = lex()

                                statement()
                        if(current.token == token['}']):
                                current = lex()

                                return

                        else:
                                printError("Non closing block ", current.line)
                                exit()
                else:

                        statement()
                        if(current.token == token[';']):
                                current = lex()

                                return
                        else:
                                printError("Missing semicolon ", current.line)
                                exit()

        def statement():
                global current

                if(current.token==token['idk']):
                        assignment_stat()
                elif(current.token==reservedWords['if']):
                        if_stat()
                elif(current.token==reservedWords['while']):
                        while_stat()
                elif(current.token==reservedWords['switchcase']):
                        switchcase_stat()
                elif(current.token==reservedWords['forcase']):
                        forcase_stat()
                elif(current.token==reservedWords['incase']):
                        incase_stat()
                elif(current.token==reservedWords['call']):
                        call_stat()
                elif(current.token==reservedWords['return']):
                        return_stat()
                elif(current.token==reservedWords['input']):
                        input_stat()
                elif(current.token==reservedWords['print']):
                        print_stat()
                return

        def assignment_stat():
                global current

                if(current.token == token['idk']):
                        myid = current.word
                        current = lex()


                        if(current.token == token[':=']):
                                current = lex()

                                Eplace = expression()
                                genQuad(':=', Eplace, '_', myid)
                                return
                        else:
                                printError("Expected assignment symbol ':=' after variable name", current.line)
                                exit()
                else:
                        printError("Faulty assignment attempt ",current.line)
                        exit()

        def if_stat():
                global current

                if(current.token == reservedWords['if']):
                        current= lex()


                        if(current.token == token['(']):
                                current = lex()


                                C = condition()
                                backPatch(C[0], nextQuad())

                                if(current.token== token[')']):
                                        current = lex()

                                        statements()
                                        ifList = makeList(nextQuad())
                                        genQuad('jump', '_', '_', '_')
                                        backPatch(C[1], nextQuad())
                                        elsepart()
                                        backPatch(ifList, nextQuad())
                                        return
                                else:
                                        printError("Non closing parenthesis in 'if' conditions ", current.line)
                                        exit()
                        else:
                                printError("Conditions in 'if' statements must be enclosed in parenthesis ", current.line)
                                exit()
                else:
                        printError("Faulty if statement ",current.line)
                        exit()


        def elsepart():
                global current

                if(current.token == reservedWords['else']):
                        current=lex()

                        statements()
                return


        def while_stat():
                global current

                if(current.token== reservedWords['while']):
                        current = lex()


                        if(current.token == token['(']):
                                current = lex()

                                Cquad=nextQuad()
                                C = condition()
                                backPatch(C[0], nextQuad())

                                if(current.token == token[')']):
                                        current = lex()


                                        statements()

                                        genQuad('jump', '_', '_', Cquad)
                                        backPatch(C[1], nextQuad())

                                        return
                                else:
                                        printError("Non closing parenthesis in 'while' conditions", current.line)
                                        exit()
                        else:
                                printError("Conditions in 'while' statements must be enclosed in parenthesis ",current.line)
                                exit()
                else:
                        printError("Faulty while statement ", current.line)
                        exit()

        def switchcase_stat():
                global current

                if(current.token == reservedWords['switchcase']):
                        current = lex()


                        outList=emptyList()

                        while(current.token == reservedWords['case']):
                                current = lex()

                                if(current.token == token['(']):
                                        current = lex()


                                        C = condition()
                                        backPatch(C[0], nextQuad())

                                        if(current.token == token[')']):
                                                current = lex()


                                                statements()
                                                outJump = makeList(nextQuad())
                                                genQuad('jump', '_', '_', '_')
                                                outList = merge(outList, outJump)
                                                backPatch(C[1], nextQuad())

                                        else:
                                                printError("Non closing parenthesis in 'switchcase' condition ", current.line)
                                                exit()
                                else:
                                        printError("Conditions in 'switchcase' statements must be enclosed in parenthesis ", current.line)
                                        exit()
                        if(current.token == reservedWords['default']):
                                current = lex()

                                statements()
                                backPatch(outList, nextQuad())
                        else:
                                printError("Faulty 'default' case in 'switchcase' statement ", current.line)
                                exit()
                else:
                        printError("Faulty 'switchcase' statement ", current.line)
                        exit()


        def forcase_stat():
                global current

                if(current.token == reservedWords['forcase']):
                        current = lex()

                        quad=nextQuad()

                        while(current.token == reservedWords['case']):
                                current = lex()

                                if(current.token == token['(']):
                                        current = lex()

                                        C = condition()
                                        backPatch(C[0], nextQuad())
                                        if(current.token == token[')']):
                                                current = lex()

                                                statements()
                                                genQuad('jump','_','_',quad)
                                                backPatch(C[1], nextQuad())
                                        else:
                                                printError("Non closing parenthesis in 'forcase' condition ", current.line)
                                                exit()
                                else:
                                        printError("Conditions in 'forcase' statements must be enclosed in parenthesis ", current.line)
                                        exit()
                        if(current.token == reservedWords['default']):
                                current = lex()

                                statements()
                        else:
                                printError("Faulty 'default' case in 'forcase' statement ", current.line)
                                exit()
                else:
                        printError("Faulty 'forcase' statement ", current.line)
                        exit()

        def incase_stat():
                global current

                if(current.token == reservedWords['incase']):
                        current = lex()

                        quad=nextQuad()
                        w = newTemp()
                        genQuad(':=','0','_',w)
                        while(current.token == reservedWords['case']):
                                current = lex()


                                if(current.token == token['(']):
                                        current = lex()


                                        C = condition()
                                        backPatch(C[0], nextQuad())

                                        if(current.token == token[')']):
                                                current = lex()


                                                statements()
                                                genQuad(':=','1','_',w)
                                                backPatch(C[1], nextQuad())
                                        else:
                                                printError("Non closing parenthesis in 'incase' condition ", current.line)
                                                exit()
                                else:
                                        printError("Conditions in 'incase' statements must be enclosed in parenthesis", current.line)
                                        exit()
                        genQuad('=',w,'1',quad)
                else:
                        printError("Faulty 'incase' statement", current.line)
                        exit()


        def return_stat():
                global current

                if(current.token == reservedWords['return']):
                        current = lex()


                        if(current.token == token['(']):
                                current = lex()


                                Eplace = expression()
                                genQuad('retv', Eplace, '_', '_')

                                if(current.token == token[')']):
                                        current = lex()

                                        return
                                else:
                                        printError("Non closing parenthesis in 'return' statement ",current.line)
                                        exit()
                        else:
                                printError("Expressions and/or variables in 'return' statements must be enclosed in parenthesis ", current.line)
                                exit()


        def call_stat():
                global current

                if(current.token == reservedWords['call']):
                        current = lex()


                        if(current.token == token['idk']):
                                idName = current.word
                                current = lex()


                                if(current.token == token['(']):
                                        current = lex()

                                        actualparlist()
                                        genQuad('call', idName, '_', '_')

                                        if(current.token == token[')']):
                                                current = lex()

                                                return
                                        else:
                                                printError("Non closing parenthesis in 'call' statement ",current.line)
                                                exit()
                                else:
                                        printError("Expressions in 'call' statements must be enclosed in parenthesis ", current.line)
                                        exit()

                        else:
                                printError("Expected identifier in 'call' statement ", current.line)
                                exit()
                else:
                        printError("Faulty 'call' statement ",current.line)
                        exit()

        def print_stat():
                global current

                if(current.token == reservedWords['print']):
                        current = lex()


                        if(current.token == token['(']):
                                current = lex()
                                Eplace = expression()
                                genQuad('out', Eplace, '_', '_')
                                if(current.token == token[')']):
                                        current = lex()


                                else:
                                        printError("Non closing parenthesis in 'print' statement",current.line)
                                        exit()
                        else:
                                printError("Expressions and/or variables in 'print' statements must be enclosed in parenthesis", current.line)
                                exit()
                else:
                        printError("Faulty 'print' statement ", current.line)
                        exit()
                return


        def input_stat():
                global current

                if(current.token == reservedWords['input']):
                        current = lex()


                        if(current.token == token['(']):
                                current = lex()

                                if(current.token == token['idk']):
                                        myid = current.word
                                        genQuad('inp',myid,'_','_')
                                        current = lex()

                                        if(current.token == token[')']):
                                                current = lex()

                                                return
                                        else:
                                                printError("Non closing parenthesis in 'input' statement",current.line)
                                                exit()
                                else:
                                        printError("Expected identifier in 'input' statement ",current.line)
                                        exit()
                        else:
                                printError("Variables in 'input' statements must be enclosed in parenthesis", current.line)
                                exit()
                else:
                        printError("Faulty 'input' statement", current.line)
                        exit()


        def actualparlist():
                global current

                actualparitem()
                while(current.token == token[',']):
                        current  = lex()

                        actualparitem()
                return


        def actualparitem():
                global current

                if(current.token == reservedWords['in']):
                        current = lex()

                        thisExpression = expression()
                        genQuad('par', thisExpression, 'VALUE', '_')
                elif(current.token == reservedWords['inout']):
                        current = lex()

                        if(current.token == token['idk']):
                                name = current.word
                                current = lex()

                                genQuad('par', name, 'REFERENCE', '_')
                        else:
                                printError("Expected variable name after 'inout' statement ", current.line)
                                exit()
                else:
                        printError("Expected either 'in' or 'inout' ", current.line)
                        exit()

                return


        def condition():
                global current

                Ctrue = []
                Cfalse = []
                BT1 = boolterm()
                Ctrue = BT1[0]
                Cfalse = BT1[1]

                while(current.token==reservedWords['or']):
                        current=lex()
                        backPatch(Cfalse, nextQuad())
                        BT2 = boolterm()
                        Ctrue = merge(Ctrue, BT2[0])
                        Cfalse = BT2[1]

                return Ctrue, Cfalse


        def boolterm():
                global current

                BTtrue = []
                BTfalse = []
                BF1 = boolfactor()
                BTtrue = BF1[0]
                BTfalse = BF1[1]

                while(current.token==reservedWords['and']):
                        current=lex()
                        backPatch(BTtrue, nextQuad())
                        BF2 = boolfactor()
                        BTfalse = merge(BTfalse, BF2[1])
                        BTtrue = BF2[0]

                return BTtrue, BTfalse



        def boolfactor():
                global current
                BFtrue = []
                BFfalse = []

                if(current.token==reservedWords['not']):
                        current=lex()


                        if(current.token==token['[']):
                                current = lex()
                                C = condition()

                                if(current.token==token[']']):
                                        current = lex()
                                        BFtrue = C[1]
                                        BFfalse = C[0]
                                else:
                                        printError("Non closing brackets in condtition ",current.line)
                                        exit()
                        else:
                                printError("Conditions following 'not' must be enclosed in brackets ", current.line)
                                exit()
                elif(current.token==token['[']):
                        current = lex()

                        C = condition()

                        if(current.token==token[']']):
                                current = lex()


                                BFtrue = C[0]
                                BFfalse = C[1]
                        else:
                                printError("Non closing brackets in condtition", current.line)
                                exit()
                else:
                        Eplace1 = expression()
                        relop = relational_oper()
                        Eplace2 = expression()
                        BFtrue=makeList(nextQuad())
                        genQuad(relop, Eplace1, Eplace2, '_')
                        BFfalse=makeList(nextQuad())
                        genQuad('jump', '_', '_', '_')

                return BFtrue, BFfalse


        def expression():
                global current

                optional_sign()
                T1place = term()
                while(current.token==token['+'] or current.token==token['-']):
                        plusOrMinus = add_oper()
                        T2place = term()
                        w = newTemp()
                        genQuad(plusOrMinus, T1place, T2place, w)
                        T1place = w
                Eplace = T1place

                return Eplace


        def term():
                global current

                F1place = factor()

                while(current.token==token['*'] or current.token==token['/']):
                        mulOrDiv = mul_oper()

                        F2place = factor()

                        w=newTemp()
                        genQuad(mulOrDiv, F1place, F2place, w)
                        F1place = w
                Tplace =F1place

                return Tplace


        def factor():
                global current

                if(current.token==token['digits']):
                        fact = current.word
                        current = lex()

                elif(current.token==token['(']):
                        current = lex()

                        Eplace = expression()
                        fact = Eplace

                        if(current.token==token[')']):
                                current = lex()

                        else:
                                printError("Non closing parenthesis following expression ",current.line)
                                exit()

                elif(current.token==token['idk']):
                        fact_temp = current.word
                        current = lex()

                        fact = idtail(fact_temp)
                else:
                        printError("Expected either expression or variable or constant ",current.line)
                        exit()

                return fact

        def idtail(name):
                global current

                if(current.token == token['('] ):
                        current = lex()

                        actualparlist()
                        w=newTemp()
                        genQuad('par', w, 'RET', '_')
                        genQuad('call', name, '_', '_')

                        if(current.token==token[')']):
                                current = lex()

                                return w
                        else:
                                printError("Non closing parenthesis ",current.line)
                                exit()
                else:
                        return name


        def optional_sign():
                global current

                if(current.token == token['+'] or current.token == token['-']):
                        add_oper()

                return


        def relational_oper():
                global current

                if(current.token==token['=']):
                        relop = current.word
                        current = lex()

                elif(current.token==token['<']):
                        relop = current.word
                        current = lex()

                elif(current.token==token['<=']):
                        relop = current.word
                        current = lex()

                elif(current.token==token['<>']):
                        relop = current.word
                        current = lex()

                elif(current.token== token['>']):
                        relop = current.word
                        current = lex()

                elif(current.token==token['>=']):
                        relop = current.word
                        current = lex()

                else:
                        printError("Expected relational operator ",current.line)
                        exit()
                return relop


        def add_oper():
                global current

                if(current.token==token['+']):
                        addOp = current.word
                        current = lex()

                elif(current.token==token['-']):
                        addOp = current.word
                        current = lex()

                return addOp


        def mul_oper():
                global current

                if (current.token == token['*']):
                        oper = current.word
                        current = lex()


                elif (current.token == token['/']):
                        oper = current.word
                        current = lex()


                return oper

        program()
        return


# Intermediate code production
def intCode(intFile):
        for i in range(len(listOfAllQuads)):
                quad = listOfAllQuads[i]
                for j in range(5):
                        intFile.write(str(quad[j]))
                        if (j==0):
                                intFile.write(":   ")
                        else :
                                intFile.write("  ")

                intFile.write("\n")
        return

# C code production
def cCode():
        global listOfTempVariables

        if(len(listOfTempVariables)!=0):
                cFile.write("int ")
        for i in range(len(listOfTempVariables)):
                cFile.write(listOfTempVariables[i])
                if(len(listOfTempVariables) == i+1):
                        cFile.write(";\n\n\t")
                else:
                        cFile.write(",")

        for j in range(len(listOfAllQuads)):

                C_dict={'begin_block':"\n\t" ,
                ':=':str(listOfAllQuads[j][4])+"="+str(listOfAllQuads[j][2])+";\n\t",
                '+':str(listOfAllQuads[j][4])+"="+str(listOfAllQuads[j][2])+"+"+str(listOfAllQuads[j][3])+";\n\t",
                '-':str(listOfAllQuads[j][4])+"="+str(listOfAllQuads[j][2])+"-"+listOfAllQuads[j][3]+";\n\t",
                '*':str(listOfAllQuads[j][4])+"="+str(listOfAllQuads[j][2])+"*"+str(listOfAllQuads[j][3])+";\n\t",
                '/':str(listOfAllQuads[j][4])+"="+str(listOfAllQuads[j][2])+"/"+str(listOfAllQuads[j][3])+";\n\t",
                'jump':"goto L_"+str(listOfAllQuads[j][4])+ ";\n\t",
                '<':"if ("+str(listOfAllQuads[j][2])+"<"+str(listOfAllQuads[j][3])+") goto L_"+str(listOfAllQuads[j][4])+";\n\t",
                '>':"if ("+listOfAllQuads[j][2]+">"+str(listOfAllQuads[j][3])+") goto L_"+str(listOfAllQuads[j][4])+";\n\t",
                '>=':"if ("+listOfAllQuads[j][2]+">="+str(listOfAllQuads[j][3])+") goto L_"+str(listOfAllQuads[j][4])+";\n\t",
                '<=':"if ("+listOfAllQuads[j][2]+"<="+str(listOfAllQuads[j][3])+") goto L_"+str(listOfAllQuads[j][4])+";\n\t",
                '<>':"if ("+str(listOfAllQuads[j][2])+"!="+str(listOfAllQuads[j][3])+") goto L_"+str(listOfAllQuads[j][4])+";\n\t",
                '=':"if ("+str(listOfAllQuads[j][2])+"=="+str(listOfAllQuads[j][3])+") goto L_"+str(listOfAllQuads[j][4])+";\n\t",
                'out':"printf(\""+str(listOfAllQuads[j][2])+"= %d\", "+str(listOfAllQuads[j][2])+");\n\t",
                'halt':": {}\n\t" }

                if(listOfAllQuads[j][1] in C_dict.keys()):
                        cFile.write("L_"+str(j+1)+": "+C_dict[listOfAllQuads[j][1]])
        cFile.write("\n}")
        return

# Main function
def main():
        global file
        global cFile
        global intFile
        global symbolFile
        global filename

        print('\n')
        print('**********')


        if (len(sys.argv))==2:
                filename=sys.argv[1]
        else:
                print(">>USAGE ERROR: Correct usage:'python3 cimple_3015_4095.py <example>.ci'")
                print('\n')
                print('Exiting...')
                print('---------')
                print('**********')
                print('\n')
                exit()
        if len(filename)<4:
                print(">>USAGE ERROR: Correct usage:'python3 cimple_3015_4095.py <example>.ci'")
                print('\n')
                print('Exiting...')
                print('---------')
                print('**********')
                print('\n')
                exit()
        if ((filename[-3]+filename[-2]+filename[-1])=='.ci') :
                if (path.exists(filename)):
                        file = open(filename,'r')
                        cFile = open(filename[:-3]+'.c','w')
                        intFile = open(filename[:-3]+'.int','w')
                        symbolFile = open(filename[:-3]+'_symbol_table.txt','w')

                else:
                        print(">>USAGE ERROR: File '"+filename+"' was not found")
                        print('\n')
                        print('Exiting...')
                        print('---------')
                        print('**********')
                        print('\n')
                        exit()
        else:
                print(">>USAGE ERROR: Files for parsing MUST be '.ci' files")
                print('\n')
                print('Exiting...')
                print('---------')
                print('**********')
                print('\n')
                exit()



        print('File selected: '+filename)
        print('---------')

        syntax_an()
        print('\n')
        print('Parsing successful!')
        print('>Total tokens generated: '+str(tokenCounter))
        print('>Total quads generated: '+str(len(listOfAllQuads)))


        intCode(intFile)
        print(">Intermediate code written at '"+filename[:-3]+".int'")

        cCode()
        print(">C code written at '"+filename[:-3]+".c'")

        print(">Symbol table written at '"+filename[:-3]+"_symbol_table.txt'")

        file.close()
        cFile.close()
        intFile.close()
        symbolFile.close()
        print('\n')
        print('Exiting...')
        print('---------')
        print('**********')
        print('\n')

main()