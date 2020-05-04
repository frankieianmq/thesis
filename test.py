mydict = { 'a': 0.01, 'b': 0.02, 'c':0.001, 'd':0.1}


mydict = {key:value for key, value in sorted(mydict.items(), key=lambda item: item[1])}

print(mydict)