from flask import Flask, render_template
import re
import math

app = Flask(__name__)

@app.route('/')
def index():
    data = {'message': 'Hello from Flask!'}
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
'''
#Перевірка IP на цифри і точки
def validate_ip_address(ip):
    ip_pattern = re.compile(r'^(\d{1,3}\.){3}\d{1,3}$')

    if ip_pattern.match(ip):
        print("IP-адреса валідна.")
    else:
        print("IP-адреса не відповідає очікуваному формату.")
'''


#Перевірка та визначення класи IP
def get_ip_class(ip):
    ip_pattern = re.compile(r'^(\d{1,3})\.')
    first_octet = int(ip_pattern.search(ip).group(1))

    if 1 <= first_octet <= 127:
        return 'A'
    elif 128 <= first_octet <= 191:
        return 'B'
    elif 192 <= first_octet <= 223:
        return 'C'
    elif 224 <= first_octet <= 239:
        return 'D'
    elif 240 <= first_octet <= 255:
        return 'E'
    else:
        return '-'

#Перевірка хоста класи C
def validate_host(host_count):
    if host_count <= 0:
        print("Не вірна кількість хостів")
        return False
    else:
        return True

#Обчислення найближчої білшої степені
def find_power_of_two(host_count):
    if host_count > 0:
        power = math.ceil(math.log2(host_count + 2)) #Добовляем 2 на Network i Rozgłoszeniowy
        return power
    else:
        return "Введене число має бути більше 0."


#Перевірка хоста класи C
def validate_host_C(host_count):
    if host_count > 254:
        print("Не вірна кількість хостів для ip класи C")
        return False
    else:
        return True


#Шукажмо класу С
# Поиск для класса C
def find_c(ip, pow2):
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
                print(f"❗ ost. {licznik_podsieci}p:")
                last_subnet_printed = True
                #Maska
                maska_koncowa = f"{N}"
            print(f"ost. N: {first_three_octets}.{N}; 1H: {first_three_octets}.{H1}; ostH: {first_three_octets}.{H_ost}; R: {first_three_octets}.{R};")
            print(f"🎭 Маска - 255.255.255.{maska_koncowa}")
        elif licznik_podsieci == 1 or licznik_podsieci == 2 or licznik_podsieci == 3:
            print(f"{licznik_podsieci}p:")
            print(f"N: {first_three_octets}.{N}; 1H: {first_three_octets}.{H1}; ostH: {first_three_octets}.{H_ost}; R: {first_three_octets}.{R};")


#Перевірка хоста класи B
def validate_host_B(host_count):
    if host_count > 65534:
        print("Не вірна кількість хостів для ip класи B")
        return False
    else:
        return True


#Шукажмо класу B
# Поиск для класса B
def find_B(ip, pow2):
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
        if last_number_ip >= 255 and thrid_number_ip >= 255:
            if not last_subnet_printed:
                print(f"❗ ost. {licznik_podsieci}p:")
                #Maska
                maska_koncowa = f"{bN_first}.{cN}"
                last_subnet_printed = True
            print(f"N: {first_two_octets}.{bN_first}.{cN}; 1H: {first_two_octets}.{bN_first}.{cH1}; ostH: {first_two_octets}.{bN_last}.{cH_ost}; R: {first_two_octets}.{bN_last}.{cR};")
            print(f"🎭 Маска - 255.255.{maska_koncowa}")


        elif licznik_podsieci == 1 or licznik_podsieci == 2 or licznik_podsieci == 3:
            print(f"{licznik_podsieci}p:")
            print(f"N: {first_two_octets}.{bN_first}.{cN}; 1H: {first_two_octets}.{bN_first}.{cH1}; ostH: {first_two_octets}.{bN_last}.{cH_ost}; R: {first_two_octets}.{bN_last}.{cR};")



        #обнуляємо останню цифру ip
        if pow2 >= 256:
            last_number_ip = 0

        if last_number_ip >= 256:
            last_number_ip = 0
            thrid_number_ip += 1




#Перевірка хоста класи A
def validate_host_A(host_count):
    if host_count > 16777214:
        print("Не вірна кількість хостів для ip класи A")
        return False
    else:
        return True



#Шукажмо класу A
# Поиск для класса A
def find_A(ip, pow2):
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

        elif pow2 >= 256 and pow2 < 65536:
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
        if last_number_ip >= 255 and thrid_number_ip >= 255 and second_number_ip >= 255:
            if not last_subnet_printed:
                print(f"❗ ost. {licznik_podsieci}p:")
                #Maska
                maska_koncowa = f"{aN_first}.{bN_first}.{cN}"
                last_subnet_printed = True

            print(f"N: {first_octet}.{aN_first}.{bN_first}.{cN}; 1H: {first_octet}.{aN_first}.{bN_first}.{cH1}; ostH: {first_octet}.{aN_last}.{bN_last}.{cH_ost}; R: {first_octet}.{aN_last}.{bN_last}.{cR};")
            print(f"🎭 Маска - 255.{maska_koncowa}")


        elif licznik_podsieci == 1 or licznik_podsieci == 2 or licznik_podsieci == 3:
            print(f"{licznik_podsieci}p:")
            print(f"N: {first_octet}.{aN_first}.{bN_first}.{cN}; 1H: {first_octet}.{aN_first}.{bN_first}.{cH1}; ostH: {first_octet}.{aN_last}.{bN_last}.{cH_ost}; R: {first_octet}.{aN_last}.{bN_last}.{cR};")



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
'''
Це на мою думку буде лишнє бо ми перевіряємо Ip в get_ip_class   
validate_ip_address(ip_address)
'''

#Приймаємо ip
ip_address = input("Введіть IP-адресу: ")

#Приймаємо host
try:
    host_count = int(input("Введіть кількість хостів/подсетів: "))
except ValueError:
    print("Введене значення не є цілим числом.")


#Степінь 2
var = True  #варифікація
var = validate_host(host_count)
if var == True:
    power_of_two = find_power_of_two(host_count)

print(f"Кількість хостів поміщається в 2^{power_of_two} = {2**power_of_two}")


#Перевірка ip та вибір класи
ip_class = get_ip_class(ip_address)
print(f"\nIP-адреса належить до класи {ip_class}")


# Подсеті (тест) -----------------------------------------
new_pow = 0
dec = int(input("1 - хости  2 - подсеті "))
if dec == 2:
    if ip_class == 'C':
        new_pow = 8 - power_of_two
    elif ip_class == 'B':
        new_pow = 16 - power_of_two
    elif ip_class == 'A':
        new_pow = 24 - power_of_two

    #знайшов баг коли new_pow = 1 або 0 то програма не коректно працює
    if new_pow == 1 or new_pow == 0:
        new_pow = 2

    power_of_two = new_pow

# -------------------------------------------------------

#Вибір відповідної функції
if ip_class =='C':
    print("Маска за замовчуванням 255.255.255.0\n")
    #Перевіряємо
    var = validate_host_C(host_count)
    # Обчислити класу С
    if var == True:
        find_c(ip_address, 2**power_of_two)

elif ip_class == 'B':
    print("Маска за замовчуванням 255.255.0.0")
    # Перевіряємо
    var = validate_host_B(host_count)
    # Обчислити класу B
    if var == True:
        find_B(ip_address, 2 ** power_of_two)

elif ip_class == 'A':
    print("Маска за замовчуванням 255.0.0.0")
    #Перевіпряємо
    var = validate_host_A(host_count)
    # Обчислити класу A
    if var == True:
        find_A(ip_address, 2 ** power_of_two)

elif ip_class == 'D':
    print("Даний IP належить до зарезервованої класи D")
elif ip_class == 'E':
    print("Даний IP належить до зарезервованої класи E")
else:
    print("Не валідний формат IP")





#binary test
'''decimal_number = 7
binary_str = bin(decimal_number)
print(binary_str)'''