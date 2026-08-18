import numpy as np

def f_phys_prog(old,new):
	return old + new

def f_com_amount(pay_amount,prev_com):
	return float(pay_amount) + float(prev_com)

def f_com_percent(pay_com,original):
	return (float(pay_com)/float(original))*100

def f_bal_amount(original,pay_com):
	return float(original) - float(pay_com)

def f_bal_percent(balance,original):
	return (float(balance)/float(original))*100
#
def f_refresh(payment):
	payment2 = []
	for i in payment:
		id = i.id
		total = i.total
		com_amount = i.com_amount
		com_percent = i.com_percent
		bal_amount = i.bal_amount
		bal_percent = i.bal_percent
		payment2.append([
				id,total,com_amount,com_percent,bal_amount,bal_percent
			])
	return np.array(payment2)