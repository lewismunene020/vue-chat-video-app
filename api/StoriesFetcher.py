from bs4 import BeautifulSoup
import requests

class StoryFetcher:
    def __init__(self):
        self.base_url = "https://www.bbc.com"
        self.topics = {
            'technology': '/news/technology',
            'design': '/news/technology/design',
            'agriculture': '/news/technology/agriculture',
            'coding': '/news/technology/coding'
        }

    def fetch_stories(self, topic: str) -> List[Dict[str, str]]:
        url = f"{self.base_url}{self.topics[topic]}"
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        stories = []
        for story in soup.find_all('li', class_='gs-c-promo-default'):
            stories.append({
                'title': story.find('h3').get_text(),
                'image': story.find('img')['src'],
                'description': story.find('p').get_text(),
                'link': f"{self.base_url}{story.find('a')['href']}"
            })
        return stories
