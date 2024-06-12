import requests
from bs4 import BeautifulSoup, Tag
import pandas as pd
import json
from collections import Counter
from datetime import datetime
import re

# Function to read the URL from config.json
def read_config():
    with open('config.json', 'r') as file:
        config = json.load(file)
    return config['url']

# Function to fetch HTML content
def fetch_html(url):
    response = requests.get(url)
    return response.text

# Function to parse HTML and gather data
def analyze_dom(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    # Initialize counters and storage for data
    tag_counter = Counter()
    depth_counter = Counter()
    attribute_counter = Counter()
    inline_styles = []
    data_attributes = []
    empty_elements = []
    css_classes = Counter()
    ids = Counter()

    # Helper function to analyze each element
    def analyze_element(element, depth):
        tag_counter[element.name] += 1
        depth_counter[depth] += 1

        # Attributes
        for attr, value in element.attrs.items():
            attribute_counter[attr] += 1
            if attr == 'style':
                inline_styles.append(value)
            elif attr.startswith('data-'):
                data_attributes.append(value)
            elif attr == 'class':
                css_classes.update(value)
            elif attr == 'id':
                ids[value] += 1

        # Check for empty elements
        if not element.get_text(strip=True):
            empty_elements.append(element.name)

        # Recursively analyze children
        for child in element.children:
            if isinstance(child, Tag):
                analyze_element(child, depth + 1)

    # Analyze the entire DOM starting from the root
    analyze_element(soup, 0)

    # Prepare data for output
    data = {
        'Total Elements': sum(tag_counter.values()),
        'Max Depth': max(depth_counter.keys()),
        'Most Common Tags': tag_counter.most_common(10),
        'Attributes Count': attribute_counter.most_common(),
        'Inline Styles Count': len(inline_styles),
        'Data Attributes Count': len(data_attributes),
        'Empty Elements Count': len(empty_elements),
        'Most Common CSS Classes': css_classes.most_common(10),
        'Most Common IDs': ids.most_common(10),
        'All CSS Classes': css_classes.most_common(),
        'All IDs': ids.most_common()
    }

    return data

# Function to save counts to DataFrame
def save_counts_to_df(counter_data):
    df = pd.DataFrame(counter_data, columns=['Element', 'Count'])
    return df

# Function to generate a valid filename
def generate_filename(url):
    url_base = re.sub(r'[^a-zA-Z0-9]', '', url)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{url_base}_{timestamp}.xlsx"

# Main function
def main():
    url = read_config()
    html_content = fetch_html(url)
    data = analyze_dom(html_content)
    
    # Save counts to DataFrames
    df_common_tags = save_counts_to_df(data['Most Common Tags'])
    df_attributes_count = save_counts_to_df(data['Attributes Count'])
    df_common_css_classes = save_counts_to_df(data['Most Common CSS Classes'])
    df_common_ids = save_counts_to_df(data['Most Common IDs'])
    df_all_css_classes = save_counts_to_df(data['All CSS Classes'])
    df_all_ids = save_counts_to_df(data['All IDs'])

    # Save other information to a text DataFrame
    text_data = {
        'Info': [
            f"Total Elements: {data['Total Elements']}",
            f"Max Depth: {data['Max Depth']}",
            f"Inline Styles Count: {data['Inline Styles Count']}",
            f"Data Attributes Count: {data['Data Attributes Count']}",
            f"Empty Elements Count: {data['Empty Elements Count']}"
        ]
    }
    df_text = pd.DataFrame(text_data)

    # Create a single Excel file with multiple sheets
    filename = generate_filename(url)
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        df_text.to_excel(writer, sheet_name='DOM Analysis Info', index=False)
        df_common_tags.to_excel(writer, sheet_name='Common Tags', index=False)
        df_attributes_count.to_excel(writer, sheet_name='Attributes Count', index=False)
        df_common_css_classes.to_excel(writer, sheet_name='Common CSS Classes', index=False)
        df_common_ids.to_excel(writer, sheet_name='Common IDs', index=False)
        df_all_css_classes.to_excel(writer, sheet_name='All CSS Classes', index=False)
        df_all_ids.to_excel(writer, sheet_name='All IDs', index=False)

    print(f"DOM analysis saved to {filename}")

# Example usage
if __name__ == "__main__":
    main()