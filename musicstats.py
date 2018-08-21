import sys
from scipy import stats

# this program takes 2 arguments (argv)
# it runs in 15 seconds

listSets = {}

# for t-test
listMobile = {}

with open(sys.argv[1], "r") as f_tracks:
# building the listSets
	for line in f_tracks:
		row = line.split(",")
		customer = row[1]
		track = row[2]
		
		# for t-test
		mobile = row[4]
		
		if customer not in listSets:
			listSets[customer] = []	
			listMobile[customer] = [0,0] # [non_mobile, mobile] 
		if track not in listSets[customer]:
			listSets[customer].append(track)
		
		# for t-test
		if mobile == '0':
			listMobile[customer][0] += 1
		elif mobile == '1':
			listMobile[customer][1] += 1
		
		
		
# picking the customer
maxi = 0
customers_id = []
for customer in listSets:
	tracks = listSets[customer]
	l = len(tracks)
	if l > maxi:
		maxi = l
		customers_id = []
		customers_id.append(customer)
	elif l == maxi:
		customers_id.append(customer)
	
	
print(" Maximum number of different tracks listened by any single customer: " + str(maxi))
#print(" Ids of customers  who listened to the maximum number of different tracks: " + str(customers_id))
"""tracks = sorted(listSets[customers[0]])
print(str(tracks))"""

# retrieving the names of these customers
# for welsh t-test
men_sample = []
women_sample = []

customers_name = []
with open(sys.argv[2], "r") as f_cust:
	f_cust.readline()
# building the listSets
	for line in f_cust:
		row = line.split(",")
		customer_id = row[0]
		
		# for welsh t-test
		customer_gender = row[2]
		if customer_id in listSets:
			if customer_gender == '0':
				tracks = listSets[customer_id]
				ml = len(tracks)
				men_sample.append(ml)
			elif customer_gender == '1':
				tracks = listSets[customer_id]
				wl = len(tracks)
				women_sample.append(wl)
		
		if customer_id in customers_id:
			customer_name = row[1]
			customers_name.append(customer_name)
print(" Names of customers  who listened to the maximum number of different tracks: " + str(customers_name))

# 2/ customers(gender, number of tracks) -> dist_men = number of tracks; dist_women =  number of tracks
welch_test = stats.ttest_ind(men_sample,women_sample, equal_var = False)
print("Welch t-test on men vs. women\'s number of tracks   :  " + str(welch_test))
if welch_test[1] > 0.1:
	print("hypthesis H0 -that men and women listen to on average as many tracks- is accepted with a precision of 10%")
else:
	print("hypthesis H0 -that men and women listen to on average as many tracks- is rejected with a precision of 10%")

# 3/ customers(mobile, number of tracks) -> dist_mobile = number of tracks; dist_non_mobile = number of tracks
# for t-test
non_mobile_sample = []
mobile_sample = []

for customer in listMobile:
	non_mobile_sample.append(listMobile[customer][0])
	mobile_sample.append(listMobile[customer][1])
	#print(str(non_mobile_sample))
t_test = stats.ttest_ind(mobile_sample,non_mobile_sample)

#print(str(t_test))
print("T-test on mobile vs. non-mobile\'s number of tracks   :  " + str(t_test))
if t_test[1] > 0.1:
	print("hypthesis H0 -that  that users listen to as many tracks when connecting from a mobile device as when connecting from a non-mobile device- is accepted with a precision of 10%")
else:
	print("hypthesis H0 -that  that users listen to as many tracks when connecting from a mobile device as when connecting from a non-mobile device- is rejected with a precision of 10%")

# now: python musicstats.py tracks.csv cust.csv
""" results:
 Maximum number of different tracks listened by any single customer: 1617
 Names of customers  who listened to the maximum number of different tracks: ['"Gregory Koval"']
Welch t-test on men vs. women's number of tracks   :  Ttest_indResult(statistic=0.90580710350470994, pvalue=0.36508598658687741)
hypthesis H0 -that men and women listen to on average as many tracks- is accepted with a precision of 10%
T-test on mobile vs. non-mobile's number of tracks   :  Ttest_indResult(statistic=17.356095771305199, pvalue=1.6649726396763154e-66)
hypthesis H0 -that  that users listen to as many tracks when connecting from a mobile device as when connecting from a non-mobile device- is rejected with a precision of 10%
"""
	
