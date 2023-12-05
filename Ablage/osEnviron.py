import os
import pprint

pp = pprint.PrettyPrinter()
adic = dict(os.environ)
keylist = list(adic.keys())

for item in keylist:
    print(item, end="  =  ")
    if item == "PATH":
        print("skipping PATH output")
        continue
    else:
        print(adic[item])

print("\n" * 2, "-----PATH INFORMATION-----", "\n" * 2)
pp.pprint(os.environ['PATH'])