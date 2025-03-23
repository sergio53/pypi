## This script provides a visual and interactive way to understand the Tower of Hanoi puzzle.

### Explanation:

1. **TowerOfHanoiSolver Function**:
   - This function solves the Tower of Hanoi puzzle recursively and returns the sequence of moves.

2. **tripleDraw Class**:
   - This class is responsible for drawing the towers and disks using `ipycanvas`.
   - The `__init__` method initializes the canvas and draws the static parts (bases and towers).
   - The `draw` method updates the canvas to reflect the current state of the disks on the towers.

3. **play_hanoi Function**:
   - This function manages the gameplay, allowing the user to step through the solution one move at a time.
   - It uses a generator to yield moves and updates the display accordingly.

4. **TowerOfHanoiRunner Function**:
   - This function ties everything together, solving the puzzle and setting up the visualization.
