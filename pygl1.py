from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import sys
import time
#import imageLoader

# A global variable storing our window ID
# (not very pythonic by standard practice for OpenGL)
window = 0

def drawface(r,g,b):
    glBegin(GL_POLYGON)
    glColor3f(r,g,b)
    glVertex3f(-.5, -.5, -.5)
    glVertex3f(.5, -.5, -.5)
    glVertex3f(.5, .5, -.5)
    glVertex3f(-.5, .5, -.5)
    glEnd()

def drawcube():
    glPushMatrix()
    
    #move forward
    glTranslate(0,0,1)
    #Draw red front
    drawface(1,0,0)
    
    #move backward
    glTranslate(0,0,-1)
    #Draw green back
    drawface(0,1,0)

    #rotate 90* around y axis to form right side
    glRotate(270, 0,1,0)
    #Draw blue right
    drawface(0,0,1)
    
    #Rotate the other way to form the other side
    glRotate(-180, 0,1,0)
    #Draw black left
    drawface(0,0,0)

    #rotate to form top
    glRotate(90, 1,0,0)
    #Draw purple top
    drawface(.5, 0, .5)

    #Rotate the other way to form the bottom
    glRotate(-180,1,0,0)
    #Draw light blue bottom
    drawface(.5, .5, 1)
    
    glPopMatrix()

def column():
    global angle
    glTranslate(0,-2.2,0)
    for i in range(5):
        drawcube()
        glRotate(angle+40, 0,1,0)
        glTranslate(0,1.1,0)

def mycubesdisplay() :
    global angle
    global framecount
    global start
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    
    #glRotate(angle, 0, 1, 0)
    angle += .1
    '''
    glTranslate(-3,0,0)
    for i in range(5):
        glPushMatrix()
        column()
        glPopMatrix()
        glTranslate(1.5,0,0)
        #glRotate(30, 0, 1, 0)
    '''
    glPushMatrix()
    
    glTranslate(-1,0,0)
    glPushMatrix()
    column()
    glPopMatrix()

    glPopMatrix()
    glTranslate(1,0,0)
    glPushMatrix()
    column()
    glPopMatrix()
    
    '''
    framecount += 1
    if framecount % 10000 == 0:
        #print time.time() - start
        #print framecount
        print framecount/ (time.time() - start)
    '''
    glutSwapBuffers()

ESCAPE = '\033' # The esc character
def keyPressed(*args):
    if args[0] == ESCAPE: 	# If escape is pressed, kill everything.
        glutDestroyWindow(window)
        sys.exit()

def BezCub(p0, p1, p2, p3, t):
    u = 1-t
    uu = u*u
    uuu = uu*u
    tt=t*t
    ttt = tt*t
    p0x, p0y, p0z = p0[0], p0[1], p0[2]
    p1x, p1y, p1z = p1[0], p1[1], p1[2]
    p2x, p2y, p2z = p2[0], p2[1], p2[2]
    p3x, p3y, p3z = p3[0], p3[1], p3[2]
    Ptx = uuu*p0x + 3*uu*t*p1x + 3*u*tt*p2x + ttt*p3x
    Pty = uuu*p0y + 3*uu*t*p1y + 3*u*tt*p2y + ttt*p3y
    Ptz = uuu*p0z + 3*uu*t*p1z + 3*u*tt*p2z + ttt*p3z
    return (Ptx, Pty, Ptz)

def lineVals(p0, p1, t):
    p0x, p0y, p0z = p0[0], p0[1], p0[2]
    p1x, p1y, p1z = p1[0], p1[1], p1[2]
    x = float(t) * p0x + (1 - t) * p1x
    y = float(t) * p0y + (1 - t) * p1y
    z = float(t) * p0z + (1 - t) * p1z
    return (x, y, z)

def mouseCallback(button, state, x,y):
    #global oldx
    #global oldy
    #print button, state, x, y
    pass
'''
Notes: 0 is left mouse button, 2 is right mouse button,
state 0 is press down, state 1 is lift up
'''
def pressmotion(x,y):
    global oldx
    global oldy
    deltax = (x-200)/200.
    deltay = (200-y)/200.
    #print deltax, deltay
    oldx = oldx+deltax
    oldy = oldy+deltay
    print oldx, oldy
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 1, 0.1, 100)
    gluLookAt(oldx, oldy, 10, 0, 0, 0, 0, 1, 0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def motion(x,y):
    pass

def mydisplay() :
    global angle
    global framecount
    global start
    global t
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    drawcube()
    
    '''
    framecount += 1
    if framecount % 10000 == 0:
        #print time.time() - start5
        #print framecount
        print framecount/ (time.time() - start)
    '''
    glutSwapBuffers()

def main():
    global window
    global angle
    global framecount
    global start
    global t
    global oldx
    global oldy
    oldx = 0
    oldy = 0
    start = time.time()
    framecount = 0
    angle = 0
    t = 0
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    
    glutInitWindowSize(400,400)
    window = glutCreateWindow("pygl1")
    glutKeyboardFunc(keyPressed)
    glClearColor(1,1,1,1)
    glShadeModel(GL_SMOOTH)
    
    glutDisplayFunc(mydisplay)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)
    glutIdleFunc(mydisplay)

    glutMouseFunc(mouseCallback)
    glutMotionFunc(pressmotion)
    glutPassiveMotionFunc(motion)
    
    '''
    #Lighting
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (1,1,1))
    #glLightfv(GL_LIGHT0, GL_POSITION, (2,2,4,0))
    #glLightfv(GL_LIGHT0, GL_SPOT_DIRECTION, (-2,-2,-4))
    '''
    
    '''
    #Texture
    global texture
    texture= glGenTextures(1); # number of textures to generate                                                   glBindTexture(GL_TEXTURE_2D, texture
    glPixelStorei(GL_UNPACK_ALIGNMENT,1)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

    img = imageLoader.loadImage("gravel_texture_gif.gif")
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img.width, img.height, 0,      
         GL_RGB, GL_UNSIGNED_BYTE, img.data)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
    glEnable(GL_TEXTURE_2D)
    '''
    #glEnable(GL_CULL_FACE)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 1, 0.1, 100)
    gluLookAt(0, 0, 10, 0, 0, 0, 0, 1, 0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
    glutMainLoop();

if __name__ == '__main__':main()




#this was in mydisplay

'''
#glRotate(angle, 0, 1, 0)
#angle += .01
if t <= 1:
    t += .0001
else:
    t = 0

p0 = (-3, -1, 1)
p1= (-3, 4, 1)
p2 = (3, 6, 1)
p3 = (3, 3, 1)
#run BezCub to get new point for x value
newbez = BezCub(p0, p1, p2, p3, t)
#run lineVals to get new point for y value
newline = lineVals(p0, p3, t)
    
glTranslate(newbez[0], newline[1], 0)
drawcube()
'''


#draw bezier curve
'''
p0 = (-3, -3, 1)
p1 = (-1.5, 8, -2)
p2 = (1.5, -8, 0)
p3 = (3, 3, 1)
old = p0
glBegin(GL_LINE_STRIP)
glColor3f(0,0,0)
glVertex3f(old[0], old[1], old[2])
for i in range(0,100, 4):
    t = i/100.0
    #run BezCub to get new point
    new = BezCub(p0, p1, p2, p3, t)
    #draw line to new point
    glVertex3f(new[0], new[1], new[2])
    #reset old
    old = new
glEnd()
'''




"""
#Draw green back
drawface(0,1,0)

#move forward
glTranslate(0,0,1)
#Draw red front
#drawface(1,0,0)

#rotate 90* around y axis to form left side
glRotate(90, 0,0,1)
#Draw blue left
drawface(0,0,1)

#Rotate the other way to form the other side
glRotate(-180, 0,1,0)
#Draw black right
drawface(0,0,0)

#rotate to form bottom
glRotate(90, 1,0,0)
#Draw purple bottom
drawface(.5, 0, .5)

#Rotate the other way to form the top
glRotate(-180,1,0,0)
#Draw light blue top
drawface(.5, .5, 1)
"""




"""
glBegin(GL_POLYGON);
#CCW by default
glColor3f(1,0,0)
glVertex2f(-0.5, -0.5);
glColor3f(0,1,0)
glVertex2f(0.5, -0.5);
glColor3f(0,0,1)
glVertex2f(0.5, 0.5);
glColor3f(1,1,1)
glVertex2f(-0.5, 0.5);
glEnd();


glTranslate(0, 0, -.5)
glRotate(30, 1,0,0)

glBegin(GL_POLYGON);
#CCW by default
glColor3f(0,0,0)
glVertex2f(-0.5, -0.5);
glVertex2f(0.5, -0.5);
glVertex2f(0.5, 0.5);
glVertex2f(-0.5, 0.5);
glEnd();
"""
"""
#Left, blue
glBegin(GL_POLYGON)
glColor3f(0,0,1)
glVertex3f(-.5, -.5, -.5)
glVertex3f(-.5, .5, -.5)
glVertex3f(-.5, .5, .5)
glVertex3f(-.5, -.5, .5)
glEnd()

glTranslate(1,0,0)
#Right, black
glBegin(GL_POLYGON)
glColor3f(0,0,0)
glVertex3f(-.5, -.5, -.5)
glVertex3f(-.5, .5, -.5)
glVertex3f(-.5, .5, .5)
glVertex3f(-.5, -.5, .5)
glEnd()

glTranslate(-1,0,0)
#Top, purple
glBegin(GL_POLYGON)
glColor3f(.5,0,.5)
glVertex3f(-.5, .5, .5)
glVertex3f(-.5, .5, -.5)
glVertex3f(.5, .5, -.5)
glVertex3f(.5, .5, .5)
glEnd()

glTranslate(0,-1,0)
#Bottom, light blue
glBegin(GL_POLYGON)
glColor3f(.5,.5,1)
glVertex3f(-.5, .5, .5)
glVertex3f(-.5, .5, -.5)
glVertex3f(.5, .5, -.5)
glVertex3f(.5, .5, .5)
glEnd()
"""




'''
glBegin(GL_QUAD_STRIP)
glColor3f(1,0,0)
glTexCoord2f(0,0)
glVertex3f(-.5, -.5, -.5)
glTexCoord2f(2,0)
glVertex3f(.5, -.5, -.5)
glColor3f(0,0,1)
glTexCoord2f(0,2)
glVertex3f(-.5, .5, -.5)
glTexCoord2f(2,2)
glVertex3f(.5, .5, -.5)

glEnd()
'''
'''
glColor3f(0,1,0)
glVertex3f(-.5, 1, -.5)
glVertex3f(.5, 1, -.5)
glColor3f(1,1,0)
glVertex3f(-.5, 1.5, 0)
glVertex3f(.5, 1.5, 0)
'''
