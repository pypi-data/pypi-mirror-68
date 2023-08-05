# ryze
League of Legends Games Update Unofficial API wrapper. Scraper included for page content.

## Installation
 - `$ pip install ryze`
 

## Example
```python
import json

from ryze import get_game_updates

# get all the game updates page data
game_updates_page = get_game_updates('en-us')

# print the game updates page title
print(game_updates_page.title)

# Updates for LOL start with 'Patch' word, so we filter for it
league_updates = game_updates_page.updates.by_title_name_re(r'^Patch')

# loop over all updates
for update in league_updates:
    with open(f'patches/{update.title}.json', 'w') as f:
        f.write(json.dumps(update.get_full_data().patch.parse_content()))
```
 
## Endorsement
lcu-driver isn’t endorsed by Riot Games and doesn’t reflect the views or opinions of Riot Games or anyone officially involved in producing or managing League of Legends. League of Legends and Riot Games are trademarks or registered trademarks of Riot Games, Inc. League of Legends © Riot Games, Inc.
