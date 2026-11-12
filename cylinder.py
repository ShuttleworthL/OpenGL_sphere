from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math

vertex_count_lat = 25 #vertical lines
vertex_count_lng = 25 #how many horozontal rings make up the height of the cylinder
cylinder_height = 1 #total height of cylinder
radius = 0.1 #row of cylinder
#offsets for cyliders position
cx = 0
cy = 0
cz = 0

def setup_camera():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 1, 0.1, 100)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    gluLookAt(
        3, 3, 3,    #cameras real 3d position
        0, 0, 0.5,  #what the camera looks at (z is halfway between start and end of cylinder height - thus perfectly centered)
        0, 0, 1     #witch direction is up (z -defualt)
    )

def draw_cylinder(): #defining a opengl display function

    #solid cylinder(triangles)

    glEnable(GL_DEPTH_TEST) #allows closer surfaces to hdie further/obstructed ones
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glColor3f(1.0, 1.0, 1.0)
    setup_camera()
    for i in range(vertex_count_lng):
        height = i*(cylinder_height/vertex_count_lng) #current proportion of the way through the height
        next_height = (i+1)*(cylinder_height/vertex_count_lng) #next proportion of the way through the height
        for j in range(vertex_count_lat): #iterating through horozontal lines
            theta = 2*(math.pi) * (j/vertex_count_lat) #angle of horozontal steps for any given vertex count by dividing vertex percentage multiplyer by radians in circle
            next_theta = 2 * math.pi * (j + 1) / vertex_count_lat #step angle for next vertex across
            

            #(v0)----(v1)
            # |       |
            # |       |
            #(v2)----(v3)

            #vertices of the quad
            #open gl can only render lines points and triangle sos the quad neds to be broken down into 2 triangles

            #covert polar verticies to cartesian co ordiantes
            v0 = (cx + radius * math.cos(theta),
                cy + radius * math.sin(theta),
                cz + height)
            
            v1 = (cx + radius * math.cos(next_theta),
                cy + radius * math.sin(next_theta),
                cz + height)
            
            v2 = (cx + radius * math.cos(theta),
                cy + radius * math.sin(theta),
                cz + next_height)
            
            v3 = (cx + radius * math.cos(next_theta),
                cy + radius * math.sin(next_theta),
                cz + next_height)
            
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
    for i in range(vertex_count_lng): #uses same math for fidnign phi and theta increments and converting polar to cartesian co ordinates but instead has each vertice added to a wireframe loop (repeated below for longtitude)
        height = i*(cylinder_height/vertex_count_lng)
        glBegin(GL_LINE_STRIP) #strip instead of loop to prevent final vertex looping back to start
        for j in range(vertex_count_lat+1): #inner loops contain +1 to let them overlap (complete full longtidudinal ring as gl line strip requires overlap to the start position)
            theta = 2 * math.pi * (j / vertex_count_lat)
            x = cx + radius * math.cos(theta)
            y = cy + radius * math.sin(theta)
            z = cz + height
            glVertex3f(x, y, z)
        glEnd()

    #longitude lines
    for j in range(vertex_count_lat):
        theta = 2 * math.pi * (j / vertex_count_lat)
        glBegin(GL_LINE_STRIP)
        for i in range(vertex_count_lng+1): #still need +1 to reach full height value of 1 instead of (1/25) *5 =0.96
            height = i*(cylinder_height/vertex_count_lng)
            x = cx + radius * math.cos(theta)
            y = cy + radius * math.sin(theta)
            z = cz + height
            glVertex3f(x, y, z)
        glEnd()

    glutSwapBuffers()

glutInit() #initializes GLUT
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH) #condigures window behaviour eg colour format
glutInitWindowSize(1200, 1200) #sets initial window size
glutCreateWindow(b"Solid cylinder") #creates window
glutDisplayFunc(draw_cylinder) #calls function when window needs to be drawn
glutMainLoop() #starts event loop