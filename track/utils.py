import numpy as np

def date_dist(date1,date2):
	return np.busday_count(date1,date2)