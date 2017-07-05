import xlrd
import os.path
import heapq
import re
import array
from sys import stdin, stdout
from graph import Graph

def dijkstra(adj, source, target):
    INF = ((1<<63) - 1)//2
    pred = { x:x for x in adj }
    dist = { x:INF for x in adj }
    dist[ source ] = 0
    PQ = []
    heapq.heappush(PQ, [dist[ source ], source])

    while(PQ):
        u = heapq.heappop(PQ)  # u is a tuple [u_dist, u_id]
        u_dist = u[0]
        u_id = u[1]
        if u_dist == dist[u_id]:
            #if u_id == target:
            #    break
            for v in adj[u_id]:
               v_id = v[0]
               w_uv = v[1]
               if dist[u_id] +  w_uv < dist[v_id]:
                   dist[v_id] = dist[u_id] + w_uv
                   heapq.heappush(PQ, [dist[v_id], v_id])
                   pred[v_id] = u_id

    if dist[target]==INF:
        stdout.write("There is no path between "+ source + " and " + target +"\n")
    else:
        st = []
        node = target
        while(True):
            st.append(str(node))
            if(node==pred[node]):
                break
            node = pred[node]
        path = st[::-1]
        stdout.write("The shortest path is: " + " ".join(path) + "\n\n")
       # stdout.write("The distance from ", +source, "to", +target, "is: " + str(dist[target]) + "\n\n")
        stdout.write("" + source  +"  "+ target + "   =   " + str(dist[target]) + "\n\n")
       # stdout.write("distance dictionary: " + str(dist) + "\n\n")
       # stdout.write("predecessor dictionary: " + str(pred))

#----------------------------------------------------------

def matricaSusjedstva(graph):
    edges = Graph(graph).edges()
    header = []
    for y in graph.keys():
        header.append(y)
    print(header);
    for y in graph.keys():
        print(edges[y])

if __name__ == "__main__":
    file = "MREZA_CESTOVNIH_PRAVACA.xlsx"
    current_path = os.path.abspath(os.path.dirname(__file__))
    data_path = os.path.join(current_path, "data")
    path = os.path.join(data_path, file)
    
    wb = xlrd.open_workbook(path)
    wb.sheet_names()
    sh = wb.sheet_by_index(0)
    i = 1

    graphDistance = {}
    graphDuration = {}
    for y in range(1, 39):
        start = sh.cell_value(y,0)
        start = start.rstrip()
        end = sh.cell_value(y,1)
        end = end.rstrip()
        road = sh.cell_value(y,2)
        distance = sh.cell_value(y,3)
        average_speed = sh.cell_value(y,4)
        #Preracun u trajanje voznje izrazen u minutama
        duration = distance/average_speed * 60
        if road:
            if start not in graphDistance.keys():
                graphDistance[start] = [((end, distance))]
                graphDuration[start] = [((end, duration))]
            else:
                graphDistance[start].append((end, distance))
                graphDuration[start].append((end, duration))

        if end not in graphDistance.keys():
            graphDistance[end] = []
            graphDuration[end] = []


    g = Graph(graphDistance)
    #1a
    print("\nLista susjedstva za graf otežan s udaljenošću u km")
    for key in graphDistance.keys():
        print(key)
        print(graphDistance[key])

    #1b
    print("\nLista susjedstva za graf otežan s trajanjem vožnje u minutama")
    for key in graphDuration.keys():
        print(key)
        print(graphDuration[key])

    #2
    #3

    #4
    print("\nBroj vrhova")
    print(len(Graph(graphDistance).vertices()))
    print("\nBroj bridova")
    print(len(Graph(graphDistance).edges()))
    print("\nSuma stupnjeva svih čvorova")
    sumDegree = 0;
    for i in Graph(graphDistance).degree_sequence():
        sumDegree = sumDegree + i;
    print(sumDegree)
    print("\nČvor s najvećim stupnjem")
    maxDegree = 0;
    maxNode = "";
    for node in graphDistance.keys():
        if g.vertex_degree(node) > maxDegree:
            maxDegree = g.vertex_degree(node)
            maxNode = node
    print(maxNode)

    #5
    #6
    #7
    print("\nNajkrači put s obzirom na udaljenost:")
    dijkstra(graphDistance, "PAKRAC", "ZAGREB")
    dijkstra(graphDistance, "PAKRAC", "VIROVITICA")
    dijkstra(graphDistance, "PAKRAC", "IVANIĆ GRAD")
    dijkstra(graphDistance, "PAKRAC", "ĐAKOVO")

    print("\nNajkrači put s obzirom na trajanje puta:")
    dijkstra(graphDuration, "PAKRAC", "ZAGREB")
    dijkstra(graphDuration, "PAKRAC", "VIROVITICA")
    dijkstra(graphDuration, "PAKRAC", "IVANIĆ GRAD")
    dijkstra(graphDuration, "PAKRAC", "ĐAKOVO")

    #8
    print("\nNajkrači put s obzirom na udaljenost:")
    dijkstra(graphDistance, "BJELOVAR", "VIROVITICA")
    dijkstra(graphDistance, "BJELOVAR", "IVANIĆ GRAD")
    dijkstra(graphDistance, "BJELOVAR", "KUTINA")

    print("\nNajkrači put s obzirom na trajanje puta:")
    dijkstra(graphDuration, "BJELOVAR", "VIROVITICA")
    dijkstra(graphDuration, "BJELOVAR", "IVANIĆ GRAD")
    dijkstra(graphDuration, "BJELOVAR", "KUTINA")
    
        
