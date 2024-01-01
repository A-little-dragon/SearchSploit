import csv
import os
import sys
import colorama
from datetime import datetime
from prettytable import PrettyTable


def bannder():
    return r"""
 ____                      _       ____        _       _ _   
/ ___|  ___  __ _ _ __ ___| |__   / ___| _ __ | | ___ (_) |_ 
\___ \ / _ \/ _` | '__/ __| '_ \  \___ \| '_ \| |/ _ \| | __|
 ___) |  __/ (_| | | | (__| | | |  ___) | |_) | | (_) | | |_ 
|____/ \___|\__,_|_|  \___|_| |_| |____/| .__/|_|\___/|_|\__|
                                        |_|                  
"""


class Logger:
    def __init__(self):
        colorama.init()
        self.default = colorama.Fore.MAGENTA + "[" + datetime.strftime(datetime.now(),
                                                                       "%Y/%m/%d %H:%M:%S") + "]\033[00m"

    def Success(self, *args):
        args = "".join(str(i) + ' ' for i in args)
        return "{} {} {}".format(self.default, colorama.Fore.GREEN + "[SUCCESS]" + "\033[00m", args)

    def Error(self, *args):
        args = "".join(str(i) + ' ' for i in args)
        return "{} {} {}".format(self.default, colorama.Fore.RED + "[ERROR]" + "\033[00m", args)

    def Warning(self, *args):
        args = "".join(str(i) + ' ' for i in args)
        return "{} {} {}".format(self.default, colorama.Fore.YELLOW + "[WARNING]" + "\033[00m", args)


class SearchExploit:
    def __init__(self):
        self.progname = os.path.basename(__file__)
        self.rootpath = os.path.dirname(__file__)
        self.exploits_csv = os.path.join(self.rootpath, 'files_exploits.csv')
        self.shellcode_csv = os.path.join(self.rootpath, 'files_shellcodes.csv')
        self.cmd_list = {"-a": []}
        self.cmd = {'-t': {'--title', 'title_query'}, '-p': 'port——query', '-m': 'down_file'}
        self.result = {'exploits': [], 'shellcodes': [], 'save_info': []}

    def usage(self):
        print(f" Usage: python {self.progname} [options] term1 [term2] ... [termN]")
        print("==========\n Examples \n==========")
        print(f"  {self.progname} afd windows local")
        print(f"  {self.progname} linux reverse password")
        print(f"  {self.progname} -t oracle windows")
        print(f"  {self.progname} -p 39446")
        print(f"  {self.progname} -m 2332.py [OutPath]")

    def read_csv(self, keys, code=None):
        try:
            def common(readr, read_flag=True, c_code=None):
                try:
                    for row in readr:
                        if row[0].lower() != "id":
                            if len(row) == 8:
                                row = [row[5], row[2], row[7], row[1]]
                            else:
                                row = [row[5], row[2], row[1]]
                            if c_code == 1 or c_code == 2:
                                if c_code == 1:
                                    lower_list = [i.lower() for i in row]
                                    for item in keys:
                                        if item.lower() not in ' '.join(str(i) for i in lower_list):
                                            read_flag = False
                                            break
                                        else:
                                            read_flag = True
                                else:
                                    for item in keys:
                                        if item.lower() not in row[1].lower():
                                            read_flag = False
                                            break
                                        else:
                                            read_flag = True
                                if read_flag:
                                    if row[0] == 'shellcode':
                                        self.result['shellcodes'].append(row)
                                    else:
                                        self.result['exploits'].append(row)
                            elif c_code == 3:
                                for item in keys:
                                    if row[2] and int(item) == int(row[2]):
                                        self.result['exploits'].append(row)

                except Exception as e:
                    print(Logger().Error(e))

            with open(file=self.exploits_csv, mode="r", encoding="utf-8") as file:
                readr = csv.reader(file)
                if code == 0:
                    for row in readr:
                        if '/' + keys in row[1].lower():
                            self.result['save_info'].append(row)
                else:
                    common(readr, c_code=code)

            with open(file=self.shellcode_csv, mode="r", encoding="utf-8") as file:
                readr = csv.reader(file)
                if code == 0:
                    for row in readr:
                        if '/' + keys in row[1].lower():
                            self.result['save_info'].append(row)
                else:
                    if code != 3:
                        common(readr, c_code=code)

        except:
            print(Logger().Error(
                "初始化数据库失败！请检查数据库{}以及{}是否存在！".format(self.exploits_csv, self.shellcode_csv)))
            return False
        else:
            print(Logger().Success("初始化数据库完成!"))
            return True

    def out_info(self):
        print('=' * 60 + colorama.Fore.RED + ' Exploits Start \033[00m' + '=' * 60)
        if not self.result['exploits']:
            print('没有找到数据！')
        else:
            table = PrettyTable(['title', 'port', 'path'])
            for item in self.result['exploits']:
                table.add_row(item[1:])
            print(table)
        print('=' * 61 + ' Exploits End ' + '=' * 61 + '\n')
        print('=' * 60 + colorama.Fore.RED + ' ShellCodes Start \033[00m' + '=' * 60)
        if not self.result['shellcodes']:
            print('没有找到数据！')
        else:
            table = PrettyTable(['title', 'path'])
            for item in self.result['shellcodes']:
                table.add_row(item[1:])
            print(table)
        print('=' * 61 + ' ShellCodes End ' + '=' * 61)

    def parse_args(self, args):
        key = None
        inargs = False
        if ' -' not in args[0]:
            index = True
        else:
            index = False
        for item in args:
            if index:
                if '-' in item:
                    inargs = True
                    if item in self.cmd.keys():
                        key = item
                        if key not in self.cmd_list:
                            self.cmd_list[key] = []
                    else:
                        print(Logger().Error("该参数{}不存在！请查看语法后重试！".format(item)))
                        sys.exit()
                else:
                    if inargs:
                        self.cmd_list[key].append(item)
                    else:
                        self.cmd_list['-a'].append(item)
            else:
                if '-' in item:
                    if item in self.cmd.keys():
                        key = item
                        if key not in self.cmd_list:
                            self.cmd_list[key] = []
                    else:
                        print(Logger().Error("该参数{}不存在！请查看语法后重试！".format(item)))
                        sys.exit()
                else:
                    self.cmd_list[key].append(item)
        if '-m' in self.cmd_list.keys():
            if len(self.cmd_list.keys()) > 2 and len(self.cmd_list['-a']) > 0:
                print(Logger().Error("-m参数不能与其他参数搭配使用！请查看语法后重试！"))
                sys.exit()

    def search_all(self):
        self.read_csv(self.cmd_list['-a'], code=1)

    def search_title(self, t_flags=True):
        if len(self.cmd_list['-a']) == 0:
            self.read_csv(keys=self.cmd_list['-t'], code=2)
        else:
            if self.result['exploits']:
                res = []
                for item in self.result['exploits']:
                    for key in self.cmd_list['-t']:
                        if key.lower() not in item[1].lower():
                            t_flags = False
                            break
                        else:
                            t_flags = True
                    if t_flags:
                        res.append(item)
                self.result['exploits'] = res
            if self.result['shellcodes']:
                res = []
                for item in self.result['shellcodes']:
                    for key in self.cmd_list['-t']:
                        if key.lower() not in item[1].lower():
                            t_flags = False
                            break
                        else:
                            t_flags = True
                    if t_flags:
                        res.append(item)
                self.result['shellcodes'] = res

    def search_port(self):
        if not self.result['exploits']:
            self.read_csv(keys=self.cmd_list['-p'], code=3)
        else:
            res = []
            for item in self.result['exploits']:
                for key in self.cmd_list['-p']:
                    if item[2] and int(key) == int(item[2]):
                        res.append(item)
            self.result['exploits'] = res
            if self.result['shellcodes']:
                self.result['shellcodes'] = []

    def save_file(self, path_info, now_path='./'):
        if len(path_info) != 2:
            print(Logger().Error(
                "Usage:{} -m [FilePath] [SavePath]\nExample: {} -m 36411.py ./".format(self.progname, self.progname)))
            sys.exit()
        else:
            self.read_csv(code=0, keys=path_info[0])
            if self.result['save_info']:
                print(Logger().Success('找到{}利用攻击脚本'.format(path_info[0])))
                print(colorama.Fore.YELLOW + '<== 攻击脚本信息如下 ==>')
                path = self.result['save_info'][0][1]
                if len(self.result['save_info'][0]) == 8:
                    print(colorama.Fore.RED + 'ID:\033[00m', colorama.Fore.CYAN + self.result['save_info'][0][0])
                    print(colorama.Fore.RED + 'FilePath:', colorama.Fore.CYAN + path)
                    print(colorama.Fore.RED + 'Description:', colorama.Fore.CYAN + self.result['save_info'][0][2])
                    print(colorama.Fore.RED + 'Port:', colorama.Fore.CYAN + self.result['save_info'][0][7])
                    print(colorama.Fore.RED + 'Type:', colorama.Fore.CYAN + self.result['save_info'][0][5])
                    print(colorama.Fore.RED + 'Platform:', colorama.Fore.CYAN + self.result['save_info'][0][6])
                else:
                    print('ID:', self.result['save_info'][0][0])
                    print('FilePath:', path)
                    print('Description:', self.result['save_info'][0][2])
                    print('Type:', self.result['save_info'][0][5])
                    print('Platform:', self.result['save_info'][0][6])
                try:
                    path_arg = os.path.dirname(path_info[1])
                    if not os.path.isdir(path_info[1]):
                        now_path = path_arg
                    else:
                        if path_arg[:1] == '.':
                            now_path = os.getcwd()
                        if path_arg[:2] == '..':
                            now_path = os.path.abspath(os.path.join(os.getcwd(), path_arg))
                        else:
                            now_path = path_info[1]
                    with open(file=os.path.join(now_path, os.path.basename(path)), mode="w+", encoding="utf-8") as f:
                        if now_path != self.rootpath:
                            path = os.path.join(self.rootpath, path)
                        with open(file=path, mode="r", encoding="utf-8") as f2:
                            f.write(f2.read())
                    print(Logger().Success(
                        '利用攻击脚本文件{}已成功下载！请自行利用！路径：{}'.format(os.path.basename(path),
                                                                                 os.path.join(now_path,
                                                                                              os.path.basename(path)))))
                except:
                    print(Logger().Error('下载文件失败！请检查目标地址是否存在！'))
                    sys.exit()
            else:
                print(Logger().Warning('未找到该{}利用攻击脚本'.format(path_info[0])))

    def main(self):
        args = sys.argv[1:]
        colorama.init(autoreset=True)
        print(colorama.Fore.RED + bannder())
        print(" " * 80 + colorama.Fore.CYAN + "Version：" + colorama.Fore.MAGENTA + "v1.0.0")
        print(" " * 80 + colorama.Fore.CYAN + "Team：" + colorama.Fore.MAGENTA + "Traceless网络安全团队")
        print(" " * 80 + colorama.Fore.CYAN + "By：" + colorama.Fore.MAGENTA + "一条'小龍龙")
        print(" " * 80 + colorama.Fore.CYAN + "StartTime：" + colorama.Fore.MAGENTA + "2022-10-18")
        print(" " * 80 + colorama.Fore.CYAN + "GitHub：" + colorama.Fore.MAGENTA + "https://github.com/A-little-dragon")
        print(colorama.Fore.RESET)
        if not args:
            self.usage()
        else:
            self.parse_args(args)
            if '-m' in self.cmd_list.keys() and self.cmd_list['-m']:
                self.save_file(self.cmd_list['-m'])
            else:
                if self.cmd_list['-a']:
                    self.search_all()
                if '-t' in self.cmd_list.keys() and len(self.cmd_list['-t']) > 0:
                    self.search_title()
                if '-p' in self.cmd_list.keys() and len(self.cmd_list['-p']) > 0:
                    self.search_port()
                self.out_info()


if __name__ == '__main__':
    search_exploit = SearchExploit()
    search_exploit.main()
