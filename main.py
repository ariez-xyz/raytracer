from canvas import Canvas
import numpy as np
import math

INFTY = 9999 # Maximum length that we're tracing rays

class Sphere:
    def __init__(self, coords, diameter, color):
        self.coords = np.array(coords)
        self.diameter = diameter
        self.color = np.array(color)

    def solve_quadratic(self, a, b, c):
        """
        Find x s.t. ax^2 + bx + c = 0 via quadratic equation
        returns tuple x1, x2
        """
        d = b**2 - 4*a*c # discriminant
        if d < 0: # don't want complex solutions
            return float("NaN"), float("NaN")
        d = math.sqrt(d)
        return (d-b)/(2*a), (-d-b)/(2*a)

    def intersect_ray(self, O, D):
        """
        Compute intersection of this sphere with line O+tD
        Let P - any point, C - center of sphere. Then:
        sphere given by             dot(P-C, P-C)=r^2
        (square |P-C|=r)
        ray given by                P=O+tD
        -> intersection given by    dot((O+tD)-C,(O+tD)-C)=r^2
        This equation is quadratic in t
        """
        CO = O - self.coords

        a = np.dot(D, D)
        b = 2 * np.dot(CO, D)
        c = np.dot(CO, CO) - self.diameter**2

        t1, t2 = self.solve_quadratic(a, b, c)

        if 1 <= min(t1, t2) <= INFTY:
            return min(t1, t2)

        return INFTY



class Raytracer:
    def __init__(self) -> None:
        self.canvas = Canvas(realtime_update=True)
        # List of spheres: center coords and radius
        self.scene = [
                Sphere((0,-1,3), 1, (255,0,0)),
                Sphere((2,0,4),  1, (0,0,255)),
                Sphere((-2,0,4), 1, (0,255,0)),
                ]
    
    def canvas_to_viewport_coords(self, cx, cy):
        # viewport width = viewport height = viewport distance from canvas = 1
        vx = cx * 1/self.canvas.width
        vy = cy * 1/self.canvas.height
        return np.array([vx, vy, 1])

    def display(self):
        self.canvas.draw()
        self.canvas.block_till_exit()

    def compute(self):
        O = np.zeros(3) # Camera position
        for x in range(-(self.canvas.width // 2), self.canvas.width // 2):
            for y in range(-(self.canvas.height // 2), self.canvas.height // 2):
                D = self.canvas_to_viewport_coords(x, y)
                ray_color = (0,0,0)
                for sphere in self.scene:
                    if sphere.intersect_ray(O, D) < INFTY:
                        ray_color = sphere.color
                    
                rt.canvas.set_color(x, y, ray_color)
                
            



if __name__ == "__main__":
    rt = Raytracer()
    rt.compute()
    print("compute finished")
    rt.display()

