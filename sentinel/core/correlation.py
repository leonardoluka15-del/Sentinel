def correlate(incidents,nodes):
    regions={n['id']:n['region'] for n in nodes}; groups={}
    for incident in incidents:
        if incident['status']=='resolved': continue
        region=regions.get(incident['device'],'Unknown')
        group=groups.setdefault(region,{'region':region,'devices':set(),'signals':[]})
        group['devices'].add(incident['device']); group['signals'].append(incident['kind'])
    return [dict(region=g['region'],devices=sorted(g['devices']),signals=sorted(set(g['signals'])),
                 hypothesis='Possible shared upstream outage' if len(g['devices'])>2 and 'availability' in g['signals'] else 'Investigate device-level telemetry') for g in groups.values()]
