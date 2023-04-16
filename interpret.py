import sys #arguments
import re #regex
import xml.etree.ElementTree as ET #xml parsing

SYNTAX_ERR = -1
PARAMETER_ERR = 10
IN_FILE_ERR = 11
XML_SYNTAX_ERR = 31
XML_SYNTAX_STRUCTURE_ERR = 32
SEMANTIC_ERR = 52
MULTIPLE_DEFINITION_ERR = 52
LABEL_ERR = 52
RUNTIME_OPERAND_TYPE_ERR = 53
RUNTIME_VARIABLE_ERR = 54
RUNTIME_FRAME_ERR = 55
RUNTIME_MISSING_VALUE_ERR = 56
RUNTIME_DIVISION_BY_ZERO_ERR = 57
RUNTIME_WRONG_RETURN_VALUE_ERR = 57
RUNTIME_WRONG_OPERAND_VALUE_ERR = 57
RUNTIME_STRING_ERR = 58
RUNTIME_INTERNAL_ERR = 99
EMPTY = ""

if len(sys.argv) == 4 and sys.argv[3] == '--testerfester':
    DEVEL = 1  
else:
    DEVEL = 0

class Context:
    def __init__(self):
        self.globalFrame = {}
        self.localFrameStack = []
        self.localFrameHead = None
        self.temporaryFrame = None
        self.labels = {}
        self.stack = []
        self.returnAddressStack = [] 
        self.instructionIndex = 0 
        self.parser = None
        
    def __repr__(self):
        return f"<context(instructionIndex={self.instructionIndex}, localFrame={self.localFrameHead}, globalFrame={self.globalFrame}, temporaryFrame={self.temporaryFrame})>"
    
    def pushAddressStack(self, address):
        self.returnAddressStack.append(address)
        
    def popAddressStack(self):
        if len(self.returnAddressStack) == 0:
            if(DEVEL == 1): print(f"\t\t[dev]: Address stack is empty")
            exit(RUNTIME_MISSING_VALUE_ERR)
        return self.returnAddressStack.pop()
        
    def getInstructionIndex(self):
        return self.instructionIndex
    
    def incrementInstructionIndex(self):
        self.instructionIndex += 1
    
    def setInstructionIndex(self, index):
        self.parser.lastInstructionnumber = 0
        self.instructionIndex = index
    
    def addLabel(self,label,position):
        if(DEVEL): print(f"\t\t[dev]: Adding label {label} to position {position} ...")
        if label not in self.labels:
            self.labels[label] = position
            if(DEVEL): print(f"\t\t[dev]: Label {label} added to position {position}")
        else:
            # label already defined but, check if the position is the same
            if self.labels[label] == position:
                return
            if(DEVEL): print(f"\t\t[dev]: Label {label} is already defined")
            exit(MULTIPLE_DEFINITION_ERR)
            
    def getLabelPosition(self,label):
        if label in self.labels:
            return self.labels[label]
        else:
            if(DEVEL): print(f"\t\t[dev]: Label {label} is not defined")
            return None
    
    def pushDataStack(self,value):
        self.stack.append(value)
        
    def popStack(self):
        if len(self.stack) == 0:
            if(DEVEL == 1): print(f"\t\t[dev]: Stack is empty")
            exit(RUNTIME_MISSING_VALUE_ERR)
        return self.stack.pop()
    
    def splitVariable(self,variable):
        if variable[0] == "G" and variable[1] == "F":
            return "GF", variable[3:]
        elif variable[0] == "L" and variable[1] == "F":
            return "LF", variable[3:]
        elif variable[0] == "T" and variable[1] == "F":
            return "TF", variable[3:]
        else:
            if(DEVEL == 1): print(f"\t\t[dev]: Variable {variable} is not defined")
            exit(SEMANTIC_ERR)
        
    def isDefined(self,variable):
        frame , variable = self.splitVariable(variable)
        frame = self.getFrame(frame)
        if variable in frame:
            return True
        else:
            return False
    
    def createVariable(self,variable):
        # check if variable is already defined
        if self.isDefined(variable) == False:
            frame , variable = self.splitVariable(variable)
            frame = self.getFrame(frame)
            frame[variable] = EMPTY
        else:
            if(DEVEL == 1): print(f"\t\t[dev]: Variable {variable} was already defined 1")
            exit(MULTIPLE_DEFINITION_ERR)
                
    def updateVariable(self,variable,value):
        if self.isDefined(variable):
            frame , variable = self.splitVariable(variable)
            frame = self.getFrame(frame)
            frame[variable] = value
            return True
        else:
            if(DEVEL == 1): print(f"\t\t[dev]: Variable {variable} is not defined 2")
            exit(RUNTIME_VARIABLE_ERR)
            
    def getVariablesValue(self,variable):
        if self.isDefined(variable):
            frame , variable = self.splitVariable(variable)
            frame = self.getFrame(frame)
            return frame[variable]
        else:
            if(DEVEL == 1): print(f"\t\t[dev]: Variable {variable} is not defined 3")
            exit(RUNTIME_VARIABLE_ERR)
    
    def getSymbValue(self,symbol):
        if symbol.type == "var" and self.isDefined(symbol.value):
            return self.getVariablesValue(symbol.value)
        else:
            return symbol.value
        
    def getSymbType(self,symbol):
        if symbol.type == "var":
            value = self.getVariablesValue(symbol.value)
            if value == None:
                return 'nil'
            elif value == 'true' or value == 'false':
                return 'bool'
            elif value.isdigit():
                return 'int'
            elif value == EMPTY:
                return None
            else:
                return 'string'
        else:
            return symbol.type
            
                
    def createFrame(self):
        self.temporaryFrame = {}
        
    def pushFrame(self):
        if self.temporaryFrame != None:
            self.localFrameStack.append(self.localFrameHead)
            self.localFrameHead = self.temporaryFrame
            self.temporaryFrame = None
        else:
            # TF not defined
            exit(RUNTIME_FRAME_ERR)

    def popFrame(self):
        if self.localFrameHead != None:
            self.temporaryFrame = self.localFrameHead
            # pop LF
            if len(self.localFrameStack) != 0:
                self.localFrameHead = self.localFrameStack.pop()
            else:
                self.localFrameHead = None
        else:
            # LF not defined
            exit(RUNTIME_FRAME_ERR)
        
    def getFrame(self,frame):
        if frame == "GF":
            return self.globalFrame
        elif frame == "LF":
            if self.localFrameHead != None:
                return self.localFrameHead
        elif frame == "TF":
            if self.temporaryFrame != None:
                return self.temporaryFrame
        # frame not defined
        exit(RUNTIME_FRAME_ERR)
        
    def setParser(self, parser):
        self.parser = parser
            
    def jumpForward(self, label):
        while self.parser.getNextLabel() == True:
            position = self.getLabelPosition(label)
            # instruction found going forward 
            # no set instruction index needed
            if position != None:
                return
        # if label is not found, exit with error
        if (DEVEL): print("Label not found")
        exit(LABEL_ERR)

class Argument:
    def __init__(self, tag, type, value):
        if(DEVEL == 1): print(f"\t\t[dev]: Argument created:{tag} {type} {value}")
        self.tag = tag
        self.type = type
        self.value = value

    def __repr__(self):
        return f"<arg#(type='{self.type}', value='{self.value}'>)"

class Instruction():
    def __init__(self, context, input=None):
        self.argumentList = {}
        self.context = context
        self.input = input
        
    def checkNumberofArguments(self, number):
        if len(self.argumentList) != number:
            exit(XML_SYNTAX_STRUCTURE_ERR)
    
    def doOperation(self):
        pass
    
    def addArgument(self,argument):
        if argument.tag in self.argumentList:
            if DEVEL == 1: print(f"\t\t[dev]: Argument {argument.tag} is already defined")
            exit(XML_SYNTAX_STRUCTURE_ERR)
        self.argumentList[argument.tag] = argument
    
    def getArgument(self,tag):
        if tag in self.argumentList:
            return self.argumentList[tag]
        else:
            if(DEVEL == 1): print(f"\t\t[dev]: Argument {tag} is not defined")
            exit(XML_SYNTAX_STRUCTURE_ERR)
        
    def __repr__(self):
        return f"<instruction({type(self).__name__})>"

class MOVE(Instruction):
    def doOperation(self):
        if (DEVEL):print(f'\t\t[dev]: {type(self).__name__} instruction in process...')
        self.checkNumberofArguments(2)
        variable = self.getArgument("arg1")
        symbol = self.getArgument("arg2")
        if symbol.type == "var":
            varValue = self.context.getVariablesValue(symbol.value)
            self.context.updateVariable(variable.value, varValue)
        else:
            self.context.updateVariable(variable.value,symbol.value)
        
class CREATEFRAME(Instruction):
    def doOperation(self):
        if (DEVEL):print(f'\t\t[dev]: {type(self).__name__} instruction in process...')
        self.context.createFrame()
        
class PUSHFRAME(Instruction):
    def doOperation(self):
        if (DEVEL):print(f'\t\t[dev]: {type(self).__name__} instruction in process...')
        self.checkNumberofArguments(0)
        self.context.pushFrame()
        
class POPFRAME(Instruction):
    def doOperation(self):
        if (DEVEL):print(f'\t\t[dev]: {type(self).__name__} instruction in process...')
        self.checkNumberofArguments(0)
        self.context.popFrame()
        
class DEFVAR(Instruction):
    def doOperation(self):
        if (DEVEL):print(f'\t\t[dev]: {type(self).__name__} instruction in process...')
        self.checkNumberofArguments(1)
        self.context.createVariable(self.getArgument("arg1").value)
        
class CALL(Instruction):
    def doOperation(self):
        if (DEVEL):print(f'\t\t[dev]: {type(self).__name__} instruction in process...')
        self.checkNumberofArguments(1)
        # push return address to stack
        currentInstruction = self.context.getInstructionIndex()
        self.context.pushAddressStack(currentInstruction)
        
        # search for label
        label = self.getArgument("arg1").value
        position = self.context.getLabelPosition(label)
        
        # look for label in instructions going forward
        if position == None:
            self.context.jumpForward(label)
        else:
            # label found, go to instruction index
            self.context.setInstructionIndex(position)

class RETURN(Instruction):
    def doOperation(self):
        if (DEVEL):print(f'\t\t[dev]: {type(self).__name__} instruction in process...')
        self.checkNumberofArguments(0)
        # pop return address from stack
        returnAddress = self.context.popAddressStack()
        self.context.setInstructionIndex(returnAddress)
        
class PUSHS(Instruction):
    def doOperation(self):
        if (DEVEL):print(f'\t\t[dev]: {type(self).__name__} instruction in process...')
        self.checkNumberofArguments(1)
        if self.getArgument("arg1").type == "var":
            varValue = self.context.getVariablesValue(self.getArgument("arg1").value)
            self.context.pushDataStack(varValue)
        else:
            self.context.pushDataStack(self.getArgument("arg1").value)
        
class POPS(Instruction):
    def doOperation(self):
        if (DEVEL):print(f'\t\t[dev]: {type(self).__name__} instruction in process...')
        self.checkNumberofArguments(1)
        var = self.getArgument("arg1")
        if var.type == "var" and self.context.isDefined(var.value):
            poppedValue = self.context.popStack()
            self.context.updateVariable(var.value, poppedValue)
        
class ADD(Instruction):
    def doOperation(self):
        if (DEVEL):print(f'\t\t[dev]: {type(self).__name__} instruction in process...')
        self.checkNumberofArguments(3)
        saveTo = self.getArgument("arg1")
        symb1 = self.getArgument("arg2")
        symb2 = self.getArgument("arg3")
        value1 = self.context.getSymbValue(symb1)
        value2 = self.context.getSymbValue(symb2)
        try:
            result = int(value1) + int(value2)
        except TypeError:
            if (DEVEL): print(f"ERR: wrong operand type for ADD")
            exit(RUNTIME_OPERAND_TYPE_ERR)
        except ValueError:
            # value is not int
            if (DEVEL): print(f"ERR: wrong operand type for ADD")
            exit(RUNTIME_OPERAND_TYPE_ERR)
            
        if (DEVEL): print(f"\t\t[dev]: ADD {value1} + {value2} = {result}")
        if saveTo.type == "var" and self.context.isDefined(saveTo.value):
            self.context.updateVariable(saveTo.value, str(result))
        
class SUB(Instruction):
    def doOperation(self):
        if (DEVEL):print(f'\t\t[dev]: {type(self).__name__} instruction in process...')
        self.checkNumberofArguments(3)
        saveTo = self.getArgument("arg1")
        symb1 = self.getArgument("arg2")
        symb2 = self.getArgument("arg3")
        value1 = self.context.getSymbValue(symb1)
        value2 = self.context.getSymbValue(symb2)
        try:
            result = int(value1) - int(value2)
        except TypeError:
            if (DEVEL): print(f"ERR: wrong operand type for ADD")
            exit(RUNTIME_OPERAND_TYPE_ERR)
        except ValueError:
            # value is not int
            if (DEVEL): print(f"ERR: wrong operand type for SUB")
            exit(RUNTIME_OPERAND_TYPE_ERR)
        
        if (DEVEL): print(f"\t\t[dev]: SUB {value1} - {value2} = {result}")
        if saveTo.type == "var" and self.context.isDefined(saveTo.value):
            self.context.updateVariable(saveTo.value, str(result))
            
class MUL(Instruction):
    def doOperation(self):
        if (DEVEL):print(f'\t\t[dev]: {type(self).__name__} instruction in process...')
        self.checkNumberofArguments(3)
        saveTo = self.getArgument("arg1")
        symb1 = self.getArgument("arg2")
        symb2 = self.getArgument("arg3")
        value1 = self.context.getSymbValue(symb1)
        value2 = self.context.getSymbValue(symb2)
        try:
            result = int(value1) * int(value2)
        except TypeError:
            if (DEVEL): print(f"ERR: wrong operand type for ADD")
            exit(RUNTIME_OPERAND_TYPE_ERR)
        except ValueError:
            # value is not int
            if (DEVEL): print(f"ERR: wrong operand type for MUL")
            exit(RUNTIME_OPERAND_TYPE_ERR)
        
        if (DEVEL): print(f"\t\t[dev]: MUL {value1} * {value2} = {result}")
        if saveTo.type == "var" and self.context.isDefined(saveTo.value):
            self.context.updateVariable(saveTo.value, str(result))
            
class IDIV(Instruction):
    def doOperation(self):
        if (DEVEL):print(f'\t\t[dev]: {type(self).__name__} instruction in process...')
        self.checkNumberofArguments(3)
        saveTo = self.getArgument("arg1")
        symb1 = self.getArgument("arg2")
        symb2 = self.getArgument("arg3")
        value1 = self.context.getSymbValue(symb1)
        value2 = self.context.getSymbValue(symb2)
        try:
            result = int(value1) // int(value2)
        except TypeError:
            if (DEVEL): print(f"ERR: wrong operand type for ADD")
            exit(RUNTIME_OPERAND_TYPE_ERR)
        except ValueError:
            # value is not int
            if (DEVEL): print(f"ERR: wrong operand type for IDIV")
            exit(RUNTIME_OPERAND_TYPE_ERR)
        except ZeroDivisionError:
            # division by zero
            if (DEVEL): print(f"ERR: division by zero")
            exit(RUNTIME_DIVISION_BY_ZERO_ERR)
        
        if (DEVEL): print(f"\t\t[dev]: IDIV {value1} / {value2} = {result}")
        if saveTo.type == "var" and self.context.isDefined(saveTo.value):
            self.context.updateVariable(saveTo.value, str(result))
            
class LT(Instruction):
    def doOperation(self):
        if (DEVEL):print(f'\t\t[dev]: {type(self).__name__} instruction in process...')
        self.checkNumberofArguments(3)
        saveTo = self.getArgument("arg1")
        symb1 = self.getArgument("arg2")
        symb2 = self.getArgument("arg3")
        # get types
        symb1Type = self.context.getSymbType(symb1)
        symb2Type = self.context.getSymbType(symb2)
        # compare types
        if symb1Type != symb2Type or symb1Type == "nil":
            exit(RUNTIME_OPERAND_TYPE_ERR)
        # get value
        symb1 = self.context.getSymbValue(symb1)
        symb2 = self.context.getSymbValue(symb2)
        
        # bool to int
        if symb1Type == "bool":
            if symb1 == "true":
                symb1 = 1
            else:
                symb1 = 0
            if symb2 == "true":
                symb2 = 1
            else:
                symb2 = 0
        
        # evaluate value
        if symb1 < symb2:
            if (DEVEL): print(f"\t\t[dev]: LT {symb1} < {symb2} = true")
            result = "true"
        else:
            if (DEVEL): print(f"\t\t[dev]: LT {symb1} < {symb2} = false")
            result = "false"
        # update variable
        self.context.updateVariable(saveTo.value, str(result))
        
class GT(Instruction):
    def doOperation(self):
        if (DEVEL):print(f'\t\t[dev]: {type(self).__name__} instruction in process...')
        self.checkNumberofArguments(3)
        saveTo = self.getArgument("arg1")
        symb1 = self.getArgument("arg2")
        symb2 = self.getArgument("arg3")
        # get types
        symb1Type = self.context.getSymbType(symb1)
        symb2Type = self.context.getSymbType(symb2)
        # compare types
        if symb1Type != symb2Type or symb1Type == "nil":
            exit(RUNTIME_OPERAND_TYPE_ERR)
        # get value
        symb1 = self.context.getSymbValue(symb1)
        symb2 = self.context.getSymbValue(symb2)
        # bool to int
        if symb1Type == "bool":
            if symb1 == "true":
                symb1 = 1
            else:
                symb1 = 0
            if symb2 == "true":
                symb2 = 1
            else:
                symb2 = 0
        # evaluate value
        if symb1 > symb2:
            if (DEVEL): print(f"\t\t[dev]: GT {symb1} > {symb2} = true")
            result = "true"
        else:
            if (DEVEL): print(f"\t\t[dev]: GT {symb1} > {symb2} = false")
            result = "false"
        # update variable
        self.context.updateVariable(saveTo.value, str(result))
        
class EQ(Instruction):
    def doOperation(self):
        if (DEVEL):print(f'\t\t[dev]: {type(self).__name__} instruction in process...')
        self.checkNumberofArguments(3)
        saveTo = self.getArgument("arg1")
        symb1 = self.getArgument("arg2")
        symb2 = self.getArgument("arg3")
        # get types
        symb1Type = self.context.getSymbType(symb1)
        symb2Type = self.context.getSymbType(symb2)
        # get value
        symb1 = self.context.getSymbValue(symb1)
        symb2 = self.context.getSymbValue(symb2)
        # compare types
        if (symb1 == None or symb2 == None) and symb1Type != symb2Type:
            return self.context.updateVariable(saveTo.value, "false")
        if symb1Type != symb2Type:
            exit(RUNTIME_OPERAND_TYPE_ERR)

        # evaluate value
        if str(symb1) == str(symb2):
            if (DEVEL): print(f"\t\t[dev]: EQ {symb1} == {symb2} = true")
            result = "true"
        else:
            if (DEVEL): print(f"\t\t[dev]: EQ {symb1} == {symb2} = false")
            result = "false"
        # update variable
        self.context.updateVariable(saveTo.value, str(result))
        
class AND(Instruction):
    def doOperation(self):
        if (DEVEL):print(f'\t\t[dev]: {type(self).__name__} instruction in process...')
        self.checkNumberofArguments(3)
        saveTo = self.getArgument("arg1")
        symb1 = self.getArgument("arg2")
        symb2 = self.getArgument("arg3")
        # get types
        symb1Type = self.context.getSymbType(symb1)
        symb2Type = self.context.getSymbType(symb2)
        # compare types
        if symb1Type != symb2Type or symb1Type != "bool" or symb2Type != "bool":
            exit(RUNTIME_OPERAND_TYPE_ERR)
        # get value
        symb1 = self.context.getSymbValue(symb1)
        symb2 = self.context.getSymbValue(symb2)
        # evaluate value
        if symb1 == "true" and symb2 == "true":
            result = "true"
        else:
            result = "false"
        # update variable
        self.context.updateVariable(saveTo.value, str(result))
        
class OR(Instruction):
    def doOperation(self):
        if (DEVEL):print(f'\t\t[dev]: {type(self).__name__} instruction in process...')
        self.checkNumberofArguments(3)
        saveTo = self.getArgument("arg1")
        symb1 = self.getArgument("arg2")
        symb2 = self.getArgument("arg3")
        # get types
        symb1Type = self.context.getSymbType(symb1)
        symb2Type = self.context.getSymbType(symb2)
        # compare types
        if symb1Type != symb2Type or symb1Type != "bool" or symb2Type != "bool":
            exit(RUNTIME_OPERAND_TYPE_ERR)
        # get value
        symb1 = self.context.getSymbValue(symb1)
        symb2 = self.context.getSymbValue(symb2)
        # evaluate value
        if symb1 == "true" or symb2 == "true":
            result = "true"
        else:
            result = "false"
        # update variable
        self.context.updateVariable(saveTo.value, str(result))
class NOT(Instruction):
    def doOperation(self):
        if (DEVEL):print(f'\t\t[dev]: {type(self).__name__} instruction in process...')
        self.checkNumberofArguments(2)
        saveTo = self.getArgument("arg1")
        symb1 = self.getArgument("arg2")
        # get type
        symb1Type = self.context.getSymbType(symb1)
        # check type
        if symb1Type != "bool":
            exit(RUNTIME_OPERAND_TYPE_ERR)
        # get value
        symb1 = self.context.getSymbValue(symb1)
        # evaluate value
        if symb1 == "true":
            result = "false"
        else:
            result = "true"
        # update variable
        self.context.updateVariable(saveTo.value, str(result))
class INT2CHAR(Instruction):
    def doOperation(self):
        if (DEVEL):print(f'\t\t[dev]: {type(self).__name__} instruction in process...')
        self.checkNumberofArguments(2)
        saveTo = self.getArgument("arg1")
        symb1 = self.getArgument("arg2")
        # get type
        symb1Type = self.context.getSymbType(symb1)
        if symb1Type != "int":
            exit(RUNTIME_OPERAND_TYPE_ERR)  
        # get value
        symb1 = self.context.getSymbValue(symb1)
        try:
            char = chr(int(symb1))
            self.context.updateVariable(saveTo.value, char)
        except:
            if (DEVEL): print("ERR: Index out of range")
            exit(RUNTIME_STRING_ERR)
        
class STRI2INT(Instruction):
    def doOperation(self):
        if (DEVEL):print(f'\t\t[dev]: {type(self).__name__} instruction in process...')
        self.checkNumberofArguments(3)
        saveTo = self.getArgument("arg1")
        symb1 = self.getArgument("arg2")
        symb2 = self.getArgument("arg3")
        # get types
        symb1Type = self.context.getSymbType(symb1)
        symb2Type = self.context.getSymbType(symb2)
        if symb1Type != "string" or symb2Type != "int":
            exit(RUNTIME_OPERAND_TYPE_ERR)  
        # get character on index
        try:
            index = int(self.context.getSymbValue(symb2))
            char = self.context.getSymbValue(symb1)[index]
            # update variable with character's ASCII code
            self.context.updateVariable(saveTo.value, f"{ord(char)}")
        except:
            if (DEVEL): print("ERR: Index out of range")
            exit(RUNTIME_STRING_ERR)
        
class CONCAT(Instruction):
    def doOperation(self):
        if (DEVEL):print(f'\t\t[dev]: {type(self).__name__} instruction in process...')
        self.checkNumberofArguments(3)
        saveTo = self.getArgument("arg1")
        symb1 = self.getArgument("arg2")
        symb2 = self.getArgument("arg3")
        # check if strings
        symb1Type = self.context.getSymbType(symb1)
        symb2Type = self.context.getSymbType(symb2)
        if symb1Type != "string" or symb2Type != "string":
            exit(RUNTIME_OPERAND_TYPE_ERR)
        # get values
        symb1 = self.context.getSymbValue(symb1)
        symb2 = self.context.getSymbValue(symb2)
        # concatenate & update variable
        result = symb1 + symb2
        self.context.updateVariable(saveTo.value, str(result))
    
class STRLEN(Instruction):
    def doOperation(self):
        if (DEVEL):print(f'\t\t[dev]: {type(self).__name__} instruction in process...')
        self.checkNumberofArguments(2)
        saveTo = self.getArgument("arg1")
        symb1 = self.getArgument("arg2")
        # get type
        symb1Type = self.context.getSymbType(symb1)
        if symb1Type != "string":
            exit(RUNTIME_OPERAND_TYPE_ERR)
        # get value
        symb1 = self.context.getSymbValue(symb1)
        # get length & update variable
        result = len(symb1)
        self.context.updateVariable(saveTo.value, str(result))
        
class GETCHAR(Instruction):
    def doOperation(self):
        if (DEVEL):print(f'\t\t[dev]: {type(self).__name__} instruction in process...')
        self.checkNumberofArguments(3)
        saveTo = self.getArgument("arg1")
        symb1 = self.getArgument("arg2")
        symb2 = self.getArgument("arg3")
        # get types
        symb1Type = self.context.getSymbType(symb1)
        symb2Type = self.context.getSymbType(symb2)
        if symb1Type != "string" or symb2Type != "int":
            exit(RUNTIME_OPERAND_TYPE_ERR)  
        # get character on index
        try:
            index = int(self.context.getSymbValue(symb2))
            char = self.context.getSymbValue(symb1)[index]
            # update variable with character's ASCII code
            self.context.updateVariable(saveTo.value, char)
        except:
            if (DEVEL): print("ERR: Index out of range")
            exit(RUNTIME_STRING_ERR)

class SETCHAR(Instruction):
    def doOperation(self):
        if (DEVEL):print(f'\t\t[dev]: {type(self).__name__} instruction in process...')
        self.checkNumberofArguments(3)
        var = self.getArgument("arg1")
        symb1 = self.getArgument("arg2")
        symb2 = self.getArgument("arg3")
        # get types
        varType = self.context.getSymbType(var)
        symb1Type = self.context.getSymbType(symb1)
        symb2Type = self.context.getSymbType(symb2)
        if varType != 'string' or symb1Type != "int" or symb2Type != "string":
            exit(RUNTIME_OPERAND_TYPE_ERR)
            
        index = int(self.context.getSymbValue(symb1))
        string = self.context.getVariablesValue(var.value)
        # conditions, if empty string
        if self.context.getSymbValue(symb2) == None:
            exit(RUNTIME_STRING_ERR)
        # if index out of range            
        if index < 0 or index > len(string):
            exit(RUNTIME_STRING_ERR)
        # replace char on index
        char = self.context.getSymbValue(symb2)[0]
        string = string[:index] + char + string[index+1:]
        #update variable
        self.context.updateVariable(var.value, string)
        
                
class READ(Instruction):
    def doOperation(self):
        if (DEVEL):print(f'\t\t[dev]: {type(self).__name__} instruction in process...')
        self.checkNumberofArguments(2)
        var = self.getArgument("arg1")
        typeArg = self.getArgument("arg2")
        # check if wanted type is valid
        typeArgType = self.context.getSymbType(typeArg)
        if typeArgType != "type":
            exit(XML_SYNTAX_STRUCTURE_ERR)
        wantedType = self.context.getSymbValue(typeArg)
        # read line from input
        line = self.input.readline().strip()
        # convert to wanted type
        if wantedType == "bool":
            line = line.lower()
            if line != "true" and line != "false":
                line = EMPTY
        elif wantedType == "int":
            if not line.isdigit():
                line = EMPTY
        elif wantedType == "nil":
            if line.lower == "nil":
                line = None
            else:
                line = EMPTY
        elif wantedType == "string":
            pass
        else:
            exit(XML_SYNTAX_STRUCTURE_ERR)
        self.context.updateVariable(self.getArgument("arg1").value, line)
    
class WRITE(Instruction):
    # search for escape sequences and replace them with their values
    def decode_decimalEscape(self,text):
        
        # converts decimal escape sequence to character
        def replace_decimal_escape(match):
            decimal_value = int(match.group(1))
            return chr(decimal_value)

        # replaces decimal escape sequences in the input text
        result = re.sub(r'\\(\d{3})', replace_decimal_escape, text)
        return result
    
    def doOperation(self):
        if (DEVEL):print(f'\t\t[dev]: {type(self).__name__} instruction in process...')
        self.checkNumberofArguments(1)
        symb = self.getArgument("arg1")
        symbValue = self.context.getSymbValue(symb)
        symbType = self.context.getSymbType(symb)
        
        if symbType == "string":
            symbValue = self.decode_decimalEscape(symbValue)
        if symbValue != None:
            print(symbValue, end='')
            
class LABEL(Instruction):
    def doOperation(self):
        if (DEVEL):print(f'\t\t[dev]: {type(self).__name__} instruction in process...')
        self.checkNumberofArguments(1)
        self.context.addLabel(str(self.getArgument("arg1").value), self.context.getInstructionIndex())
        
class JUMP(Instruction):
    def doOperation(self):
        if (DEVEL):print(f'\t\t[dev]: {type(self).__name__} instruction in process...')
        self.checkNumberofArguments(1)
        expectedLabel = self.getArgument("arg1").value
        position = self.context.getLabelPosition(expectedLabel)
        # look for label in instructions going forward
        if position == None:
            self.context.jumpForward(expectedLabel)
        else:
            # label found, set instruction index
            self.context.setInstructionIndex(position)
        
class JUMPIFEQ(Instruction):
    def doOperation(self):
        def makeJump(self, expectedLabel):
            position = self.context.getLabelPosition(expectedLabel)
            if position == None:
                # label not found, look for it in instructions going forward
                self.context.jumpForward(expectedLabel)
                if(DEVEL):print(f'\t\t[dev]: Jumping forward to label {expectedLabel}')
            else:
                self.context.setInstructionIndex(position)
                if(DEVEL):print(f'\t\t[dev]: Jumping back to label {expectedLabel}')
        
        
        if (DEVEL):print(f'\t\t[dev]: {type(self).__name__} instruction in process...')
        self.checkNumberofArguments(3)
        expectedLabel = self.getArgument("arg1").value
        symb1 = self.getArgument("arg2")
        symb2 = self.getArgument("arg3")
        # get types and value
        symb1Type = self.context.getSymbType(symb1)
        symb2Type = self.context.getSymbType(symb2)
        value1 = self.context.getSymbValue(symb1)
        value2 = self.context.getSymbValue(symb2)
        # compare types
        if value1 == None or value2 == None:
            # if one of the operands is nil jump
            return makeJump(self,expectedLabel)
        elif symb1Type != symb2Type:
            if (DEVEL):print(f'\t\t[dev]: {symb1Type} AND {symb2Type} operands are not of the same type')
            exit(RUNTIME_OPERAND_TYPE_ERR)
            
        # check if values are equal
        if str(value1) == str(value2):
            makeJump(self,expectedLabel)
        
            
class JUMPIFNEQ(Instruction):
    def doOperation(self):
        def makeJump(self, expectedLabel):
            position = self.context.getLabelPosition(expectedLabel)
            if position == None:
                # label not found, look for it in instructions going forward
                self.context.jumpForward(expectedLabel)
            else:
                self.context.setInstructionIndex(position)
        
        if (DEVEL):print(f'\t\t[dev]: {type(self).__name__} instruction in process...')
        self.checkNumberofArguments(3)
        expectedLabel = self.getArgument("arg1").value
        symb1 = self.getArgument("arg2")
        symb2 = self.getArgument("arg3")
        # get types
        symb1Type = self.context.getSymbType(symb1)
        symb2Type = self.context.getSymbType(symb2)
        # compare types
        value1 = self.context.getSymbValue(symb1)
        value2 = self.context.getSymbValue(symb2)
        
        # compare types
        if value1 == None or value2 == None:
            # if one of the operands is nil jump
            return makeJump(self,expectedLabel)
        elif symb1Type != symb2Type:
            exit(RUNTIME_OPERAND_TYPE_ERR)
                    
        # check if values are equal
        if str(value1) != str(value2):
            makeJump(self,expectedLabel)
            
class EXIT(Instruction):
    def doOperation(self):
        if (DEVEL):print(f'\t\t[dev]: {type(self).__name__} instruction in process...')
        self.checkNumberofArguments(1)
        if self.getArgument("arg1").type == "int":
            if int(self.getArgument("arg1").value) >= 0 and int(self.getArgument("arg1").value) <= 49:
                exit(int(self.getArgument("arg1").value))
            else:
                exit(RUNTIME_WRONG_OPERAND_VALUE_ERR)
        else:
            exit(RUNTIME_OPERAND_TYPE_ERR)
    
class DPRINT(Instruction):
    def doOperation(self):
        if (DEVEL):print(f'\t\t[dev]: {type(self).__name__} instruction in process...')
        print(self.getArgument("arg1").value, end='',file=sys.stderr)
        
class BREAK(Instruction):
    def doOperation(self):
        if (DEVEL):print(f'\t\t[dev]: {type(self).__name__} instruction in process...')
        self.checkNumberofArguments(0)
        print(self.context,end='',file=sys.stderr)
class TYPE(Instruction):
    def doOperation(self):
        if (DEVEL):print(f'\t\t[dev]: {type(self).__name__} instruction in process...')
        self.checkNumberofArguments(2)
        var = self.getArgument("arg1")
        symb = self.getArgument("arg2")
        symbType = self.context.getSymbType(symb)
        self.context.updateVariable(var.value,symbType)
                  

# Factory method for instruction
# Creates instruction class based on the input
class InstructionFactory:
    def __init__(self, context):
        self.input = None
        self.context = context
        
    def setInput(self,input):
        self.input = input
    
    def getInput(self):
        return self.input
    
    def createInstruction(self,instruction):
        instruction = instruction.upper()
        if instruction == 'MOVE':
            return MOVE(self.context)
        elif instruction == 'CREATEFRAME':
            return CREATEFRAME(self.context)
        elif instruction == 'PUSHFRAME':
            return PUSHFRAME(self.context)
        elif instruction == 'POPFRAME':
            return POPFRAME(self.context)
        elif instruction == 'DEFVAR':
            return DEFVAR(self.context)
        elif instruction == 'CALL':
            return CALL(self.context)
        elif instruction == 'RETURN':
            return RETURN(self.context)
        elif instruction == 'PUSHS':
            return PUSHS(self.context)
        elif instruction == 'POPS':
            return POPS(self.context)
        elif instruction == 'ADD':
            return ADD(self.context)
        elif instruction == 'SUB':
            return SUB(self.context)
        elif instruction == 'MUL':
            return MUL(self.context)
        elif instruction == 'IDIV':
            return IDIV(self.context)
        elif instruction == 'LT':
            return LT(self.context)
        elif instruction == 'GT':
            return GT(self.context)
        elif instruction == 'EQ':
            return EQ(self.context)
        elif instruction == 'AND':
            return AND(self.context)
        elif instruction == 'OR':
            return OR(self.context)
        elif instruction == 'NOT':
            return NOT(self.context)
        elif instruction == 'INT2CHAR':
            return INT2CHAR(self.context)
        elif instruction == 'STRI2INT':
            return STRI2INT(self.context)
        elif instruction == 'READ':
            return READ(self.context, self.getInput())
        elif instruction == 'WRITE':
            return WRITE(self.context)
        elif instruction == 'CONCAT':
            return CONCAT(self.context)
        elif instruction == 'STRLEN':
            return STRLEN(self.context)
        elif instruction == 'GETCHAR':
            return GETCHAR(self.context)
        elif instruction == 'SETCHAR':
            return SETCHAR(self.context)
        elif instruction == 'WRITE':
            return WRITE(self.context)
        elif instruction == 'LABEL':
            return LABEL(self.context)
        elif instruction == 'JUMP':
            return JUMP(self.context)
        elif instruction == 'JUMPIFEQ':
            return JUMPIFEQ(self.context)
        elif instruction == 'JUMPIFNEQ':
            return JUMPIFNEQ(self.context)
        elif instruction == 'EXIT':
            return EXIT(self.context)
        elif instruction == 'DPRINT':
            return DPRINT(self.context)
        elif instruction == 'BREAK':
            return BREAK(self.context)
        elif instruction == 'TYPE':
            return TYPE(self.context)
        else:
            print("ERR: Instruction not found")
            exit(XML_SYNTAX_STRUCTURE_ERR)

class Parser:
    # constructor
    def __init__(self,context):
        # check number of arguments
        if len(sys.argv) == 4 and sys.argv[3] == '--testerfester':
            self.test = True 
        elif not(len(sys.argv) == 2 or len(sys.argv) == 3):
            print("ERR: Invalid number of arguments")
            exit(PARAMETER_ERR)
        self.source = None
        self.input = None
        self.rootList = None # list of root elements(Instructions)
        self.context = context
        self.lastInstructionnumber = 0 # order number of tha latest instruction to catch duplicits
        self.instructionFactory = InstructionFactory( context)

    # print usage
    def usage(self):
        print("This is a Python script (interpret.py) that interprets an input XML representation of a program and generates output based on the command line parameters. The input XML representation is more loosely defined than the XML generated by the parse.php script, but it is assumed that it does not contain errors. The script supports optional documentation text attributes and various formatted tags. The program's instructions are described in section 5 and are interpreted in ascending order based on the order attribute.\n\nThe script has three parameters:\n--help (common to all scripts),\n--source=file (input file with XML representation of source code),\n--input=file (file with inputs for program interpretation).\n`At least one parameter (--source or --input) must be specified. If one is missing, the data is read from standard input.")
        exit(0)

    def parseArgument(self, argument):
        argExploded = argument.split('=')
        # expect format --source=file or --input=file
        if(len(argExploded) != 2):
            if(argExploded[0] == '--help'):
                self.usage()
            print("ERR: Invalid parameter")
            exit(PARAMETER_ERR)
        # open file
        if(DEVEL):print(f'\t\t[dev]: opening file ... {argExploded[1]}')
        try:
            file = open(argExploded[1], 'r')
        except FileNotFoundError:
            print("ERR: Could not open file.")
            exit(IN_FILE_ERR)
            
        # assign file to stream
        if(argExploded[0] == '--source' and self.source == None):
            if(DEVEL):print('\t\t[dev]: setting up source filestream ... ')
            self.source = file.read()
            file.close()
        elif(argExploded[0] == '--input' and self.input == None): 
            if(DEVEL):print('\t\t[dev]: setting up input filestream ... ')
            self.input = file
        else:
            print("ERR: Invalid parameter. 1")
            print(argExploded[0])
            exit(PARAMETER_ERR)
        # close file after reading

    # open input streams for source and input file from the arguments
    def openStream(self):
        # number of arguments checked in the init
        self.parseArgument(sys.argv[1])
        if(len(sys.argv) == 3):
            # every file was specified
            self.parseArgument(sys.argv[2])
        else:
            # if no input/source file is specified, read from stdin
            if(self.source == None):
                self.source = sys.stdin.read()
            else:
                self.input = sys.stdin
        # get the whole structure of the XML file
        try:
            self.rootList = ET.fromstring(self.source)
        except ET.ParseError as e:
            print(f"Error parsing well-formed XML: {e}")
            exit(XML_SYNTAX_ERR)
        
        self.instructionFactory.setInput(self.input)
        #order the instructions by their order attribute
        try:
            self.rootList = sorted(self.rootList, key=lambda child: int(child.attrib['order']))
        except :
            if DEVEL: print("ERR: Instruction attribute order error")
            exit(XML_SYNTAX_STRUCTURE_ERR)
            
    def closeStream(self):
        self.input.close()
        
    # parses XML element (with closing tag) and creates instruction/argument object
    def parseXMLElement(self, element):
        attributes = {}
        # check if the element is an instruction
        if element.tag == 'instruction':
            try:
                attributes["opcode"] = element.attrib['opcode']
                attributes["order"] = element.attrib['order']
            except KeyError:
                if(DEVEL):print(f'\t\t[dev]: {element.tag} element is missing attribute')
                exit(XML_SYNTAX_STRUCTURE_ERR)
            return ("instruction", attributes)
        
        # check if the element is an argument
        elif element.tag in ['arg1', 'arg2', 'arg3']:
            try:
                attributes["tag"] = element.tag 
                attributes["type"] = element.attrib['type']
                attributes["content"] = element.text
            except KeyError:
                if(DEVEL):print(f'\t\t[dev]: {element.tag} element is missing attribute')
                exit(XML_SYNTAX_STRUCTURE_ERR)
            return ("argument", attributes)
        else:
            exit(XML_SYNTAX_STRUCTURE_ERR)
            
    # gets every argument (child element) from the instruction (root) element and adds them to the instruction
    def getArguments(self,instructionElement,instructionInstance):
        if instructionElement.findall("./*") is not None:
            for argument in instructionElement.findall('./*'):
                elementType, elementData = self.parseXMLElement(argument)
                if elementType == "argument":
                    # create argument object
                    argument = self._createArgument(elementData["tag"],elementData["type"], elementData["content"])
                    instructionInstance.addArgument(argument)
                else:
                    # if the element is not an argument, it is an error in the XML syntax
                    exit(XML_SYNTAX_ERR)
                    
    # searches for the next instruction LABEL in the source code
    # return true if successful or false
    def getNextLabel(self):
        while self.context.getInstructionIndex() < len(self.rootList):
            # if any label is found, add it to labels
            instruction = self.getInstruction()
            if  type(instruction).__name__ == "LABEL":
                # create label 
                instruction.doOperation()
                return True
        return False
    
    # returns instruction or argument object or none
    # expects correct syntax
    def getInstruction(self):
        if self.context.getInstructionIndex() >= len(self.rootList):
            return None
        
        #parse XML element
        rootElement = self.rootList[self.context.getInstructionIndex()]
        elementData = self.parseXMLElement(rootElement)
        
        #root must be instruction
        elementType, elementData = elementData
        if elementType == "instruction":
            instruction = self._createInstruction(elementData)
            
            # get arguments
            self.getArguments(rootElement,instruction)
            return instruction
        else:
            print("ERR: Unknown root element encountered:")
            exit(XML_SYNTAX_ERR)
        
    # creates instruction object
    # checks if the order of the instructions is correct
    def _createInstruction(self, instructiontData):
        if(DEVEL):print(f'\t\t[dev]: {instructiontData["order"]} creating instruction {instructiontData["opcode"]} ... ')
        self.context.incrementInstructionIndex()
        # check if the order of the instructions is correct and if there are no duplicit orders
        if self.lastInstructionnumber >= int(instructiontData['order']):
            print("ERR: Invalid order of instructions")
            exit(XML_SYNTAX_STRUCTURE_ERR)
        else:
            self.lastInstructionnumber = int(instructiontData['order'])

        return self.instructionFactory.createInstruction(instructiontData['opcode'])
        

    # creates argument object
    def _createArgument(self, tag, type, value):
        if value is not None:
            value = value.strip()
        else:
            value = EMPTY
        if(DEVEL):print('\t\t[dev]: \t\tcreating Argument ... ')
        if(type == 'nil'):
            # value of nil is represented as None
            return Argument(tag, type, None)
        else:
            return Argument(tag, type, str(value))
        

def main():
    context = Context()
    parser = Parser(context)
    context.setParser(parser)
    parser.openStream()
    while True:
        instruction = parser.getInstruction()
        # no more instructions
        if instruction is None:
            break
        instruction.doOperation()
        
    parser.closeStream()
    return 0

if __name__ == '__main__':
    main()
    