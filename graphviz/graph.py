import os
import subprocess
from graphviz import Digraph
import json


graph_data = {
    "nodes": [
        {"id": "Science", "label": "Science\nعلم"},
        {"id": "System", "label": "System\nسیستم"},
        {"id": "Problem", "label": "Problem\nمسئله"},
        {"id": "Concept", "label": "Concept\nمفهوم"},
        {"id": "Framework", "label": "Framework\nچارچوب"},
        {"id": "Paradigm", "label": "Paradigm\nپارادایم"},
        {"id": "Architecture", "label": "Architecture\nمعماری"},
        {"id": "Pattern", "label": "Pattern\nالگو"},
        {"id": "Architectural Pattern", "label": "Architectural Pattern\nالگوی معماری"},
        {"id": "Model", "label": "Model\nمدل"},
        {"id": "Approach", "label": "Approach\nرویکرد"},
        {"id": "Hypothesis", "label": "Hypothesis\nفرضیه"},
        {"id": "Theorem", "label": "Theorem\nقضیه"},
        {"id": "Theory", "label": "Theory\nنظریه"},
        {"id": "Law", "label": "Law\nقانون"},
        {"id": "Principle", "label": "Principle\nاصل"},
        {"id": "Observation", "label": "Observation\nمشاهده"},
        {"id": "Data Collection", "label": "Data Collection\nجمع آوری داده"},
        {"id": "Data analysis", "label": "Data analysis\nتحلیل داده ها"},
        {"id": "Intuition", "label": "Intuition\nشهود"},
        {"id": "Experience", "label": "Experience\nتجربه"},
        {"id": "Test", "label": "Test\nآزمون"},
        {"id": "Quantitative and Qualitative Methods", "label": "Quantitative and Qualitative Methods\nروش‌های کمی و کیفی"},
        {"id": "Induction", "label": "Induction\nاستقرا"},
        {"id": "Deduction", "label": "Deduction\nقیاس"},
        {"id": "Inference", "label": "Inference\nاستنتاج"},
        {"id": "Research", "label": "Research\nپژوهش"}
    ],
    "edges": [
        {"source": "Science", "target": "System"},
        {"source": "System", "target": "Problem"},
        {"source": "Problem", "target": "Concept"},
        {"source": "Concept", "target": "Science"},
        {"source": "Framework", "target": "Paradigm"},
        {"source": "Architecture", "target": "Pattern"},
        {"source": "Pattern", "target": "Architectural Pattern"},
        {"source": "Architectural Pattern", "target": "Model"},
        {"source": "Model", "target": "Approach"},
        {"source": "Approach", "target": "Hypothesis"},
        {"source": "Hypothesis", "target": "Observation"},
        {"source": "Theorem", "target": "Theory"},
        {"source": "Theory", "target": "Law"},
        {"source": "Law", "target": "Principle"},
        {"source": "Observation", "target": "Data Collection"},
        {"source": "Data Collection", "target": "Data analysis"},
        {"source": "Data analysis", "target": "Intuition"},
        {"source": "Intuition", "target": "Experience"},
        {"source": "Experience", "target": "Test"},
        {"source": "Test", "target": "Quantitative and Qualitative Methods"},
        {"source": "Quantitative and Qualitative Methods", "target": "Induction"},
        {"source": "Induction", "target": "Deduction"},
        {"source": "Deduction", "target": "Inference"},
        {"source": "Inference", "target": "Research"}
    ]
}

with open('graph_data.json', 'w', encoding='utf-8') as f:
    json.dump(graph_data, f, ensure_ascii=False, indent=4)


output_file = 'high_res_graph'
g = Digraph('G', filename=output_file, format='png')
g.attr(dpi='300')  


for node in graph_data['nodes']:
    g.node(node['id'], label=node['label'])


for edge in graph_data['edges']:
    g.edge(edge['source'], edge['target'])


rendered_file = g.render()


print(f"Graph generated: {rendered_file}")
try:
    if os.name == 'nt':  
        os.startfile(rendered_file)
    elif os.name == 'posix':  
        subprocess.run(['open' if sys.platform == 'darwin' else 'xdg-open', rendered_file])
except Exception as e:
    print(f"Could not open the file: {e}")
