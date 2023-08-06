from os import path
from robot.parsing.model import ForLoop
from robot.parsing.settings import Setting
import re
from .reference import Reference
from .referencesMethods import *

def is_keyword_use_in_attribute(keyword, attribute):
    return any([is_keyword_use_in_attribute(keyword, step) for step in attribute]) if isinstance(attribute, ForLoop) else any([is_keyword_match(keyword,attr) for attr in attribute.as_list()])

class KeywordUsageFinder:
    def get_keyword_references_from_attribute(self, keyword, attribute):
        return Reference(attribute, get_present_method(attribute), get_replace_method(attribute, 'keyword'))

    def find_usage_from_keyword(self, targetKeyword, sourceKeyword):
        source = [step for step in sourceKeyword.steps+[sourceKeyword.teardown]]
        return [self.get_keyword_references_from_attribute(targetKeyword, step) for step in source if is_keyword_use_in_attribute(targetKeyword, step)]

    def find_usage_from_testcase(self, targetKeyword, testcase):
        source = [step for step in testcase.steps+[testcase.template, testcase.setup, testcase.teardown]]
        return [self.get_keyword_references_from_attribute(targetKeyword, setting) for setting in source if is_keyword_use_in_attribute(targetKeyword, setting)]

    def find_usage_from_settings(self, targetKeyword, setting):
        return [self.get_keyword_references_from_attribute(targetKeyword, setting) for setting in [setting.suite_setup, setting.suite_teardown,setting.test_setup, setting.test_teardown] if is_keyword_use_in_attribute(targetKeyword, setting)]

    def find_usage_from_testdataFile(self, targetKeyword, testcaseFile):
        usages = []
        for kw in testcaseFile.keyword_table:
            usages.extend(self.find_usage_from_keyword(targetKeyword,kw))
        for test in testcaseFile.testcase_table:
            usages.extend(self.find_usage_from_testcase(targetKeyword, test))
        usages.extend(self.find_usage_from_settings(targetKeyword, testcaseFile.setting_table))
        return {'testdata':testcaseFile,'references':usages}

class VariableUsageFinder:
    def is_variable_match(self, variableName, string):
        return len(get_variable_match_result(variableName, string))>0

    def is_var_assign_in_step(self, variable, step):
        if isinstance(step, ForLoop):
            return any([self.is_var_assign_in_step(variable, loop_step) for loop_step in step]) or any([self.is_variable_match(variable, var) for var in step.vars])
        else:
            for assign_variable in step.assign:
                if self.is_variable_match(variable, assign_variable):
                    return True
            return False

    def is_var_use_in_attribute(self, variable, attribute):
        if isinstance(attribute, ForLoop):
            return any([self.is_var_use_in_attribute(variable, data) for data in attribute]) or any([self.is_variable_match(variable, data) for data in attribute.items])
        return any([self.is_variable_match(variable, data) for data in attribute.as_list()])

    def is_var_def_in_argument(self, variable, argument):
        def is_arg_match(variable, data):
            arg = data.split("=")
            if len(arg) == 1:
                return self.is_variable_match(variable, data)
            else:
                return len(arg)>1 and self.is_variable_match(variable, arg[0])
        return any([is_arg_match(variable, data) for data in argument.as_list()])
        
    def get_references_from_attribute(self, attribute):
            return Reference(attribute, get_present_method(attribute) ,get_replace_method(attribute, 'variable'))

    def find_global_variable_from_testcase_obj(self, variable, testcase):
        testcase_contents = [content for content in testcase]
        variable_assign_step = next((step for step in testcase.steps if self.is_var_assign_in_step(variable, step)),None)
        source = [testcase_contents[index] for index in range(testcase_contents.index(variable_assign_step))] if variable_assign_step else testcase_contents
        return [self.get_references_from_attribute(content) for content in source if self.is_var_use_in_attribute(variable, content)]

    def find_global_variable_usage_from_keyword(self, variable, keyword):
        return [] if self.is_var_def_in_argument(variable, keyword.args) else self.find_global_variable_from_testcase_obj(variable, keyword)

    def find_global_variable_usage_from_setting(self, variable, settingTable):
        return [self.get_references_from_attribute(setting) for setting in settingTable if self.is_var_use_in_attribute(variable, setting)]

    def find_global_variable_from_testdata_file(self, variable, testData):
        def is_variable_def_in_testData(variable, testData):
            return any(self.is_variable_match(variable, var.name) for var in testData.variable_table)
        source = variable.parent.parent.source
        if path.normpath(source) != path.normpath(testData.source) and is_variable_def_in_testData(variable.name, testData):
            return {'testdata':testData, 'references':[]}
        references = []
        references.extend(self.find_global_variable_usage_from_setting(variable.name, testData.setting_table))
        for keyword in testData.keyword_table:
            references.extend(self.find_global_variable_usage_from_keyword(variable.name, keyword))
        for testcase in testData.testcase_table:
            references.extend(self.find_global_variable_from_testcase_obj(variable.name, testcase))
        return {'testdata':testData, 'references':references}
    
    def find_local_variable_from_test_case_obj(self, variable, testcase):
        return [self.get_references_from_attribute(content) for content in [testcase.doc, testcase.tags, testcase.timeout] + testcase.steps + [testcase.teardown, testcase.return_] if self.is_var_use_in_attribute(variable, content)]