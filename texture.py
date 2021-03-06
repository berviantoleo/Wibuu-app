import numpy as np
from glumpy import app, gl, glm, gloo, data
from os.path import abspath 

def cube():
    vtype = [('a_position', np.float32, 3),
             ('a_texcoord', np.float32, 2),
             ('a_normal',   np.float32, 3)]
    itype = np.uint32

    # Vertices positions
    p = np.array([[1, 1, 1], [-1, 1, 1], [-1, -1, 1], [1, -1, 1],
                  [1, -1, -1], [1, 1, -1], [-1, 1, -1], [-1, -1, -1]], dtype=float)
    # Face Normals
    n = np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0],
                  [-1, 0, 1], [0, -1, 0], [0, 0, -1]])
    # Texture coords
    t = np.array([[0, 0], [0, 1], [1, 1], [1, 0]])

    faces_p = [0, 1, 2, 3,  0, 3, 4, 5,   0, 5, 6, 1,
               1, 6, 7, 2,  7, 4, 3, 2,   4, 7, 6, 5]
    faces_n = [0, 0, 0, 0,  1, 1, 1, 1,   2, 2, 2, 2,
               3, 3, 3, 3,  4, 4, 4, 4,   5, 5, 5, 5]
    faces_t = [0, 1, 2, 3,  0, 1, 2, 3,   0, 1, 2, 3,
               0, 1, 2, 3,  0, 1, 2, 3,   0, 1, 2, 3]

    vertices = np.zeros(24, vtype)
    vertices['a_position'] = p[faces_p]
    vertices['a_normal']   = n[faces_n]
    vertices['a_texcoord'] = t[faces_t]

    filled = np.resize(
       np.array([0, 1, 2, 0, 2, 3], dtype=itype), 6 * (2 * 3))
    filled += np.repeat(4 * np.arange(6, dtype=itype), 6)
    vertices = vertices.view(gloo.VertexBuffer)
    filled = filled.view(gloo.IndexBuffer)

    return vertices, filled



vertex = """
uniform mat4   u_model;         // Model matrix
uniform mat4   u_view;          // View matrix
uniform mat4   u_projection;    // Projection matrix
attribute vec3 a_position;      // Vertex position
attribute vec3 a_texcoord;      // Vertex texture coordinates
varying vec3   v_texcoord;      // Interpolated fragment texture coordinates (out)
void main()
{
    // Assign varying variables
    v_texcoord  = a_texcoord;
    // Final position
    gl_Position = u_projection * u_view * u_model * vec4(a_position,1.0);
}
"""

fragment = """
uniform samplerCube texture;
    varying vec3 v_texcoord;
    void main()
    {
        gl_FragColor = textureCube(texture, v_texcoord);
    }
"""

window = app.Window(width=1024, height=1024,
                    color=(0.30, 0.30, 0.35, 1.00))

@window.event
def on_draw(dt):
	global phi, theta, duration

	window.clear()
	gl.glDisable(gl.GL_BLEND)
	gl.glEnable(gl.GL_DEPTH_TEST)
	cube.draw(gl.GL_TRIANGLES, indices)

	# Rotate cube
	theta += 0.5 # degrees
	phi += 0.5 # degrees
	model = np.eye(4, dtype=np.float32)
	glm.rotate(model, theta, 0, 0, 1)
	glm.rotate(model, phi, 0, 1, 0)
	glm.scale(model, 1)
	cube['u_model'] = model

@window.event
def on_resize(width, height):
    cube['u_projection'] = glm.perspective(45.0, width / float(height), 2.0, 100.0)

@window.event
def on_init():
    gl.glEnable(gl.GL_DEPTH_TEST)

texture = np.zeros((6,1024,1024,3),dtype=np.float32).view(gloo.TextureCube)
texture.interpolation = gl.GL_LINEAR
texture[2] = data.get(abspath("Left_t2.png"))/255.
texture[3] = data.get(abspath("Right_t2.png"))/255.
texture[0] = data.get(abspath("Front_t2.png"))/255.
texture[1] = data.get(abspath("Back_t2.png"))/255.
texture[4] = data.get(abspath("Top_t2.png"))/255.
texture[4] = data.get(abspath("Top_t2.png"))/255.
texture[5] = data.get(abspath("Bottom_t2.png"))/255.

vertices, indices = cube()
cube = gloo.Program(vertex, fragment)
cube.bind(vertices)
model = np.eye(4,dtype=np.float32)
cube['texture'] = texture
cube['u_model'] = model
cube['u_view'] = glm.translation(0, 0, -5)
phi, theta = 40, 30

app.run()