import glfw

if not glfw.init():
    raise Exception("Cannot initialise GLFW.")
    
window = glfw.create_window(
    width=800, 
    height=800, 
    title="3D Gaussian Splatting", 
    monitor=None, 
    share=None
)

if not window:
    glfw.terminate()
    raise Exception("Cannot create GLFW window.")

glfw.set_window_pos(
    window=window, 
    xpos=400,
    ypos=100
)

glfw.make_context_current(window)

while not glfw.window_should_close(window):
    glfw.poll_events()
    glfw.swap_buffers(window)

glfw.terminate()
