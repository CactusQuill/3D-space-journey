@echo off

REM Set the project root directory
set ROOT_DIR=3d-space-journey

REM Create main project directory
mkdir %ROOT_DIR%
cd %ROOT_DIR%

REM Create source code directories
mkdir src
mkdir src\models
mkdir src\shaders
mkdir src\utils

REM Create assets and fonts directories
mkdir assets
mkdir assets\textures
mkdir assets\fonts

REM Create documentation and tests directories
mkdir docs
mkdir tests

REM Create main files in the root directory
echo # 3D Space Journey with Solar System, Galaxies, and Stars > README.md
echo python main.py > .gitignore
echo Python requirements for the project > requirements.txt
echo MIT License > LICENSE

REM Create main.py in src folder
echo # Main entry point > src\main.py

REM Create settings.py for configurations
echo # Configuration and constants for the project > src\settings.py

REM Create models folder files
echo # Define classes for planets, moons, etc. > src\models\celestial_objects.py
echo # Define Galaxy and star creation functions > src\models\galaxy.py
echo # Define Saturn's ring and similar structures > src\models\ring.py

REM Create shaders (vertex and fragment shaders)
echo // Vertex shader > src\shaders\vertex_shader.glsl
echo // Fragment shader > src\shaders\fragment_shader.glsl

REM Create utils helper file
echo # Helper functions for geometry, physics > src\utils\math_utils.py

REM Create README for documentation
echo # Project Documentation > docs\README.md
echo # Detailed setup and configuration guide > docs\setup_guide.md

REM Create test files
echo # Tests for celestial objects functionality > tests\test_celestial_objects.py
echo # Tests for galaxy generation and rendering > tests\test_galaxy.py
echo # Tests for utility functions > tests\test_utils.py

echo Project structure created successfully.
