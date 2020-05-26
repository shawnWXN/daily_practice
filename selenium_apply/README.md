# 自动预报(实报)加班
基于python3和selenium,登陆HRM系统,并根据task.json文件内的配置来完成预(实)报加班

# 使用指南
step-1 使用pip安装selenium库和pillow库：pip install selenium pillow

step-2 修改task.json文件，配置登录名、密码并填写需要预(实)报的信息

step-3 启动start.py文件

# 备注

1.task.json说明
``` json
{
    "username":"F1334535", # 登录名
    "password":"******", # 密码
    "reason":"xxxxxxxxxxxxxxx", # 加班理由
    "prediction_job":[ # 预报加班任务列表,没有预报可以为空列表[]
        {
            "date":"2019/07/25", # 加班日期
            "start_time":"17:00", # 加班开始时间,必须是xx:xx
            "end_time":"19:00", # 加班结束时间,必须是xx:xx
            "continuous":"Y" # 是否连班, 只能是Y或者N
        }
    ],
    "practical_job":[ # 实报加班任务列表,没有实报可以为空列表[]
        {
            "have_predict":"False", # 没有预报资料
            "date":"2019/07/25",
            "start_time":"17:00",
            "end_time":"19:00",
            "continuous":"Y"
        },
        {
            "have_predict":"True", # 有预报资料
            "date":"2019/07/26",
            "start_time":"17:00",
            "end_time":"19:00",
            "continuous":"Y"
        }
    ]
}
```

2.task.json文件必须与start.py在同一级目录

3.使用VScode启动start.py的，要先在.vscode/settings.json中正确配置运行环境中python解释器的绝对路径(注意需要反斜杠转义)，如：
```bash
"python.pythonPath": "C:\\Users\\Administrator.USER-20181225KU\\envs\\WebSpiderEnv\\Scripts\\python.exe",
```
再使用快捷键Ctrl+Shift+B