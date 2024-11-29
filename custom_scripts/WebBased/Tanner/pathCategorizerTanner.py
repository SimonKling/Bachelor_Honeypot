import os
import re
import json
from collections import defaultdict
from urllib.parse import unquote
import matplotlib.pyplot as plt

#  REGEX
categories = {
    'Root Path': re.compile(r'^\s*/\s*$', re.IGNORECASE),
    'Git Repository': re.compile(
        r'/\.git(?:/|$)|\.gitignore$|\.gitattributes$|/\.gitmodules$',
        re.IGNORECASE
    ),
    'WordPress': re.compile(
        r'wordpress|/wp-(?:content|admin|includes|login|config)\b|'
        r'wp-(?:login|config|cron|signup|links-opml|trackback|comments-post)\.php|'
        r'wp-blog-header\.php|wp-settings\.php',
        re.IGNORECASE
    ),
    'PHP related': re.compile(
        r'\.(?:php[\d]?|phar|phtml|inc|class\.php|module\.php|theme\.php)$',
        re.IGNORECASE
    ),
    '.exe Files': re.compile(
        r'\.(?:exe|apk|dll|sys|ps1|bat|msi|com)$',
        re.IGNORECASE
    ),
    'Bootstrap': re.compile(
        r'bootstrap|/bootstrap(?:\.min)?\.css|/bootstrap\.js|/bootstrap-theme\.css',
        re.IGNORECASE
    ),
    'Sensitive Paths': re.compile(
        r'/(?:admin|administrator|user|login|signin|signup|register|auth|dashboard|console|download)\b|'
        r'\.(?:env|aws|bak|old|swp|orig)$|'
        r'\b(config|credentials|password|database|db|dump|backup|shell|passwd|shadow|htpasswd)\b|'
        r'phpmyadmin|wp-config\.php|mysql|/assets/|actuator|cgi-bin',
        re.IGNORECASE
    ),
    'Harmless Paths': None  
}

excluded_paths = {
    '/favicon.ico', '/robots.txt', '/info.php', '/version',
    '/index.php', '/1.zip', '/a',
}

# BoatPoke
botpoke_paths = set()
with open('../full_list_PokeBot_URLs.txt', 'r') as botpoke_file:
    for line in botpoke_file:
        path = line.strip()
        if path and path not in excluded_paths:
            botpoke_paths.add(path)

def categorize_uri(uri, count, category_counts):
    uri = unquote(uri.strip())


#Prevent double checking 

    if categories['Root Path'].search(uri):
        category_counts['Root Path'] += count
        return

    if uri in botpoke_paths:
        category_counts['Botpoke'] += count
        return

    for category, pattern in categories.items():
        if pattern is not None and pattern.search(uri):
            category_counts[category] += count
            return

    category_counts['Other'] += count

input_dir = 'paths_tanner'    
output_dir = 'plots_output'   
os.makedirs(output_dir, exist_ok=True)

# Process each JSON file in the input directory
for filename in os.listdir(input_dir):
    if filename.endswith('_processed.json'):
        file_path = os.path.join(input_dir, filename)
        category_counts = defaultdict(int)

        with open(file_path, 'r', encoding='utf-8') as json_file:
            uri_counts = json.load(json_file)
            for uri, count in uri_counts.items():
                categorize_uri(uri, count, category_counts)


        sorted_categories = sorted(category_counts.items(), key=lambda x: x[1], reverse=True)
        categories_list = [item[0] for item in sorted_categories]
        counts_list = [item[1] for item in sorted_categories]
        
        
        
    
        plt.figure(figsize=(10, 6))
        bars = plt.bar(categories_list, counts_list, color='skyblue')
        plt.xlabel('Categories')
        plt.ylabel('Counts')
        plt.title(f'Category Counts for {filename}')
        plt.xticks(rotation=45)
        plt.tight_layout()

        for bar, count in zip(bars, counts_list):
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2.0, yval + 1, count, ha='center', va='bottom')

        # Save the plot to the output directory
        plot_filename = f"{os.path.splitext(filename)[0]}_category_counts.png"
        plot_path = os.path.join(output_dir, plot_filename)
        plt.savefig(plot_path)
        plt.close()
