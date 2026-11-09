from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math

vertex_count_lat = 50 #vertical lines
vertex_count_lng = 50 #horozontal lines
radius = 0.7 #row of sphere
#offsets for spheres position
cx = 0
cy = 0
cz = 0

def draw_sphere(): #defining a opengl display function

    #solid sphere(triangles)

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glColor3f(1.0, 1.0, 1.0)
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
            v0 = (cx + radius * math.cos(theta) * math.sin(phi),
                cy + radius * math.sin(theta) * math.sin(phi),
                cz + radius * math.cos(phi))
            
            v1 = (cx + radius * math.cos(next_theta) * math.sin(phi),
                cy + radius * math.sin(next_theta) * math.sin(phi),
                cz + radius * math.cos(phi))
            
            v2 = (cx + radius * math.cos(theta) * math.sin(next_phi),
                cy + radius * math.sin(theta) * math.sin(next_phi),
                cz + radius * math.cos(next_phi))
            
            v3 = (cx + radius * math.cos(next_theta) * math.sin(next_phi),
                cy + radius * math.sin(next_theta) * math.sin(next_phi),
                cz + radius * math.cos(next_phi))
            
            glBegin(GL_TRIANGLES) #every 3 vertices onward = 1 triangle

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

    # latitude lines
    for i in range(vertex_count_lng):
        phi = math.pi * (i / vertex_count_lng)
        glBegin(GL_LINE_LOOP)
        for j in range(vertex_count_lat):
            theta = 2 * math.pi * (j / vertex_count_lat)
            x = cx + radius * math.cos(theta) * math.sin(phi)
            y = cy + radius * math.sin(theta) * math.sin(phi)
            z = cz + radius * math.cos(phi)
            glVertex3f(x, y, z)
        glEnd()

    # longitude lines
    for j in range(vertex_count_lat):
        theta = 2 * math.pi * (j / vertex_count_lat)
        glBegin(GL_LINE_LOOP)
        for i in range(vertex_count_lng):
            phi = math.pi * (i / vertex_count_lng)
            x = cx + radius * math.cos(theta) * math.sin(phi)
            y = cy + radius * math.sin(theta) * math.sin(phi)
            z = cz + radius * math.cos(phi)
            glVertex3f(x, y, z)
        glEnd()

    glutSwapBuffers()

glutInit() #initializes GLUT
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH) #condigures window behaviour eg colour format
glutInitWindowSize(600, 600) #sets initial window size
glutCreateWindow(b"Solid Sphere") #creates window
glutDisplayFunc(draw_sphere) #calls function when window needs to be drawn
glutMainLoop() #starts event loop