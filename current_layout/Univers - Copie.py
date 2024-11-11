import numpy as np
import moderngl
import pyglet
from pyrr import Matrix44, Vector3
from math import sin, cos, pi
import random

# Window setup
window = pyglet.window.Window(width=800, height=600, resizable=True)
window.set_caption('3D Space Journey with Solar System, Orbits, Galaxies, Stars, and Black Holes')

# Context and shader program
ctx = moderngl.create_context()
prog = ctx.program(
    vertex_shader="""
    #version 330
    in vec3 in_position;
    in vec3 in_color;
    uniform mat4 model;
    uniform mat4 view;
    uniform mat4 proj;
    out vec3 color;
    void main() {
        gl_Position = proj * view * model * vec4(in_position, 1.0);
        color = in_color;
    }
    """,
    fragment_shader="""
    #version 330
    in vec3 color;
    out vec4 fragColor;
    void main() {
        fragColor = vec4(color, 1.0);
    }
    """
)

# Set background color
ctx.clear(0.01, 0.01, 0.02)

# Camera and movement parameters
initial_eye_distance = 30.0
camera_position = Vector3([0.0, 5.0, 25.0])
camera_target = Vector3([0.0, 0.0, 0.0])
eye_distance = initial_eye_distance
rotation_x = 0.0
rotation_y = 0.0
camera_speed = 0.1
time_elapsed = 0.0

# Solar System objects
solar_system_objects = [
    {"name": "Sun", "radius": 2.0, "distance": 0.0, "color": (1.0, 0.9, 0.0), "speed": 0},
    {"name": "Mercury", "radius": 0.2, "distance": 3.0, "color": (0.5, 0.5, 0.5), "speed": 0.4},
    {"name": "Venus", "radius": 0.5, "distance": 5.0, "color": (1.0, 0.8, 0.4), "speed": 0.3},
    {"name": "Earth", "radius": 0.5, "distance": 7.0, "color": (0.0, 0.5, 1.0), "speed": 0.25},
    {"name": "Mars", "radius": 0.3, "distance": 9.0, "color": (1.0, 0.2, 0.2), "speed": 0.2},
    {"name": "Jupiter", "radius": 1.0, "distance": 12.0, "color": (1.0, 0.6, 0.3), "speed": 0.15},
    {"name": "Saturn", "radius": 0.9, "distance": 15.0, "color": (1.0, 0.9, 0.6), "speed": 0.1},
    {"name": "Uranus", "radius": 0.7, "distance": 18.0, "color": (0.5, 1.0, 1.0), "speed": 0.08},
    {"name": "Neptune", "radius": 0.7, "distance": 21.0, "color": (0.3, 0.3, 1.0), "speed": 0.07}
]

moon = {
    "name": "Moon",
    "radius": 0.1,
    "distance": 1.0,
    "color": (0.8, 0.8, 0.8),
    "speed": 0.5,
    "parent": "Earth"
}

# Generate vertices for a sphere
def generate_sphere(radius, segments=12):
    vertices = []
    for i in range(segments + 1):
        theta = i * pi / segments
        sin_theta = sin(theta)
        cos_theta = cos(theta)
        for j in range(segments + 1):
            phi = j * 2 * pi / segments
            x = cos(phi) * sin_theta
            y = cos_theta
            z = sin(phi) * sin_theta
            vertices.extend([x * radius, y * radius, z * radius])
    return np.array(vertices, dtype='f4')

# Solar System VAOs
solar_vaos = []
for obj in solar_system_objects:
    sphere_vertices = generate_sphere(obj["radius"])
    vbo_sphere = ctx.buffer(sphere_vertices.tobytes())
    color = np.array([obj["color"]] * (len(sphere_vertices) // 3), dtype='f4')
    vbo_color = ctx.buffer(color.tobytes())
    vao = ctx.vertex_array(prog, [
        (vbo_sphere, '3f', 'in_position'),
        (vbo_color, '3f', 'in_color')
    ])
    solar_vaos.append((vao, obj))

# Moon VAO
earth_object = next(obj for obj in solar_system_objects if obj["name"] == "Earth")
moon_vao = ctx.vertex_array(
    prog,
    [
        (ctx.buffer(generate_sphere(moon["radius"]).tobytes()), '3f', 'in_position'),
        (ctx.buffer(np.array([moon["color"]] * (len(generate_sphere(moon["radius"])) // 3), dtype='f4').tobytes()), '3f', 'in_color'),
    ]
)
solar_vaos.append((moon_vao, moon))

# Orbit paths setup
orbit_vaos = []
orbit_color = (0.6, 0.6, 0.6)
orbit_segments = 100
for obj in solar_system_objects:
    if obj["distance"] > 0:
        orbit_vertices = []
        for i in range(orbit_segments):
            angle = i * (2 * pi / orbit_segments)
            x = cos(angle) * obj["distance"]
            z = sin(angle) * obj["distance"]
            orbit_vertices.extend([x, 0.0, z])
        vbo_orbit = ctx.buffer(np.array(orbit_vertices, dtype='f4').tobytes())
        vbo_orbit_color = ctx.buffer(np.array([orbit_color] * orbit_segments, dtype='f4').tobytes())
        orbit_vao = ctx.vertex_array(prog, [
            (vbo_orbit, '3f', 'in_position'),
            (vbo_orbit_color, '3f', 'in_color')
        ])
        orbit_vaos.append(orbit_vao)

# Saturn's ring
def generate_ring(inner_radius, outer_radius, segments=30):
    vertices = []
    for i in range(segments + 1):
        angle = i * 2 * pi / segments
        x_outer = cos(angle) * outer_radius
        z_outer = sin(angle) * outer_radius
        x_inner = cos(angle) * inner_radius
        z_inner = sin(angle) * inner_radius
        vertices.extend([x_inner, 0.0, z_inner, x_outer, 0.0, z_outer])
    return np.array(vertices, dtype='f4')

saturn_object = next(obj for obj in solar_system_objects if obj["name"] == "Saturn")
saturn_ring_vertices = generate_ring(1.2, 2.2)
saturn_ring_vao = ctx.vertex_array(
    prog,
    [
        (ctx.buffer(saturn_ring_vertices.tobytes()), '3f', 'in_position'),
        (ctx.buffer(np.array([(0.9, 0.7, 0.5)] * (len(saturn_ring_vertices) // 3), dtype='f4').tobytes()), '3f', 'in_color'),
    ]
)

# Generate spiral galaxy with varied orientations
num_stars_per_galaxy = 1000
spiral_arms = 4
max_galaxy_radius = 5.0
max_star_offset = 0.1

def generate_spiral_positions(num_stars, arms, radius, color_offset):
    positions = []
    colors = []
    for i in range(num_stars):
        arm_offset = (i % arms) * (2 * pi / arms)
        distance = (i / num_stars) * radius
        angle = distance * 5 + arm_offset
        x = cos(angle) * distance + random.uniform(-max_star_offset, max_star_offset)
        y = random.uniform(-max_star_offset, max_star_offset)
        z = sin(angle) * distance + random.uniform(-max_star_offset, max_star_offset)
        positions.append((x, y, z))
        color_intensity = 1 - (distance / radius)
        colors.append((
            color_intensity * (0.5 + color_offset[0]),
            color_intensity * (0.3 + color_offset[1]),
            color_intensity * (0.6 + color_offset[2])
        ))
    return np.array(positions, dtype='f4'), np.array(colors, dtype='f4')

# Galaxy VAOs
galaxies = []
num_galaxies = 200
for _ in range(num_galaxies):
    galaxy_radius = random.uniform(2.0, max_galaxy_radius)
    color_offset = (random.uniform(0.3, 0.7), random.uniform(0.3, 0.7), random.uniform(0.3, 0.7))
    galaxy_positions, galaxy_colors = generate_spiral_positions(num_stars_per_galaxy, spiral_arms, galaxy_radius, color_offset)
    depth_offset = random.uniform(-150, 150)
    galaxy_data = {
        "positions": galaxy_positions,
        "colors": galaxy_colors,
        "offset": Vector3([random.uniform(-150, 150), random.uniform(-100, 100), depth_offset]),
        "scale": galaxy_radius / max_galaxy_radius,
        "rotation": Matrix44.from_eulers((random.uniform(0, 2 * pi), random.uniform(0, 2 * pi), random.uniform(0, 2 * pi)))
    }
    vbo_positions = ctx.buffer(galaxy_data["positions"].tobytes())
    vbo_colors = ctx.buffer(galaxy_data["colors"].tobytes())
    vao = ctx.vertex_array(prog, [
        (vbo_positions, '3f', 'in_position'),
        (vbo_colors, '3f', 'in_color')
    ])
    galaxy_data["vao"] = vao
    galaxies.append(galaxy_data)

# Distant stars
num_stars = 2500
star_positions = []
for _ in range(num_stars):
    x = random.uniform(-200, 200)
    y = random.uniform(-150, 150)
    z = random.uniform(-200, 200)
    star_positions.extend([x, y, z])
vbo_stars = ctx.buffer(np.array(star_positions, dtype='f4').tobytes())
vbo_star_colors = ctx.buffer(np.array([(1.0, 1.0, 1.0)] * num_stars, dtype='f4').tobytes())
star_vao = ctx.vertex_array(prog, [
    (vbo_stars, '3f', 'in_position'),
    (vbo_star_colors, '3f', 'in_color')
])

# Update the view matrix for smooth camera movement
def update_view_matrix():
    global view
    rotation_matrix_x = Matrix44.from_x_rotation(rotation_x)
    rotation_matrix_y = Matrix44.from_y_rotation(rotation_y)
    rotated_position = rotation_matrix_x * rotation_matrix_y * Vector3([0, 0, -eye_distance])
    view = Matrix44.look_at(
        eye=camera_position + rotated_position,
        target=camera_target,
        up=(0.0, 1.0, 0.0),
    )
    prog['view'].write(view.astype('f4').tobytes())

# Animation function to update time and move Solar System objects
def update(dt):
    global time_elapsed, camera_position
    time_elapsed += dt
    camera_position.z += camera_speed * dt
    update_view_matrix()

# Rendering logic
@window.event
def on_draw():
    window.clear()
    ctx.clear(0.01, 0.01, 0.02)
    
    # Render orbital paths
    for orbit_vao in orbit_vaos:
        prog['model'].write(Matrix44.identity().astype('f4').tobytes())
        orbit_vao.render(moderngl.POINTS)
    
    # Render distant stars
    prog['model'].write(Matrix44.identity().astype('f4').tobytes())
    star_vao.render(moderngl.POINTS)
    
    # Render Solar System objects
    for vao, obj in solar_vaos:
        angle = time_elapsed * obj["speed"]
        position = Vector3([
            cos(angle) * obj["distance"],
            0,
            sin(angle) * obj["distance"]
        ]) if obj["distance"] > 0 else Vector3([0, 0, 0])
        translation = Matrix44.from_translation(position)
        prog['model'].write(translation.astype('f4').tobytes())
        vao.render(moderngl.TRIANGLE_STRIP)

    # Render the moon orbiting Earth
    earth_position = Vector3([
        cos(time_elapsed * earth_object["speed"]) * earth_object["distance"],
        0,
        sin(time_elapsed * earth_object["speed"]) * earth_object["distance"]
    ])
    moon_angle = time_elapsed * moon["speed"]  # Calculate the moon's orbital angle
    moon_position = Vector3([
        cos(moon_angle) * moon["distance"],
        0,
        sin(moon_angle) * moon["distance"]
    ]) + earth_position
    prog['model'].write(Matrix44.from_translation(moon_position).astype('f4').tobytes())
    moon_vao.render(moderngl.TRIANGLE_STRIP)

    # Render Saturn's ring
    saturn_position = Vector3([
        cos(time_elapsed * saturn_object["speed"]) * saturn_object["distance"],
        0,
        sin(time_elapsed * saturn_object["speed"]) * saturn_object["distance"]
    ])
    saturn_ring_translation = Matrix44.from_translation(saturn_position)
    prog['model'].write(saturn_ring_translation.astype('f4').tobytes())
    saturn_ring_vao.render(moderngl.TRIANGLE_STRIP)

    # Render galaxies with varied rotations
    for galaxy in galaxies:
        vao = galaxy["vao"]
        galaxy_translation = Matrix44.from_translation(galaxy["offset"] - camera_position)
        galaxy_scale = Matrix44.from_scale(Vector3([galaxy["scale"], galaxy["scale"], galaxy["scale"]]))
        model_matrix = galaxy_translation * galaxy_scale * galaxy["rotation"]
        prog['model'].write(model_matrix.astype('f4').tobytes())
        vao.render(moderngl.POINTS)
# Event handlers for resize and mouse control
@window.event
def on_resize(width, height):
    ctx.viewport = (0, 0, width, height)
    proj = Matrix44.perspective_projection(45.0, width / height, 0.1, 300.0)
    prog['proj'].write(proj.astype('f4').tobytes())

@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    global rotation_x, rotation_y
    if buttons & pyglet.window.mouse.LEFT:
        rotation_x += dy * 0.01
        rotation_y += dx * 0.01
        update_view_matrix()

@window.event
def on_mouse_scroll(x, y, scroll_x, scroll_y):
    global eye_distance
    eye_distance -= scroll_y * 0.5
    eye_distance = max(5.0, min(50.0, eye_distance))
    update_view_matrix()

# Run the app
pyglet.clock.schedule_interval(update, 1/60)
pyglet.app.run()
