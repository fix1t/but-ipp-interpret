import sys #arguments
import xml.etree.ElementTree as ET #xml parsing

SYNTAX_ERR = -1
PARAMETER_ERR = 10
IN_FILE_ERR = 11
XML_SYNTAX_ERR = 31
XML_SYNTAX_STRUCTURE_ERR = 32
SEMANTIC_ERR = 52
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

DEVEL = 1

class Context:
    def __init__(self):
        self.localFrame = {}
        self.globalFrame = {}
        self.temporaryFrame = {}
        
    def __repr__(self):
        return f"<context(localFrame={self.localFrame}, globalFrame={self.globalFrame}, temporaryFrame={self.temporaryFrame})>"
    
    def splitVariable(self,variable):
        if variable[0] == "G" and variable[1] == "F":
            return "GF", variable[3:]
        elif variable[0] == "L" and variable[1] == "F":
            return "LF", variable[3:]
        elif variable[0] == "T" and variable[1] == "F":
            return "TF", variable[3:]
        else:
            if(DEVEL == 1): print(f"[dev]: Variable {variable} is not defined")
            exit(RUNTIME_VARIABLE_ERR)
        
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
            if(DEVEL == 1): print(f"[dev]: Variable {variable} is not defined 1")
            exit(RUNTIME_VARIABLE_ERR)
                
    def updateVariable(self,variable,value):
        if self.isDefined(variable):
            frame , variable = self.splitVariable(variable)
            frame = self.getFrame(frame)
            frame[variable] = value
            return True
        else:
            if(DEVEL == 1): print(f"[dev]: Variable {variable} is not defined 2")
            exit(RUNTIME_VARIABLE_ERR)
            
    def getVariablesValue(self,variable):
        if self.isDefined(variable):
            frame , variable = self.splitVariable(variable)
            frame = self.getFrame(frame)
            return frame[variable]
        else:
            if(DEVEL == 1): print(f"[dev]: Variable {variable} is not defined 3")
            exit(RUNTIME_VARIABLE_ERR)
            
    def createFrame(self):
        self.temporaryFrame = []
        
    def pushFrame(self):
        self.localFrame = self.temporaryFrame
        self.temporaryFrame = []

    def popFrame(self):
        self.temporaryFrame = self.localFrame
        self.localFrame = []
        
    def getFrame(self,frame):
        if frame == "GF":
            return self.globalFrame
        elif frame == "LF":
            return self.localFrame
        elif frame == "TF":
            return self.temporaryFrame
        else:
            exit(RUNTIME_FRAME_ERR)

class Argument:
    def __init__(self, tag, type, value):
        if(type != "var" and type != "symb" and type != "label" and type != "type" and\
            type != "nil" and type != "bool" and type != "int" and type != "string" and\
                type != "float" and type != "LF" and type != "GF" and type != "TF"):
            exit(PARAMETER_ERR)
        if(DEVEL == 1): print(f"[dev]: Argument created:{tag} {type} {value}")
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
            exit(SYNTAX_ERR)
    
    def doOperation(self):
        pass
    
    def addArgument(self,argument):
        self.argumentList[argument.tag] =argument
        
    def __repr__(self):
        return f"<instruction({type(self)})>"

class MOVE(Instruction):
    def doOperation(self):
        self.checkNumberofArguments(2)
        variable = self.argumentList["arg1"]
        symbol = self.argumentList["arg2"]
        if symbol.type == "var":
            varValue = self.context.getVariablesValue(symbol.value)
            self.context.updateVariable(variable.value, varValue)
        else:
            self.context.updateVariable(variable.value,symbol.value)
        
class CREATEFRAME(Instruction):
    def doOperation(self):
        pass
class PUSHFRAME(Instruction):
    def doOperation(self):
        pass
class POPFRAME(Instruction):
    def doOperation(self):
        pass
class DEFVAR(Instruction):
    def doOperation(self):
        self.checkNumberofArguments(1)
        self.context.createVariable(self.argumentList["arg1"].value)
class CALL(Instruction):
    def doOperation(self):
        pass
class RETURN(Instruction):
    def doOperation(self):
        pass
class PUSHS(Instruction):
    def doOperation(self):
        pass
class POPS(Instruction):
    def doOperation(self):
        pass
class ADD(Instruction):
    def doOperation(self):
        pass
class SUB(Instruction):
    def doOperation(self):
        pass
class MUL(Instruction):
    def doOperation(self):
        pass
class IDIV(Instruction):
    def doOperation(self):
        pass
class LT(Instruction):
    def doOperation(self):
        pass
class GT(Instruction):
    def doOperation(self):
        pass
class EQE(Instruction):
    def doOperation(self):
        pass
class AND(Instruction):
    def doOperation(self):
        pass
class OR(Instruction):
    def doOperation(self):
        pass
class NOT(Instruction):
    def doOperation(self):
        pass
class INT2CHAR(Instruction):
    def doOperation(self):
        pass
class STRI2INT(Instruction):
    def doOperation(self):
        pass
class READ(Instruction):
    def doOperation(self):
        self.checkNumberofArguments(2)
        var = self.argumentList["arg1"].value
        wantedType = self.argumentList["arg2"].value
        # read line from input
        line = self.input.readline()
        line = line.rstrip('\n')
        # convert to wanted type
        if wantedType == "bool":
            if line.lower == "true":
                line = "true"
            elif line.lower == "false":
                line = "false"
        elif wantedType == "int":
            line = int(line)
        elif wantedType == "string":
            pass
        self.context.updateVariable(self.argumentList["arg1"].value, line)
    
class WRITE(Instruction):
    def doOperation(self):
        self.checkNumberofArguments(1)
        if self.argumentList["arg1"].type == "var":
            print(self.context.getVariablesValue(self.argumentList["arg1"].value), end='')
            
        elif self.argumentList["arg1"].type == "nil":
            pass #TODO
        
        elif self.argumentList["arg1"].type == "bool":
            if (self.argumentList["arg1"].type == "true"):
                print("true", end='')
            else:
                print("false", end='')
        else:
            print(self.argumentList["arg1"].value, end='')
            
class LABEL(Instruction):
    def doOperation(self):
        pass
class JUMP(Instruction):
    def doOperation(self):
        pass
class JUMPIFEQ(Instruction):
    def doOperation(self):
        pass
class JUMPIFNEQ(Instruction):
    def doOperation(self):
        pass
class EXIT(Instruction):
    def doOperation(self):
        self.checkNumberofArguments(1)
        if self.argumentList["arg1"].type == "int" and int(self.argumentList["arg1"].value) < 50:
            exit(int(self.argumentList["arg1"].value))
        else:
            exit(RUNTIME_WRONG_OPERAND_VALUE_ERR)
class DRPINT(Instruction):
    def doOperation(self):
        pass
class BREAK(Instruction):
    def doOperation(self):
        pass
class TYPE(Instruction):
    def doOperation(self):
        self.checkNumberofArguments(2)
        var = self.argumentList["arg1"]
        symb = self.argumentList["arg2"]
        # first argument must be variable
        if var.type == "var":
            # if symbol is variable
            if symb.type == "var":
                # not initialized variable
                if self.context.getVariablesValue(symb.value) == "":
                    return self.context.updateVariable(var.value, "")
                # initialized variable, get its type
                else:
                    dataType = type(symb.value).__name__
                    if(dataType == "str"):
                        dataType = "string"
                    return self.context.updateVariable(var.value, dataType)
            else:
                return self.context.updateVariable(var.value, symb.type)
        else:
            exit(RUNTIME_WRONG_OPERAND_VALUE_ERR)
                  

# Factory method for instruction
# Creates instruction class based on the input
class InstructionFactory:
    def __init__(self,context):
        self.input = None
        self.context = context
        
    def setInput(self,input):
        self.input = input
    
    def getInput(self):
        return self.input
    
    def createInstruction(self,instruction):
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
        elif instruction == 'EQE':
            return EQE(self.context)
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
        elif instruction == 'DRPINT':
            return DRPINT(self.context)
        elif instruction == 'BREAK':
            return BREAK(self.context)
        elif instruction == 'TYPE':
            return TYPE(self.context)
        else:
            print("ERR: Instruction not found")
            exit(SYNTAX_ERR)

class Parser:
    # constructor
    def __init__(self):
        # check number of arguments
        if not(len(sys.argv) == 2 or len(sys.argv) == 3):
            print("ERR: Invalid number of arguments")
            exit(PARAMETER_ERR)
        self.source = None
        self.input = None
        self.rootList = None # list of root elements(Instructions)
        self.instructionNum = 0 
        self.lastInstructionnumber = 0 # order number of tha latest instruction to catch duplicits
        self.instructionFactory = InstructionFactory(Context())

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
        if(DEVEL):print(f'[dev]: opening file ... {argExploded[1]}')
        try:
            file = open(argExploded[1], 'r')
        except FileNotFoundError:
            print("ERR: Could not open file.")
            exit(IN_FILE_ERR)
            
        # assign file to stream
        if(argExploded[0] == '--source' and self.source == None):
            if(DEVEL):print('[dev]: setting up source filestream ... ')
            self.source = file.read()
            file.close()
        elif(argExploded[0] == '--input' and self.input == None): 
            if(DEVEL):print('[dev]: setting up input filestream ... ')
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
            self.parseArgument(sys.argv[2])
        else:
            # if no input/source file is specified, read from stdin
            if(self.source == None):
                self.source = sys.stdin.read()
            else:
                self.input = sys.stdin.open()
        # get the whole structure of the XML file
        try:
            self.rootList = ET.fromstring(self.source)
        except ET.ParseError as e:
            print(f"Error parsing well-formed XML: {e}")
            exit(XML_SYNTAX_ERR)
        
        self.instructionFactory.setInput(self.input)
        #order the instructions by their order attribute
        self.rootList = sorted(self.rootList, key=lambda child: int(child.attrib['order']))
        
    def closeStream(self):
        self.input.close()
        
    # parses XML element (with closing tag) and creates instruction/argument object
    def parseXMLElement(self, element):
        attributes = {}
        if element.tag == 'instruction':
            attributes["opcode"] = element.attrib['opcode']
            attributes["order"] = element.attrib['order']
            return ("instruction", attributes)
        elif element.tag in ['arg1', 'arg2', 'arg3']:
            attributes["tag"] = element.tag 
            attributes["type"] = element.attrib['type']
            attributes["content"] = element.text
            return ("argument", attributes)
        else:
            exit(XML_SYNTAX_ERR)
            
    # gets every argument (child element) from the instruction (root) element and adds them to the instruction
    def getArguments(self,instructionElement,instructionInstance):
        if instructionElement.findall("./*") is not None:
            for argument in instructionElement.findall('./*'):
                element_data = self.parseXMLElement(argument)
                element_type, element_data = element_data
                if element_type == "argument":
                    # create argument object
                    argument = self._createArgument(element_data["tag"],element_data["type"], element_data["content"])
                    instructionInstance.addArgument(argument)
                else:
                    exit(XML_SYNTAX_ERR)
    
    # returns instruction or argument object or none
    # expects correct syntax
    def getInstruction(self):
        if self.instructionNum >= len(self.rootList):
            return None
        
        #parse XML element
        rootElement = self.rootList[self.instructionNum]
        elementData = self.parseXMLElement(rootElement)
        
        #root must be instruction
        element_type, elementData = elementData
        if element_type == "instruction":
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
        if(DEVEL):print(f'[dev]: creating instruction {instructiontData["opcode"]} ... ')
        self.instructionNum += 1
        # check if the order of the instructions is correct and if there are no duplicit orders
        if self.lastInstructionnumber >= int(instructiontData['order']):
            print("ERR: Invalid order of instructions")
            exit(XML_SYNTAX_STRUCTURE_ERR)
        else:
            self.lastInstructionnumber = int(instructiontData['order'])

        return self.instructionFactory.createInstruction(instructiontData['opcode'])
        

    # creates argument object
    def _createArgument(self, tag, type, value):
        if(DEVEL):print('[dev]: \t\tcreating Argument ... ')
        return Argument(tag, type, value)
        

def main():
    parser = Parser()
    parser.openStream()
    while True:
        instruction = parser.getInstruction()
        if instruction is None:
            break
        instruction.doOperation()
        
    parser.closeStream()
    return 0

if __name__ == '__main__':
    main()
    