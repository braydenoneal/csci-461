from dataclasses import dataclass
import xml.dom.minidom
import json


@dataclass
class Node:
    node_id: int
    lat: float
    lon: float
    connections: list[int]


nodes: list[Node] = []

xml_doc = xml.dom.minidom.parse('map.xml')
root = xml_doc.documentElement

nodes_data = xml_doc.getElementsByTagName('node')

bottom = 37.0870
top = 37.4291
left = -93.6262
right = -93.0604

for node in nodes_data:
    node_id = int(node.getAttribute('id'))
    lat = (float(node.getAttribute('lat')) - bottom) / abs(top - bottom)
    lon = (float(node.getAttribute('lon')) - left) / abs(left - right)

    nodes.append(Node(node_id, lat, lon, []))

way_data = xml_doc.getElementsByTagName('way')

for way in way_data:
    connections = way.getElementsByTagName('nd')

    for i in range(len(connections) - 1):
        ref = int(connections[i].getAttribute('ref'))
        next_ref = int(connections[i + 1].getAttribute('ref'))

        for node in nodes:
            if node.node_id == ref:
                node.connections.append(next_ref)

with open('out.json', 'w', encoding='utf-8') as output_file:
    json.dump([node.__dict__ for node in nodes], output_file, ensure_ascii=False, indent=4)

