import svgwrite
import math
import random

class Blob:
    def __init__(self, width:int = 500, 
                       height:int=500, 
                       num_points:int=None, 
                       color:str=None,
                       opacity:float=None):
        
        self.height=height
        self.width=width
        self.dwg = svgwrite.Drawing("./images/blob.svg", size=(height, width))
        self.blur_filter = self.dwg.defs.add(self.dwg.filter(x="-40%",width="180%",y="-40%",height="180%"))
        self.blur_filter.feGaussianBlur(in_='SourceGraphic', stdDeviation=random.randint(1,5))
        self.center_x=width/2
        self.center_y=height/2
        self.radius = min(self.center_x-width*.2, self.center_y-height*.2)
        if num_points:
            self.num_points = num_points
        else:
            self.num_points = random.randint(3,9)
        self.angle_step = math.radians(360/self.num_points)
        if not color:
            color = "#%06x" % random.randint(0, 0xFFFFFF)
        self.color = color
        if opacity is None:
            opacity = random.uniform(0, 100)
        self.opacity = opacity


    def get_svg(self):
        return self.path_bw, self.path_color
    
    def make_circle(self):
        self.circle_coords=[]
        x_rand = self.width*.1
        y_rand = self.height*.1
        for i in range(self.num_points):
            x = self.center_x + self.radius * math.sin(self.angle_step * i) + random.randint(x_rand*-1,x_rand)
            y = self.center_y + self.radius * math.cos(self.angle_step * i) + random.randint(y_rand*-1,y_rand)
            self.circle_coords.append((x,y))
        
    def make_blob(self):
        self.make_circle()
        self.path_bw = self.dwg.path(
                d=("M",(self.circle_coords[0][0],self.circle_coords[0][1])),
                fill="none",
                stroke="black",
                stroke_width="2"
            )
        self.path_color = self.dwg.path(
                d=("M",(self.circle_coords[0][0],self.circle_coords[0][1])),
                fill=self.color,
                opacity=self.opacity,
                stroke_width="0",
                filter=self.blur_filter.get_funciri(),
                style="mix-blend-mode:multiply"
            )
        self.path_color.rotate(random.randint(-2, 2))
        # each line segment is composed of a start control point
        # and end control point and an end anchor point
        for i in range(self.num_points):
            opposed_line_start = self.calc_opposed_line(i)
            opposed_line_end = self.calc_opposed_line((i+1)%self.num_points)
            control_point_start = self.calc_control_point(i, 
                                                          opposed_line_start,
                                                          False)
            control_point_end = self.calc_control_point((i+1)%self.num_points, 
                                                          opposed_line_end,
                                                          True)
            new_segment = ("C", (control_point_start[0],
                                 control_point_start[1],
                                 control_point_end[0],
                                 control_point_end[1],
                                 self.circle_coords[(i+1)%self.num_points][0],
                                 self.circle_coords[(i+1)%self.num_points][1]
                                 ))
            self.path_bw.push(new_segment[0],new_segment[1])
            self.path_color.push(new_segment[0],new_segment[1])

    def calc_opposed_line(self, i):
        # This is a line connecting the previous and next points
        # This line will be used to determine the control point
        pointB = self.circle_coords[(i+1)%self.num_points]
        pointA = self.circle_coords[(i-1)%self.num_points]
        lengthX = pointB[0] - pointA[0]
        lengthY = pointB[1] - pointA[1]
        length = ((lengthX**2) + (lengthY**2))**.5
        angle = math.atan2(lengthY, lengthX)
        return length, angle

    def calc_control_point(self, i, opposed_line,is_end):
        #The control point is a point a scaled length of the opposed line
        #from the current point at the same angle as the opposed line

        current_pt=self.circle_coords[i]
        smoothing = 0.2
        length = opposed_line[0] * smoothing
        angle = opposed_line[1]
        if is_end:
            angle = angle +math.pi
        x = current_pt[0] + math.cos(angle) * length
        y = current_pt[1] + math.sin(angle) * length
        return x,y  
    
    def make_eyeball(self):
        self.eye_space = self.radius*random.uniform(.1, .25)
        self.right_eye_x = self.center_x + self.eye_space
        self.left_eye_x = self.center_x - self.eye_space
        self.eye_y = self.center_y - self.radius*random.uniform(.2, .45)
        rand1 = random.uniform(.09, self.eye_space)
        rand2 = random.uniform(.09, self.eye_space)
        right_eye=self.dwg.ellipse(center=(self.right_eye_x,self.eye_y),
                    r=(rand1, rand2),
                    stroke=svgwrite.rgb(10, 10, 16, '%'),
                    fill='white')
        right_pupil=self.dwg.ellipse(center=(self.right_eye_x,self.eye_y),
                    r=(rand1/5, rand2/5),
                    stroke=svgwrite.rgb(10, 10, 16, '%'),
                    fill='black')
        left_eye  = self.dwg.ellipse(center=(self.left_eye_x,self.eye_y),
                    r=(rand1,rand2),
                    stroke=svgwrite.rgb(10, 10, 16, '%'),
                    fill='white')
        left_pupil=self.dwg.ellipse(center=(self.left_eye_x,self.eye_y),
                    r=(rand1/5,rand2/5),
                    stroke=svgwrite.rgb(10, 10, 16, '%'),
                    fill='black')
        
        return [right_eye, left_eye, right_pupil, left_pupil]

    def make_smile(self):
        path_smile = self.dwg.path(
            fill="none",
            stroke="black",
            stroke_width="2"
        )
        start_x = self.left_eye_x + self.eye_space/2*random.uniform(.2, .5)
        start_y = self.eye_y + self.radius*random.uniform(.15, .25)

        end_x = self.right_eye_x - self.eye_space/2*random.uniform(.2, .5)
        end_y = self.eye_y + self.radius*random.uniform(.15, .25)

        x1 = (start_x + end_x)/2
        y1 = end_y + self.radius*random.uniform(.1, .25)
        smile_path = [("M",(start_x, start_y)),
              ("Q",(x1, y1, end_x, end_y))]
        for edge in smile_path:
            path_smile.push(edge[0],edge[1])     
        return path_smile

    def complete(self):   
        bw, color= self.get_svg()
        eyepaths = self.make_eyeball()
        self.dwg.add(bw)
        self.dwg.add(color)
        for p in eyepaths:
            self.dwg.add(p)
        self.dwg.add(self.make_smile())
        # self.dwg.save()

    def get_svg_string(self):
        return self.dwg.tostring()       
        
'''
    width:int = 500, 
    height:int=500, 
    num_points:int=random.randint(3,6), 
    color="green",
    opacity:float=0.8
'''
b=Blob()
b.make_blob()
b.complete()
svg_string = b.get_svg_string()



