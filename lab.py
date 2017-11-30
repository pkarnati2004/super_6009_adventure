# -*- coding: utf-8 -*-
## 6.009 -- Fall 2017 -- Lab 9
#  Time spent on the lab:
#    Week 1: ...
#    Week 2: ...

class Textures:
    """A collection of object textures.

    Each constant in this class describes one texture, and
    single-letter texture names are also used in level maps.
    For example, the letter "e" in a game level map indicates
    that there is a bee at that position in the game.

    To add support for a new blob type, or to add a new texture
    for an existing blob, you'll probably want to update this
    list and the TEXTURE_MAP list in ``Constants``.
    """
    Bee = "e"
    Boat = "b"
    Building = "B"
    Castle = "C"
    Cloud = "c"
    Fire = "f"
    Fireball = "F"
    Floor = "="
    Helicopter = "h"
    Mushroom = "m"
    Player = "p"
    PlayerBored = "bored"
    PlayerFlying = "h"
    PlayerLost = "defeat"
    PlayerWon = "victory"
    Rain = "r"
    Storm = "s"
    Sun = "o"
    Tree = "t"
    Water = "w"

class Constants:
    """A collection of game-world constants.

    You can experiment with tweaking these constants, but
    remember to revert the changes when running the test suite!
    """
    TILE_SIZE = 128
    GRAVITY = -9
    MAX_DOWNWARDS_SPEED = 48

    PLAYER_DRAG = 6
    PLAYER_MAX_HORIZONTAL_SPEED = 48
    PLAYER_HORIZONTAL_ACCELERATION = 16
    PLAYER_JUMP_SPEED = 62
    PLAYER_JUMP_DURATION = 3
    PLAYER_BORED_THRESHOLD = 60

    STORM_LIGHTNING_ROUNDS = 5
    STORM_RAIN_ROUNDS = 10

    BEE_SPEED = 40
    MUSHROOM_SPEED = 16
    FIREBALL_SPEED = 60

    SUN_POWER = 5

    TEXTURE_MAP = {Textures.Bee: '1f41d',
                   Textures.Boat: '26f5',
                   Textures.Building: '1f3e2',
                   Textures.Castle: '1f3f0',
                   Textures.Cloud: '2601',
                   Textures.Fire: '1f525',
                   Textures.Fireball: '1f525',
                   Textures.Floor: '2b1b',
                   Textures.Helicopter: '1f681',
                   Textures.Mushroom: '1f344',
                   Textures.Player: '1f60a',
                   Textures.PlayerBored: '1f634',
                   Textures.PlayerFlying: '1f681',
                   Textures.PlayerLost: '1f61e',
                   Textures.PlayerWon: '1f60e',
                   Textures.Rain: '1f327',
                   Textures.Storm: '26c8',
                   Textures.Sun: '2600',
                   Textures.Tree: '1f333',
                   Textures.Water: '1f30a'}

class Rectangle:
    """A rectangle object to help with collision detection and resolution."""

    def __init__(self, x, y, w, h):
        """Initialize a new rectangle.

        `x` and `y` are the coordinates of the bottom-left corner. `w`
        and `h` are the dimensions of the rectangle.
        """
        self.x, self.y = x, y
        self.w, self.h = w, h

    def intersects(self, other):
        """Check whether `self` and `other` overlap.

        Rectangles are open on the top and right sides, and closed on
        the bottom and left sides; concretely, this means that the
        rectangle [0, 0, 1, 1] does not intersect either of [0, 1, 1, 1]
        or [1, 0, 1, 1].
        """
        # raise NotImplementedError

        # check corners from left
        if self.x < other.x:
            if (self.x + self.w) > other.x:
                if self.y < other.y:
                    if (self.y + self.h) > other.y:
                        return True
                elif self.y < (other.y + other.h):
                    return True
        
        # check corners from right
        elif self.x < (other.x + other.w):
            if self.y < other.y:
                if other.y < (self.y + self.h):
                    return True
            elif self.y < (other.y + other.h):
                return True

        
        return False

    @staticmethod
    def translationvector(r1, r2):
        """Compute how much `r2` needs to move to stop intersecting `r1`.

        If `r2` does not intersect `r1`, return ``None``.  Otherwise,
        return a minimal pair ``(x, y)`` such that translating `r2` by
        ``(x, y)`` would suppress the overlap. ``(x, y)`` is minimal in
        the sense of the "L1" distance; in other words, the sum of
        ``abs(x)`` and ``abs(y)`` should be as small as possible.

        When two pairs ``(x, y)`` and ``(y, x)`` are tied, return the
        one whose first element has the smallest magnitude.
        """
        # raise NotImplementedError
        if not r1.intersects(r2):
            return None

        right = r1.x + r1.w - r2.x
        left = -(r2.x + r2.w - r1.x)
        up = r1.y + r1.h - r2.y
        down = -(r2.y + r2.h - r1.y)

        # y min
        min_val = float('inf')
        miny = None
        for y in (up, down):
            if 0 + abs(y) < min_val:
                min_val = 0 + abs(y)
                miny = y
        # print(0, miny)

        # x min
        min_val = float('inf')
        minx = None
        for x in (left, right):
            if abs(x) + 0 < min_val:
                min_val = abs(x) + 0
                minx = x
        # print(minx, 0)

        # print(right, left, up, down)

        if sum([abs(minx), 0]) == sum([0, abs(miny)]):
            if abs(minx) < abs(0):
                return (minx, 0)
            else:
                return (0, miny)
        elif sum([abs(minx), 0]) < sum([0, abs(miny)]):
            return (minx, 0)
        else:
            return (0, miny)
        
        return 'hello'



    def __str__(self):
        return 'x: ' + str(self.x) + ' y: ' + str(self.y) + ' w: ' + str(self.w) + ' h: ' + str(self.h)

r1, r2 = Rectangle(0, 119, 128, 128), Rectangle(0, 0, 128, 128)
print(r2.intersects(r1))

class Blob:
    """ a blob class to handle objects in the game """
    def __init__(self, name, texture, x, y, w, h):
        """ 
        initialize variables 
        """
        self.name = name
        self.texture = texture
        self.vertical = 0
        self.horizontal = 0
        self.bbox = Rectangle(x, y, w, h)
        self.pos = [x,y]
        self.hard = True
        self.gravity = False
    
    def get_x(self):
        """ 
        get x pos 
        """
        return self.bbox.x

    def get_y(self):
        """ 
        get y pos
        """
        return self.bbox.y

    def set_x(self, x):
        """
        change x pos
        """
        self.pos[0] = x
        self.bbox.x = x

    def set_y(self, y):
        """
        change y pos
        """
        self.pos[1] = y
        self.bbox.y = y

    def resting(self, blobs):
        """
        if this is a soft blob, determines whether it is resting
        on a hard blob
        """
        # for all of the blobs, if it is a hard blob, check if 
        # y position of self - TILE == blob y aka it is resting
        for b in blobs:
            if b.hard:
                if self.pos[1] - Constants.TILE_SIZE == b.pos[1]:
                    return True
        return False

    def __str__(self):
        return self.name + ' at position ' + str(self.pos)

class Game:
    def __init__(self, levelmap):
        """Initialize a new game, populated with objects from `levelmap`.

        `levelmap` is a 2D array of 1-character strings; all possible
        strings (and some others) are listed in the ``Textures`` class.
        Each character in `levelmap` corresponds to a blob of size
        ``TILE_SIZE * TILE_SIZE``.

        This function is free to store `levelmap`'s data however it
        wants.  For example, it may choose to just keep a copy of
        `levelmap`; or it could choose to read through `levelmap` and
        extract the position of each blob listed in `levelmap`.

        Any choice is acceptable, as long as it plays well with the
        implementation of ``timestep`` and ``render`` below.
        """
        # raise NotImplementedError

        # a list of lists, with chars to positions
        self.characters = []
        self.player = []
        self.hard = ['B', 'C', 'c', '=', 's', 't', 'w']
        self.hard_blobs = []
        self.soft_blobs = []
        self.gravity = ['f', 'h', 'm', 'p', 'o']

        rev = reversed(levelmap)
        # get chars
        x, y = 0, 0
        for line in rev:
            x = 0
            for char in line:
                if char == 'p':
                    self.player = Blob(char, Constants.TEXTURE_MAP[char], x, y, Constants.TILE_SIZE, Constants.TILE_SIZE)
                    self.player.hard = False
                    self.player.gravity = True
                    self.soft_blobs.append(self.player)
                elif char != ' ':
                    character = Blob(char, Constants.TEXTURE_MAP[char], x, y, Constants.TILE_SIZE, Constants.TILE_SIZE)
                    if char in self.hard:
                        character.hard = True
                    if char in self.gravity:
                        character.gravity = True
                    self.characters.append(character)
                    if character.hard:
                        self.hard_blobs.append(character)
                    else:
                        self.soft_blobs.append(character)
                x += Constants.TILE_SIZE
            y += Constants.TILE_SIZE
        

    def timestep(self, keys):
        """Simulate the evolution of the game state over one time step.
        `keys` is a list of currently pressed keys."""
        # raise NotImplementedError
        
        # player events

        horizontal_acceleration = 0
        if keys:
            for event in keys:
                if event == 'up':
                    self.player.vertical = Constants.PLAYER_JUMP_SPEED
                elif event == 'left':
                    horizontal_acceleration = -Constants.PLAYER_HORIZONTAL_ACCELERATION
                elif event == 'right':
                    horizontal_acceleration = Constants.PLAYER_HORIZONTAL_ACCELERATION

        horizontal, drag = self.player.horizontal + horizontal_acceleration, 0
        if horizontal < 0:
            drag = Constants.PLAYER_DRAG
            if drag > abs(horizontal): drag = horizontal
        elif horizontal > 0:
            drag = -Constants.PLAYER_DRAG
            if abs(drag) > horizontal: drag = -horizontal

        horizontal += drag
        
        if horizontal < 0 and horizontal < -Constants.PLAYER_MAX_HORIZONTAL_SPEED:
            diff = -Constants.PLAYER_MAX_HORIZONTAL_SPEED - horizontal
            horizontal += diff
        elif horizontal > 0 and horizontal > Constants.PLAYER_MAX_HORIZONTAL_SPEED:
            diff = Constants.PLAYER_MAX_HORIZONTAL_SPEED - horizontal
            horizontal += diff

        self.player.horizontal = horizontal
        self.player.set_x(self.player.get_x() + self.player.horizontal)

        if self.player.vertical + Constants.GRAVITY > -Constants.MAX_DOWNWARDS_SPEED:
            self.player.vertical += Constants.GRAVITY
        else:
            diff = -Constants.MAX_DOWNWARDS_SPEED - self.player.vertical
            self.player.vertical += diff
        self.player.set_y(self.player.get_y() + self.player.vertical)



        # other character events

        for char in self.characters:
            if not char.hard:
                if char.vertical + Constants.GRAVITY > -Constants.MAX_DOWNWARDS_SPEED:
                    char.vertical += Constants.GRAVITY
                else:
                    diff = -Constants.MAX_DOWNWARDS_SPEED - char.vertical
                    char.vertical += diff



        
        # # collison resolution

        

        # for soft in self.soft_blobs:
        #     for hard in self.hard_blobs:
        #         if soft.bbox.intersects(hard.bbox):
        #             (deltax, deltay) = Rectangle.translationvector(hard.bbox, soft.bbox)
        #             soft.set_x(soft.bbox.x+ deltax)
        #             soft.set_y(soft.bbox.y+ deltay)


        # vertical collisions first
        for soft in self.soft_blobs:
            for hard in self.hard_blobs:
                if soft.bbox.intersects(hard.bbox):
                    (deltax, deltay) = Rectangle.translationvector(hard.bbox, soft.bbox)
                    if deltax == 0:
                        soft.set_x(soft.bbox.x+ deltax)
                        soft.set_y(soft.bbox.y+ deltay)
                        if deltay != 0 and soft.vertical*deltay < 0:
                            soft.vertical = 0

        # horizontal collisons second
        for soft in self.soft_blobs:
            for hard in self.hard_blobs:
                if soft.bbox.intersects(hard.bbox):
                    (deltax, deltay) = Rectangle.translationvector(hard.bbox, soft.bbox)
                    soft.set_x(soft.bbox.x+ deltax)
                    soft.set_y(soft.bbox.y+ deltay)
                    if deltax != 0 and soft.horizontal*deltax < 0:
                        soft.horizontal = 0


    def render(self, w, h):
        """Report status and list of blob dictionaries for blobs
        with a horizontal distance of w//2 from player.  See writeup
        for details."""
        # raise NotImplementedError
        valid_blob_dicts = []

        player = {'texture': self.player.texture,
                  'pos': self.player.pos,
                  'player': True}
        if -Constants.TILE_SIZE < self.player.pos[1] and self.player.pos[1] < h:
            valid_blob_dicts.append(player)

        px = self.player.pos[0]

        screen = Rectangle(self.player.pos[0] - w//2, self.player.pos[1] - h//2, w, h)

        # print(screen)
        # print(self.player)

        for char in self.characters:
            blob, pos = char.name, char.pos
            if px - w//2 - Constants.TILE_SIZE < pos[0] and pos[0] < px + w//2 and -Constants.TILE_SIZE < pos[1] and pos[1] < h:
            # print(char.bbox)
            # print('intersection', screen.intersects(char.bbox))
            # if screen.intersects(char.bbox):
                blob_dict = {'texture': char.texture,
                             'pos': pos,
                             'player': False}
                valid_blob_dicts.append(blob_dict)
        return ('ongoing', valid_blob_dicts)