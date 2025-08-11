# toplogy_generator.py
import networkx as nx
import random
import matplotlib.pyplot as plt

DEVICE_CPES = [
    "cpe:2.3:a:microsoft:edge:-",
    "cpe:2.3:a:apache:log4j:2.14.1",
    "cpe:2.3:a:openssl:openssl:3.0.0",
    "cpe:2.3:a:oracle:mysql:8.0.0",
    "cpe:2.3:a:postgresql:postgresql:14.0",
    "cpe:2.3:a:mongodb:mongodb:5.0.0",
    "cpe:2.3:a:redis:redis:6.2.0",
    "cpe:2.3:a:nodejs:node:18.0.0",
    "cpe:2.3:a:python:python:3.10.0",
    "cpe:2.3:a:php:php:8.1.0",
    "cpe:2.3:a:jenkins:jenkins:2.346.0",
    "cpe:2.3:a:docker:docker_engine:20.10.0",
    "cpe:2.3:a:kubernetes:kubernetes:1.24.0",
    "cpe:2.3:a:elasticsearch:elasticsearch:8.3.0",
    "cpe:2.3:a:hashicorp:vault:1.11.0"
]

def build_graph(device_cpes=None):
    """Rastgele ama her düğümün en az iki bağlantısı olacak şekilde topoloji üretir"""
    if device_cpes is None:
        device_cpes = DEVICE_CPES

    G = nx.Graph()
    for cpe in device_cpes:
        G.add_node(cpe)

    n = len(device_cpes)

    # Halka şeklinde bağla
    for i in range(n):
        G.add_edge(device_cpes[i], device_cpes[(i+1) % n])

    # Ek bağlantılar ekle (her düğümün en az 2 komşusu olsun)
    for _ in range(n):
        a, b = random.sample(device_cpes, 2)
        if not G.has_edge(a, b):
            G.add_edge(a, b)

    return G

def draw_graph(G, title="IoT Network Topology"):
    """Topolojiyi görsel olarak çizer"""
    plt.figure(figsize=(10, 8))
    pos = nx.spring_layout(G, seed=42)
    nx.draw(
        G, pos,
        with_labels=True,
        node_size=2000,
        node_color="lightblue",
        font_size=8,
        font_weight="bold",
        edge_color="gray"
    )
    plt.title(title)
    plt.show()

def print_graph_info(G):
    """Graf hakkında genel bilgi verir"""
    print(f"🔹 Düğüm sayısı: {G.number_of_nodes()}")
    print(f"🔹 Kenar sayısı: {G.number_of_edges()}")
    print("🔹 Düğüm dereceleri:")
    for node, degree in G.degree():
        print(f"  {node}: {degree}")

def get_device_neighbors(G, device):
    """Belirli bir cihazın komşularını döndürür"""
    if device in G:
        return list(G.neighbors(device))
    else:
        return []

# Test amaçlı çalıştırma
if __name__ == "__main__":
    G = build_graph()
    print_graph_info(G)
    draw_graph(G)
