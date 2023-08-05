
import re
import os
from lib.parsing import DfxParser
from lib.state import RegOperation
from lib.dump import Dump


class Executor(object):

    def __init__(self, rout):
        self.parser = DfxParser()
        self.log_dump = None
        self.rout = rout
        self.variable_list = list()
        self.dfx_folder = os.path.join(os.path.dirname(__file__), "..", "configuration")
        self.pass_count = 0
        self.fail_count = 0

    def execute(self, dfx_file, log_folder=None):
        full_path = self.get_full_path(dfx_file)
        if full_path is not None:
            self.log_dump = Dump(log_folder)
            parse_dict = self.parser.run(full_path)
            self.print_coms(parse_dict["com"])
            self.read_and_write_reg(parse_dict["var"])
            self.check_expected(parse_dict["exp"])
        return self.log_dump.get_result_path(), self.pass_count, self.fail_count

    def print_coms(self, coms):
        self.log_dump.log("[COM]\n")
        self.log_dump.dump_com("Name", "Register", "Index", "Value")
        for item in coms:
            for index in range(int(item[2])):
                reg_addr = int(item[1], 16)
                reg_addr = reg_addr + index*4
                value = self.rout.read_uint32(reg_addr)
                self.log_dump.dump_com(item[0], "{:#x}".format(reg_addr), str(index), "{:#x}".format(value))

    def check_expected(self, expressions):
        self.log_dump.log("\n[EXP]\n")
        for expression in expressions:
            if expression["equation"] is not None:
                if self.calc_expression(expression["equation"]):
                    expression_string = expression["exp"][0]
                    expression_info = expression["info"][0]
                else:
                    if len(expression["exp"])>1:
                        expression_string = expression["exp"][1]
                        expression_info = expression["info"][1]
                    else:
                        expression_string, expression_info = None, None
            else:
                expression_string = expression["exp"][0]
                expression_info = expression["info"][0]
            if expression_string is not None:
                result, convert_exp = self.calc_expression(expression_string)
                if result:
                    self.pass_count += self.pass_count
                    self.log_dump.log("Pass   {}   {} => {}\n".format(expression_info, expression_string, convert_exp))
                else:
                    self.fail_count += self.fail_count
                    self.log_dump.log("Fail   {}   {} => {}\n".format(expression_info, expression_string, convert_exp))

    def calc_expression(self, expression):
        convert_exp = expression
        for item in self.variable_list:
            if item["name"] in convert_exp:
                convert_exp = convert_exp.replace(item["name"], "0x%x" % item["value"])
        try:
            result = eval(convert_exp)
        except Exception as e:
            print(e)
            result = False
        return result, convert_exp

    def get_full_path(self, dfx_file):
        if os.path.exists(dfx_file) is False:
            full_path = os.path.join(self.dfx_folder, dfx_file)
            if os.path.exists(full_path) is False:
                full_path = os.path.join(os.getcwd(), dfx_file)
                if os.path.exists(full_path) is False:
                    print("{} not exist".format(dfx_file))
                    full_path = None
        else:
            full_path = dfx_file
        return full_path

    def read_and_write_reg(self, vars):
        self.log_dump.log("\n[var]\n")
        self.log_dump.dump("Name", "Operation", "Value", "Expression")
        for var in vars:
            if var["type"] == RegOperation.write:
                self.write_reg(var["reg_address"], var["value"])
            else:
                self.read_var(var)

    def read_var(self, var):
        expression = self.get_read_var(var["expression"])
        if expression is None:
            print("expression failed; {}".format(expression))
        else:
            expression = self.get_expression_var(expression)
            if expression is None:
                print("expression failed: {}".format(expression))
            else:
                value = eval(expression)
                final_value = {
                    "name": var["name"],
                    "value": value
                }
                self.variable_list.append(final_value)
                self.log_dump.dump(var["name"], "read", value, var["expression"])

    def get_read_var(self, expression):
        reg_list = re.findall("(reg.*?\])", expression)
        if reg_list:
            for item in reg_list:
                value = self.get_expression_reg(item)
                if value is None:
                    return None
                expression = expression.replace(item, str(value))
        return expression

    def get_expression_var(self, expression):
        vars = re.findall("var\(\w+\)", expression)
        if vars:
            for item in vars:
                var_name = re.findall("var\((\w+)\)", item)[0]
                get_value = [var["value"] for var in self.variable_list if var["name"] == var_name]
                if get_value:
                    expression = expression.replace(item, str(get_value[0]))
                else:
                    return None
        return expression

    def get_expression_reg(self, reg_string):
        value = None
        rets = re.findall("reg\((\w+)\)\[(.+)\]", reg_string)
        if rets:
            reg_addr = int(rets[0][0], 16)
            reg_range = rets[0][1]
            orgi_value = self.rout.read_uint32(reg_addr)
            value = self.get_value_with_range(orgi_value, reg_range)
        return value

    def write_reg(self, offset, value):
        get_value = eval(self.get_expression_var(value))
        offset = int(offset, 16)
        self.rout.write_uint32(offset, get_value)
        self.log_dump.dump(operation="write", value=get_value, expression="Register 0x{:x}".format(offset))

    @staticmethod
    def get_value_with_range(value, bit_range):
        value_ = None
        rets = re.findall("(\d+)\:(\d+)", bit_range)
        if rets:
            start_ = int(rets[0][1])
            end_ = int(rets[0][0])
            value_ = (value&(2**(end_+1)-1)) >> start_
        return value_


if __name__ == '__main__':
    E = Executor("pcie")
    E.execute("nsc_read.dfx")
