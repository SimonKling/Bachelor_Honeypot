import os
import csv
import re
from collections import defaultdict
import matplotlib.pyplot as plt
from urllib.parse import unquote  


#REGEX

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
    'bootsrap': re.compile(
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

botpoke_paths = set()
with open('../full_list_PokeBot_URLs.txt', 'r') as botpoke_file:
    for line in botpoke_file:
        path = line.strip()
        if path and path not in excluded_paths: 
            botpoke_paths.add(path)

def categorize_uri(uri, count, category_counts, botpoke_matches):
    uri = unquote(uri.strip()) 
    
    if uri in excluded_paths:
        return


    if categories['Root Path'].search(uri):
        category_counts['Root Path'] += count
        return

    if uri in botpoke_paths:
        category_counts['Botpoke'] += count
        botpoke_matches.append(uri)
        return

    matched = False
    for category, pattern in categories.items():
        if pattern is not None and pattern.search(uri):
            category_counts[category] += count
            matched = True
            break

    if not matched:
        category_counts['Other'] += count

def process_csv_file(file_path):
    category_counts = defaultdict(int)
    botpoke_matches = []  
    with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if not row or row.get('Request Path', '').strip().startswith('#'):
                continue

            uri = row.get('Request Path', '').strip()
            count_part = row.get('Count', '1').strip()

            try:
                count = int(count_part)
            except ValueError:
                continue

            categorize_uri(uri, count, category_counts, botpoke_matches)
    return category_counts, botpoke_matches

def plot_category_counts(category_counts, output_path, title):
    sorted_categories = sorted(category_counts.items(), key=lambda x: x[1], reverse=True)
    categories_list = [item[0] for item in sorted_categories]
    counts_list = [item[1] for item in sorted_categories]


     # Plot Generation

    plt.figure(figsize=(10, 6))
    bars = plt.bar(categories_list, counts_list, color='skyblue')
    plt.xlabel('Categories')
    plt.ylabel('Counts')
    plt.title(title)
    plt.xticks(rotation=45)
    plt.tight_layout()

    for bar, count in zip(bars, counts_list):
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2.0, yval + 1, count, ha='center', va='bottom')

    plt.savefig(output_path)
    plt.close()

input_folder = "output"
plot_output_folder = "plots"
os.makedirs(plot_output_folder, exist_ok=True)

processed_files = 0
for filename in os.listdir(input_folder):
        if filename.endswith('.csv'):
            file_path = os.path.join(input_folder, filename)
            category_counts, botpoke_matches = process_csv_file(file_path)

            plot_file = os.path.join(plot_output_folder, f"{os.path.splitext(filename)[0]}_category_counts.png")
            plot_category_counts(category_counts, plot_file, f"Category Counts")

            processed_files += 1
