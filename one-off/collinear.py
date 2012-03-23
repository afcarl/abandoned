import random

debug = False

# generate_points():
# returns a list of num tuples with randomly generated coordinates
# between min and max
def generate_points(num, min, max):
    random.seed()
    points = set()
    for i in range(num):
        x = random.randint(min, max)
        y = random.randint(min, max)
        point = (x,y)
        points.add(point)
    return points

# form_pairs():
# returns a list consisting of all pairs of tuples in points
def form_pairs(points):
    pairs = []
    points = set(points)
    others = points.copy()
    for point in points:
       	others.remove(point)
        for other in others:
            pairs.append({point, other})
    return pairs

# on_line():
# determines if the tuple q falls on the line determined by the tuples
# p1 and p2
#
# recall: eqn of a line is given by the following formula:
# y - y0 = m(x - x0), where m is the slope (y1 - y0) / (x1 - x0)
def on_line(p0, p1, q):
    try:
        m = (p1[1] - p0[1]) / (p1[0] - p0[0])
        LHS = q[1] - p0[1]
        RHS = m * (q[0] - p0[0])
        return (LHS == RHS)
    except ZeroDivisionError:
        return (p0[0] == p1[0] == q[0])

# max_collinear():
# finds the maximum number of collinear points from points
def max_collinear(points):
    pairs = form_pairs(points)
    num_collinear = 0
    the_pair = set()
    the_points = set()
    
    for pair in pairs:
        p0 = pair.pop()
        p1 = pair.pop()
        pair.add(p0)
        pair.add(p1)
        
        collinear = {point for point in points if on_line(p0, p1, point)}
        if len(collinear) > num_collinear:
            num_collinear = len(collinear)
            the_pair = pair
            the_points = collinear
        
        if debug:
        	print("Pair:", pair)
        	print("Collinear points ({0}):".format(len(collinear)), collinear)
    
    return (num_collinear, the_pair, the_points)

# ===========================================================================

if __name__ == '__main__':
    nums = [i for i in range(5)]
    points = []
    for x in nums:
        for y in nums:
            points.append((x,y))
    
    print("==="*5)
    print("Counting collinear points from the set:")
    print(points)
    print("Max collinear points:", max_collinear(points))
