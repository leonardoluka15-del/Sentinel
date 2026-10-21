from .graph import adjacency,components

def impact(nodes,links,target):
    groups=components(adjacency(nodes,links,target))
    isolated=[n for group in groups[1:] for n in group]
    return {'removed':target,'components':len(groups),'isolated':isolated,'impacted_count':len(isolated)+1}

def criticality(nodes,links):
    return sorted([impact(nodes,links,n['id']) for n in nodes],key=lambda x:x['impacted_count'],reverse=True)
