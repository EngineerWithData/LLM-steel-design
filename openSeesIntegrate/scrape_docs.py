#!/usr/bin/env python3
"""
OpenSeesPy Documentation Scraper
Scrapes the OpenSeesPy documentation and converts it to clean Markdown files
organized by the documentation structure.
"""

import os
import re
import time
import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md
from urllib.parse import urljoin, urlparse
from pathlib import Path

BASE_URL = "https://openseespydoc.readthedocs.io/en/latest/"
OUTPUT_DIR = "openseespyDoc"

# Create output directory
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Track visited URLs to avoid duplicates
visited_urls = set()

def clean_filename(name):
    """Convert a title to a valid filename"""
    # Remove special characters and replace spaces with underscores
    name = re.sub(r'[<>:"/\\|?*]', '', name)
    name = name.strip().replace(' ', '_')
    return name

def get_page_content(url):
    """Fetch and parse a page"""
    if url in visited_urls:
        return None

    visited_urls.add(url)

    try:
        print(f"Fetching: {url}")
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        time.sleep(0.5)  # Be polite to the server
        return response.text
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

def extract_main_content(html):
    """Extract the main content area from the HTML"""
    soup = BeautifulSoup(html, 'html.parser')

    # Find the main content section
    content = soup.find('div', {'role': 'main'}) or soup.find('section')

    if not content:
        return None

    # Remove navigation elements, scripts, etc.
    for element in content.find_all(['script', 'style', 'nav', 'footer']):
        element.decompose()

    # Remove the "Edit on GitHub" and similar links
    for link in content.find_all('a', class_=['headerlink', 'reference external']):
        if 'headerlink' in link.get('class', []):
            link.decompose()

    return content

def html_to_markdown(html_content):
    """Convert HTML content to clean Markdown"""
    if not html_content:
        return ""

    # Convert to markdown
    markdown = md(str(html_content), heading_style="ATX", code_language="python")

    # Clean up the markdown
    # Remove excessive blank lines
    markdown = re.sub(r'\n{3,}', '\n\n', markdown)

    # Fix code block formatting
    markdown = re.sub(r'```\s*\n\s*```', '', markdown)

    return markdown.strip()

def extract_toc_structure(html):
    """Extract the table of contents structure from the sidebar"""
    soup = BeautifulSoup(html, 'html.parser')

    # Find the navigation menu
    nav = soup.find('div', class_='wy-menu')
    if not nav:
        return []

    toc = []
    current_section = None

    # Parse the TOC list
    for item in nav.find_all('li', class_='toctree-l1'):
        link = item.find('a', recursive=False)
        if link:
            title = link.get_text(strip=True)
            href = link.get('href', '')
            if href.startswith('../'):
                href = href[3:]  # Remove '../'

            section = {
                'title': title,
                'url': urljoin(BASE_URL, href) if href else None,
                'children': []
            }

            # Check for subsections
            subsections = item.find_all('li', class_='toctree-l2')
            for sub in subsections:
                sub_link = sub.find('a', recursive=False)
                if sub_link:
                    sub_title = sub_link.get_text(strip=True)
                    sub_href = sub_link.get('href', '')
                    if sub_href.startswith('../'):
                        sub_href = sub_href[3:]

                    subsection = {
                        'title': sub_title,
                        'url': urljoin(BASE_URL, sub_href) if sub_href else None,
                        'children': []
                    }

                    # Check for sub-subsections (level 3)
                    subsubsections = sub.find_all('li', class_='toctree-l3')
                    for subsub in subsubsections:
                        subsub_link = subsub.find('a', recursive=False)
                        if subsub_link:
                            subsub_title = subsub_link.get_text(strip=True)
                            subsub_href = subsub_link.get('href', '')
                            if subsub_href.startswith('../'):
                                subsub_href = subsub_href[3:]

                            subsection['children'].append({
                                'title': subsub_title,
                                'url': urljoin(BASE_URL, subsub_href) if subsub_href else None
                            })

                    section['children'].append(subsection)

            toc.append(section)

    return toc

def scrape_section(section, base_path, level=1):
    """Recursively scrape a section and its subsections"""
    # Create directory for this section
    section_name = clean_filename(section['title'])
    section_path = os.path.join(base_path, section_name)

    # Check if section has children
    has_children = 'children' in section and section['children']

    if has_children:
        os.makedirs(section_path, exist_ok=True)

    # Fetch and save the section content
    if 'url' in section and section['url']:
        html = get_page_content(section['url'])
        if html:
            content = extract_main_content(html)
            if content:
                markdown = html_to_markdown(content)

                # Save to file
                if has_children:
                    # If has children, save as README.md in the folder
                    filename = os.path.join(section_path, 'README.md')
                else:
                    # If no children, save as a single file
                    filename = os.path.join(base_path, f"{section_name}.md")

                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(f"# {section['title']}\n\n")
                    f.write(markdown)

                print(f"Saved: {filename}")

    # Process children
    if has_children:
        for child in section['children']:
            scrape_section(child, section_path, level + 1)

def main():
    """Main scraping function"""
    print("Starting OpenSeesPy documentation scraper...")
    print(f"Output directory: {OUTPUT_DIR}\n")

    # Fetch the index page to get the TOC structure
    index_html = get_page_content(BASE_URL + "index.html")
    if not index_html:
        print("Failed to fetch index page!")
        return

    # Extract TOC structure
    print("Extracting table of contents...")
    toc = extract_toc_structure(index_html)

    print(f"Found {len(toc)} main sections\n")

    # Create index README
    with open(os.path.join(OUTPUT_DIR, 'README.md'), 'w', encoding='utf-8') as f:
        f.write("# OpenSeesPy Documentation\n\n")
        f.write("This is a cleaned and organized version of the OpenSeesPy documentation.\n\n")
        f.write("## Contents\n\n")
        for i, section in enumerate(toc, 1):
            f.write(f"{i}. [{section['title']}](./{clean_filename(section['title'])}/README.md)\n")
            for j, subsection in enumerate(section['children'], 1):
                f.write(f"   {i}.{j}. {subsection['title']}\n")

    # Scrape each section
    for section in toc:
        print(f"\n=== Processing: {section['title']} ===")
        scrape_section(section, OUTPUT_DIR)

    print(f"\n\nDone! Scraped {len(visited_urls)} pages.")
    print(f"Documentation saved to: {OUTPUT_DIR}/")

if __name__ == "__main__":
    main()
