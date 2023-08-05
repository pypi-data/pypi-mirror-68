from bs4 import BeautifulSoup

SUPPORTED_CATEGORIES = ('champions', 'items')


def build_summoner_or_item(element):
    champion_element = element.find('h3')

    summary = element.find('p', class_='summary')
    summary_text = summary.text if summary else None

    quote = element.find('blockquote', class_='blockquote context')
    quote_text = quote.text if quote else None

    updates = []

    change_elements = element.find_all('h4', class_='change-detail-title')
    for change_element in change_elements:
        attributes = []
        for sibling in change_element.next_siblings:
            if sibling is not None and sibling.name == 'div':
                attributes.append({
                    'attribute': sibling.find('span', class_='attribute').text,
                    'change': {
                        'before': sibling.find('span', class_='attribute-before').text
                        if sibling.find('span', class_='attribute-before') else None,
                        'after': sibling.find('span', class_='attribute-after').text
                        if sibling.find('span', class_='attribute-after') else None
                    }
                })

        updates.append({
            'skill': change_element.text,
            'updates': attributes
        })
        if img := change_element.find('img'):
            updates[-1]['image_url'] = img['src']

    return {
        'name': champion_element.find('a').text,
        'info_url': champion_element.find('a')['href'],
        'summary': summary_text,
        'quote': quote_text,
        'changes': updates
    }


def parse(html):
    soup = BeautifulSoup(html, 'lxml')
    container = soup.find('div', id='patch-notes-container')

    parsed = {}
    category = None

    for element in container.find_all(recursive=False):
        if element.name == 'header':
            category = element.find('h2').text.lower().replace(' ', '_')
        if category is None:
            continue

        if element.name == 'div':
            if category not in parsed and category in SUPPORTED_CATEGORIES:
                parsed[category] = []

        if category in ('champions', 'items'):
            if change_block := element.find('div', class_='patch-change-block'):
                parsed[category].append(build_summoner_or_item(change_block))

    return parsed
