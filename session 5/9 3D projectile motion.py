from visual import *

scene.width = 1300
scene.height = 1000
scene.autoscale = False

launch_pos = vector(-5,0,0) # Initial position of projectile.

### Make display adjustable.
global drag,lastpos
drag = False
def down():
    global drag,lastpos
    #print "mousedown"
    scene.center = scene.mouse.pos
    drag = True
    lastpos = vector(scene.mouse.pos.x,scene.mouse.pos.y,0)

##def move(): ### Not working yet...
##    global drag, lastpos
##    if drag: # mouse button is down
##        dpos = scene.mouse.pos-lastpos
##        scene.center += dpos
##        lastpos = vector(scene.mouse.pos.x,scene.mouse.pos.y,0)
##        print scene.center

def up():
    global drag
    drag = False

scene.bind("mousedown", down)

#scene.bind("mousemove", move)

scene.bind("mouseup", up)
###

use_ruler = True
## Start rulers at projectile initial position.
if (use_ruler):
    # Make x-axis.
    dx = 1.0 # Box center-to-center separation (AKA ruler marking).
    box_x = launch_pos.x + 0.5*dx # Box's x-coordinate.
    box_x_max = -box_x ## Will likely need to change.
    while box_x <= box_x_max:
        box(pos=(box_x,-0.05,0),
            size=(0.95*dx,0.05,0.05),
            color=color.white,
            opacity=0.5)
        box_x += dx

    # Make y-axis.
    dy = dx # Box center-to-center separation (AKA ruler marking).
    box_y = launch_pos.y + 0.5*dy # Box's y-coordinate.
    box_y_max = max(-box_y,box_x_max) ## Will likely need to change.
    ### May need to generate more ruler boxes within the motion loop.
    while box_y <= box_y_max:
        box(pos=(-0.05,box_y,0),
            size=(0.05,0.95*dy,0.05),
            color=color.white,
            opacity=0.5)
        box_y += dy

### Stop block definitions here.
list_of_stops = []
class stop_block:
    def __init__(self, posn, size, opac):
        self.posn = posn
        self.size = size
        self.opac = opac
        # Create box.
        self.object = box(pos = self.posn,
                          size = self.size,
                          color = color.green,
                          opacity = self.opac)
        # Calculate edges.
        self.top = posn.y+0.5*size.y
        self.bottom = posn.y-0.5*size.y
        self.right = posn.x+0.5*size.x
        self.left = posn.x-0.5*size.x
        self.front = posn.z+0.5*size.z
        self.back = posn.z-0.5*size.z

### Side bar height.
wall_height = 2.44
### Side bar thickness.
wall_thickness = 0.1
### Distance to kicker.
wall_x = 20 # Max = 110, penalt kick ~ 11.
### Set wall bottom to be at launch_pos.y.
wall_y = launch_pos.y + wall_height*0.5
wall_z = 7.32*0.5
### Add side bars.
list_of_stops.append(stop_block(posn = vector(wall_x,wall_y,wall_z),
                             size = vector(wall_thickness,wall_height,wall_thickness),
                                opac = 1.0))
list_of_stops.append(stop_block(posn = vector(wall_x,wall_y,-wall_z),
                             size = vector(wall_thickness,wall_height,wall_thickness),
                                opac = 1.0))
### Top bar width.
wall_width = 7.32
### Top bar thickness.
wall_thickness = 0.1
wall_y = wall_height
### Add top bar.
list_of_stops.append(stop_block(posn = vector(wall_x,wall_y,0),
                             size = vector(wall_thickness,wall_thickness,wall_width),
                                opac = 1.0))

list_of_stops.append(stop_block(posn = vector(wall_x+1,25,0),
                                size = vector(0.1,50,5.6388),
                                opac = 0))

### Maximum ball speed = 80 mph (35.7632 m/s).
### Typical launch angle = 20-60 degrees. --> I think this was *approach* angle.

## Loop over initial launch angle.
angle = 0.0 # Initial angle measured in degrees.
delta_angle = 1.0
max_angle = 10

### Set approach angle. Initial velocity vector is angle2 degrees from x-axis.
angle2 = 0.0

landing_y = launch_pos.y ### Made this easier!

for stop in list_of_stops:
    landing_y = min(landing_y,stop.bottom)

while (angle <= max_angle):

    ## Projectile information here.

    projectile = sphere(pos = launch_pos,
                        radius = 0.1,
                        color = color.red,
                        make_trail = True)


    projectile.speed = 20 # Initial speed.
    projectile.angle = angle*3.141459/180 # Initial angle, from the +x-axis.
    projectile.angle2 = angle2*3.141459/180 # Initial angle, from the +x-axis.

    projectile.velocity = vector(projectile.speed*cos(projectile.angle)*cos(projectile.angle2),
                                 projectile.speed*sin(projectile.angle),
                                 projectile.speed*cos(projectile.angle)*sin(projectile.angle2))



    projectile.mass = 1.0
    grav_field = 1.0

    dt = 0.01
    time = 0

    keep_going = True

    while (keep_going):
        keep_going = projectile.pos.y >= landing_y
        if (keep_going):
            # Check for collision with a stop_block.
            for block in list_of_stops:
                if (block.left <= projectile.pos.x + projectile.radius):
                    if (block.right >= projectile.pos.x - projectile.radius):
                        if (block.top >= projectile.pos.y - projectile.radius):
                            if (block.bottom <= projectile.pos.y + projectile.radius):
                                if (block.front >= projectile.pos.z - projectile.radius):
                                    if (block.back <= projectile.pos.z + projectile.radius):
                                        keep_going = False
        
        rate(150)

        # Calculate the force.
        grav_force = vector(0,-projectile.mass*grav_field,0)

        force = grav_force
        
        # Update velocity.
        projectile.velocity = projectile.velocity + force/projectile.mass * dt

        # Update position.
        projectile.pos = projectile.pos + projectile.velocity * dt

        # Update time.
        time = time + dt

        # Add ruler boxes as necessary.
        if (projectile.pos.x > box_x_max):
            # Add box on x-axis.
            box_x_max += dx
            box(pos=(box_x_max,-0.05,0),
                size=(0.95*dx,0.05,0.05),
                color=color.white,
                opacity=0.5)

        if (projectile.pos.y > box_y_max):
            # Add box on y-axis.
            box_y_max += dy
            box(pos=(-0.05,box_y_max,0),
                size=(0.05,0.95*dy,0.05),
                color=color.white,
                opacity=0.5)

    angle += delta_angle
