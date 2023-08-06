import os
import sys
import json
import threading
import time
import urllib
import urllib.request
import subprocess

#apiHost = 'https://ojservice.acmcoder.com'
apiHost = 'https://ojservice.acmcoder.com/pythonturtle'
baseR = 0

# 获取自己的待判题目
def get_waiting_code(user_id):
    w = baseR + 0
    r = baseR + 3
    url = apiHost + '/api/code/waitJudgeUser/1/PYTHONTURTLE/' + str(w) + '/' + str(r) + '/' + user_id
    params = {
        'lfb': 'zhm'
    }

    params = json.dumps(params)
    headers = {'Accept-Charset': 'utf-8', 'Content-Type': 'application/json'}
    params = bytes(params, 'utf8')

    req = urllib.request.Request(url=url, data=params, headers=headers, method='POST')
    response = urllib.request.urlopen(req).read()
    #print(url)
    #print(response)
    return response

# 更新题目的状态
def update_result(solution_id, user_id, result, time, memory):
    url = apiHost + '/api/code/updateMine/' + str(solution_id) + '/' + user_id + '/0'
    params = {
        'result': result,
        'time': time,
        'memory': memory
    }

    params = json.dumps(params)
    headers = {'Accept-Charset': 'utf-8', 'Content-Type': 'application/json'}
    params = bytes(params, 'utf8')

    req = urllib.request.Request(url=url, data=params, headers=headers, method='POST')
    response = urllib.request.urlopen(req).read()
    return response

# 记录运行错误的日志
def add_runtime_info(solution_id, user_id, info):
    url = apiHost + '/api/code/myruntimeinfoadd/' + str(solution_id) + '/' + user_id + ''
    params = {
        'error': info
    }

    params = json.dumps(params)
    headers = {'Accept-Charset': 'utf-8', 'Content-Type': 'application/json'}
    params = bytes(params, 'utf8')

    req = urllib.request.Request(url=url, data=params, headers=headers, method='POST')
    response = urllib.request.urlopen(req).read()
    return response

# 记录考生所生成的图形
def add_output(solution_id, user_id, result, time, memory, info):
    url = apiHost + '/api/code/myoutputadd/' + str(solution_id) + '/' + user_id + ''
    params = {
        'error': info,
        'result': result,
        'time': time,
        'memory': memory
    }

    params = json.dumps(params)
    headers = {'Accept-Charset': 'utf-8', 'Content-Type': 'application/json'}
    params = bytes(params, 'utf8')

    req = urllib.request.Request(url=url, data=params, headers=headers, method='POST')
    response = urllib.request.urlopen(req).read()
    return response

# 往硬盘写入
def write_file(path, code):
    cf = path
    with open(cf, mode='w') as hcf:
        hcf.write(code)
        hcf.close()
    return cf

# 往硬盘写入考生的代码
def write_code(solution_id, code):
    cf = str(solution_id) + '.py'
    with open(cf, mode='w') as hcf:
        hcf.write(code)
        hcf.close()
    return cf

# 从远端加载模板
def load_template():
    try:
        url = 'https://examacmcoder.oss-cn-beijing.aliyuncs.com/download/pytt/template.py'
        headers = {'Accept-Charset': 'utf-8', 'Content-Type': 'text/html'}
        
        req = urllib.request.Request(url=url, headers=headers, method='GET')
        response = urllib.request.urlopen(req).read()
        return response.decode('utf-8')
    except Exception as e:
        print("Unexpected error: ", e)

# 从远端加载svg_turtle
def load_svg_turtle():
    try:
        url = 'https://examacmcoder.oss-cn-beijing.aliyuncs.com/download/pytt/svg_turtle.py'
        headers = {'Accept-Charset': 'utf-8', 'Content-Type': 'text/html'}
        
        req = urllib.request.Request(url=url, headers=headers, method='GET')
        response = urllib.request.urlopen(req).read()
        return response.decode('utf-8')
    except Exception as e:
        print("Unexpected error: ", e)

# 从远端加载key
def load_key():
    try:
        url = 'https://examacmcoder.oss-cn-beijing.aliyuncs.com/download/pytt/pythonturtlekey.txt'
        headers = {'Accept-Charset': 'utf-8', 'Content-Type': 'text/html'}
        
        req = urllib.request.Request(url=url, headers=headers, method='GET')
        response = urllib.request.urlopen(req).read()
        return response.decode('utf-8')
    except Exception as e:
        print("Unexpected error: ", e)

# 从远端加载pem
def load_pem():
    try:
        url = 'https://examacmcoder.oss-cn-beijing.aliyuncs.com/download/pytt/pythonturtlepem.txt'
        headers = {'Accept-Charset': 'utf-8', 'Content-Type': 'text/html'}
        
        req = urllib.request.Request(url=url, headers=headers, method='GET')
        response = urllib.request.urlopen(req).read()
        return response.decode('utf-8')
    except Exception as e:
        print("Unexpected error: ", e)

# 加载生成的svg文件
def load_svg():
    with open('test.svg') as f:
        return f.read()

# 判断python可执行文件名
def pythonexe():
    try:
        result = subprocess.Popen('python3 -V', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        win = result.stdout.read().decode('utf-8')
        return "python3"
    except Exception as e:
        #print(e)
        return "python"

# 主方法
def main(user_id, guid, solution_id, template):
    python3 = sys.executable
    if python3 == "":
        python3 = pythonexe()
    print(python3)
    #print(template)
    #code = get_code(18648551)

    # 获取我的一个没有运行的代码
    code = get_waiting_code(user_id)
    try:
        code = json.loads(code.decode('utf-8'))
    except Exception as e:
        print(code, e)
        print('An unexcepted error occured, continuing......')
        return

    # 接口正确
    if "id" in code:
        solution_id = code['id']
        code = code['code']
        print("we are goting to run this code:")
        print(code)
        codef = write_code(solution_id, "# coding=utf-8\n" + code)
        print("The code save in: " + codef)
        # 开始运行代码，可以看到窗口
        result = subprocess.Popen('"' + python3 + '" ' + codef + ' 0', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        win = result.stdout.read().decode('utf-8')
        if win.strip() != '':
            # 运行错误
            print(win)
            update_result(solution_id, user_id, baseR + 10, 0, 0)
            add_runtime_info(solution_id, user_id, win)
        else:
            codef = write_code(solution_id, template.replace('# your code #', code))
            # 开始生成svg文件
            result = subprocess.Popen('"' + python3 + '" ' + codef + ' 1', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            svg = result.stdout.read().decode('utf-8')
            if svg.strip() != '':
                # 生成错误
                print(svg)
                add_runtime_info(solution_id, user_id, win)
                update_result(solution_id, user_id, baseR + 10, 0, 0)
            else:
                # 运行没有问题，设置状态为4
                add_output(solution_id, user_id, baseR + 4, 0, 0, load_svg())
                update_result(solution_id, user_id, baseR + 4, 0, 0)
        try:
            os.remove(codef)
            os.remove('test.svg')
        except Exception as e:
            print('')