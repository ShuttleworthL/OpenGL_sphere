from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math

vertex_count_lat = 25 #vertical lines
vertex_count_lng = 25 #horozontal lines
radius = 0.7 #row of sphere
#offsets for spheres position
cx = 0
cy = 0
cz = 0

#first previous mouse values
previous_x = 0
previous_y = 0

#initial polar coordiantes for camera
camera_theta = 0 
camera_phi =  math.pi / 2 #level spheres equator
camera_r = 3 #semi zoomed out

#initial cartesian coordiantes for camera (perfectly line up wuith init polar coordinates)
camera_x = 3 
camera_y = 0
camera_z = 0

click = False

sensitivity = 0.003 #how sensitive the camera rotation is to mouse movement

def update(Value): #update time and calculate mouse accelaration (value is for the manditory data argument from glut timer func)
    glutPostRedisplay() #redraw the display
    glEnable(GL_DEPTH_TEST) #allows closer surfaces to hdie further/obstructed ones
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glColor3f(1.0, 1.0, 1.0)
    setup_camera()

    glutPassiveMotionFunc(mouse_movement) #calls mouse_movement function with x and y values included
    glutMouseFunc(mouse_click) #detects button presses, same idea as above

    glutTimerFunc(16, update, 0) #schedule update in 16 millisceonds (about 60fps -  1/60 = 0.0166..)

def mouse_movement(x,y): #handles mouse input and calculates mouse displacement used to rotate camera
    global previous_x, previous_y, camera_phi, camera_theta, camera_r #the last recorded mouse position used to calculate mouse displacement and the phi and theta and r values for the camera
    global camera_x, camera_y, camera_z #camera vlaues in cartesian co ordinates
    if click == True:
        x_displacement = x-previous_x #changes in x and y every frame
        y_displacement = y-previous_y
        print(x_displacement, y_displacement)

        camera_theta -= x_displacement * sensitivity #ccumulating mouse changes to camera angles multiplied by a sensitivity dampener
        camera_phi -= y_displacement * sensitivity

        camera_x = camera_r * math.cos(camera_theta) * math.sin(camera_phi) #uses same principles as for drawring the sphere for finding position of camera
        camera_y = camera_r * math.sin(camera_theta) * math.sin(camera_phi)
        camera_z = camera_r * math.cos(camera_phi)

    #update previous recorded mouse locations now camera calculations are done
    previous_x = x
    previous_y = y

def mouse_click(button, state, x, y): #only allows passive camera movement following left clicks
    global click #updates click condition
    if button == 0 and state == 1: #left mouse click button is clicked
        if click == False: #and if click is currently stll false
            click = True
        else:
            click = False

    print(button, state)

def setup_camera():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 1, 0.1, 100)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    gluLookAt(
        camera_x, camera_y, camera_z,    #cameras real 3d position
        0, 0, 0,  #what position the camera looks at
        0, 0, 1     #witch direction is up (z -defualt)
    )

def draw_sphere(): #defining a opengl display function

    #solid sphere(triangles)
    for i in range (vertex_count_lng): #iterating through vertical lines
        phi = (math.pi) * (i/vertex_count_lng) #angle of vertical steps for any given vertex count by dividing vertex percentage multiplyer by radians in semi circle
        next_phi = math.pi * (i + 1) / vertex_count_lng #step angle for next vertex down
        for j in range (vertex_count_lat): #iterating through horozontal lines
            theta = 2*(math.pi) * (j/vertex_count_lat) #angle of horozontal steps for any given vertex count by dividing vertex percentage multiplyer by radians in circle
            next_theta = 2 * math.pi * (j + 1) / vertex_count_lat #step angle for next vertex across

            #(v0)----(v1)
            # |       |
            # |       |
            #(v2)----(v3)

            #vertices of the quad
            #open gl can only render lines points and triangle sos the quad neds to be broken down into 2 triangles

            #covert polar verticies to cartesian co ordiantes
            v0 = (cx + radius * math.cos(theta) * math.sin(phi), #finding opposite side (width wize length) using cos(on xy plane) while additionally multiplying by sin(phi) (proportion between hypot and opposite side on z plane - scales radius with polar angle) +offsets
                cy + radius * math.sin(theta) * math.sin(phi), #finding adjacent side (depth wize length) using sin(on xy plane) while additionally multiplying by sin(phi) (proportion between hypot and opposite side on z plane - scales radius with polar angle) +offsets
                cz + radius * math.cos(phi)) #finding adjacent side (height length) using cos(on z plane) +offsets
            
            v1 = (cx + radius * math.cos(next_theta) * math.sin(phi), #repeated steps for further angle increments to form all four verticies in grid pattern - to later construct into 2 triangles
                cy + radius * math.sin(next_theta) * math.sin(phi),
                cz + radius * math.cos(phi))
            
            v2 = (cx + radius * math.cos(theta) * math.sin(next_phi),
                cy + radius * math.sin(theta) * math.sin(next_phi),
                cz + radius * math.cos(next_phi))
            
            v3 = (cx + radius * math.cos(next_theta) * math.sin(next_phi),
                cy + radius * math.sin(next_theta) * math.sin(next_phi),
                cz + radius * math.cos(next_phi))
            
            glBegin(GL_TRIANGLES) #every 3 vertices stated past this declaration form 1 triangle

            # triangle 1
            glVertex3f(*v0) #unpacking x, y and z for each vertex
            glVertex3f(*v2)
            glVertex3f(*v1)

            # triangle 2
            glVertex3f(*v1)
            glVertex3f(*v2)
            glVertex3f(*v3)

            glEnd()

    #sphere wireframe(line loop)

    glColor3f(0.0, 0.0, 0.0)

    #latitude lines
    for i in range(vertex_count_lng): #uses same math for fidnding phi and theta increments and converting polar to cartesian co ordinates but instead has each vertice added to a wireframe loop (repeated below for longtitude)
        phi = math.pi * (i / vertex_count_lng)
        glBegin(GL_LINE_STRIP)
        for j in range(vertex_count_lat+1): #inner loops contain +1 to let them overlap (complete full latitudinal ring as gl line strip requires overlap to the start position)
            theta = 2 * math.pi * (j / vertex_count_lat)
            x = cx + radius * math.cos(theta) * math.sin(phi)
            y = cy + radius * math.sin(theta) * math.sin(phi)
            z = cz + radius * math.cos(phi)
            glVertex3f(x, y, z)
        glEnd()

    #longitude lines
    for j in range(vertex_count_lat):
        theta = 2 * math.pi * (j / vertex_count_lat)
        glBegin(GL_LINE_STRIP)
        for i in range(vertex_count_lng+1): #still contains +1 to reach final semi circle position
            phi = math.pi * (i / vertex_count_lng)
            x = cx + radius * math.cos(theta) * math.sin(phi)
            y = cy + radius * math.sin(theta) * math.sin(phi)
            z = cz + radius * math.cos(phi)
            glVertex3f(x, y, z)
        glEnd()

    glutSwapBuffers()

glutInit() #initializes GLUT
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH) #condigures window behaviour eg colour format
glutInitWindowSize(800, 800) #sets initial window size
glutCreateWindow(b"Solid Sphere") #creates window
glutDisplayFunc(draw_sphere) #calls function when window needs to be drawn
glutTimerFunc(16, update, 0) #starts update function for first time
glutMainLoop() #starts event loop