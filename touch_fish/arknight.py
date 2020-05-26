#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/12/23 10:07
# @Author  : Shawn Wang

"""
明日方舟作业记录器
"""
notes = {}
while True:
    name = input('关卡名:')
    soldier = {}
    index = 1
    print('开始编队:')
    while True:
        s = input('第{}名干员:'.format(index))
        if s == 'end':
            print('结束编队！')
            break
        soldier.setdefault(index, s)
        index += 1
    operation = []
    index = 1
    while True:
        print('开始第{}次操作, 请输入操作干员编号...'.format(index))
        print(soldier)
        i = input()
        if i == 'end':
            break
        op = input('操作说明(坐标,部署还是撤退,朝向):')
        operation.append((soldier.get(int(i)), op))
        index += 1
    notes.setdefault(name, operation)
    judge = input('是否开始下一关(y/n):')
    if judge == 'n':
        break

print(notes)
