import re
from .state import RegOperation



class DfxParser(object):

    def __init__(self):
        self.handler_func_map = {"com": self._parse_com,
                                 "var": self._parse_var_,
                                 "exp": self._parse_exp_}

    def run(self, dfx_file):
        parse_dict = dict()
        data_dict = self.read_and_splite_file(dfx_file)
        for data in data_dict:
            parse_dict[data[0]] = self.handler_func_map[data[0]](data[1])
        return parse_dict

    @staticmethod
    def read_and_splite_file(dfx_file):
        with open(dfx_file, 'rb') as f:
            content_raw = f.read()
        pat = '\[(.*?)\]:([\s\S]*?)(?=(\[.*\]:|$$))'
        data_dict = re.findall(pat, content_raw.decode())
        return data_dict

    def _parse_com(self, com):
        rets = re.findall("des.*?(\w+).*?addr.*?(\w+).*?count.*?(\w+)", com, re.DOTALL)
        return rets

    @staticmethod
    def _re_parse_write_string(line):
        temp = dict()
        rets = re.findall("reg\((.+?)\)\s*\=\s*(.*)", line)
        if rets:
            temp["reg_address"] = rets[0][0]
            temp["value"] = rets[0][1]
            temp["type"] = RegOperation.write
        else:
            pass
        return temp

    @staticmethod
    def _re_parse_read_string(line):
        temp = dict()
        rets = re.findall("(\w+)\s*\=\s*(.*)", line)
        if rets:
            temp["name"] = rets[0][0]
            temp["expression"] = rets[0][1]
            temp["type"] = RegOperation.read
        else:
            pass
        return temp

    def _parse_var_(self, var):
        var_list = list()
        lines = [each_raw.strip() for each_raw in var.split("\n") if each_raw.strip()]
        for line in lines:
            if self._comment(line) is True:
                continue
            ret = re.findall("reg\(.+?\=", line)
            if ret:
                value = self._re_parse_write_string(line)
            else:
                value = self._re_parse_read_string(line)
            var_list.append(value)
        return var_list

    @staticmethod
    def _re_parse_exp_info(line):
        exp, info = None, None
        ret = re.findall("\s*(.+?)(\{.*)", line)
        if ret:
            exp = ret[0][0]
            info = ret[0][1]
        return exp, info

    @staticmethod
    def _re_parse_equation(line):
        equation = None
        ret = re.findall("if\s*(.*?)\:", line)
        if ret:
            equation = ret[0]
        return equation

    def _parse_exp_(self, exp):
        exp_list, index = list(), 0
        lines = [item.strip() for item in exp.split("\n") if item.strip()]
        while index < len(lines):
            temp_dict = {"exp":list(), "info":list(), "equation":None}
            line = lines[index]
            if self._comment(line):
                index = index + 1
                continue
            if "if " in line:
                true_exp, true_info = self._re_parse_exp_info(lines[index+1])
                temp_dict["equation"] = self._re_parse_equation(line)
                temp_dict["exp"].append(true_exp)
                temp_dict["info"].append(true_info)
                if "else" in lines[index+2]:
                    false_exp, false_info = self._re_parse_exp_info(lines[index+3])
                    temp_dict["exp"].append(false_exp)
                    temp_dict["info"].append(false_info)
                    index = index + 4
                else:
                    index = index + 2
            else:
                exp, info = self._re_parse_exp_info(line)
                temp_dict["exp"].append(exp)
                temp_dict["info"].append(info)
                index = index + 1
            exp_list.append(temp_dict)
        return exp_list

    @staticmethod
    def _comment(each):
        if not each.startswith("#") and not each.startswith("//"):
            return False
        else:
            return True

    # def _parse_var(self, var):
    #     var_dict = OrderedDict()
    #     right_dict = {"right_string": "",
    #                   "reg_list": [],
    #                   "var_list": [],
    #                   "info": "REG_MESSAGE",
    #                   "value": 0
    #                   }
    #     left_pat = "(.*?)[ =]"
    #     right_pat = "[ =]+(.*?)(?=\{|$)"
    #     right_reg_pat = "(reg\(.*?\).*?)(?=[ \+\*\-\/\|\&\{\)]|$)"
    #     right_var_pat = "var\((\w+)\)"
    #     left_reg_pat = "reg\((.*?)\)"
    #     info_pat = "\{(.*?)\}"
    #     for each in [each_raw.strip() for each_raw in var.split("\n") if each_raw.strip()]:
    #         if not self._comment(each):
    #             tmp_right_dict = copy.deepcopy(right_dict)
    #             left_string = re.findall(left_pat, each)[0]
    #             right_string = re.findall(right_pat, each)[0]
    #             tmp_right_dict["right_string"] = right_string
    #             if "reg(" in left_string:
    #                 left_string = re.findall(left_reg_pat, left_string)[0]
    #             else:
    #                 for reg in re.findall(right_reg_pat, each):
    #                     tmp_right_dict["reg_list"].append(self._parse_reg(reg))
    #                 for var in re.findall(right_var_pat, each):
    #                     tmp_right_dict["var_list"].append(var)
    #             if "{" in each:
    #                 tmp_right_dict["info"] = re.findall(info_pat, each)[0]
    #             var_dict[left_string] = tmp_right_dict
    #     return var_dict
    #
    # def _parse_reg(self, reg):
    #     reg_dict = {"reg_string": reg,
    #                 "addr": "",
    #                 "range": "",
    #                 "value": 0
    #     }
    #     addr_pat = "reg\((.*?)\)"
    #     range_pat = "\[(.*?)\]"
    #     reg_dict["addr"] = re.findall(addr_pat, reg)[0]
    #     if "[" in reg:
    #         reg_dict["range"] = re.findall(range_pat, reg)[0]
    #     return reg_dict
    #
    # def _parse_exp(self, exp):
    #     exp_list = []
    #     each_dict = {}
    #     exp_pat = "(.*?)[\{]+"
    #     info_pat = "\{(.*?)\}"
    #     bak_dict_raw = {"dict": {"exp": [],
    #                              "info": [],
    #                              "equation": []},
    #                     "flag": 0}
    #     bak_dict = copy.deepcopy(bak_dict_raw)
    #     equa_pat = "[el]?if(.*):$"
    #     for each in [each_raw.strip() for each_raw in exp.split("\n") if each_raw.strip()]:
    #         if self._comment(each):
    #             continue
    #         elif "if" in each or "else" in each or bak_dict["flag"] != 0:
    #             if bak_dict["flag"] == 0 and "else" in each:
    #                 bak_dict["dict"]["equation"].append("True")
    #                 bak_dict["flag"] = 2
    #             elif bak_dict["flag"] == 1:
    #                 bak_dict["dict"]["exp"].append(re.findall(exp_pat, each)[0].strip())
    #                 bak_dict["dict"]["info"].append(re.findall(info_pat, each))
    #                 bak_dict["flag"] = 0
    #             elif bak_dict["flag"] == 2:
    #                 bak_dict["dict"]["exp"].append(re.findall(exp_pat, each)[0].strip())
    #                 bak_dict["dict"]["info"].append(re.findall(info_pat, each))
    #                 exp_list.append(bak_dict["dict"])
    #                 del bak_dict
    #                 bak_dict = copy.deepcopy(bak_dict_raw)
    #             else:
    #                 bak_dict["dict"]["equation"].append(re.findall(equa_pat, each)[0].strip())
    #                 bak_dict["flag"] = 1
    #         else:
    #             tmp_each_dict = copy.deepcopy(each_dict)
    #             tmp_each_dict["exp"] = re.findall(exp_pat, each)[0].strip()
    #             tmp_each_dict["info"] = re.findall(info_pat, each)
    #             exp_list.append(tmp_each_dict)
    #     #for dict in exp_list:
    #     #    print(dict)
    #     return exp_list




if __name__ == '__main__':
    text = r"D:\Automation\self_build_tools\Venus_Tool\script\dfx\nvc.dfx"
    dfx = DfxParser()
    dfx.run(text)
    # dfx.start(text)