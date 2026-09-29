"""Draw the lab topology to docs/topology.png (the Packet Tracer build follows this layout)."""
import matplotlib.pyplot as plt
import networkx as nx

nodes = {  # name: (x, y, kind, label)
    "ISP-R3": (5, 6, "router", "ISP-R3\n198.51.100.1"),
    "Internet-SRV": (8.2, 6, "server", "Internet server\n203.0.113.10\nDNS + www.example.com"),
    "HQ-R1": (5, 4.2, "router", "HQ-R1\nNAT · DHCP · ACLs · OSPF"),
    "SRV-R2": (8.2, 4.2, "router", "SRV-R2\nOSPF"),
    "HQ-SW1": (5, 2.4, "switch", "HQ-SW1\nVLAN 10/20/40/99"),
    "SRV-SW2": (8.2, 2.4, "switch", "SRV-SW2\nVLAN 30"),
    "Staff": (2.6, 0.6, "pc", "Staff PCs\nVLAN 10\n192.168.10.0/25"),
    "Students": (4.3, 0.6, "pc", "Student PCs\nVLAN 20\n192.168.10.128/26"),
    "Guest": (6.0, 0.6, "pc", "Guest laptop\nVLAN 40\n192.168.10.224/28"),
    "DNS": (7.6, 0.6, "server", "SRV-DNS\n192.168.10.194"),
    "WEB": (9.2, 0.6, "server", "SRV-WEB\n192.168.10.195"),
}
links = [
    ("ISP-R3", "HQ-R1", "198.51.100.0/30\n(NAT outside)"),
    ("ISP-R3", "Internet-SRV", "203.0.113.0/24"),
    ("HQ-R1", "SRV-R2", "WAN 192.168.10.248/30\nOSPF area 0"),
    ("HQ-R1", "HQ-SW1", "802.1Q trunk"),
    ("SRV-R2", "SRV-SW2", "192.168.10.192/27"),
    ("HQ-SW1", "Staff", ""), ("HQ-SW1", "Students", ""), ("HQ-SW1", "Guest", ""),
    ("SRV-SW2", "DNS", ""), ("SRV-SW2", "WEB", ""),
]
style = {"router": ("#3a6ea5", "o"), "switch": ("#2a9d8f", "s"), "pc": ("#8d99ae", "D"), "server": ("#e76f51", "h")}

g = nx.Graph()
g.add_edges_from((a, b) for a, b, _ in links)
pos = {n: (x, y) for n, (x, y, *_) in nodes.items()}
fig, ax = plt.subplots(figsize=(12, 8))
ax.add_patch(plt.Rectangle((1.6, -0.4), 5.3, 5.3, fill=False, ls="--", ec="#3a6ea5", lw=1.2))
ax.text(1.7, 4.75, "HQ campus", color="#3a6ea5", fontsize=11, weight="bold")
ax.add_patch(plt.Rectangle((7.0, -0.4), 2.9, 5.3, fill=False, ls="--", ec="#e76f51", lw=1.2))
ax.text(7.1, 4.75, "Server site", color="#e76f51", fontsize=11, weight="bold")
nx.draw_networkx_edges(g, pos, ax=ax, width=2, edge_color="#555")
for a, b, t in links:
    (x1, y1), (x2, y2) = pos[a], pos[b]
    if t and x1 == x2:  # vertical link: label to the right, clear of node labels
        ax.text(x1 + 0.15, (y1 + y2) / 2 - 0.25, t, ha="left", va="center", fontsize=8, color="#333")
    elif t:
        ax.text((x1 + x2) / 2, y1 + 0.12, t, ha="center", va="bottom", fontsize=8, color="#333")
for kind, (color, marker) in style.items():
    members = [n for n, v in nodes.items() if v[2] == kind]
    nx.draw_networkx_nodes(g, pos, nodelist=members, node_color=color, node_shape=marker, node_size=900, ax=ax)
for n, (x, y, _, label) in nodes.items():
    ax.text(x, y - 0.42, label, ha="center", va="top", fontsize=8.5, bbox={"fc": "white", "ec": "none", "pad": 1.5})
ax.set_title("Campus network topology: 2 sites, 5 VLANs, OSPF, NAT to a simulated ISP", fontsize=13)
ax.set_xlim(1.3, 10.2); ax.set_ylim(-1.2, 6.8); ax.axis("off")
fig.tight_layout(); fig.savefig("docs/topology.png", dpi=110)
