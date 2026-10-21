def summarize(rows,target=99.9):
    availability=100*sum(r['available'] for r in rows)/len(rows) if rows else 100
    return {'availability':round(availability,3),'target':target,'budget_remaining_percentage_points':round(availability-target,3),
            'scope':'Retained sampled observations, not monthly contractual SLA.'}
