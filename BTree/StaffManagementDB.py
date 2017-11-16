#!usr/bin/env python3
# _*_coding:utf-8_*_

'staff infomation management module'
__author__ = 'Byron Li'

'''----------------------------------------------员工信息数据库操作指令语法---------------------------------------------
数据记录包含6个关键字：id,name,age,phone,dept,enroll_date
指令可用的逻辑运算符：<,>,=,<=,>=,like,and,or,not
1.增（add to xxxx values xxxx）
  示例：add to staff_table values Alex Li,22,13651054608,IT,2013-04-01  
2.删（delete from xxxx where xxxx）
  示例：delete from staff_table where age<=18 and enroll_date like "2017"
3.改(update xxxx set xxxx where xxxx)
  示例：update staff_table set dept="Market",age=30 where dept="IT" and phone like "189"
4.查(select xxxx from xxxx where xxxx)
  示例1：select * from staff_table where age>=25 and not phone like "136" or name like "李"
  示例2：select name,age,dept from  db.txt  where id<9  and  enroll_date like "-05-"
  示例3：select * from staff_table where *           #显示所有记录
---------------------------------------------------------------------------------------------------------------------'''
import re
import os


class staff(object):  # 员工类
    def __init__(self, *args):  # 员工信息初始化：从字符串列表传参赋值
        self.id = args[0]
        self.name = args[1]
        self.age = args[2]
        self.phone = args[3]
        self.dept = args[4]
        self.enroll_date = args[5]
        self.allinfo = ','.join(args)

    def update(self, **kwargs):  # 员工信息更新：从字典传参赋值
        if 'id' in kwargs:
            self.id = kwargs['id']
        if 'name' in kwargs:
            self.name = kwargs['name']
        if 'age' in kwargs:
            self.age = kwargs['age']
        if 'phone' in kwargs:
            self.phone = kwargs['phone']
        if 'dept' in kwargs:
            self.dept = kwargs['dept']
        if 'enroll_date' in kwargs:
            self.enroll_date = kwargs['enroll_date']
        self.allinfo = ','.join(map(str, [self.id, self.name, self.age, self.phone, self.dept, self.enroll_date]))

    def print_info(self, info):  # 员工信息打印显示：传入的参数为"*"或数据记录的若干个关键字
        if info == '*':
            print(self.allinfo)
        else:
            info = info.split(',')
            res = []
            for i in info:
                if hasattr(self, i.strip()):
                    res.append(str(getattr(self, i.strip())))
            print(','.join(res))


def command_exe(command):  # 指令执行主函数，根据指令第一个字段识别何种操作，并分发给相应的处理函数执行
    command = command.strip()
    return {
        'add': add,
        'delete': delete,
        'update': update,
        'select': search,
    }.get(command.split()[0], error)(command)


def error(command):  # 错误提示函数，指令不合语法调用该函数报错
    print('\033[31;1m语法错误，请重新输入！\033[0m\n')


def add(command):  # 增加员工记录函数
    command_parse = re.search(r'add\s*?to\s(.*?)values\s(.*)', command)  # 正则表达式指令解析
    if (command_parse):
        data_file = command_parse.group(1).strip()  # 数据库文件
        info = command_parse.group(2).strip()  # 需新增的员工信息，不含id
        id = 1  # 新增员工id，默认为1以防数据库为空表时新增记录id取1
        with open(data_file, 'r+', encoding='utf-8') as fr:
            line = fr.readline()
            while (line):
                if line.strip() == '':
                    fr.seek(fr.tell() - len(line) - 2)  # 定位文件最后一行(只有空字符)的开头
                    break
                staff_temp = staff(*line.strip().split(','))  # 读取的信息转换为staff对象
                id = int(staff_temp.id) + 1  # 末行员工id加1为新员工id
                line = fr.readline()
            info_new = ''.join([str(id), ',', info])  # id与其他信息合并成完整记录
            fr.write(info_new)
            fr.write('\n')
            fr.flush()
            print("数据库本次\033[31;1m新增1条\033[0m员工信息：", info_new)  # 新增记录打印
    else:
        error(command)


def delete(command):  # 删除员工记录函数
    command_parse = re.search(r'delete\s*?from\s(.*?)where\s(.*)', command)  # 指令解析
    if (command_parse):
        data_file = command_parse.group(1).strip()  # 数据库文件
        condition = command_parse.group(2).strip()  # 检索条件
        data_file_bak = ''.join([data_file, '.bak'])
        count = 0  # 删除记录计数
        staff_list = []  # 删除记录的员工对象列表
        with open(data_file, 'r', encoding='utf-8') as fr, \
                open(data_file_bak, 'w', encoding='utf-8') as fw:
            for line in fr:
                staff_temp = staff(*line.strip().split(','))
                if (verify(staff_temp, condition)):  # 验证员工信息是否符合条件
                    count += 1
                    staff_list.append(staff_temp)
                    continue
                fw.write(staff_temp.allinfo)
                fw.write('\n')
            fw.flush()
        os.remove(data_file)
        os.rename(data_file_bak, data_file)
        print("数据库本次共\033[31;1m删除%d条\033[0m员工信息，如下:" % count)
        for staff_temp in staff_list:
            staff_temp.print_info('*')  # 删除记录打印
    else:
        error(command)


def update(command):  # 修改和更新员工记录函数
    command_parse = re.search(r'update\s(.*?)set\s(.*?)where\s(.*)', command)  # 指令解析
    if (command_parse):
        data_file = command_parse.group(1).strip()  # 数据库文件
        info = command_parse.group(2).strip()  # 需更新的信息
        condition = command_parse.group(3).strip()  # 检索条件
        data_file_bak = ''.join([data_file, '.bak'])

        info = ''.join(['{', info.replace('=', ':'), '}'])  # 将需更新的信息按字典格式修饰字符串
        info = eval(re.sub(r'(\w+)\s*:', r'"\1":', info))  # 将字符串进一步修饰最终转化成字典
        count = 0
        staff_list = []
        with open(data_file, 'r', encoding='utf-8') as fr, \
                open(data_file_bak, 'w', encoding='utf-8') as fw:
            for line in fr:
                staff_temp = staff(*line.strip().split(','))
                if (verify(staff_temp, condition)):  # 验证员工信息是否符合条件
                    staff_temp.update(**info)  # 调用员工对象成员函数更新信息
                    count += 1
                    staff_list.append(staff_temp)
                fw.write(staff_temp.allinfo)
                fw.write('\n')
            fw.flush()
        os.remove(data_file)
        os.rename(data_file_bak, data_file)
        print("数据库本次共\033[31;1m更新%d条\033[0m员工信息，如下:" % count)
        for staff_temp in staff_list:
            staff_temp.print_info('*')  # 更新记录打印
    else:
        error(command)


def search(command):  # 查询员工记录函数
    command_parse = re.search(r'select\s(.*?)from\s(.*?)where\s(.*)', command)  # 指令解析
    if (command_parse):
        info = command_parse.group(1).strip()  # 检索结束后需显示的信息，"*"为显示整体记录
        data_file = command_parse.group(2).strip()  # 数据库文件
        condition = command_parse.group(3).strip()  # 检索条件
        count = 0
        staff_list = []
        with open(data_file, 'r', encoding='utf-8') as fr:
            for line in fr:
                staff_temp = staff(*line.strip().split(','))
                if (verify(staff_temp, condition)):  # 验证员工信息是否符合条件
                    count += 1
                    staff_list.append(staff_temp)
        print("数据库本次共\033[31;1m查询到%d条\033[0m员工信息，如下:" % count)
        for staff_temp in staff_list:
            staff_temp.print_info(info)  # 查询记录打印
    else:
        error(command)


def verify(staff_temp, condition):  # 员工信息验证函数，传入一个员工对象和条件字符串
    if condition.strip() == '*': return True  # 如果条件为'*',即所有记录都满足条件
    condition_list = condition.split()  # 检索条件字符串转列表
    if len(condition_list) == 0: return False
    logic_str = ['and', 'or', 'not']  # 逻辑运算字符串 且、或、非
    logic_exp = []  # 单个条件的逻辑表达式组成的列表，形如[‘age',' ','>','=',20] 或 [‘dept',' ','like',' ','HR']
    logic_list = []  # 每个条件的表达式的计算结果再重组后的列表，形如 [‘True','and','False','or','not','False']
    for i in condition_list:
        if i in logic_str:
            if (len(logic_exp) != 0):
                logic_list.append(str(logic_cal(staff_temp, logic_exp)))  # 逻辑表达式计算并将返回的True或False转化成字符串添加到列表
            logic_list.append(i)
            logic_exp = []
        else:
            logic_exp.append(i)
    logic_list.append(str(logic_cal(staff_temp, logic_exp)))
    return eval(' '.join(logic_list))  # 列表转化成数学表达式完成所有条件的综合逻辑运算，结果为True或False


def logic_cal(staff_temp, logic_exp):  # 单个逻辑表达式的运算函数
    logic_exp = re.search('(.+?)([=<>]{1,2}|like)(.+)',
                          ''.join(logic_exp))  # 表达式列表优化成三个元素，形如[‘age','>=',20] 或 [‘dept','like','HR']
    if (logic_exp):
        logic_exp = list(logic_exp.group(1, 2, 3))
        if (hasattr(staff_temp, logic_exp[0])):
            logic_exp[0] = getattr(staff_temp, logic_exp[0])
        else:
            return False
        if logic_exp[1] == '=':  # 指令中的'='转化成程序中相等判别的"=="
            logic_exp[1] = '=='
        if logic_exp[1] == 'like':  # 运算符为like的表达式运算
            return re.search(logic_exp[2].strip("'").strip('"'), logic_exp[0]) and True
        elif (logic_exp[0].isdigit() and logic_exp[2].isdigit()):  # 两头为数字的运算，直接eval函数转数学表达式
            return eval(''.join(logic_exp))
        elif (logic_exp[1] == '=='):  # 非数字的运算，即字符串运算，此时逻辑符只可能是‘=’，若用eval函数则字符串会转成无定义变量而无法计算，所以拿出来单独用"=="直接计算
            return logic_exp[0] == logic_exp[2].strip("'").strip('"')  # 字符串相等判别，同时消除指令中字符串引号的影响，即输引号会比记录中的字符串多一层引号
        else:  # 其他不合语法的条件格式输出直接返回False
            return False
    else:
        return False


if __name__ == '__main__':  # 主函数，数据库指令输入和执行
    while (True):
        command = input("请按语法输入数据库操作指令：")  # 指令输入
        if command == 'exit':
            print("数据库操作结束，成功退出！".center(50, '*'))
            break
        command_exe(command)  # 指令执行
