import sys #arguments
import xml.etree.ElementTree as ET #xml parsing

# source format
# <?xml version="1.0" encoding="UTF-8"?>
# <program language="IPPcode23">
#     <instruction order="1" opcode="DEFVAR">
#         <arg1 type="var">
#             GF@a
#         </arg1>
#     </instruction>
#     <instruction order="2" opcode="READ">
#         <arg1 type="var">
#             GF@a
#         </arg1>
#         <arg2 type="type">
#             int
#         </arg2>
#     </instruction>
#     <instruction order="3" opcode="WRITE">
#         <arg1 type="var"> 
#             GF@a
#         </arg1>
#     </instruction>
#     <instruction order="4" opcode="WRITE">
#         <arg1 type="string"> 
#             \032&lt;not-tag/&gt;\032
#         </arg1>
#     </instruction>
#     <instruction order="5" opcode="WRITE">
#         <arg1 type="bool"> 
#             true
#         </arg1>
#     </instruction>
# </program>


PARAMETER_ERR = 10
IN_FILE_ERR = 11
SEMANTIC_ERR = 52
DEVEL = 1

class Instruction():
    argumentList = []
    def doOperation(self):
        pass
    def addArgument(self,argument):
        self.argumentList.append(argument)

class MOVE(Instruction):
    def doOperation(self):
        pass
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
        pass
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
        pass
class WRITE(Instruction):
    def doOperation(self):
        pass
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
        pass
class DRPINT(Instruction):
    def doOperation(self):
        pass
class BREAK(Instruction):
    def doOperation(self):
        pass

# Factory method for instruction
# Creates instruction class based on the input
class InstructionFactory:
    def createInstruction(self,instruction):
        if instruction == 'MOVE':
            return MOVE()
        elif instruction == 'CREATEFRAME':
            return CREATEFRAME()
        elif instruction == 'PUSHFRAME':
            return PUSHFRAME()
        elif instruction == 'POPFRAME':
            return POPFRAME()
        elif instruction == 'DEFVAR':
            return DEFVAR()
        elif instruction == 'CALL':
            return CALL()
        elif instruction == 'RETURN':
            return RETURN()
        elif instruction == 'PUSHS':
            return PUSHS()
        elif instruction == 'POPS':
            return POPS()
        elif instruction == 'ADD':
            return ADD()
        elif instruction == 'SUB':
            return SUB()
        elif instruction == 'MUL':
            return MUL()
        elif instruction == 'IDIV':
            return IDIV()
        elif instruction == 'LT':
            return LT()
        elif instruction == 'GT':
            return GT()
        elif instruction == 'EQE':
            return EQE()
        elif instruction == 'AND':
            return AND()
        elif instruction == 'OR':
            return OR()
        elif instruction == 'NOT':
            return NOT()
        elif instruction == 'INT2CHAR':
            return INT2CHAR()
        elif instruction == 'STRI2INT':
            return STRI2INT()
        elif instruction == 'READ':
            return READ()
        elif instruction == 'WRITE':
            return WRITE()
        elif instruction == 'LABEL':
            return LABEL()
        elif instruction == 'JUMP':
            return JUMP()
        elif instruction == 'JUMPIFEQ':
            return JUMPIFEQ()
        elif instruction == 'JUMPIFNEQ':
            return JUMPIFNEQ()
        elif instruction == 'EXIT':
            return EXIT()
        elif instruction == 'DRPINT':
            return DRPINT()
        elif instruction == 'BREAK':
            return BREAK()

class Parser:
    # constructor
    def __init__(self):
        self.source = None
        self.input = None
        self.instructionNum = 0
        self.list = []
        # check number of arguments
        if not(len(sys.argv) == 2 or len(sys.argv) == 3):
            print("ERR: Invalid number of arguments")
            exit(PARAMETER_ERR)

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
        try:
            file = open(argExploded[1], 'r')
        except FileNotFoundError:
            print("ERR: Could not open file.")
            exit(IN_FILE_ERR)
        # assign file to stream
        if(argExploded[0] == '--source' and self.source == None):
            if(DEVEL):print('[dev]: setting up source filestream ... ')
            self.source = file
        elif(argExploded[0] == '--input' and self.input == None): 
            if(DEVEL):print('[dev]: setting up input filestream ... ')
            self.input = file
        else:
            print("ERR: Invalid parameter. 1")
            print(argExploded[0])
            exit(PARAMETER_ERR)

    # open input streams for source and input file from the arguments
    def openStream(self):
        # number of arguments checked in the init
        self.parseArgument(sys.argv[1])
        if(len(sys.argv) == 3):
            self.parseArgument(sys.argv[2])
        else:
            # if no input/source file is specified, read from stdin
            if(self.source == None):
                self.source = sys.stdin
            else:
                self.input = sys.stdin
        
    def closeStream(self):
        if(self.input != None):
            if(DEVEL):print('[dev]: closing input filestream ... ')
            self.input.close()
        if(self.source != None):
            if(DEVEL):print('[dev]: closing source filestream ... ')
            self.source.close()
        
    # sheds the first lines of the source file until the first instruction is found
    def start(self):
        if(DEVEL):print('[dev]: starting ... ')
        # shed the first lines until program tag is found
        line = self.source.readline()
        root = ET.fromstring(line)
        while root.tag != 'program':
            line = self.source.readline()
            root = ET.fromstring(line)
        if root.attrib['language'] != 'IPPcode23':
            print("ERR: Invalid language")
            exit(SEMANTIC_ERR)
    
#TODO fix element on one line
    # parses XML element (with closing tag) and creates instruction object
    def parseXMLElement(self, element):
        if(DEVEL):print('[dev]: parsing XML element ... ')
        if(element.tag == 'instruction'):
            self.instructionNum += 1
            return self._createInstruction(element.attrib['opcode'])
        elif (element.tag == 'arg1' or element.tag == 'arg2' or element.tag == 'arg3'):
            if (element.end):
                return self._createArgument(element)
            while True:
                line = self.source.readline()
                if line.isspace() or not line:
                    continue
                if(line == '</arg1>' or line == '</arg2>' or line == '</arg3>'):
                    break
                else:
                    # line is the body of the argument
                    return self._createArgument(line)
        else:  
            return None
            
            
#TODO fix multiple elements on one line            
    # reads line from the source file and parses it
    # returns instruction or argument object or list of instructions and arguments  or none
    # expects correct syntax
    def parseLine(self):
        if(DEVEL):print('[dev]: parsing line ... ')
        
        line = self.source.readline()
        root = ET.fromstring(line)
        # if root is list, parse each element 
        # return list of instructions and arguments
        if isinstance(root, list):
            # multiple elements on one line
            for child in root:
                self.list.append(self.parseXMLElement(child))
        else:
            return self.parseXMLElement(root)
        

    def _createInstruction(self, instructionName):
        if(DEVEL):print('[dev]: creating instruction ... ')

    def _createArgument(self, arg1=None, arg2=None, arg3=None):
        if(DEVEL):print('[dev]: creating Argument ... ')

def main():
    parser = Parser()
    
    parser.openStream()
    parser.parseLine()
    
    parser.closeStream()

if __name__ == '__main__':
    main()