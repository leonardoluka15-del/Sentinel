REGIONS = ['Lagos', 'Abuja', 'Port Harcourt', 'Nantes', 'Paris', 'Lyon']

def devices():
    return [dict(id=f'SNT-{i:03}', name=f'{REGIONS[(i-1)//8]} / Node {((i-1)%8)+1}',
                 region=REGIONS[(i-1)//8], vendor=['Ericsson','Nokia','Huawei'][i%3],
                 technology=['2G','3G','4G','5G'][i%4], capacity=1000 if i%8 else 10000)
            for i in range(1,49)]
