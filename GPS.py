import xml.etree.ElementTree as ET
import math
from collections import defaultdict
import random



class Node:
    """
kuskasssssssssssssssssss GITTrieda reprezentujuca jeden nod. Mala by mat dobre definovane funckie __hash__ a __eq__ aby sme
ju vedeli davat do mnozin, dictov a porovnavat
"""

    def __init__(self, elem):
       self.ways=set()
       self.skuska='skuska2'
       #pozor, id je string, nie cislo!
       self.id=elem.attrib['id']
       self.lat=elem.attrib['lat']
       self.lon=elem.attrib['lon']
    
    def __hash__(self):
        return self.id.__hash__()
                
    def __eq__(self, other): 
        return self.id==other.id
        #TODO: rovnost by mala fungovat na baze id-ciek

    def __repr__(self):
        return "Node(id=%s, way=%s)"%(self.id, ', '.join({way.name for way in self.ways if way.name!='unnamed'}))

class Way:
    def __init__(self, elem):
       self.nodes=set()
       self.id=elem.attrib['id']
       try:
           self.name=elem.findall("./tag[@k='name']")[0].attrib['v']
       except Exception:
           self.name='unnamed'
       self.nodes=set()
       self.elem=elem

    def __hash__(self):
        return self.id.__hash__()

    def __eq__(self, other):
        return self.id==other.id      

    def __repr__(self):
        return "Way(id=%s, meno= %m)"%(self.id, self.name)

def dist(node1, node2):
    """
vrati vzdialenost dvoch nodov v metroch
"""

    lat1, lon1 = float(node1.lat),float(node1.lat)
    lat2, lon2 = float(node2.lat),float(node2.lat)
    radius = 6371 # km

    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c

    return d


    #TODO
    
def is_way(elem):
    """
vrati True, ak dany xml element popisuje motorovu cestu

"""
    motorways={'living_street', 'motorway_link', 'trunk', 'track', 'give_way', 'tertiary_link',
            'tertiary', 'motorway_junction', 'residential', 'secondary_link', 'service',
            'traffic_signals', 'trunk_link', 'primary', 'primary_link', 'raceway',
            'motorway', 'crossing', 'secondary'}
    typ_cesty=elem.findall("./tag[@k='highway']")
    if len(typ_cesty)>0:
            return typ_cesty[0].attrib['v'] in motorways
    else: 
            return False

    #TODO: zistit na zaklade xml elementu elem, ci sa jedna o motorovu cestu, hodi sa pouzit mnozinu
    #motorways

def graph_from_dict(graph_dict):
    """
creates graph from dict representration.

arguments:
graph_dict[vertex] is iterable of all (neighbour, distance) pairs

returns:
function acceptable by dijkstra function

"""
    def graph(vertex):
        return graph_dict[vertex]
    return graph

def dijkstra(graph, ver_start, ver_end):
    """
find optimal path between vertices ver_start and ver_end. Graph is function, that accepts vertex
and returns list of (neighbour, distance) pairs.

returns tuple (dist, path) where dist is optimal distance and path is sequence of vertices

the code is quite ugly and shouldn't be read by anyone!
"""
    #boundary and final have the following structure: {vertex: (distance, previous_vertex)} where
    #distance is the distance from node_start to vertex and previous_vertex is semi-last vertex on
    #the ver_start - vertext path optimal path.

    
    boundary={}
    final={}
    boundary[ver_start]=(0, None)
    while True:
        if not boundary:
            return None, None
        closest_ver, (closest_dist, prev_vertex) = min(boundary.items(), key=lambda item: item[1][0])
        final[closest_ver] = closest_dist, prev_vertex
        del boundary[closest_ver]
        for ver, dst in graph(closest_ver):
            if ver not in final:
                if ver not in boundary or boundary[ver][0]>closest_dist+dst:
                    boundary[ver]=(closest_dist+dst, closest_ver)
        if closest_ver == ver_end:
            break
    path=[ver_end]
    iterator=ver_end
    while not iterator is ver_start:
        iterator=final[iterator][1]
        path.append(iterator)

    return final[ver_end][0], path


if __name__=="__main__":
    tree = ET.parse('map.osm')
    #way=tree.findall(".//way")[0]

    all_ways={Way(elem) for elem in tree.findall(".//way") if is_way(elem)}
    all_nodes={Node(elem) for elem in tree.findall(".//node")}
    all_nodes_dict={node.id: node for node in all_nodes}
    #TODO; all_nod es_dicts je pomocna struktura, ktora mapuje node.id na prislusny
    #node object. zahrna vsetky nody z all_nodes
    graph_dict=defaultdict(set)

    for way in all_ways:
        elem_nodes=list(way.elem.findall(".//nd"))
        nodes = [all_nodes_dict[elem_node.attrib['ref']] for elem_node in elem_nodes]
        node_susedia=nodes[1:]
        for node,node_sused in zip(nodes,node_susedia):
            way.nodes.add(node)
            node.ways.add(way)

            graph_dict[node].add((node_sused, dist(node, node_sused)))
            #print(list(graph_dict.items())[0])

        #TODO: pridat node do way.nodes, way do node.ways
        #TODO: preiterovat cez susedov node1, node2 a pridat ich do graph_dict
                    
    #vyfiltrujeme nody patriace nejakej ulici
    all_street_nodes=[node for node in all_nodes if node.ways]

    graph=graph_from_dict(graph_dict)
    #najdeme nejake 2 nahodne nody, ktore patria nejakej ulici a hadam budu spojene
    node1=random.choice(all_street_nodes)
    node2=random.choice(all_street_nodes)
    print(dijkstra(graph, node1, node2))
    
