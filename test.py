import math 

def calculate_line_angle(x1, y1, x2, y2):
    y = (y2 - y1)**2
    x = (x2 - x1)**2
    theta = math.atan(math.sqrt(y)/math.sqrt(x))
    theta_deg = math.degrees(theta)
    return theta_deg 

angle = calculate_line_angle(100, 100, 200, 200)
print(angle)