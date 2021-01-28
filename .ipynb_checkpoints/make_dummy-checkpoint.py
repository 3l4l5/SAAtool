import pandas as pd
import numpy as np
from PIL import Image, ImageFilter, ImageDraw

class MakeDummy:
    def __init__(self, radius, margin, xy=(588, 358)):
        
        if type(radius) == int and type(margin) == int:
            self.radius = radius
            self.margin = margin
            self.xy = xy
            self.im = Image.new("L", self.xy, 0)
            self.draw = ImageDraw.Draw(self.im)

            #一つの箱の大きさ
            self.box_size = (self.radius + self.margin) * 2
            #横に敷き詰められる数
            self.num_cercle_x = self.xy[0] // self.box_size
            #縦に敷き詰められる数
            self.num_cercle_y = self.xy[1] // self.box_size
            #敷き詰められる最大の個数
            self.max_cercle_num = self.num_cercle_x * self.num_cercle_y
            
            self.make_box_coordinate()
            self.make_circle()
            
            self.area = radius**2 * np.pi
        else:
            print("radius and margin must be int because these are px.")
            print("Try again.")
    
    # 円を描くための座標を作成する関数[(左上x,左上y,右下x,右下y), (...), ...]
    def make_box_coordinate(self):
        self.out_left_x_list = [n*self.box_size for n in range(self.num_cercle_x)]
        self.out_left_y_list = [n*self.box_size for n in range(self.num_cercle_y)]
        
        self.inner_left_x_list = [x + y for (x, y) in zip(self.out_left_x_list, [self.margin] * self.num_cercle_x)]
        self.inner_right_x_list = [x + y for (x, y) in zip(self.out_left_x_list, [self.margin + self.radius * 2] * self.num_cercle_x)]
        
        self.inner_left_y_list = [x + y for (x, y) in zip(self.out_left_y_list, [self.margin] * self.num_cercle_y)]
        self.inner_right_y_list = [x + y for (x, y) in zip(self.out_left_y_list, [self.margin + self.radius * 2] * self.num_cercle_y)]
        
        self.left_coordinate = [[x,y] for x in self.inner_left_x_list for y in  self.inner_left_y_list]
        self.right_coordinate = [[x,y] for x in self.inner_right_x_list for y in self.inner_right_y_list]
        
        self.circle_coordinate = [(left[0], left[1], right[0], right[1]) for (left, right) in zip(self.left_coordinate, self.right_coordinate)]
    
    #与えられた座標を元に円を描く
    def make_circle(self):
        for coordinate in self.circle_coordinate:
            self.draw.ellipse(coordinate, fill=(255))