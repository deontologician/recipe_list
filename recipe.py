#!/usr/bin/env python2
from collections import namedtuple, defaultdict
from random import choice
from pprint import pprint

RECIPES = '''\
steamed carrots               | vegetable | medium
pureed peaches                | fruit     | medium
three bean chili              | main      | hard
white beans & tomatoes        | main      | medium
steamed sweet potatoes        | vegetable | medium
apple sauce                   | fruit     | easy
avocado                       | vegetable | easy
banana                        | fruit     | easy
pureed pears                  | fruit     | medium
pureed spinach                | vegetable | medium
chicken noodle soup           | main      | hard
oatmeal chicken broth         | main      | medium
oatmeal banana                | fruit     | easy
peanut butter                 | main      | easy
fingerling potatoes with dill | main      | medium
roasted vegetables            | vegetable | medium
steamed broccoli              | vegetable | medium
hardboiled eggs               | main      | medium
pita and hummus               | main      | easy
mozzarella                    | main      | easy
meatballs                     | main      | hard
'''

DIFFICULTY = {
    'easy': 1,
    'medium': 2,
    'hard': 3,
}

DOTW = {
    0: 'Monday',
    1: 'Tuesday',
    2: 'Wednesday',
    3: 'Thursday',
    4: 'Friday',
}

FoodItem = namedtuple('FoodItem', 'name category difficulty')
Menu = namedtuple('Menu', 'items hard_thing')

# RULES
# 1. 2 things per day
# 2. Can't have both be fruit
# 3. Can't have same thing 3 days in a row
# 4. The 2 things can't be the same
# 5. One kind of hard thing per week

class RecipeLookup(object):
    def __init__(self, contents=RECIPES):
        self.diff2items = defaultdict(list)
        self.name2item = {}
        self.cat2items = defaultdict(list)
        for line in contents.splitlines():
            if not line:
                continue
            name, category, difficulty = line.split('|')
            name = name.strip()
            category = category.strip()
            difficulty = DIFFICULTY[difficulty.strip()]
            item = FoodItem(name, category, difficulty)
            self.diff2items[difficulty].append(item)
            self.name2item[name] = item
            self.cat2items[category].append(item)
    @property
    def all_items(self):
        return self.name2item.values()

    def random_item(self):
        return choice(self.all_items)

    def same_thing_3_days_in_a_row(self, menu):
        on_a_streak = set()
        for (first, second) in menu.items:
            pass
        return False

    def suggest_menu(self):
        items = []
        hard_thing = None
        for i in range(0, 5):
            first = self.random_item()
            if hard_thing is not None and first.difficulty == 3:
                first = hard_thing
            elif hard_thing is None and first.difficulty == 3:
                hard_thing = first
            second = self.random_item()
            while (first.name == second.name or
                   first.category == second.category == 'fruit' or
                   first.difficulty == 3 and second.difficulty == 3):
                second = self.random_item()
            if hard_thing is None and second.difficulty == 3:
                hard_thing = second
            items.append((first, second))
        return Menu(items, hard_thing)

    def create_menu(self):
        menu = self.suggest_menu()
        while self.same_thing_3_days_in_a_row(menu):
            menu = self.suggest_menu()
        return menu


def main():
    rl = RecipeLookup()
    menu = rl.create_menu()
    if menu.hard_thing is None:
        print 'Nothing hard to make this week'
    else:
        print 'Hard thing:', menu.hard_thing.name

    for i, (first, second) in enumerate(menu.items):
        print DOTW[i], ':', first.name, 'and', second.name



if __name__ == '__main__':
    main()
