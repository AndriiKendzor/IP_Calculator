from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os
import re
import math
from flask_cors import CORS
load_dotenv()

app = Flask(__name__)
CORS(app)

#Get the environment variables
app.config['DEBUG'] = os.environ.get('FLASK_DEBUG')

@app.route('/')
def index():
    data = {'message': ''}
    return render_template('index.html', data=data)


@app.route('/WhoWeAre')
def who_we_are():
    data = {'message': ''}
    return render_template('WhoWeAre.html', data=data)

@app.route('/Contacts_Us')
def Contacts_us():
    data = {'message': ''}
    return render_template('contact_us.html', data=data)


@app.route('/Privacy_Policy')
def Privacy_Policy():
    data = {'message': ''}
    return render_template('Privacy_Policy.html', data=data)



def validate_ip_address(ip):
    ip_pattern = re.compile(r'^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$')
    match = ip_pattern.match(ip)

    first_octet = int(match.group((1)))
    last_number_ip = int(match.group(4))
    thrid_number_ip = int(match.group(3))
    second_number_ip = int(match.group(2))

    if ip_pattern.match(ip) and 0 <= first_octet <= 255 and 0 <= second_number_ip <= 255 and 0 <= thrid_number_ip <= 255 and 0 <= last_number_ip <= 255:
        return True
    else:
        return False

#Перевірка та визначення класи IP
def get_ip_class(ip):
    ip_pattern = re.compile(r'^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$')
    match = ip_pattern.match(ip)

    first_octet = int(match.group((1)))
    last_number_ip = int(match.group(4))
    thrid_number_ip = int(match.group(3))
    second_number_ip = int(match.group(2))

    if 1 <= first_octet <= 127 and second_number_ip == 0 and thrid_number_ip == 0 and last_number_ip == 0:
        return 'A'
    elif 128 <= first_octet <= 191 and thrid_number_ip == 0 and last_number_ip == 0:
        return 'B'
    elif 192 <= first_octet <= 223 and last_number_ip == 0:
        return 'C'
    elif 224 <= first_octet <= 239:
        return 'D'
    elif 240 <= first_octet <= 255:
        return 'E'
    else:
        if 1 <= first_octet <= 127:
            return '-A'
        elif 128 <= first_octet <= 191:
            return '-B'
        elif 192 <= first_octet <= 223:
            return '-C'



#Перевірка хоста класи C
def validate_host(host_count):
    if host_count <= 0:
        print("Incorrect number of hosts")
        return False
    else:
        return True

#Обчислення найближчої білшої степені
def find_power_of_two(host_count):
    if host_count > 0:
        power = math.ceil(math.log2(host_count + 2)) #Добовляем 2 на Network i Rozgłoszeniowy
        return power
    else:
        return "The entered number must be greater than 0."


#Перевірка хоста класи C
def validate_host_C(host_count):
    if host_count > 254 or host_count <= 0:
        print("Invalid number of hosts for ip class C")
        return False
    else:
        return True


#Шукажмо класу С
# Поиск для класса C
def find_c(ip, pow2):
    result = ""
    ip_pattern = re.compile(r'^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$')
    match = ip_pattern.match(ip)
    last_number_ip = int(match.group(4))

    licznik_podsieci = 0
    last_subnet_printed = False

    first_three_octets = f"{match.group(1)}.{match.group(2)}.{match.group(3)}"

    while last_number_ip < 256:
        licznik_podsieci += 1

        N = last_number_ip
        H1 = N + 1

        last_number_ip = last_number_ip + pow2

        H_ost = last_number_ip - 2
        R = last_number_ip - 1

        if last_number_ip >= 256:
            if not last_subnet_printed:
                result +=f"❗ost.{licznik_podsieci}p:\n"
                last_subnet_printed = True
                #Maska
                maska_koncowa = f"{N}"
            result +=f"ost. N: {first_three_octets}.{N}; 1H: {first_three_octets}.{H1}; ostH: {first_three_octets}.{H_ost}; R: {first_three_octets}.{R};\n"
            result +=f"🎭 Mask - 255.255.255.{maska_koncowa}\n"
        elif licznik_podsieci == 1 or licznik_podsieci == 2 or licznik_podsieci == 3:
            result +=f"{licznik_podsieci}p:\n"
            result +=f"N: {first_three_octets}.{N}; 1H: {first_three_octets}.{H1}; ostH: {first_three_octets}.{H_ost}; R: {first_three_octets}.{R};\n"

    print(result)
    return result


#Перевірка хоста класи B
def validate_host_B(host_count):
    if host_count > 65534 or host_count <= 0:
        print("Invalid number of hosts for ip class B")
        return False
    else:
        return True


#Шукажмо класу B
# Поиск для класса B
def find_B(ip, pow2):
    result = ""
    ip_pattern = re.compile(r'^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$')
    match = ip_pattern.match(ip)

    last_number_ip = int(match.group(4))
    thrid_number_ip = int(match.group(3))

    licznik_podsieci = 0
    last_subnet_printed = False

    first_two_octets = f"{match.group(1)}.{match.group(2)}"

    while thrid_number_ip < 256:
        licznik_podsieci += 1

        cN = last_number_ip
        cH1 = cN + 1

        #bN_first - третя цифра до обчислень
        bN_first = thrid_number_ip

        #перевіряємо чи степінь більша 256 бо інакше до останньої цифри додасть 512 чи 1024 ...  - (вона вийде за межі 255)
        if pow2 >= 256:
            step = pow2/256
            thrid_number_ip += int(step)
            last_number_ip = last_number_ip + 256

        else:
            last_number_ip = last_number_ip + pow2


        #bN_last - третя цифра після обчислень
        if last_number_ip >= 255 and thrid_number_ip > bN_first:
            bN_last = thrid_number_ip-1 #ми віднімаємо 1 бо без цього не коректно показує результат типу  1p ... R: 3.255; 2p N: 3.0; ....
        else:                           #через те що ми відняли 1 буде показувати правильно тобто  1p ... R: 2.255; 2p N: 3.0; ....
            bN_last = thrid_number_ip

        cH_ost = last_number_ip - 2
        cR = last_number_ip - 1

    #Вывожу в консоль все подсети + последний ОТДЕЛЬНО с эмодзи
        if bN_last >= 255 and cR >= 255:
            if not last_subnet_printed:
                result += f"❗ ost. {licznik_podsieci}p:\n"
                #Maska
                maska_koncowa = f"{bN_first}.{cN}"
                last_subnet_printed = True
            result += f"N: {first_two_octets}.{bN_first}.{cN}; 1H: {first_two_octets}.{bN_first}.{cH1}; ostH: {first_two_octets}.{bN_last}.{cH_ost}; R: {first_two_octets}.{bN_last}.{cR};\n"
            result +=f"🎭 Mask - 255.255.{maska_koncowa}\n"


        elif licznik_podsieci == 1 or licznik_podsieci == 2 or licznik_podsieci == 3:
            result +=f"{licznik_podsieci}p:\n"
            result +=f"N: {first_two_octets}.{bN_first}.{cN}; 1H: {first_two_octets}.{bN_first}.{cH1}; ostH: {first_two_octets}.{bN_last}.{cH_ost}; R: {first_two_octets}.{bN_last}.{cR};\n"



        #обнуляємо останню цифру ip
        if pow2 >= 256:
            last_number_ip = 0

        if last_number_ip >= 256:
            last_number_ip = 0
            thrid_number_ip += 1

    print(result)
    return result


#Перевірка хоста класи A
def validate_host_A(host_count):
    if host_count > 16777214 or host_count <= 0:
        print("Invalid number of hosts for ip class A")
        return False
    else:
        return True



#Шукажмо класу A
# Поиск для класса A
def find_A(ip, pow2):
    result = "";
    ip_pattern = re.compile(r'^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$')
    match = ip_pattern.match(ip)

    last_number_ip = int(match.group(4))
    thrid_number_ip = int(match.group(3))
    second_number_ip = int(match.group(2))

    licznik_podsieci = 0
    last_subnet_printed = False

    first_octet = f"{match.group(1)}"

    while second_number_ip < 256:
        licznik_podsieci += 1

        cN = last_number_ip
        cH1 = cN + 1

        #bN_first - третя цифра до обчислень
        bN_first = thrid_number_ip

        #aN_first - друга цифра ip до обчислення
        aN_first = second_number_ip


        if pow2 >= 65536:
            step_a = pow2 / 65536
            second_number_ip +=int(step_a)
            thrid_number_ip = thrid_number_ip + 256
            last_number_ip = last_number_ip + 256

        elif pow2 >= 256 and pow2 <= 65536:
            step_b = pow2 / 256
            thrid_number_ip += int(step_b)
            last_number_ip = last_number_ip + 256
        elif pow2 < 256:
            last_number_ip = last_number_ip + pow2

        # aN_last - друга цифра після обчислень
        if thrid_number_ip >= 255 and second_number_ip > aN_first:
            aN_last = second_number_ip-1
        else:
            aN_last = second_number_ip


        #bN_last - третя цифра після обчислень
        if last_number_ip >= 255 and thrid_number_ip > bN_first:
            bN_last = thrid_number_ip-1
        else:
            bN_last = thrid_number_ip



        cH_ost = last_number_ip - 2
        cR = last_number_ip - 1

    #Вывожу в консоль все подсети + последний ОТДЕЛЬНО с эмодзи
        if aN_last >= 255 and bN_last >= 255 and cR >= 255:
            if not last_subnet_printed:
                result +=f"❗ ost. {licznik_podsieci}p:\n"
                #Maska
                maska_koncowa = f"{aN_first}.{bN_first}.{cN}"
                last_subnet_printed = True

            result +=f"N: {first_octet}.{aN_first}.{bN_first}.{cN}; 1H: {first_octet}.{aN_first}.{bN_first}.{cH1}; ostH: {first_octet}.{aN_last}.{bN_last}.{cH_ost}; R: {first_octet}.{aN_last}.{bN_last}.{cR};\n"
            result +=f"🎭 Mask - 255.{maska_koncowa}\n"


        elif licznik_podsieci == 1 or licznik_podsieci == 2 or licznik_podsieci == 3:
            result +=f"{licznik_podsieci}p:\n"
            result +=f"N: {first_octet}.{aN_first}.{bN_first}.{cN}; 1H: {first_octet}.{aN_first}.{bN_first}.{cH1}; ostH: {first_octet}.{aN_last}.{bN_last}.{cH_ost}; R: {first_octet}.{aN_last}.{bN_last}.{cR};\n"



        #обнуляємо останню цифру ip
        if pow2 >= 256 and pow2 < 65536:
            last_number_ip = 0

        if pow2 >= 65536:
            thrid_number_ip = 0
            last_number_ip = 0

        if last_number_ip >= 256:
            last_number_ip = 0
            thrid_number_ip += 1

        if thrid_number_ip >= 256:
            last_number_ip = 0
            thrid_number_ip = 0
            second_number_ip += 1

    print(result)
    return result


@app.route('/process_another_ip', methods=['POST'])
def process_ip():

    data = request.form.to_dict()
    result = "________"
    ip_address = data.get('ipAddress')


    # Проверяем, содержит ли IP-адрес буквы
    pattern = re.compile(r'^\d+\.\d+\.\d+\.\d+$')

    # Перевірте, чи введений рядок відповідає формату
    if pattern.match(ip_address):
        pass
    else:
        ip_address = "999.999.999.999"



    # Приймаємо host
    try:
        host_count = int(data.get('hostCount'))
    except ValueError:
        host_count = 0




    ip_class = get_ip_class(ip_address)

    if request.headers.get('X-Networks-Button-Active') == 'true':
        var = True  # варифікація
        var = validate_host(host_count)
        if var == True:
            power_of_two = find_power_of_two(host_count)
            print(f"Кількість хостів поміщається в 2^{power_of_two} = {2 ** power_of_two}")
        else:
            result = "Invalid number of hosts for this ip class"

            # Вибір відповідної функції
        var_ip = validate_ip_address(ip_address)
        if var_ip == True:

            if ip_class == 'C':
                # Перевіряємо
                var = validate_host_C(host_count)
                # Обчислити класу С
                if var == True:
                    result = find_c(ip_address, 2 ** power_of_two)
                else:
                    result = "Incorrect number of Hosts for class C"

            elif ip_class == 'B':
                # Перевіряємо
                var = validate_host_B(host_count)
                # Обчислити класу B
                if var == True:
                    result = find_B(ip_address, 2 ** power_of_two)
                else:
                    result = "Incorrect number of Hosts for class B"

            elif ip_class == 'A':
                # Перевіпряємо
                var = validate_host_A(host_count)
                # Обчислити класу A
                if var == True:
                    result = find_A(ip_address, 2 ** power_of_two)
                else:
                    result = "Incorrect number of Hosts for class A"

            elif ip_class == 'D':
                result = "This IP belongs to the reserved class D"
            elif ip_class == 'E':
                result = "This IP belongs to the reserved class E"
            elif ip_class == '-':
                result = "An invalid IP is entered---------------хосты"
            elif ip_class == '-A':
                result = "The wrong IP address was entered for class A " \
                         f"\rAn example here - 1.0.0.0"
            elif ip_class == '-B':
                result = "The wrong IP address was entered for class B"\
                         f"\rAn example here - 128.168.0.0"
            elif ip_class == '-C':
                result = "The wrong IP address was entered for class С"\
                         f"\rAn example here - 192.168.1.0"
        else:
            result = "An invalid IP is entered"


        return jsonify({'result': result})






@app.route('/process_ip', methods=['POST'])
def process_another_ip():

    data = request.form.to_dict()
    # Поверніть відповідь (опціонально)
    result = "________"

    # Приймаємо ip
    ip_address = data.get('ipAddress')

    # Проверяем, содержит ли IP-адрес буквы
    pattern = re.compile(r'^\d+\.\d+\.\d+\.\d+$')

    # Перевірте, чи введений рядок відповідає формату
    if pattern.match(ip_address):
        pass
    else:
        ip_address = "999.999.999.999"


    # Приймаємо host
    try:
        host_count = int(data.get('hostCount'))
    except ValueError:
        host_count = 16777215


    #Степінь 2
    var = True  #варифікація
    var = validate_host(host_count)
    if var == True:
        power_of_two = find_power_of_two(host_count)
    else:
        result = "Invalid number of hosts for this ip class"

    print(f"Кількість хостів поміщається в 2^{power_of_two} = {2**power_of_two}")


    #Перевірка ip та вибір класи
    ip_class = get_ip_class(ip_address)

    # Подсеті (тест) -----------------------------------------

    if request.headers.get('X-Network-Button-Active') == 'true':
        if ip_class == 'C':
            new_pow = 8 - power_of_two
        elif ip_class == 'B':
            new_pow = 16 - power_of_two
        elif ip_class == 'A':
            new_pow = 24 - power_of_two
        else:
            new_pow = power_of_two

        #знайшов баг коли new_pow = 1 або 0 то програма не коректно працює
        if new_pow == 1 or new_pow == 0:
            new_pow = 2
        power_of_two = new_pow

    # -------------------------------------------------------

    #Вибір відповідної функції
    var_ip = validate_ip_address(ip_address)
    if var_ip == True:

        if ip_class =='C':
            #Перевіряємо
            var = validate_host_C(host_count)
            # Обчислити класу С
            if var == True:
                result = find_c(ip_address, 2**power_of_two)
            else:
                result = "Incorrect number of Subnets for class C"

        elif ip_class == 'B':
            # Перевіряємо
            var = validate_host_B(host_count)
            # Обчислити класу B
            if var == True:
                result = find_B(ip_address, 2 ** power_of_two)
            else:
                result = "Incorrect number of Subnets for class B"

        elif ip_class == 'A':
            #Перевіпряємо
            var = validate_host_A(host_count)
            # Обчислити класу A
            if var == True:
                result = find_A(ip_address, 2 ** power_of_two)
            else:
                result = "Incorrect number of Subnets for class A"

        elif ip_class == 'D':
            result = "This IP belongs to the reserved class D"
        elif ip_class == 'E':
            result = "This IP belongs to the reserved class E"
        elif ip_class == '-':
            result = "An invalid IP is entered----------------------------подсети"
        elif ip_class == '-A':
            result = "The wrong IP address was entered for class A " \
                     f"\rAn example here - 1.0.0.0"
        elif ip_class == '-B':
            result = "The wrong IP address was entered for class B" \
                     f"\rAn example here - 128.168.0.0"
        elif ip_class == '-C':
            result = "The wrong IP address was entered for class С" \
                     f"\rAn example here - 192.168.1.0"
    else:
        result = "An invalid IP is entered"


    return jsonify({'result': result})


if __name__ == "__main__":
    app.run()

#binary test
'''decimal_number = 7
binary_str = bin(decimal_number)
print(binary_str)'''