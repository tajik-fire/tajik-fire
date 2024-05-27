from flask import Flask, request, jsonify, render_template, redirect, send_from_directory, send_file
from flask_cors import CORS
from collections import Counter, deque
import subprocess, os, webbrowser
import threading, time
import uuid
# Определяем блокировку для синхронизации доступа к очереди запросов
queue_lock = threading.Lock()

# Создаем очередь для управления запросами
request_queue = deque()
number_last_submit = 1
app = Flask(__name__)
app.static_folder = 'static'
name_task = dict()
name_task[0] = 'A + B = ?'
name_task[1] = 'День Рождения у Илхома ?'
name_task[2] = 'Полёт Мухамммада'
name_task[3] = 'Багаж Мухаммада'
CORS(app)
def run_cpp_code(cpp_file, cpp_file_o, cpp_file_ans):
  #  cpp_file = '/home/imeon/Project_Olympiad/CheckProblems/Debugging/zapuskator.cpp'
  #  cpp_file_o = '/home/imeon/Project_Olympiad/CheckProblems/Debugging/zapuskator'
    #compilation_result = subprocess.run(["g++", cpp_file, "-o", cpp_file_o], capture_output=True, text=True)
    os.system("g++ " + cpp_file + " -o " + cpp_file_o)
    os.system(cpp_file_o)

    with open(cpp_file_ans, 'r') as file:
        ans = file.readline()

    return ans.strip()

# def get_mac_address(request):
#     ip_address = request.remote_addr
#     mac_address = uuid.uuid5(uuid.NAMESPACE_DNS, ip_address)
#     return mac_address

def process_next_request():
    while True:
        # Проверяем, есть ли запросы в очереди
        if request_queue:
            # Обрабатываем самый старый запрос в очереди
            with queue_lock:
                request_data = request_queue.popleft()
            process_request(request_data)
        else:
            # Если очередь пуста, ждем некоторое время перед повторной проверкой
            # Это предотвращает избыточное использование процессора
            time.sleep(0.2)

# Функция для обработки запроса
def process_request(request_data):
    ip_address = request_data['ip_address']
    file_path = "/home/imeon/Project_Olympiad/Submissions/"
    file = request_data['file']
    timee = request_data['timestamp']
    number_submit = str(request_data['number_submit'])
    content = file
    name = str(request_data['name'])
    if name == '0':name = ''
    file_path_c = '/home/imeon/impossible' + '/stupid.cpp'
    cpp_file = '/home/imeon/Project_Olympiad/CheckProblems/Debugging' + name + '/zapuskator.cpp'
    cpp_file_o = '/home/imeon/Project_Olympiad/CheckProblems/Debugging' + name + '/zapuskator'
    cpp_file_ans = '/home/imeon/Project_Olympiad/CheckProblems/Debugging' + name + '/Verdict.txt'

    with open(file_path_c, 'w') as output_file:
        output_file.write(content)
    
    with open(file_path + number_submit + '.txt', 'w') as output_file:
        output_file.write(file + '\n' + '\n' + '\n')

    login = ''
    with open('/home/imeon/Project_Olympiad/online_users/online.txt', 'r') as file:
        f = file.readline()
        while ip_address not in f:
            f = file.readline()
        p1 = f
    ind = p1.index('%')
    ind1 = p1.index('%', ind + 1)
    login = p1[ind + 1:ind1]
    p = run_cpp_code(cpp_file, cpp_file_o, cpp_file_ans)
    if name == '':name = 0
    name = int(name)
    new_text = name_task[name] + "%" + p + '%' + timee + "%" + number_submit + "\n"
    with open('/home/imeon/Project_Olympiad/logins_submit/' + login + '.txt', 'a') as file:
        file.write(new_text)
from datetime import datetime

@app.route('/upload', methods=['POST'])
def upload_file():
    global number_last_submit
    ip_address = request.remote_addr
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    name = request.form.get('x')  # Получение значения x из FormData
    # Добавляем запрос в очередь для последующей обработки
    file = request.files['file']
    content = file.read().decode('utf-8')
    
    with queue_lock:
        request_queue.append({'number_submit':number_last_submit,'timestamp': timestamp, 'ip_address': ip_address, 'file': content, 'name': name})
        number_last_submit += 1
    return jsonify({'result': 1}), 200

@app.route('/login', methods = ['POST'])
def login_user():
    ip_address = request.remote_addr


    login = request.form.get('login')
    password = request.form.get('password')
    file_path_l = '/home/imeon/Project_Olympiad/login_list/login_list.txt'
    login2 = ''
    with open(file_path_l, 'r') as ss:
        login2 = ss.read()
    ok = 1
    sf = '%' + login + '%' + password
    if sf in login2:
        x = login2.index(sf) + len(sf)
        if login2[x] != '%':
            ok = 0
    if ok and sf in login2 and password != '' and login != '':
        file_path_online = '/home/imeon/Project_Olympiad/online_users/online.txt'
        with open(file_path_online, 'a') as ss:
            ss.write("\n" + ip_address + "%" + login + '%')
        return jsonify({"result":"Вы успешно вошли в свой аккаунт!"})
    elif not ok or ("%" + login in login2 and ip_address + "%" + login + "%" + password not in login2) or password == '':
        return jsonify({"result":"Неправильный Парол"})
   
    else:

        return jsonify({"result":"Такой логин не существует("})

@app.route('/register', methods=['POST'])
def register_user():
    username = request.form.get('username')
    login = request.form.get('login')
    ip_address = request.remote_addr

    password = request.form.get('password')
    file_path_l = '/home/imeon/Project_Olympiad/login_list/login_list.txt'
    login2 = ''
    with open(file_path_l, 'r') as ss:
        login2 = ss.read()
    if login in login2 or login == '':
        return jsonify({"result":"Такой логин уже существует!"})

    with open(file_path_l, 'a') as ss:
        ss.write('\n' + ip_address + "%" + login + '%' + password + '%' + username)

    return jsonify({"result":"Вы успешно создали Аккаунт!"})

@app.route('/get_code')
def get_code():
    number_submit = request.args.get('number_submit')
    file_path = '/home/imeon/Project_Olympiad/Submissions/'
    with open(file_path + f'{number_submit}.txt', 'r') as file:
        code = file.read()
    return jsonify({'code': code})

@app.route('/get_login')
def get_login():
    login2 = ''
    ip_address = request.remote_addr
  #  mac_address = get_mac_address(request)
    real_ip = request.headers.get('X-SocketXP-Forwarded-For')
    ip_address1 = request.headers.get('X-Forwarded-For', request.remote_addr)

    login = ''
    with open('/home/imeon/Project_Olympiad/online_users/online.txt', 'r') as file:
        login2 = file.read().strip()
    if ip_address in login2:
        ind = login2.index(ip_address)
        ind1 = login2.index('%', ind + 1)
        ind2 = login2.index('%', ind1 + 1)
        login = login2[ind1 + 1:ind2]
    return {"login":login}

@app.route('/logout')
def logout():
    ip_address = request.remote_addr
    f = ''
    p = []
    with open('/home/imeon/Project_Olympiad/online_users/online.txt', 'r') as file:
        f = file.readline()
        while f != '':
            if ip_address not in f:p += [f]
            f = file.readline()
    with open('/home/imeon/Project_Olympiad/online_users/online.txt', 'w') as file:
        file.write('')
    with open('/home/imeon/Project_Olympiad/online_users/online.txt', 'a') as file:
        for i in p:
            file.write('\n' + i)
    return 'File cleared successfully', 200
@app.route('/get_packages', methods=['GET'])
def get_packages():
    login = ''
    ip_address = request.remote_addr

    with open('/home/imeon/Project_Olympiad/online_users/online.txt', 'r') as file:
        f = file.readline()
        while ip_address not in f:
            f = file.readline()
        p1 = f
    ind = p1.index('%')
    ind1 = p1.index('%', ind + 1)
    login = p1[ind + 1:ind1]
    packages_data = []
    login += '.txt'
    with open('/home/imeon/Project_Olympiad/logins_submit/' + login, 'a+') as ss:
        ss.seek(0)
        x = ss.readline()
        for i in range(1000):
            if x != '' and x != '\n':
                ix = x.index('%')
                ix1 = x[ix + 1:].index('%') + ix + 1
                ix2 = x[ix1 + 1:].index('%') + ix1 + 1
                packages_data.append({'name':x[:ix], 'verdict':x[ix + 1:ix1], 'timestamp': x[ix1 + 1:ix2], 'number_submit':x[ix2 + 1:]})
                print(packages_data[-1])
            x = ss.readline()
    packages_data.reverse()
    return jsonify(packages_data)
@app.route('/get_task_description1', methods=['POST'])
def get_task_description1():
    langg = str(request.form.get('langg'))
    number_task = str(request.form.get('number_task'))
    file_path = '/home/imeon/Project_Olympiad/Tasks/' + 'Task' + number_task + '_' + langg + 'description.txt'

    with open(file_path, 'r') as file:
        task_description = file.read()
    return jsonify({'taskDescription': task_description})

@app.route('/<path:image_name>')
def get_image(image_name):
    return send_from_directory('/home/imeon/Project_Olympiad/', image_name)
@app.route('/get_news')
def get_newss():
    ip_address = request.remote_addr

    file_path = '/home/imeon/Project_Olympiad/text_news/text_news.txt'
    with open(file_path, 'r',  encoding='utf-8') as ss:
        login2 = ss.readlines()
    return jsonify(*login2)
@app.route('/get_info_user')
def get_info_userr():
    ip_address = request.remote_addr
    v = get_login()
    login = v['login']
    with open('/home/imeon/Project_Olympiad/login_list/login_list.txt', 'r') as file:
        f = file.readline()
        while login not in f:
            f = file.readline()
        p1 = f
    ind = p1.index('%')
    ind1 = p1.index('%', ind + 1)
    ind2 = p1.index('%', ind1 + 1)
    login = p1[ind + 1:ind1]
    name = p1[ind2 + 1:]
    cnt = 0
    v = Counter()
    with open('/home/imeon/Project_Olympiad/logins_submit/' + login + '.txt', 'r') as ss:
        ss.seek(0)
        x = ss.readline()
        for i in range(1000):
            if x != '' and x != '\n':
                ix = x.index('%')
                #packages_data.append({'name':x[:ix], 'verdict':x[ix + 1:]})

                if v[x[:ix]] == 0 and x[ix + 1:] == 'Ok\n':
                    cnt += 1
                    v[x[:ix]] = 1
            x = ss.readline()
    return {'name':name, "login":login, 'count':cnt}

@app.route('/change_name', methods=['POST'])
def change_name():
    data = request.json
    new_username = data.get('newUserName')
    ip_address = request.remote_addr
    p = []
    login = ''
    with open('/home/imeon/Project_Olympiad/login_list/login_list.txt', 'r') as file:
        f = file.readline()
        while f != '':
            if ip_address not in f:
                p += [f]
            else:
                ind = f.index('%')
                ind1 = f.index('%', ind + 1)
                ind2 = f.index('%', ind1 + 1)
                login = f[ind + 1:ind2]

            f = file.readline()
    with open('/home/imeon/Project_Olympiad/login_list/login_list.txt', 'w') as file:
        file.write('')
    with open('/home/imeon/Project_Olympiad/login_list/login_list.txt', 'a') as file:
        for i in p:
            if i == '\n':continue
            
            file.write('\n' + i)
        file.write('\n' + ip_address + '%' + login + "%" + new_username)
    
    return jsonify({"message": "Имя пользователя успешно изменено."})

@app.route('/change_password', methods=['POST'])
def change_password():
    data = request.json
    new_password = data.get('newPassword')
    ip_address = request.remote_addr
    p = []
    login = ''
    with open('/home/imeon/Project_Olympiad/login_list/login_list.txt', 'r') as file:
        f = file.readline()
        while f != '':
            if ip_address not in f:
                p += [f]
            else:
                ind = f.index('%')
                ind1 = f.index('%', ind + 1)
                ind2 = f.index('%', ind1 + 1)
                login = '%' + f[ind + 1:ind1] + '%' + new_password + '%' + f[ind2 + 1:]
            f = file.readline()
    with open('/home/imeon/Project_Olympiad/login_list/login_list.txt', 'w') as file:
        file.write('')
    with open('/home/imeon/Project_Olympiad/login_list/login_list.txt', 'a') as file:
        for i in p:
            file.write('\n' + i)
        file.write('\n' + ip_address + login)
    
    return jsonify({"message": "Пароль пользователя успешно изменен."})

if __name__ == '__main__':
    # Запускаем отдельный поток для обработки запросов из очереди
    request_processor_thread = threading.Thread(target=process_next_request)
    request_processor_thread.daemon = True
    request_processor_thread.start()
 
     # Запускаем Flask приложение

    app.run(host='127.0.0.1', port = 3000)