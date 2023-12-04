import re

from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import Static
from textual.widget import Widget

from bs4 import BeautifulSoup

import requests


class Contribution(Widget):

    contribution_level_to_color = {
        '0': 'white',
        '1': 'success-lighten-3',
        '2': 'success-lighten-1',
        '3': 'success-darken-1',
        '4': 'success-darken-3',
    }

    def __init__(
        self,
        user_url: str,
        *,
        name=None,
        id=None,
        classes=None,
    ):
        super().__init__(name=name, id=id, classes=classes)
        self.user_url = user_url

    def compose(self) -> ComposeResult:
        raw_request = requests.get(self.user_url)
        if raw_request.status_code != 200:
            return ""

        soup = BeautifulSoup(raw_request.content)
        rects = soup.find_all('td', attrs={'class': 'ContributionCalendar-day'})
        contributions = [rect.attrs['data-level'] for rect in rects if 'data-date' in rect.attrs]

        # contribution_regex = re.compile(r'(?P<number>\d{1,4}) contributions? on')
        total_contributions = 0
        for contribution in contributions:
            total_contributions += int(contribution)

        # for rect in [rect for rect in rects if rect.contents]:
            # search = re.search(contribution_regex, rect.contents[0])
            # if search:
            #     total_contributions += int(search.groupdict()['number'])

        yield Container(
            Static(str(total_contributions), classes='text-bold w-auto mr-2'),
            Static('contributions in the last year', classes='w-auto'),
            classes='mb-1 layout-horizontal h-auto w-auto',
        )

        for week_day_index in range(0, 7):
            # Filter contributions with a slice of every 7 contributions,
            # starting from the index of the week day considered (sunday = 0)
            week_day_contributions = contributions[week_day_index::7]
            yield Container(
                *[
                    Static("\u25a0", classes=f'{self.contribution_level_to_color[contribution_level]} w-auto mr-1')
                    for contribution_level in week_day_contributions
                ],
                classes='layout-horizontal h-auto w-auto',
            )
