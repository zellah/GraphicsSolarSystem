"""
A model of the solar system.
Created by Zella Henderson
December 2011
"""

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import sys
import time
import imageLoader

"""
Notes:
This program requires 10 gifs and imageLoader.py.

This is a mostly-to-scale replica of our solar system.
The planets' relative sizes, distances from the sun, and
orbit speeds and direction are roughly accurate.
The sun has been shrunk so that the small inner planets are visible.
To aid in visibility, final_inner displays only the inner 4 planets,
whereas final_system displays all the planets (zoomed farther out).

This displays texture mapping to a sphere and a luminescent object
(light source inside the sun). Shadows proved too complex to be worthile.

Known problems:
The texture mapped to the moons' surfaces doesn't display properly
due to the moons' small sizes- the same texture map works fine on the
larger planets.
Texture mapping to the large planets worked poorly- the loaded image
seems to be set up as a 1x1 image regardless of its original size,
and 
I haven't rendered Jupiter's rings.
The moons all rotate at the same rate, which isn't strictly accurate.

Sources:
http://www.opengl.org/sdk/docs/man/xhtml/glColorMaterial.xml
http://www.cse.msu.edu/~cse872/tutorial4.html
http://www.blitzmax.com/Community/posts.php?topic=43543
http://www.opengl.org/discussion_boards/ubbthreads.php?ubb=showflat&Number=234880
http://en.wikipedia.org/wiki/Solar_System and related
"""

# A global variable storing our window ID
# (not very pythonic by standard practice for OpenGL)
window = 0

ESCAPE = '\033' # The esc character
def keyPressed(*args):
    if args[0] == ESCAPE: 	# If escape is pressed, kill everything.
        glutDestroyWindow(window)
        sys.exit()

def SolarSystem():
    global angle
    angle += .05
    
    #sets up radiant light from the sun at the origin
    #without emission, the light source will be dark because it'll be inside the sun
    glColorMaterial(GL_FRONT_AND_BACK, GL_EMISSION)

    #sets up texture mapping
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_TEXTURE_GEN_S)
    glEnable(GL_TEXTURE_GEN_T)
    #glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
    glTexGeni(GL_S, GL_TEXTURE_GEN_MODE, GL_OBJECT_LINEAR)
    glTexGeni(GL_T, GL_TEXTURE_GEN_MODE, GL_OBJECT_LINEAR)

    glBindTexture(GL_TEXTURE_2D, textures[0])
    #the sun
    Planet(12, 1, .9, .4, PlanetType.SUN)
    #glColorMaterial(GL_FRONT_AND_BACK, GL_DIFFUSE)
    
    #Mercury
    glPushMatrix()
    glRotate(15*angle, 0, 1, 0)
    #move so orbit has r=4
    glTranslate(12+4,0,0)
    glBindTexture(GL_TEXTURE_2D, textures[1])
    #radius 0.6, color (.52, .52, .52)
    Planet(.6, .52, .52, .52, PlanetType.MERCURY)
    glPopMatrix()

    #Venus
    glPushMatrix()
    glRotate(2.5*angle, 0, 1, 0)
    #move so orbit has r=7
    glTranslate(12+7,0,0)
    glBindTexture(GL_TEXTURE_2D, textures[2])
    #planet has radius 1, color (.7, .7, 0)
    Planet(1, .72, .45, .12, PlanetType.VENUS)
    glPopMatrix()

    #Earth
    glPushMatrix()
    glRotate(angle, 0, 1, 0)
    #move so orbit has r=10
    glTranslate(12+10,0,0)
    glBindTexture(GL_TEXTURE_2D, textures[3])
    Planet(1.2, .37, .4, 0.6, PlanetType.EARTH)
    glPopMatrix()

    #Mars
    glPushMatrix()
    glRotate(1.03*angle, 0, 1, 0)
    #move so orbit has r=15
    glTranslate(12+15,0,0)
    glBindTexture(GL_TEXTURE_2D, textures[4])
    Planet(.8, .8, .55, .32, PlanetType.MARS)
    glPopMatrix()

    #Jupiter
    glPushMatrix()
    glRotate(0.4*angle, 0, 1, 0)
    #move so orbit has r=52
    glTranslate(12+52,0,0)
    glBindTexture(GL_TEXTURE_2D, textures[5])
    Planet(10, .52, .42, .35, PlanetType.JUPITER)
    glPopMatrix()

    #Saturn
    glPushMatrix()
    glRotate(0.45*angle, 0, 1, 0)
    #move so orbit has r=95
    glTranslate(12+95,0,0)
    glBindTexture(GL_TEXTURE_2D, textures[6])
    Planet(9, .92, .77, .51, PlanetType.SATURN)
    glPopMatrix()

    #Uranus
    glPushMatrix()
    glRotate(-0.71*angle, 0, 1, 0)
    #move so orbit has r=196
    glTranslate(12+196,0,0)
    glBindTexture(GL_TEXTURE_2D, textures[7])
    Planet(5, .73, .88, .88, PlanetType.URANUS)
    glPopMatrix()

    #Neptune
    glPushMatrix()
    glRotate(0.71*angle, 0, 1, 0)
    #move so orbit has r=300
    glTranslate(12+300,0,0)
    glBindTexture(GL_TEXTURE_2D, textures[8])
    Planet(4, .45, .65, 1, PlanetType.NEPTUNE)
    glPopMatrix()

class PlanetType(object):
    SUN = 0
    MERCURY = 1
    VENUS = 2
    EARTH = 3
    MARS = 4
    JUPITER = 5
    SATURN = 6
    URANUS = 7
    NEPTUNE = 8

def Planet(r, c1, c2, c3, planet_type):
    glColor3f(c1, c2, c3)
    glutSolidSphere(r, 20, 20)
    if planet_type == 3:
        #Earth has one moon
        Moon(0,0,1)
    if planet_type == 4:
        #Mars has two moons, Phobos and Deimos
        glPushMatrix()
        #moon that starts above the planet
        Moon(0,0,1)
        glPopMatrix()
        #moon with a satellite that starts right of the planet
        Moon(1,0,0)
    if planet_type >= 5:
        #Jupiter has 64 moons, Saturn 62, Uranus unknown Neptune 12.
        #I'm rendering 6 in all cases.
        glPushMatrix()
        Moon(0,0,4)
        glPopMatrix()
        glPushMatrix()
        Moon(4,0,0)
        glPopMatrix()
        glPushMatrix()
        Moon(0,0,4)
        glPopMatrix()
        glPushMatrix()
        Moon(0,4,4)
        glPopMatrix()
        glPushMatrix()
        Moon(4,0,4)
        glPopMatrix()
        glPushMatrix()
        Moon(4,4,0)
        glPopMatrix()

def Moon(x, y, z):
    glRotate(angle*8, x,y,z)
    #Translate (in a different direction than the axis of rotation)
    ## to move out of the planet's center
    glTranslate(y*2, z*2, x*2)
    glBindTexture(GL_TEXTURE_2D, textures[4])
    glColor3f(.5, .5, .5)
    glutSolidSphere(.2, 10, 10)

def mydisplay() :
    global angle
    global framecount
    global start
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    SolarSystem()
    glutSwapBuffers()

def drawSolarSystem():
    global window
    global angle
    global framecount
    global start
    start = time.time()
    framecount = 0
    angle = 0
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)

    glutInitWindowSize(800,800)
    window = glutCreateWindow("Inner planets")
    glutKeyboardFunc(keyPressed)
    glClearColor(0,0,0,1)
    glShadeModel(GL_SMOOTH)

    glutDisplayFunc(mydisplay)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)
    glutIdleFunc(mydisplay)
    
    #Lighting
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (.3,.3,.3, 1))
    glLightfv(GL_LIGHT0, GL_POSITION, (0,0,0,1))
    #glLightfv(GL_LIGHT0, GL_SPOT_DIRECTION, (-2,-2,-4))
    
    #Texture
    global textures
    textures= glGenTextures(10); # number of textures to generate
    glBindTexture(GL_TEXTURE_2D, textures[0])
    glPixelStorei(GL_UNPACK_ALIGNMENT,1)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

    img0 = imageLoader.loadImage("sun.gif")
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img0.width, img0.height, 0,      
         GL_RGB, GL_UNSIGNED_BYTE, img0.data)

    glBindTexture(GL_TEXTURE_2D, textures[1])
    glPixelStorei(GL_UNPACK_ALIGNMENT,1)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    
    img1 = imageLoader.loadImage("mercury.gif")
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img1.width, img1.height, 0,      
         GL_RGB, GL_UNSIGNED_BYTE, img1.data)

    glBindTexture(GL_TEXTURE_2D, textures[2])
    glPixelStorei(GL_UNPACK_ALIGNMENT,1)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    
    img2 = imageLoader.loadImage("venus.gif")
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img2.width, img2.height, 0,      
         GL_RGB, GL_UNSIGNED_BYTE, img2.data)

    glBindTexture(GL_TEXTURE_2D, textures[3])
    glPixelStorei(GL_UNPACK_ALIGNMENT,1)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    
    img3 = imageLoader.loadImage("earth.gif")
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img3.width, img3.height, 0,      
         GL_RGB, GL_UNSIGNED_BYTE, img3.data)

    glBindTexture(GL_TEXTURE_2D, textures[4])
    glPixelStorei(GL_UNPACK_ALIGNMENT,1)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    
    img4 = imageLoader.loadImage("mars.gif")
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img4.width, img4.height, 0,      
         GL_RGB, GL_UNSIGNED_BYTE, img4.data)

    glBindTexture(GL_TEXTURE_2D, textures[5])
    glPixelStorei(GL_UNPACK_ALIGNMENT,1)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    
    img5 = imageLoader.loadImage("jupiter.gif")
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img5.width, img5.height, 0,      
         GL_RGB, GL_UNSIGNED_BYTE, img5.data)

    glBindTexture(GL_TEXTURE_2D, textures[6])
    glPixelStorei(GL_UNPACK_ALIGNMENT,1)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    
    img6 = imageLoader.loadImage("saturn.gif")
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img6.width, img6.height, 0,      
         GL_RGB, GL_UNSIGNED_BYTE, img6.data)

    glBindTexture(GL_TEXTURE_2D, textures[7])
    glPixelStorei(GL_UNPACK_ALIGNMENT,1)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    
    img7 = imageLoader.loadImage("uranus.gif")
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img7.width, img7.height, 0,      
         GL_RGB, GL_UNSIGNED_BYTE, img7.data)

    glBindTexture(GL_TEXTURE_2D, textures[8])
    glPixelStorei(GL_UNPACK_ALIGNMENT,1)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    
    img8 = imageLoader.loadImage("neptune.gif")
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img8.width, img8.height, 0,      
         GL_RGB, GL_UNSIGNED_BYTE, img8.data)

    glBindTexture(GL_TEXTURE_2D, textures[9])
    glPixelStorei(GL_UNPACK_ALIGNMENT,1)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    
    img9 = imageLoader.loadImage("moon.gif")
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img9.width, img9.height, 0,      
         GL_RGB, GL_UNSIGNED_BYTE, img9.data)
    
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 1, 0.1, 400)
    gluLookAt(0, 40, 80, 0, 0, 0, 0, 1, 0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
    glutMainLoop()


drawSolarSystem()











