
from datetime import date
import os, hashlib, calendar
import numpy as np
from collections import OrderedDict
from uuid import uuid4
import random

def getnewid(table_name):
	result = table_name.objects.last()
	if result:
		newid = result.id + 1
		hashid = hashlib.md5(str(newid).encode())
	else:
		newid = 1
		hashid = hashlib.md5(str(newid).encode())
	return newid, hashid.hexdigest()

def hash_md5(strhash):
	hashed = hashlib.md5(strhash.encode())
	return hashed.hexdigest()

def split_string(string):
	string2 = string.split()
	return string2[0].lower()
def f_rem_space(string):
	str = string.replace(" ", "")
	return str.lower()
def username_gen(code,m,id):
	x = random.randint(1,99999)
	string = str(code)+str(m)+str(id)+str(x)
	return string

def date_dist(data1,date2):
	return np.busday_count(data1,date2)

def f_monthname_tet(month):
	m = ['Janeiru','Fevereiru','Marsu','Abril','Maiu','Junhu','Julhu','Agostu','Setembru',
		'Outubru','Novembru','Dezembru']
	return m[month-1]

def f_get_mondays(year,month):
	A=calendar.TextCalendar(calendar.MONDAY)
	mondays = []
	for k in A.itermonthdays(year,month):
		if k!=0:
			day=date(year,month,k)
			if day.weekday()==6:
				dayname = calendar.day_name[0]
				day = "%s-%s-%s" % (year,month,k)
				mondays.append([dayname,day])
	mondays.append([""])
	return mondays

def write_roman(num):

    roman = OrderedDict()
    roman[12] = "XII"
    roman[11] = "XI"
    roman[10] = "X"
    roman[9] = "IX"
    roman[8] = "VIII"
    roman[7] = "VII"
    roman[6] = "VI"
    roman[5] = "V"
    roman[4] = "IV"
    roman[3] = "III"
    roman[2] = "II"
    roman[1] = "I"

    def roman_num(num):
        for r in roman.keys():
            x, y = divmod(num, r)
            yield roman[r] * x
            num -= (r * x)
            if num <= 0:
                break

    return "".join([a for a in roman_num(num)])