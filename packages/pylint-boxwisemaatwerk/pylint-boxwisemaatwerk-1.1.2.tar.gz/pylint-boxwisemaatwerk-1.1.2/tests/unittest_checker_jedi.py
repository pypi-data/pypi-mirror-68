import unittest
import jedi
import sys
from pylint.testutils import CheckerTestCase

sys.path.insert(0, 'C:\dev\pylint-boxwisemaatwerk\pylint_boxwisemaatwerk')
import boxwise_plugin
import astroid

class TestCheckJedi(unittest.TestCase):
    CHECKER_CLASS = boxwise_plugin.FunctionVariableChecker

    def test_jedi_mock_scenario_1(self):
        subject = "\nfrom Wms.RemotingImplementation import General\nGeneral().AddOrUpdateErpLock"
        #a = jedi.create_environment(r"C:\Python27amd64\python.exe")
        project = jedi.get_default_project()
        project.added_sys_path = [r"C:/Users/k.pawiroredjo/AppData/Local/Programs/Microsoft VS Code/linter_storage/stubs"]
        script = jedi.Script(subject, environment=jedi.api.environment.InterpreterEnvironment(),project = project)
        completions = script.complete(3, len('General().AddOrUpdateErpLock'))
        self.assertEquals("AddOrUpdateErpLock",completions[0].name)

    def test_jedi_default(self):
        subject = "\nimport json\njson.load"
        #a = jedi.create_environment(r"C:\Python27amd64\python.exe")
        script = jedi.Script(subject, environment=jedi.api.environment.InterpreterEnvironment())
        completions = script.complete(3, len('json.'))
        self.assertIsNotNone(completions)

    def test_node_diff(self):
        node_a, node_b= astroid.extract_node("""
        import json
        json.load()                           #@
        def test(alex):
            alex.load                         #@
        """)
        self.assertIsNotNone(node_b)