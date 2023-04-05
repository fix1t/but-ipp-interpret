from abc import ABC, abstractmethod

# Instruction interface
class IInstruction(ABC):
    @abstractmethod
    def doOperation(self):
        pass
    @abstractmethod
    def addArgument(self):
        pass


# Factory method for instruction
# Creates instruction class based on the input
class InstructionFactory:
    def createInstruction(self,instruction):
        

    


class Parser:
    def parseLine():
        print('[dev]: parsing line ... \n')

    def _createInstruction():
        print('[dev]: creating instruction ... \n')

    def _createArgument():
        print('[dev]: creating Argument ... \n')

