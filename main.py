from flask import Flask
import re
import math

#Перевірка IP на цифри і точки
'''
def validate_ip_address(ip):
    ip_pattern = re.compile(r'^(\d{1,3}\.){3}\d{1,3}$')

    if ip_pattern.match(ip):
        print("IP-адреса валідна.")
    else:
        print("IP-адреса не відповідає очікуваному формату.")
'''

#Перевірка та визначення класи IP
def get_ip_class(ip):
    ip_pattern = re.compile(r'^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$')
    match = ip_pattern.match(ip)

    if match:
        octet1 = int(match.group(1))
        octet2 = int(match.group(2))
        octet3 = int(match.group(3))
        octet4 = int(match.group(4))

        if 1 <= octet1 <= 127 and octet4==0 and octet3==0 and octet2==0: #не знаю чи нам потрібна ця умова - треба перевірити !!!!!
            return 'A'
        elif 128 <= octet1 <= 191 and octet4==0 and octet3==0: #!!!!
            return 'B'
        elif 192 <= octet1 <= 223 and octet4==0: #!!!!
            return 'C'
        elif 224 <= octet1 <= 239:
            return 'D'
        elif 240 <= octet1 <= 255:
            return 'E'
        else:
            return '-'
    else:
        return '-'


#Обчислення найближчої білшої степені
def find_power_of_two(host_count):
    if host_count > 0:
        power = math.ceil(math.log2(host_count + 2)) #Добовляем 2 на Network i Rozgłoszeniowy
        return power
    else:
        return "Введене число має бути більше 0."



#Перевірка хоста класи C
def validate_host_C(host_count):
    if host_count>254:
        print("Не вірна кількість хостів для ip класи C")



#Шукажмо класу С
def find_c(ip, pow2):

    ip_pattern = re.compile(r'^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$')
    match = ip_pattern.match(ip)
    last_number_ip = int(match.group(4))

    #N,H1,Host,R;
    licznik_podsieci=0;

    while(last_number_ip < 256):
        licznik_podsieci+=1

        N = last_number_ip
        H1 = N+1

        last_number_ip = last_number_ip + pow2

        H_ost = last_number_ip-2
        R = last_number_ip-1

        print(f"{licznik_podsieci}p:")
        print(f"N: {N}; 1H: {H1}; ostH: {H_ost}; R:{R};")


'''
Це на мою думку буде лишнє бо ми перевіряємо Ip в get_ip_class   
validate_ip_address(ip_address)
'''

#Приймаємо ip
ip_address = input("Введіть IP-адресу: ")

#Приймаємо host
try:
    host_count = int(input("Введіть кількість хостів: "))
except ValueError:
    print("Введене значення не є цілим числом.")

#Степінь 2
power_of_two = find_power_of_two(host_count)
print(f"Кількість хостів поміщається в 2^{power_of_two} = {2**power_of_two}")


#Перевірка ip та вибір класи
ip_class = get_ip_class(ip_address)
print(f"\nIP-адреса належить до класи {ip_class}")



#Вибір відповідної функції
if ip_class=='C':
    print("Маска за замовчуванням 255.255.255.0\n")
    #Перевіряємо
    validate_host_C(host_count)
    # Обчислити класу С
    find_c(ip_address, 2**power_of_two)

elif ip_class=='B':
    print("Маска за замовчуванням 255.255.0.0")
    # Обчислити класу B
    pass
elif ip_class=='A':
    print("Маска за замовчуванням 255.0.0.0")
    # Обчислити класу A
    pass
elif ip_class=='D':
    print("Даний IP належить до зарезервованої класи D")
elif ip_class=='E':
    print("Даний IP належить до зарезервованої класи E")
else:
    print("Не валідний формат IP")





#binary test
'''decimal_number = 7
binary_str = bin(decimal_number)
print(binary_str)'''