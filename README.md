# DASS Assignment 1

Rishav Kundu - 2019121007

## Controls

- `w a s`: up, left, right
- `q`: fire bullet (1s cooldown)
- `<space>`: activate shield, which prevents loss of lives (60s cooldown)
- `b`: speeds up the game

To exit, press `<Ctrl-C>`

## Functionality

- Collect coins to increase your score (1pt)
- Stay away from the fire beams. Otherwise lose one life when you touch a beam! You can also shoot the beams to get 5 points.
- Activate the shield to temporarily prevent losing lives!
- You have a total of 3 lives.
- Going near the magnets will pull you towards them!
- You cannot destroy the magnet and neither will the shield protect you from it!
- The final boss has 5 health.

## Cool features

I calculate the actual fps and compare it to the expected fps. Quite a stark difference is observable, implying that my code is not very efficient :P

## Game architecture overview

- I keep a list of all entities in the game.
- On every tick, I
  - clear the draw buffer
  - call the tick() and render() methods on all entities.

## OOPS overview

- Inheritance: All objects in the game inherit from a common Entity class. The Snowballs fired by the boss are derived from Mando's bullets.

- Polymorphism: The game loop does not care about the types of individual objects, meaning that all objects have a common tick() and render() API and can be rendered without object specific knowledge.

- Encapsulation: Underscored variables have been used to denote private APIs. Corresponding getters/setters are provided.

- Abstraction: As such there is no abstraction, as each entity takes care of its own internal operations and doesn't expose any operations such as `move()` or `attack()`. However, my API design wherein every entity is reduced to its `render()` and `tick()` method is a good example of abstraction in the system. Some other smaller examples like Mando's decrement_life() exist as well.

## Module Overview

- beam.py: represents the Beam entity
- bullet.py: represents the Bullet entity and contains functionality to check collisions, etc.
- coin.py: coins
- entity.py: contains the parent class of all entities in the game. decleares the abstract methods render and tick and also defines the protected position variables x and y
- floor.py: floor and sky
- magnet.py: magnets
- mando.py: mando and associated collision logic as well as movement logic and interaction with the magnet
- screen.py: an interface for drawing to the screen via a buffer
- main.py: contains the main Game class which stores several game attributes. Also responsible for running the main game loop

## Improvements

- Better class design - Right now, a couple of classes have too much functionality inside their `render()` methods, which should ideally be decomposed into smaller methods. For example, mando's render should be reduced into move, attack, shield, etc. methods.

- Performance - I clear the game buffer on every tick. This is not very efficient computationally.

## ASCII art credits

- Brick Wall: https://ascii.co.uk/art/brickwall

- Dragon ASCII art: John VanderZwaag
