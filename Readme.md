# 3D Space Journey with Solar System, Galaxies, and Stars

A **3D space simulation** built using `Pyglet`, `ModernGL`, and `Pyrr` libraries. This project visualizes a miniaturized version of the **Solar System**, including **orbiting moons**, **Saturn’s ring**, **galaxies**, and **distant stars** to create an immersive space exploration experience. The simulation includes a counter that tracks Earth's orbits around the Sun in real-time.

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [Future Enhancements](#future-enhancements)

## Project Overview

This 3D space simulation allows users to observe a scaled-down Solar System, where each planet, moon, and galaxy moves with simplified orbital physics. Using this project, you can visualize:

1. **The Solar System**: Planets orbiting around the Sun, with Earth’s moon orbiting Earth.
2. **Realistic Space Elements**: Spiral galaxies, stars, and additional celestial objects.
3. **Orbit Counter**: A display counter that tracks Earth's completed orbits around the Sun, shown in the top-left corner.

The primary goal is to create a visually engaging representation of space while maintaining modularity and simplicity.

## Features

- **Planetary Orbits**: Each planet has a unique speed and orbital distance.
- **Earth’s Moon**: The moon orbits Earth, creating a secondary orbit.
- **Saturn’s Ring**: A ring structure is visualized around Saturn.
- **Spiral Galaxies and Stars**: Multiple galaxies with randomized orientations and colors, along with a background of distant stars.
- **Orbit Counter**: A display that increments each time Earth completes an orbit around the Sun.

## Requirements

- **Python 3.10+**
- **Pyglet**: `pip install pyglet`
- **ModernGL**: `pip install moderngl`
- **Pyrr**: `pip install pyrr`

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/3d-space-journey.git
    cd 3d-space-journey
    ```

2. Install dependencies:

    ```bash
    pip install pyglet moderngl pyrr
    ```

3. Run the project:

    ```bash
    python main.py
    ```

## Usage

- **Mouse Controls**: Drag the left mouse button to rotate the view. Use the mouse wheel to zoom in and out.
- **Display**: Observe the orbit counter in the top-left corner, which increments as Earth completes each orbit.

## How It Works

This simulation builds a 3D space scene with various celestial objects and uses trigonometric functions to animate planetary orbits around the Sun.

### Components

1. **Solar System**: Each planet has unique properties like distance, color, and speed, giving each a distinct orbit.
2. **Earth’s Moon**: The moon orbits Earth by calculating its position relative to Earth in each frame.
3. **Saturn’s Ring**: Saturn’s ring is a flat disk represented with vertices arranged in concentric circles.
4. **Galaxies**: Each galaxy is a point-based spiral with randomized orientation, position, and color for variety.
5. **Orbit Counter**: A `pyglet.text.Label` updates with each full orbit of Earth around the Sun.

### Code Structure

- **Procedural Design**: Currently, the code is written in a procedural style for simplicity.
- **Real-Time Rendering**: The simulation updates each frame using `on_draw()` and `update()` functions, with real-time adjustments to object positions and rotations.

## Future Enhancements

To make the simulation more accurate, visually appealing, and modular, the next steps include:

1. **Object-Oriented Refactoring**: Transition the project to an object-oriented structure for better modularity and maintainability.
    - Create classes for celestial bodies (`Planet`, `Moon`, `Star`, `Galaxy`, etc.).
    - Implement a `SolarSystem` class to manage inter-object interactions and rendering.
  
2. **Visual Detail Improvements**:
    - **Enhanced Models**: Add more detail to planets, rings, and stars, with higher resolution for smoother shapes.
    - **Texture Mapping**: Apply textures to planets and galaxies to create a more realistic look.
  
3. **Lighting and Shadows**:
    - **Dynamic Lighting**: Implement light sources (like the Sun) to cast realistic lighting on planets.
    - **Shadow Casting**: Integrate shadows for planets and moons, improving the depth and realism of the simulation.

4. **Physics-Based Movements**:
    - **Realistic Distances and Speeds**: Adjust distances, sizes, and orbital speeds to more accurately represent real-world values.
    - **Physics Calculations**: Incorporate basic physics to calculate gravitational influence and orbital mechanics for improved accuracy.

5. **Performance Optimizations**:
    - **Level of Detail (LOD)**: Implement LOD techniques to reduce the detail of distant objects.
    - **Frustum Culling**: Improve performance by only rendering objects within the visible area of the camera.

## Conclusion

This 3D Space Journey project provides an educational and entertaining representation of the Solar System and galaxies. Future enhancements will improve its realism, accuracy, and visual fidelity, creating an even more captivating experience. Contributions and suggestions for improvement are always welcome!
