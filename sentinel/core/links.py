def links(devices):
    result=[]
    for start in range(0,len(devices),8):
        hub=devices[start]['id']
        for node in devices[start+1:start+8]:
            result.append({'source':hub,'target':node['id'],'capacity':1000})
        next_hub=devices[(start+8)%len(devices)]['id']
        result.append({'source':hub,'target':next_hub,'capacity':10000})
    return result
