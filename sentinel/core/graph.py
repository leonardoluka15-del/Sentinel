from collections import deque

def adjacency(nodes,links,excluded=None):
    graph={n['id']:set() for n in nodes if n['id']!=excluded}
    for e in links:
        a,b=e['source'],e['target']
        if a in graph and b in graph: graph[a].add(b); graph[b].add(a)
    return graph

def components(graph):
    unseen=set(graph); groups=[]
    while unseen:
        queue=[unseen.pop()]; group=[]
        while queue:
            node=queue.pop(); group.append(node)
            for other in graph[node]&unseen: unseen.remove(other); queue.append(other)
        groups.append(sorted(group))
    return sorted(groups,key=len,reverse=True)

def shortest(graph,start,end):
    if start not in graph or end not in graph: return []
    queue=deque([[start]]); seen={start}
    while queue:
        path=queue.popleft()
        if path[-1]==end: return path
        for n in sorted(graph[path[-1]]-seen): seen.add(n); queue.append(path+[n])
    return []
