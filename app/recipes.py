from app import db
from app.model import Recipe, User

''' This file contains sample users and recipes. See README for instructions on how to add to database.'''

# Example user information
admin = User(email='forbairt.post@gmail.com',
             username='dev',
             password='cat',
             confirmed=True,
             )

eoghan = User(email='e.quinn27@nuigalway.ie',
              username='eoghan',
              password='eoghan',
              confirmed=True, )

john = User(email='john@sample.com',
            username='chefjohn',
            password='secretingredient',
            confirmed=True,
            )

malory = User(email='malory@nsa.com',
              username='badcook',
              password='letmein',
              confirmed=True,
              )

gordon = User(email='gordon@ramsey.com',
              username='yeschef',
              password='itsraw',
              confirmed=True,
              )

sample_users = [admin, eoghan, john, malory, gordon]


# Adds all users from sample_users
def add_all_users():
    for user in sample_users:
        if User.query.filter_by(username=user.username).first() is None:
            db.session.add(user)
            db.session.commit()


# Example recipes
waffle = Recipe(title='Waffles',
                ingredients='2 cups Flour, '
                            '2 Eggs,\n '
                            '1 tbs Butter(melted), '
                            '1 cup Milk,\n '
                            '0.5 cups Sugar,\n '
                            'pinch Cinnamon,\n '
                            '1 tsp Baking powder,\n '
                            'pinch salt.',
                method='Turn on waffle iron/press.\n'
                       'Sift together the dry ingredients in a bowl. \n'
                       'Whisk together the wet ingerdents in another bowl.\n'
                       'While stirring, slowly add the dry ingredients to the wet.\n'
                       'Cook the batter in batches on the waffle iron/press. \n'
                       'Cook until they reach a light golden colour.(approx 10 min)\n'
                       'Enjoy with delicious maple syrup or honey or nutella.',
                public=True,
                meal='Breakfast',
                author_id='eoghan',
                )

roast_chicken = Recipe(title='Roast Chicken',
                       ingredients='1 whole chicken,\n '
                                   '2 lemons,\n '
                                   'pepper,\n '
                                   'salt.',
                       method='Turn on oven 180C.\n'
                              'Salt and pepper chicken inside and out.\n'
                              'Wash lemons. \n'
                              'Roll on lemons surface and prick with a fork 10-20 times. \n'
                              'Insert lemons in chicken cavity.\n'
                              'Cook the chickens breast side down for 30 mins. \n'
                              'Flip the chicken on to back, raise oven temp to 220 and cook for another 20-35,\n'
                              'Ensure chicken is cooked to at least 74C before removing from oven. \n'
                              'Allow rest for 15 mins before serving.\n'
                              'Enjoy!',
                       public=True,
                       meal='Dinner',
                       author_id='dev', )

garlic_oil_pasta = Recipe(title='Garlic, olive oil and parsley pasta',
                          ingredients='500g Spaghetti, \n'
                                      '4 tbs Olive Oil\n'
                                      '4 cloves Garlic, \n'
                                      'bunch of Parsley,\n'
                                      'salt',
                          method='Cook pasta in boiling salted water for 8 mins,\n'
                                 'While pasta is cooking gently fry garlic in olive oil,\n'
                                 'Remove garlic once light golden colour and turn off heat,\n'
                                 'Drain pasta and add to frying pan,\n'
                                 'Add parsley, season with salt and toss to coat pasta,\n'
                                 'Serve immediately. ',
                          public=True,
                          meal='Dinner',
                          author_id='chefjohn',
                          )

white_russian = Recipe(title='White Russian',
                       ingredients='Vodka,\n '
                                   'Coffee liquer,\n'
                                   'Milk,\n'
                                   'Ice',
                       method='Fill a glass with ice\n'
                              'Add one measure of vodka and coffee liquer.\n'
                              'Top off with milk.\n'
                              'Enjoy',
                       public=True,
                       meal='Drink',
                       author_id='eoghan', )

cross_site_script_attempt = Recipe(title='<script>alert(‘XSS’)</script>',
                                   ingredients='<script>alert(‘Attack!’)</script>',
                                   method='<b onmouseover=alert(‘XSS testing!‘)></b>',
                                   public=True,
                                   meal='Drink',
                                   author_id='badcook', )

gordons_secret = Recipe(title='Top Secret Sauce',
                        ingredients='Buffalo sauce\n '
                                    'Butter',
                        method='Mix buffalo sauce and butter in saucepan and heat gently.\n'
                               'Enjoy over some crispy wings.',
                        public=False,
                        meal='Drink',
                        author_id='yeschef', )

sample_recipes = [waffle, roast_chicken, garlic_oil_pasta, white_russian, cross_site_script_attempt, gordons_secret]


# Adds all recipes from sample_recipes
def add_all_recipes():
    for recipe in sample_recipes:
        if Recipe.query.filter_by(title=recipe.title).first() is None:
            db.session.add(recipe)
            db.session.commit()



