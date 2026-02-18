import base64
import io
from PIL import Image

def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def create_html_with_graphs(graph1_path, graph2_path, output_path):
    # Read the template
    with open('graphs.html', 'r', encoding='utf-8') as file:
        html_content = file.read()
    
    # Convert images to base64
    graph1_base64 = image_to_base64(graph1_path)
    graph2_base64 = image_to_base64(graph2_path)
    
    # Replace placeholders with actual base64 data
    html_content = html_content.replace('{{graph1_base64}}', graph1_base64)
    html_content = html_content.replace('{{graph2_base64}}', graph2_base64)
    
    # Save the final HTML
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(html_content)
    
    print(f"HTML file created at: {output_path}")

if __name__ == "__main__":
    # Save the graphs as PNG files first
    import matplotlib.pyplot as plt
    
    # Save the graphs (you'll need to replace this with your actual graph generation code)
    # For now, I'll create a simple example
    plt.figure(figsize=(10, 6))
    plt.plot([1, 2, 3, 4], [1, 4, 2, 3])
    plt.title('Example Graph 1')
    plt.savefig('graph1.png')
    plt.close()
    
    plt.figure(figsize=(10, 6))
    plt.pie([65.3, 31.6, 3.1], labels=['0-5 years', '5-17 years', '18+ years'], autopct='%1.1f%%')
    plt.title('Example Graph 2')
    plt.savefig('graph2.png')
    
    # Generate the HTML with the graphs
    create_html_with_graphs('graph1.png', 'graph2.png', 'aadhaar_dashboard.html')
