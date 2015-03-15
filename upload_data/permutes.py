from pprint import pprint

alist = [x for x in range(5)]

adict = {x:None for x in alist}

for k in adict:
	adict[k] = {x:None for x in alist if x!=k}

pprint(k) 