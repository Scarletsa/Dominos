from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import pandas as pd

good = []
garb = []

dfsl = pd.read_csv('Streets_1954.csv')
dfsl = dfsl.drop(0)
dfsm = pd.read_csv('SM_1954.csv')
dfsm = dfsm.drop(0)

print(dfsl)
print(dfsm)

for smi, sms in dfsm.iterrows():
    for sli, sls in dfsl.iterrows():
        sls[0] = sls[0].replace('\\n', '').replace('\\r', '').replace('\\t', '').upper()
        ratio = fuzz.partial_ratio(sms[0], sls[0])
        if (ratio >= 90):
            good.append(sls[0])
        elif ('R' in sls[0]):
            ratio = fuzz.partial_ratio(sms[0], sls[0].replace('FI', 'R'))
            if (ratio >= 90):
                good.append(sls[0])
            else:
                ratio = fuzz.partial_ratio(sms[0], sls[0].replace('FH', 'R'))
                if (ratio >= 90):
                    good.append(sls[0])
        elif ('U' in sls):
            ratio = fuzz.partial_ratio(sms[0], sls[0].replace('U', 'O'))
            if (ratio >= 90):
                good.append(sls[0])
        else:
            garb.append(sls[0])

print(good)
print(garb)
