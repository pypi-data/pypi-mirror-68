from robot.parsing.model import Step, Variable
from robot.parsing.settings import Setting

class KeywordRefactorHelper:
    def rename_keyword(self, references, old, new):
        for reference in references:
            reference.replace(old, new)
          
class VariableRefactorHelper:
    def rename_variable(self, references, old, new):
        for reference in references:
            reference.replace(old, new)