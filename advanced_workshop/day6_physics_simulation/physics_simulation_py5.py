"""
Day 6: Physics-Based Generative Art (py5 version)
==================================================

Explore Newton's Laws of Motion and apply them to create
dynamic, physics-driven generative art.

Learning Objectives:
- Understand Newton's Three Laws of Motion
- Implement realistic physics simulations
- Create gravity, springs, and collision systems
- Build kinetic sculptures and force fields

Newton's Laws:
1. Inertia: An object at rest stays at rest, an object in motion
   stays in motion (unless acted upon by a force)
2. F = ma: Force equals mass times acceleration
3. Action-Reaction: Every action has an equal and opposite reaction

Run with: python physics_simulation_py5.py
"""

import py5
import math

# Simulation objects
objects = []
springs = []
mode = 0
modes = [
    "Newton's 1st Law (Inertia)",
    "Newton's 2nd Law (F=ma)",
    "Newton's 3rd Law (Action-Reaction)",
    "Gravity Well",
    "Spring Physics",
    "Kinetic Sculpture"
]

# Physics constants
GRAVITY = 0.3
FRICTION = 0.99
BOUNCE = 0.8


class PhysicsObject:
    """A physics-enabled object with mass, position, velocity, and acceleration."""

    def __init__(self, x, y, mass=1.0):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.ax = 0
        self.ay = 0
        self.mass = mass
        self.radius = mass * 10
        self.col = py5.color(
            py5.random(100, 255),
            py5.random(100, 255),
            py5.random(100, 255)
        )
        self.trail = []
        self.max_trail = 50

    def apply_force(self, fx, fy):
        """Apply a force to this object (F = ma, so a = F/m)."""
        self.ax += fx / self.mass
        self.ay += fy / self.mass

    def update(self):
        """Update physics: velocity += acceleration, position += velocity."""
        # Newton's 2nd Law: acceleration changes velocity
        self.vx += self.ax
        self.vy += self.ay

        # Apply friction
        self.vx *= FRICTION
        self.vy *= FRICTION

        # Update position
        self.x += self.vx
        self.y += self.vy

        # Reset acceleration each frame
        self.ax = 0
        self.ay = 0

        # Store trail
        self.trail.append((self.x, self.y))
        if len(self.trail) > self.max_trail:
            self.trail.pop(0)

    def check_boundaries(self):
        """Bounce off screen edges."""
        if self.x - self.radius < 0:
            self.x = self.radius
            self.vx *= -BOUNCE
        elif self.x + self.radius > py5.width:
            self.x = py5.width - self.radius
            self.vx *= -BOUNCE

        if self.y - self.radius < 0:
            self.y = self.radius
            self.vy *= -BOUNCE
        elif self.y + self.radius > py5.height:
            self.y = py5.height - self.radius
            self.vy *= -BOUNCE

    def display(self, show_trail=True):
        """Draw the object and its trail."""
        # Draw trail
        if show_trail and len(self.trail) > 1:
            py5.no_fill()
            py5.stroke(py5.red(self.col), py5.green(self.col), py5.blue(self.col), 100)
            py5.stroke_weight(2)
            py5.begin_shape()
            for tx, ty in self.trail:
                py5.vertex(tx, ty)
            py5.end_shape()

        # Draw object
        py5.fill(self.col)
        py5.stroke(255)
        py5.stroke_weight(2)
        py5.ellipse(self.x, self.y, self.radius * 2, self.radius * 2)

        # Draw velocity vector
        py5.stroke(255, 255, 0)
        py5.stroke_weight(2)
        py5.line(self.x, self.y, self.x + self.vx * 5, self.y + self.vy * 5)


class Spring:
    """A spring connecting two physics objects."""

    def __init__(self, obj_a, obj_b, rest_length=100, stiffness=0.05):
        self.obj_a = obj_a
        self.obj_b = obj_b
        self.rest_length = rest_length
        self.stiffness = stiffness
        self.damping = 0.1

    def update(self):
        """Apply spring force to connected objects."""
        # Calculate distance
        dx = self.obj_b.x - self.obj_a.x
        dy = self.obj_b.y - self.obj_a.y
        distance = math.sqrt(dx * dx + dy * dy)

        if distance == 0:
            return

        # Calculate spring force (Hooke's Law: F = -k * displacement)
        displacement = distance - self.rest_length
        force = self.stiffness * displacement

        # Normalize direction
        nx = dx / distance
        ny = dy / distance

        # Apply force to both objects (Newton's 3rd Law)
        fx = force * nx
        fy = force * ny

        self.obj_a.apply_force(fx, fy)
        self.obj_b.apply_force(-fx, -fy)

    def display(self):
        """Draw the spring."""
        py5.stroke(150)
        py5.stroke_weight(2)
        py5.line(self.obj_a.x, self.obj_a.y, self.obj_b.x, self.obj_b.y)


def setup():
    py5.size(800, 600)
    reset_simulation()

    print("Day 6: Physics-Based Generative Art")
    print("\nNewton's Laws of Motion:")
    print("  1st Law (Inertia): Objects maintain their state of motion")
    print("  2nd Law (F=ma): Force = mass x acceleration")
    print("  3rd Law: Every action has an equal and opposite reaction")
    print("\nControls:")
    print("  Press 1-6 to switch modes")
    print("  Click to interact (mode-dependent)")
    print("  Press 'r' to reset simulation")
    print("  Press 's' to save image")
    print("  Press 'q' to quit")


def reset_simulation():
    """Reset the simulation for the current mode."""
    global objects, springs
    objects = []
    springs = []

    if mode == 0:  # Newton's 1st Law - Inertia
        # Create objects with initial velocities
        obj = PhysicsObject(200, 300, 2)
        obj.vx = 3
        obj.vy = 0
        objects.append(obj)

        obj2 = PhysicsObject(600, 300, 2)
        obj2.vx = 0  # At rest
        obj2.vy = 0
        objects.append(obj2)

    elif mode == 1:  # Newton's 2nd Law - F=ma
        # Create objects with different masses
        for i in range(3):
            mass = (i + 1) * 1.5
            obj = PhysicsObject(150 + i * 200, 300, mass)
            objects.append(obj)

    elif mode == 2:  # Newton's 3rd Law - Action-Reaction
        # Create two objects that will collide
        obj1 = PhysicsObject(200, 300, 2)
        obj1.vx = 4
        objects.append(obj1)

        obj2 = PhysicsObject(600, 300, 2)
        obj2.vx = -4
        objects.append(obj2)

    elif mode == 3:  # Gravity Well
        # Create orbiting objects
        center_x, center_y = py5.width / 2, py5.height / 2
        for i in range(5):
            angle = i * py5.TWO_PI / 5
            dist = 150
            obj = PhysicsObject(
                center_x + py5.cos(angle) * dist,
                center_y + py5.sin(angle) * dist,
                py5.random(1, 3)
            )
            # Give tangential velocity for orbit
            obj.vx = -py5.sin(angle) * 3
            obj.vy = py5.cos(angle) * 3
            objects.append(obj)

    elif mode == 4:  # Spring Physics
        # Create a chain of springs
        prev = None
        for i in range(5):
            obj = PhysicsObject(200 + i * 100, 300, 1.5)
            objects.append(obj)
            if prev is not None:
                springs.append(Spring(prev, obj, 100, 0.03))
            prev = obj
        # Fix the first object
        objects[0].mass = 1000  # Very heavy = fixed

    elif mode == 5:  # Kinetic Sculpture
        # Create a complex spring network
        center_x, center_y = py5.width / 2, py5.height / 2

        # Central anchor (fixed)
        anchor = PhysicsObject(center_x, center_y, 1000)
        objects.append(anchor)

        # Orbiting nodes
        for i in range(6):
            angle = i * py5.TWO_PI / 6
            obj = PhysicsObject(
                center_x + py5.cos(angle) * 150,
                center_y + py5.sin(angle) * 150,
                1.5
            )
            objects.append(obj)
            springs.append(Spring(anchor, obj, 150, 0.02))

            # Connect to neighbors
            if i > 0:
                springs.append(Spring(objects[i], obj, 100, 0.01))


def draw():
    py5.background(20)

    # Update and display based on mode
    if mode == 0:
        draw_first_law()
    elif mode == 1:
        draw_second_law()
    elif mode == 2:
        draw_third_law()
    elif mode == 3:
        draw_gravity_well()
    elif mode == 4:
        draw_spring_physics()
    elif mode == 5:
        draw_kinetic_sculpture()

    # Draw UI
    draw_ui()


def draw_first_law():
    """Demonstrate Newton's First Law: Inertia."""
    for obj in objects:
        obj.update()
        obj.check_boundaries()
        obj.display()

    # Explanation
    py5.fill(255)
    py5.text_size(12)
    py5.text("Left ball: Moving at constant velocity", 20, py5.height - 50)
    py5.text("Right ball: At rest, stays at rest", 20, py5.height - 35)
    py5.text("Click to apply a force to any ball", 20, py5.height - 20)


def draw_second_law():
    """Demonstrate Newton's Second Law: F = ma."""
    # Apply same force to all (gravity)
    for obj in objects:
        # Same force, different accelerations due to mass
        obj.apply_force(0, obj.mass * GRAVITY)
        obj.update()
        obj.check_boundaries()
        obj.display()

        # Show mass label
        py5.fill(255)
        py5.text_size(12)
        py5.text_align(py5.CENTER)
        py5.text(f"m={obj.mass:.1f}", obj.x, obj.y - obj.radius - 10)

    py5.text_align(py5.LEFT)
    py5.fill(255)
    py5.text_size(12)
    py5.text("Same force applied, different acceleration (a = F/m)", 20, py5.height - 40)
    py5.text("Heavier objects accelerate slower. Click to add upward force.", 20, py5.height - 20)


def draw_third_law():
    """Demonstrate Newton's Third Law: Action-Reaction."""
    # Check for collision
    if len(objects) >= 2:
        obj1, obj2 = objects[0], objects[1]
        dx = obj2.x - obj1.x
        dy = obj2.y - obj1.y
        dist = math.sqrt(dx * dx + dy * dy)
        min_dist = obj1.radius + obj2.radius

        if dist < min_dist and dist > 0:
            # Collision! Apply equal and opposite forces
            nx = dx / dist
            ny = dy / dist

            # Relative velocity
            dvx = obj1.vx - obj2.vx
            dvy = obj1.vy - obj2.vy
            dvn = dvx * nx + dvy * ny

            # Only collide if objects are approaching
            if dvn > 0:
                # Impulse (simplified elastic collision)
                impulse = dvn * 1.5

                # Apply to both objects (equal and opposite)
                obj1.vx -= impulse * nx
                obj1.vy -= impulse * ny
                obj2.vx += impulse * nx
                obj2.vy += impulse * ny

                # Separate objects
                overlap = min_dist - dist
                obj1.x -= overlap * nx / 2
                obj1.y -= overlap * ny / 2
                obj2.x += overlap * nx / 2
                obj2.y += overlap * ny / 2

    for obj in objects:
        obj.update()
        obj.check_boundaries()
        obj.display()

    py5.fill(255)
    py5.text_size(12)
    py5.text("When objects collide, they exert equal and opposite forces", 20, py5.height - 40)
    py5.text("Watch the momentum exchange! Press 'r' to reset.", 20, py5.height - 20)


def draw_gravity_well():
    """Simulate gravitational attraction."""
    center_x, center_y = py5.width / 2, py5.height / 2

    # Draw gravity well
    py5.no_fill()
    for i in range(5):
        alpha = 100 - i * 20
        py5.stroke(100, 150, 255, alpha)
        py5.stroke_weight(1)
        py5.ellipse(center_x, center_y, 50 + i * 60, 50 + i * 60)

    # Draw center mass
    py5.fill(255, 200, 100)
    py5.no_stroke()
    py5.ellipse(center_x, center_y, 40, 40)

    for obj in objects:
        # Calculate gravitational force toward center
        dx = center_x - obj.x
        dy = center_y - obj.y
        dist = math.sqrt(dx * dx + dy * dy)

        if dist > 30:  # Avoid singularity at center
            # F = G * m1 * m2 / r^2 (simplified)
            force = 200 / (dist * dist) * obj.mass
            force = min(force, 2)  # Cap force

            nx = dx / dist
            ny = dy / dist
            obj.apply_force(force * nx * 50, force * ny * 50)

        obj.update()
        obj.display()

    py5.fill(255)
    py5.text_size(12)
    py5.text("Gravitational attraction: F = G*m1*m2/r^2", 20, py5.height - 40)
    py5.text("Click to add new orbiting objects", 20, py5.height - 20)


def draw_spring_physics():
    """Demonstrate spring physics with Hooke's Law."""
    # Apply gravity to all except fixed objects
    for obj in objects:
        if obj.mass < 100:  # Not fixed
            obj.apply_force(0, GRAVITY * 10)

    # Update springs
    for spring in springs:
        spring.update()
        spring.display()

    # Update and display objects
    for obj in objects:
        if obj.mass < 100:  # Not fixed
            obj.update()
            obj.check_boundaries()
        obj.display(show_trail=False)

    py5.fill(255)
    py5.text_size(12)
    py5.text("Hooke's Law: F = -k * x (spring force)", 20, py5.height - 40)
    py5.text("Drag the balls to stretch the springs", 20, py5.height - 20)


def draw_kinetic_sculpture():
    """Create a kinetic sculpture with springs."""
    # Update springs
    for spring in springs:
        spring.update()
        spring.display()

    # Update and display objects
    for obj in objects:
        if obj.mass < 100:  # Not fixed
            # Add slight random perturbation
            obj.apply_force(py5.random(-0.5, 0.5), py5.random(-0.5, 0.5))
            obj.update()
        obj.display(show_trail=True)

    py5.fill(255)
    py5.text_size(12)
    py5.text("Kinetic sculpture: Combined spring forces create organic motion", 20, py5.height - 40)
    py5.text("Click to disturb the sculpture", 20, py5.height - 20)


def draw_ui():
    """Draw mode indicator."""
    py5.fill(255)
    py5.no_stroke()
    py5.text_size(16)
    py5.text_align(py5.LEFT)
    py5.text(f"Mode {mode + 1}: {modes[mode]}", 20, 30)
    py5.text_size(12)
    py5.text("Press 1-6 to switch modes | 'r' to reset | 's' to save", 20, 50)


def mouse_pressed():
    """Handle mouse interaction."""
    global objects

    if mode == 0:  # Apply force to nearest object
        for obj in objects:
            dx = py5.mouse_x - obj.x
            dy = py5.mouse_y - obj.y
            dist = math.sqrt(dx * dx + dy * dy)
            if dist < 100:
                obj.apply_force(-dx * 0.5, -dy * 0.5)

    elif mode == 1:  # Apply upward force
        for obj in objects:
            obj.apply_force(0, -20)

    elif mode == 3:  # Add new orbiting object
        center_x, center_y = py5.width / 2, py5.height / 2
        obj = PhysicsObject(py5.mouse_x, py5.mouse_y, py5.random(1, 3))
        # Calculate tangential velocity
        dx = py5.mouse_x - center_x
        dy = py5.mouse_y - center_y
        dist = math.sqrt(dx * dx + dy * dy)
        if dist > 0:
            obj.vx = -dy / dist * 4
            obj.vy = dx / dist * 4
        objects.append(obj)

    elif mode == 5:  # Disturb sculpture
        for obj in objects:
            if obj.mass < 100:
                dx = obj.x - py5.mouse_x
                dy = obj.y - py5.mouse_y
                dist = math.sqrt(dx * dx + dy * dy)
                if dist > 0 and dist < 200:
                    force = 10 / dist * 100
                    obj.apply_force(dx / dist * force, dy / dist * force)


def mouse_dragged():
    """Handle mouse dragging for spring mode."""
    if mode == 4:
        for obj in objects:
            if obj.mass < 100:
                dx = py5.mouse_x - obj.x
                dy = py5.mouse_y - obj.y
                dist = math.sqrt(dx * dx + dy * dy)
                if dist < obj.radius * 2:
                    obj.x = py5.mouse_x
                    obj.y = py5.mouse_y
                    obj.vx = 0
                    obj.vy = 0


def key_pressed():
    global mode

    if py5.key == '1':
        mode = 0
        reset_simulation()
    elif py5.key == '2':
        mode = 1
        reset_simulation()
    elif py5.key == '3':
        mode = 2
        reset_simulation()
    elif py5.key == '4':
        mode = 3
        reset_simulation()
    elif py5.key == '5':
        mode = 4
        reset_simulation()
    elif py5.key == '6':
        mode = 5
        reset_simulation()
    elif py5.key == 'r':
        reset_simulation()
        print(f"Simulation reset: {modes[mode]}")
    elif py5.key == 's':
        filename = f"physics_{modes[mode].replace(' ', '_')}_{py5.frame_count}.png"
        py5.save(filename)
        print(f"Saved: {filename}")
    elif py5.key == 'q':
        py5.exit_sketch()


# -------------------------------------------------
# Newton's Laws of Motion:
#
# 1st Law (Inertia):
#    An object at rest stays at rest.
#    An object in motion stays in motion.
#    (Unless acted upon by an external force)
#
# 2nd Law (F = ma):
#    Force equals mass times acceleration.
#    More massive objects need more force to accelerate.
#    a = F / m
#
# 3rd Law (Action-Reaction):
#    For every action, there is an equal and
#    opposite reaction. When A pushes B, B pushes A.
#
# Physics Implementation:
#    acceleration = force / mass
#    velocity += acceleration
#    position += velocity
#
# Hooke's Law (Springs):
#    F = -k * x
#    Force is proportional to displacement from rest length
#
# Gravitational Force:
#    F = G * m1 * m2 / r^2
#    Force decreases with square of distance
# -------------------------------------------------

py5.run_sketch()
