import pandas as pd
import requests
from bs4 import BeautifulSoup
import os

# Load the .xlsx file
file_path = 'Input.xlsx'
df = pd.read_excel(file_path, engine='openpyxl')

# Create a directory to save the .txt files
output_dir = 'scraped_articles'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Iterate through each row of the DataFrame
for index, row in df.iterrows():
    url_id = row['URL_ID']  # The first column contains URL_ID
    url = row['URL']  # The second column contains the URL
    
    # Fetch the webpage content
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP request errors
        
        # Parse the webpage content with BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract the article title
        title = soup.find('title').get_text() if soup.find('title') else 'No Title'
        
        # Extract the article text
        paragraphs = soup.find_all('p')  # Assuming article content is in <p> tags
        article_text = "\n".join([para.get_text() for para in paragraphs])
        
        # Save to a .txt file named after URL_ID inside the new folder
        file_name = os.path.join(output_dir, f'{url_id}.txt')
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write(f"Title: {title}\n\n")
            f.write(article_text)
        
        print(f"Successfully saved {file_name}")
    
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch {url}: {e}")