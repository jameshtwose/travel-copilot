import json
from bs4 import BeautifulSoup

def extract_events(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    events = []

    result_items = soup.find_all('div', class_='result-item')
    for item in result_items:
        title = item.find('h2', class_='result-item__title').get_text(strip=True)
        date = item.find('span', class_='event-dates__item').get_text(strip=True)
        description = item.find('section', class_='result-item__summary').get_text(strip=True)
        
        events.append({
            'title': title,
            'date': date,
            'description': description
        })

    return json.dumps(events, indent=4)

# Example usage
with open('data/visit_lisboa.html', 'r') as file:
    html_content = file.read()

events_json = extract_events(html_content)

with open('data/visit_lisboa.json', 'w') as file:
    file.write(events_json)