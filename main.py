from flask import Flask
import re
import math

#Перевірка IP на цифри і точки
def validate_ip_address(ip):
    ip_pattern = re.compile(r'^(\d{1,3}\.){3}\d{1,3}$')

    if ip_pattern.match(ip):
        print("IP-адреса валідна.")
    else:
        print("IP-адреса не відповідає очікуваному формату.")


#Визначення класи IP
def get_ip_class(ip):
    ip_pattern = re.compile(r'^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$')
    match = ip_pattern.match(ip)

    if match:
        first_octet = int(match.group(1))

        if 1 <= first_octet <= 127:
            return 'IP класу A'
        elif 128 <= first_octet <= 191:
            return 'IP класу B'
        elif 192 <= first_octet <= 223:
            return 'IP класу C'
        elif 224 <= first_octet <= 239:
            return 'IP класу D'
        elif 240 <= first_octet <= 255:
            return 'IP класу E'
        else:
            return 'Інший клас IP'
    else:
        return 'Не валідний формат IP'


#Обчислення найближчої білшої степені
def find_power_of_two(number):
    if number > 0:
        power = math.ceil(math.log2(number + 2)) #Добовляем 2 на Network i Rozgłoszeniowy
        return power
    else:
        return "Введене число має бути більше 0."


#Приймаємо інформацію
#ip
ip_address = input("Введіть IP-адресу: ")

#host
try:
    host_count = int(input("Введіть кількість хостів: "))
except ValueError:
    print("Введене значення не є цілим числом.")


#Перевірка ip
validate_ip_address(ip_address)

#Класа ip
ip_class = get_ip_class(ip_address)
print(f"IP-адреса належить до {ip_class}")

#Степінь 2
power_of_two = find_power_of_two(host_count)
print(f"Кількість хостів поміщається в 2^{power_of_two} = {2**power_of_two}")
