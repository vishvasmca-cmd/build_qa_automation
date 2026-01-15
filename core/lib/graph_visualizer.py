
import json
import os
import sys

def generate_visualization(graph_path):
    """
    Reads a GraphMemory JSON and outputs a Mermaid HTML file.
    """
    if not os.path.exists(graph_path):
        print(f"Error: File not found {graph_path}")
        return

    with open(graph_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    nodes = data.get("nodes", {})
    edges = data.get("edges", [])

    mermaid_graph = ["graph TD"]
    
    # 1. Define Nodes
    # Use short ID: "State 1", "State 2" mapping
    # Node Hash -> Short ID
    id_map = {}
    counter = 0
    
    for state_hash, node_data in nodes.items():
        counter += 1
        short_id = f"S{counter}"
        id_map[state_hash] = short_id
        
        # Label: Title + URL path
        url = node_data.get('url', '')
        # Simple path extraction
        path = url.split('.in/')[-1] if '.in/' in url else url.split('/')[-1]
        if not path: path = "Home"
        
        title = node_data.get('title', 'No Title')[:20].replace('"', '')
        label = f"{short_id}[{path}<br/><small>{title}</small>]"
        
        # Style
        if "dyson.in" not in url: 
             mermaid_graph.append(f"    style {short_id} fill:#f9f,stroke:#333,stroke-width:2px") # External
        
        mermaid_graph.append(f"    {label}")

    # 2. Define Edges
    for edge in edges:
        src = id_map.get(edge['from'])
        dst = id_map.get(edge['to'])
        
        if src and dst:
            action_text = edge['action'].get('target_text', 'Click')[:15].replace('"', '')
            mermaid_graph.append(f"    {src} -->|{action_text}| {dst}")

    # 3. Generate HTML
    mermaid_str = "\n".join(mermaid_graph)
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <body>
        <script type="module">
            import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
            mermaid.initialize({{ startOnLoad: true }});
        </script>
        <h2>Deep Explorer Map: {data.get('domain')}</h2>
        <div class="mermaid">
        {mermaid_str}
        </div>
    </body>
    </html>
    """
    
    output_path = graph_path.replace(".json", ".html")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)
        
    print(f"✅ Visualization generated: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python core/lib/graph_visualizer.py <path_to_graph_json>")
    else:
        generate_visualization(sys.argv[1])
