
from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker
import json
import jedi


class FunctionVariableChecker(BaseChecker):
    __implements__ = IAstroidChecker
    source = {}
    stubsfile = ""
    name = 'FunctionVariable-notvalid'
    priority = -1
    msgs = {
        'E8104': (
            'variable is not valid.',
            'function-variable-cant-be-found',
            'AddReference string should be a valid module.'
        ),
    }

    def __init__(self, linter=None):
        super(FunctionVariableChecker, self).__init__(linter)

    def setup_after_pylintrc_read(self):
        try:
            self.stubsfile = self.linter_storage['sourcefile'] + "/stubs"
        except:
            print "setup refactors broke"

    def visit_functiondef(self, node):
        if not self.setup:
            self.setup_after_pylintrc_read()
        try:
            regex = ":type (\s*\S*): ([^[][\w]*)"
        except: #catch if the function doesn't reference an external source.
            return

    def visit_attribute(self,node):
        self.node
