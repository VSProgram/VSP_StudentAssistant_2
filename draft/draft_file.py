import ast# # for i in range(1,13):
import datetime
# #     print(i)

from datetime import datetime
from datetime import timedelta
from calendar import Calendar
#
# a = '2024-07-30'
# b = a.split('-')
# print(b)
# print(f'{b[1]}-{b[2]}-{b[0]}')
#
c = [1,2,3]
# print(type(c))
#
# date_1 = '2024-08-06 21:16:00'
# s = date_1.split(' ')
# t1 = s[1].split(':')
# t2 = t1[0] +':'+ t1[1]
# m1 = s[0].split('-')
# m2 = m1[2]+'-'+m1[1]+'-'+m1[0]
# m3 = m2 + ' '+ t2
# print(m3)

# for element in range(len([1,2,3])):
#     print(element)
#
#
# phot_7 = "['AgACAgIAAxkBAAIFKGa3ml0Y_vbjNWYwSzXxiiqDYpjSAAKj3jEbW1u4Se35CJJjP69MAQADAgADeQADNQQ']"
# list_media = ast.literal_eval(phot_7)
#
# print(f'list_media = {list_media}')
#
# print(datetime.date(year=2024,month=8,day=1))

# k = 0
# for i in range(1,len(c)):
#     print(i)
#     if i == 9:
#         print('vs')
#     else:
#         print('ne vse')
# print(len('Безопасность жизнедеятельности12345'))

# c = [1,2,3]
# print(str.isdigit('44244w'))

# a = Calendar()
# m = a.monthdays2calendar(year=2024, month=8)
# m2 = a.monthdays2calendar(year=2024, month=9)
a = range(len(c))
m = []
for i in range(25,31):
    m.append(i)

k = ('свсу', '25-08-2024 21:10', 'Саня', 5540384350, '-', "['AgACAgIAAxkBAAIeM2bLc7knYAPan71vq5NZfuPQhIudAAIN3zEb_WxYSuwninG_T42TAQADAgADeQADNQQ', 'AgACAgIAAxkBAAIeNGbLc7l4h3DVeM3LnFZutdGWM8l_AAIO3zEb_WxYSgmyF8D70b3LAQADAgADeQADNQQ']", 'BQACAgIAAxkBAAIeNmbLc73Gp5DeYm_CK6fJcjaDMquBAAIjUwAC_WxYSlQFLFDt5x7wNQQ')
print(k[1:-1])