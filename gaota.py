import pyxel
#from collections import  namedtuple
#Point = namedtuple("Point", ["x", "y"], "Tile_Point", ["x", "y"])

WINDOW_W = 128
#WINDOW_H = 128
WINDOW_H = 140
ROCK_IMG = 0
ROCK_U = 16
ROCK_V = 0
ROCK_H = 16
ROCK_W = 16
ROCK_COLKEY = 0

IMG_ROCK_UPPER_LEFT = 2
IMG_ROCK_UPPER_RIGHT = 3
IMG_ROCK_LOWER_LEFT = 34
IMG_ROCK_LOWER_RIGHT = 35
IMG_WALL = 1
IMG_ONIGIRI_UPPER_LEFT = 128
IMG_ONIGIRI_UPPER_RIGHT = 129
IMG_ONIGIRI_LOWER_LEFT = 160
IMG_ONIGIRI_LOWER_RIGHT = 161
IMG_TRASURE_UPPER_LEFT = 6
IMG_TRASURE_UPPER_RIGHT = 7
IMG_TRASURE_LOWER_LEFT = 38
IMG_TRASURE_LOWER_RIGHT = 39

# TODO:Classing, OVERALL!!!!!!
class App:
    def __init__(self):
        # TODO:wanna gorgeous title!
        pyxel.init(WINDOW_W, WINDOW_H, caption="gaota", fps=25)
        pyxel.load('assets/gaota.pyxel')
        self.title()
        self.deep_reset()
        self.reset()
        pyxel.run(self.update, self.draw)

    def reset(self):
        self.x = 0
        self.y = 0
        self.tile_x = self.stage * 16
        self.tile_y = 0
        self.move_x = 0
        self.move_y = 0
        self.direction_x = 2
        self.direction_y = 0
        self.walk = [0, 16]
        self.direction = [16, -16]
        self.vector = 0
        self.rock_x = 0
        self.rock_y = 0
        self.rock_move_y = 0
        self.is_rock_fall = False
        self.is_spewing = False
        self.spew_count = 0
        self.spew = [0, 16, 32, 48]
        self.rock_count = 0

    def deep_reset(self):
        self.stage = 0

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        elif pyxel.btnp(pyxel.KEY_R):
            self.reset()
            self.deep_reset()

        self.update_gaota()
        if self.is_rock_fall:
            self.update_rock()

    def draw(self):
        pyxel.cls(0)
        self.tilemap_draw()
        self.draw_gaota()
        if self.is_rock_fall:
            self.draw_rock()

    def update_gaota(self):
        # Any judgments are made every 8 dots.
        if self.x % 8 == 0 and self.y % 8 == 0:
            self.move_x = 0
            self.move_y = 0
            self.direction_y = 0

            # fall if no wall under gaota
            if self.is_nothing_at_my_feet():
                self.move_y = 1
                self.direction_y = 1
            
            # for spewing animations
            elif self.is_spewing:
                if self.spew_count == 3:
                    self.spew_count = 0
                    self.is_spewing = False
                    self.is_rock_fall = True
                else:
                    self.spew_count += 1
    
            # push h to move to left
            elif pyxel.btn(pyxel.KEY_H) and self.x>0:
                self.direction_x = -1
                self.move_x = -1
                self.vector = 1
                # TODO:The functionalization is kinda odd..
                obj_upper, obj_below = self.object_of_front()
                if (
                        obj_upper in [
                            IMG_WALL, 
                            IMG_ROCK_UPPER_RIGHT, 
                            IMG_ROCK_LOWER_RIGHT
                        ] or 
                        obj_below in [
                            IMG_WALL, 
                            IMG_ROCK_UPPER_RIGHT, 
                            IMG_ROCK_LOWER_RIGHT
                        ]):
                    self.move_x = 0 

            # push l to move to right
            elif pyxel.btn(pyxel.KEY_L) and self.x<112:
                self.direction_x = 2
                self.move_x = 1
                self.vector = 0
                # TODO:Here too.
                obj_upper, obj_below = self.object_of_front()
                if ( 
                        obj_upper in [
                            IMG_WALL, 
                            IMG_ROCK_UPPER_LEFT, 
                            IMG_ROCK_LOWER_LEFT
                        ] or 
                        obj_below in [
                            IMG_WALL, 
                            IMG_ROCK_UPPER_LEFT, 
                            IMG_ROCK_LOWER_LEFT
                        ]):
                    self.move_x = 0

            # push z to spew a rock
            elif pyxel.btn(pyxel.KEY_Z):
                if self.is_rock_fall:
                    pass
                elif self.rock_count == 0:
                    pass
                else:
                    if self.is_puttable():
                        self.rock_tile_x = self.tile_x + self.direction_x if self.vector == 0 else self.tile_x + self.direction_x - 1
                        self.rock_tile_y = self.tile_y
                        self.rock_x = (self.rock_tile_x - (self.stage * 16)) * 8
                        self.rock_y = self.rock_tile_y * 8
                        self.rock_count -= 1
                        self.update_rock_count()
                        self.is_spewing = True

        # move gaota
        self.x += self.move_x
        self.y += self.move_y

        # set gaota location on the tile.
        self.tile_x = 0 if self.x == 0 else int(self.x / 8)
        self.tile_x += self.stage * 16
        self.tile_y = 0 if self.y == 0 else int(self.y / 8)

        # got something?(shoot, gaota cannot get anything at the air.)
        if self.object_of_behind() == IMG_ONIGIRI_UPPER_LEFT and not(self.is_nothing_at_my_feet()):
            self.rock_count += 1
            self.update_rock_count()
            self.delete_behind()
        elif self.object_of_behind() == IMG_TRASURE_UPPER_LEFT and not(self.is_nothing_at_my_feet()):
            # TODO: need much more rich stage clear process
            self.stage += 1
            self.reset()
            self.tilemap_draw()


    def update_rock_count(self):
        # TODO: Ahhhhhhgggggg....
        i = self.rock_count
        j = 1
        while i > 0:
            #pyxel.tilemap(0).copy(
            #    j,
            #    16,
            #    7, 2, 0, 1, 1)
            #pyxel.tilemap(0).copy(
            #    j,
            #    16,
            #    7, 2, 1, 1, 1)
            pyxel.bltm(
                j * 8,
                132,
                0,
                2, 0, 1, 1)
            pyxel.bltm(
                j * 8,
                10,
                0,
                2, 1, 1, 1)
            j += 1
            i -= 1

    def is_puttable(self):
        # TODO:this is too ugly...
        if self.vector == 0:
            obj_upper_left = pyxel.tilemap(0).get(self.tile_x+2, self.tile_y)
            obj_upper_right = pyxel.tilemap(0).get(self.tile_x+3, self.tile_y)
            obj_lower_left = pyxel.tilemap(0).get(self.tile_x+2, self.tile_y+1)
            obj_lower_right = pyxel.tilemap(0).get(self.tile_x+3, self.tile_y+1)
        else:
            obj_upper_left = pyxel.tilemap(0).get(self.tile_x-2, self.tile_y)
            obj_upper_right = pyxel.tilemap(0).get(self.tile_x-1, self.tile_y)
            obj_lower_left = pyxel.tilemap(0).get(self.tile_x-2, self.tile_y+1)
            obj_lower_right = pyxel.tilemap(0).get(self.tile_x-1, self.tile_y+1)

        if IMG_WALL not in [obj_upper_left, obj_upper_right, obj_lower_right, obj_lower_left]:
            return True
        return False

    def update_rock(self):
        if self.rock_y % 8 == 0:
            self.rock_move_y = 0

            # fall if no wall under rock
            if self.is_nothing_at_my_bottom():
                self.rock_move_y = 1
            else:
                # put static rock after landing.
                # TODO:i think i should not use tilemap().copy.
                #      actually im using tilemap(7) to copy tile and that is not good, i think. 
                pyxel.tilemap(0).copy(
                        self.rock_tile_x,
                        self.rock_tile_y,
                        7, 0, 0, 2, 2)
                self.is_rock_fall = False

        self.rock_y += self.rock_move_y

        # set rock location on the tile.
        self.rock_tile_y = 0 if self.rock_y == 0 else int(self.rock_y / 8)

    def object_of_front(self):
        obj_upper = pyxel.tilemap(0).get(
            self.tile_x + self.direction_x, 
            self.tile_y + self.direction_y)
        obj_below = pyxel.tilemap(0).get(
            self.tile_x + self.direction_x, 
            self.tile_y + self.direction_y + 1)
        print(obj_upper, obj_below)
        return obj_upper, obj_below

    def object_of_below(self):
        obj_left = pyxel.tilemap(0).get(
                self.tile_x,
                self.tile_y + 2)
        obj_right = pyxel.tilemap(0).get(
                self.tile_x + 1,
                self.tile_y + 2)
        return obj_left, obj_right

    def object_of_behind(self):
        obj_behind = pyxel.tilemap(0).get(
                self.tile_x,
                self.tile_y)
        return obj_behind

    def is_nothing_at_my_feet(self):
        obj_left_feet = pyxel.tilemap(0).get(
                self.tile_x,
                self.tile_y + 2)
        obj_right_feet = pyxel.tilemap(0).get(
                self.tile_x + 1,
                self.tile_y + 2)

        if obj_left_feet in [
                IMG_WALL, 
                IMG_ROCK_UPPER_LEFT, 
                IMG_ROCK_UPPER_RIGHT]:
            return False
        if obj_right_feet in [
                IMG_WALL, 
                IMG_ROCK_UPPER_LEFT, 
                IMG_ROCK_UPPER_RIGHT]:
            return False
        return True

    def is_nothing_at_my_bottom(self):
        obj_left_bottom = pyxel.tilemap(0).get(
                self.rock_tile_x,
                self.rock_tile_y + 2)
        obj_right_bottom = pyxel.tilemap(0).get(
                self.rock_tile_x + 1,
                self.rock_tile_y + 2)

        if obj_left_bottom in [
                IMG_WALL, 
                IMG_ROCK_UPPER_LEFT, 
                IMG_ROCK_UPPER_RIGHT]:
            return False
        if obj_right_bottom in [
                IMG_WALL, 
                IMG_ROCK_UPPER_LEFT, 
                IMG_ROCK_UPPER_RIGHT]:
            return False
        return True

    def delete_behind(self):
        # TODO: i think i should not use tilemap().copy.
        pyxel.tilemap(0).copy(
                self.tile_x,
                self.tile_y,
                1, 2, 0, 2, 2)

    def draw_gaota(self):
        x = self.x
        y = self.y
        img = 0
        u = self.spew[self.spew_count] if self.is_spewing else self.walk[self.x % 2]
        v = 16
        w = self.direction[self.vector]
        h = 16
        colkey = 0
        pyxel.blt(x, y, img, u, v, w, h, colkey)

    def draw_rock(self):
        x = self.rock_x
        y = self.rock_y
        pyxel.blt(x, y, ROCK_IMG, ROCK_U, ROCK_V, ROCK_W, ROCK_H, ROCK_COLKEY)

    def tilemap_draw(self):
        x = 0
        y = 0
        tm = 0
        u = self.stage * 16
        v = 0
        w = 16
        h = 16
        pyxel.bltm(x, y, tm, u, v, w, h)

    def title(self):
        # TODO: title yoteichi.
        pass
        #pyxel.image(0).load(0, 0, "assets/title.png")

App()
