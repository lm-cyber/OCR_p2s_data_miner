import random
def gen_vin(count):
    nums ='0123456789'
    alphabite = 'ABCDEFGHJKLMNPRSTUVWXYZ'
    dist_for_choose = nums*5+alphabite*2+alphabite.lower()
    vins = []
    for _ in range(count):
        vins.append(''.join(random.choices(dist_for_choose,k=17)))
    return vins
        