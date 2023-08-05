import argparse
import os
import re


class Finder(object):

    def __init__(self, dir_path, kw, name_only, is_re, return_container):
        self.path = dir_path
        self.sep = "<<<***0...>>>"
        self.kw = kw
        self.name_only = name_only
        self.is_re = is_re
        self.return_container = return_container

    def start(self):
        f_lis = []
        for root, sub_dir, file_names in os.walk(self.path):
            f_lis += [os.path.join(root, file_name) for file_name in file_names]

        container = self.get_container(f_lis) if not self.is_re else self.get_container_re(f_lis)
        if self.return_container:
            return container
        ft = " >>> "
        for match, type_line_id in container.items():
            type_str = 'file content'
            if isinstance(type_line_id, str):
                if not self.is_re:
                    match_str = match.replace(self.kw, f"\033[0;31;48m{self.kw}\033[0m")
                else:
                    match_str = re.sub(fr'(?P<kw>{self.kw})', self.make_re_color, match)
                if f'{self.sep}dir_name' in type_line_id:
                    type_str = 'folder'
                if f'{self.sep}file_name' in type_line_id:
                    type_str = 'file name'
                print(f"{ft}[ {type_str} ] [ {match_str} ]")
            else:
                print(f"in file [ {match} ]: ")
                for line in type_line_id:
                    line_no, line_str = line.split(self.sep)
                    if not self.is_re:
                        line_str = line_str.replace(self.kw, f"\033[0;31;48m{self.kw}\033[0m")
                    else:
                        line_str = re.sub(fr'(?P<kw>{self.kw})', self.make_re_color, line_str)
                    print(f"{ft}[ {line_no} ] [ {line_str} ]")
                print()

    @staticmethod
    def make_re_color(matched):
        res = f"\033[0;31;48m{matched.group('kw')}\033[0m"
        return res

    def get_container(self, lis):
        container = dict()
        for f in lis:
            if self.name_only:
                fs = f.split(os.sep)
                fsn = [os.sep.join(fs[:-1]), fs[-1]]
                if self.kw in fsn[0]:
                    container[fsn[0]] = f'{self.sep}dir_name'
                if self.kw in fsn[1]:
                    container[os.sep.join(fsn)] = f'{self.sep}file_name'
            else:
                try:
                    with open(f, 'r') as rf:
                        lines = rf.readlines()
                    lines_with_kw = [f'{lines.index(x)+1}{self.sep}{x.strip()}' for x in lines if self.kw in x]
                    if lines_with_kw:
                        container[f] = lines_with_kw
                except Exception as E:
                    pass
        return container

    def get_container_re(self, lis):
        container = dict()
        for f in lis:
            if self.name_only:
                if self.sep in f:
                    f = f.replace(self.sep, ''.join([f"\\{x}" for x in self.sep]))
                fs = f.split(os.sep)
                fsn = [os.sep.join(fs[:-1]), fs[-1]]
                if re.findall(self.kw, fsn[0]):
                    container[fsn[0]] = f'{self.sep}dir_name'
                if re.findall(self.kw, fsn[1]):
                    container[os.sep.join(fsn)] = f'{self.sep}file_name'
            else:
                try:
                    with open(f, 'r') as rf:
                        lines = rf.readlines()
                    lines = [x.replace(self.sep, ''.join([f"\\{x}" for x in self.sep])) if self.sep in x else x for x in lines]
                    lines_with_kw = [f'{lines.index(x)+1}{self.sep}{x.strip()}' for x in lines if re.findall(self.kw, x)]
                    if lines_with_kw:
                        container[f] = lines_with_kw
                except Exception as E:
                    pass
        return container


def find():
    dp = ' *** 这是一个在文件夹下所有的地方查找关键字的工具'
    da = "--->   "
    parser = argparse.ArgumentParser(description=dp, add_help=True)
    parser.add_argument("-f", "--folder", type=str, default='', help=f'{da}需要查找的文件夹，默认运行目录')
    parser.add_argument("-k", "--keyword", type=str, default='', help=f'{da}要查找的关键字，必须值')
    parser.add_argument("-r", "--re_mode", type=str, default='n', help=f'{da}y/n 是否以正则方式查找，默认n')
    parser.add_argument("-o", "--filename_only", type=str, default='n', help=f'{da}y/n 是否只查找文件夹名和文件名，默认n')
    args = parser.parse_args()

    kw = args.keyword
    if not kw:
        raise ValueError('关键字是必须的: findkw -k xxx')

    folder = args.folder
    if not folder:
        folder = os.getcwd()

    fn_only = False
    if args.filename_only.lower() == 'y':
        fn_only = True

    re_mode = False
    if args.re_mode.lower() == 'y':
        re_mode = True

    fd = Finder(folder, kw, fn_only, re_mode, False)
    fd.start()


if __name__ == '__main__':
    fdr = Finder(os.getcwd(), 'py', True, True, False)
    fdr.start()
