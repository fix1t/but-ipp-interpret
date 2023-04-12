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

DEVEL = 0

class Context:
    def __init__(self):
        self.localFrame = {}
        self.globalFrame = {}
        self.temporaryFrame = {}
        self.labels = {}
        self.stack = []
        self.instructionIndex = 0 
        self.parser = None
        
    def __repr__(self):
        return f"<context(localFrame={self.localFrame}, globalFrame={self.globalFrame}, temporaryFrame={self.temporaryFrame})>"
    
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
    
    def setParser(self, parser):
        self.parser = parser
    
    def getInstructionIndex(self):
        return self.instructionIndex
    
    def incrementInstructionIndex(self):
        self.instructionIndex += 1
    
    def setInstructionIndex(self, index):
        self.parser.lastInstructionnumber = 0
        self.instructionIndex = index
    
    def addLabel(self,label,position):
        if label not in self.labels:
            self.labels[label] = position
        else:
            if(DEVEL == 1): print(f"[dev]: Label {label} is already defined")
            exit(MULTIPLE_DEFINITION_ERR)
            
    def getLabelPosition(self,label):
        if label in self.labels:
            return self.labels[label]
        else:
            if(DEVEL == 1): print(f"[dev]: Label {label} is not defined")
            return None
    
    def pushStack(self,value):
        self.stack.append(value)
        
    def popStack(self):
        if len(self.stack) == 0:
            if(DEVEL == 1): print(f"[dev]: Stack is empty")
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
            if(DEVEL == 1): print(f"[dev]: Variable {variable} is not defined")
            exit(RUNTIME_VARIABLE_ERR)
        
    def isDefined(self,variable):
        frame , variable = self.splitVariable(variable)
        frame = self.getFrame(frame)
        if variable in frame:
            return True
        else:
            return False
    
    def getSymbValue(self,symbol):
        if symbol.type == "var" and self.isDefined(symbol.value):
            return self.getVariablesValue(symbol.value)
        else:
            return symbol.value
    
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
            exit(XML_SYNTAX_STRUCTURE_ERR)
    
    def doOperation(self):
        pass
    
    def addArgument(self,argument):
        self.argumentList[argument.tag] =argument
        
    def __repr__(self):
        return f"<instruction({type(self).__name__})>"

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
        self.checkNumberofArguments(1)
        if self.argumentList["arg1"].type == "var":
            varValue = self.context.getVariablesValue(self.argumentList["arg1"].value)
            self.context.pushStack(varValue)
        else:
            self.context.pushStack(self.argumentList["arg1"].value)
        
class POPS(Instruction):
    def doOperation(self):
        self.checkNumberofArguments(1)
        var = self.argumentList["arg1"]
        if var.type == "var" and self.context.isDefined(var.value):
            poppedValue = self.context.popStack()
            self.context.updateVariable(var.value, poppedValue)
        
class ADD(Instruction):
    def doOperation(self):
        self.checkNumberofArguments(3)
        saveTo = self.argumentList["arg1"]
        symb1 = self.argumentList["arg2"]
        symb2 = self.argumentList["arg3"]
        value1 = self.context.getSymbValue(symb1)
        value2 = self.context.getSymbValue(symb2)
        result = int(value1) + int(value2)
        if (DEVEL): print(f"[dev]: ADD {value1} + {value2} = {result}")
        if saveTo.type == "var" and self.context.isDefined(saveTo.value):
            self.context.updateVariable(saveTo.value, result)
        
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
        self.checkNumberofArguments(2)
        var = self.argumentList["arg1"]
        symbol = self.argumentList["arg2"]
        # confirm that first argument is variable
        if var.type == "var" and self.context.isDefined(var.value):
            # if second argument is variable, get its value
            if symbol.type == "var" and self.context.isDefined(symbol.value):
                value = self.context.getVariablesValue(symbol.value)
            else:
                value = symbol.value
            try:
                value = int(value)
                self.context.updateVariable(var.value, chr(value))
            except :
                exit(RUNTIME_WRONG_OPERAND_VALUE_ERR)
        else:
            exit(RUNTIME_WRONG_OPERAND_VALUE_ERR)
        
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
    # search for escape sequences and replace them with their values
    def decode_decimal_escape(self,text):
        
        # converts decimal escape sequence to character
        def replace_decimal_escape(match):
            decimal_value = int(match.group(1))
            return chr(decimal_value)

        # replaces decimal escape sequences in the input text
        result = re.sub(r'\\(\d{3})', replace_decimal_escape, text)
        return result
    
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
            text = self.argumentList["arg1"].value
            text = self.decode_decimal_escape(text)
            print(text, end='')
            
class LABEL(Instruction):
    def doOperation(self):
        self.checkNumberofArguments(1)
        self.context.addLabel(str(self.argumentList["arg1"].value), self.context.getInstructionIndex())
        
class JUMP(Instruction):
    def doOperation(self):
        self.checkNumberofArguments(1)
        expectedLabel = self.argumentList["arg1"].value
        position = self.context.getLabelPosition(expectedLabel)
        # look for label in instructions going forward
        if position == None:
            self.context.jumpForward(expectedLabel)
        else:
            # label found, set instruction index
            self.context.setInstructionIndex(position)
        
class JUMPIFEQ(Instruction):
    def doOperation(self):
        self.checkNumberofArguments(3)
        expectedLabel = self.argumentList["arg1"].value
        symb1 = self.argumentList["arg2"]
        symb2 = self.argumentList["arg3"]
        
        value1 = self.context.getSymbValue(symb1)
        value2 = self.context.getSymbValue(symb2)
            
        # check if values are equal
        if str(value1) == str(value2):
            # get label
            position = self.context.getLabelPosition(expectedLabel)
            if position == None:
                # label not found, look for it in instructions going forward
                self.context.jumpForward(expectedLabel)
            else:
                self.context.setInstructionIndex(position)
        
            
class JUMPIFNEQ(Instruction):
    def doOperation(self):
        self.checkNumberofArguments(3)
        expectedLabel = self.argumentList["arg1"].value
        symb1 = self.argumentList["arg2"]
        symb2 = self.argumentList["arg3"]
        
        value1 = self.context.getSymbValue(symb1)
        value2 = self.context.getSymbValue(symb2)
            
        # check if values are equal
        if str(value1) != str(value2):
            # get label
            position = self.context.getLabelPosition(expectedLabel)
            if position == None:
                # label not found, look for it in instructions going forward
                self.context.jumpForward(expectedLabel)
            else:
                self.context.setInstructionIndex(position)
class EXIT(Instruction):
    def doOperation(self):
        self.checkNumberofArguments(1)
        if self.argumentList["arg1"].type == "int" and int(self.argumentList["arg1"].value) < 50:
            exit(int(self.argumentList["arg1"].value))
        else:
            exit(RUNTIME_WRONG_OPERAND_VALUE_ERR)
class DPRINT(Instruction):
    def doOperation(self):
        print(self.argumentList["arg1"].value, end='',file=sys.stderr)
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
    def __init__(self, parser,context):
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
        if not(len(sys.argv) == 2 or len(sys.argv) == 3):
            print("ERR: Invalid number of arguments")
            exit(PARAMETER_ERR)
        self.source = None
        self.input = None
        self.rootList = None # list of root elements(Instructions)
        self.context = context
        self.lastInstructionnumber = 0 # order number of tha latest instruction to catch duplicits
        self.instructionFactory = InstructionFactory(self, context)

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
            exit(XML_SYNTAX_STRUCTURE_ERR)
            
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
        if(DEVEL):print(f'[dev]: {instructiontData["order"]} creating instruction {instructiontData["opcode"]} ... ')
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
        if(DEVEL):print('[dev]: \t\tcreating Argument ... ')
        return Argument(tag, type, value)
        

def main():
    context = Context()
    parser = Parser(context)
    context.setParser(parser)
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
    