import json
import math
import re
from operator import attrgetter

max_price = 1380
compute_scores = ['gsmarenaBatteryScore', 'mobileScore']
#compute_scores = ['gsmarenaBatteryScore', 'mobileScore', 'priceScore']
#compute_scores = ['batteryScore', 'mobileScore', 'priceScore']
#compute_scores = ['mobileScore', 'priceScore']
#compute_scores = ['batteryScore', 'mobileScore']

class Phone:
    def __init__(self, phonedata):
        self.data = phonedata
        if 'launch_price' in self.data:
            self.data['priceScore'] = self._price_score(self.data)
        totalScore = 0
        self.valid = True
        for score in compute_scores:
            # Filter out smartphone data that is missing any of the scores above
            if score not in self.data.keys():
                self.valid = False
                break
            else:
                # compute geometric mean of scores
                totalScore += self.data[score]**2
        self.data['totalScore'] = int(math.sqrt(totalScore))

    def __repr__(self):
        s = f"{self.data['name']} Total: {self.data['totalScore']}"
        for score in compute_scores:
            s += f" {score}: {self.data[score]}"
        s += f" (MSRP: ${self.data['launch_price']})"
        return s

    def _price_score(self, phone):
        # give a higher score to lower prices, with >=max_price scoring 0
        if phone['launch_price'] > max_price:
            return 0
        else:
            return max_price - phone['launch_price']

def merge_data(dxomark, gsmarena):
    def bare_name(name):
        return re.sub(r'5G', '', re.sub(r'\([^()]*\)', '', name)).strip()

    def find_gsmarena_phone(name):
        name = bare_name(name)
        for phone in gsmarena:
            gsmarena_name = bare_name(phone['name'])
            if gsmarena_name == name:
                return phone
        return None

    for i in range(len(dxomark)):
        gsmarena_phone = find_gsmarena_phone(dxomark[i]['name'])
        if gsmarena_phone != None:
            dxomark[i]['gsmarenaBatteryScore'] = gsmarena_phone['score']
    
    #print(json.dumps(dxomark, indent=4))
    return dxomark


with open('smartphones.json') as f:
    dxomark = json.load(f)

with open('gsmarena.json') as f:
    gsmarena = json.load(f)

smartphones = merge_data(dxomark, gsmarena)

valid_smartphones = []
for phone in smartphones:
    p = Phone(phone)
    if p.valid:
        valid_smartphones.append(p)

print('Sorting smartphones using scores:', ' '.join(compute_scores))
print(f"Found {len(valid_smartphones)} smartphones with this criteria (out of {len(smartphones)})")
sorted_smartphones = sorted(valid_smartphones, key=lambda phone: phone.data['totalScore'], reverse=True)
for p in sorted_smartphones:
    print(p)
