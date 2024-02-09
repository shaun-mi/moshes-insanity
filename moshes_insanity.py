"""
Moshe's Insanity

This game takes 8 small cubes and stacks them into a 2x2x2 stack so that the larger cube built has a solid color on each face.
"""
from itertools import permutations
from random import randint

# Cube position designations are as follows:
# 0: bottom face
# 1: top face
# 2: face directly facing you
# 3-5: faces in counter-clockwise order from #2

# These are valid abbreviations for the cube colors.
CUBE_COLORS = ['B', 'G', 'P', 'R', 'W', 'Y']

def spin_cube_clockwise(cube):
    """Return a new cube which is the given cube turned clockwise."""
    # the first 2 are top and bottom. Since we are spinning, they stay the same.
    new_cube = cube[:2]
    # the next 3 are the last 3 in the provided cube because we count faces counter-clockwise
    new_cube += cube[3:]
    # the last 1 in the new cube is the first face in the given cube
    new_cube += (cube[2],)
    return new_cube

def safe_remove_cube_from_list(cubes, cube_to_remove):
    """Remove the given cube from the list of cubes without crashing if the cube doesn't exist in the list."""
    try:
        cubes.remove(cube_to_remove)
    except ValueError:
        # if the cube doesn't exist in the list, don't crash the program
        return False
    return True

def generate_cubes():
    """Generates the 30 unique cubes for the game."""
    # Start with 6! =720 permutations.
    # We can fix the bottom color to always be the same color since every cube has one of each color. In this case, we choose yellow.
    # If we reverse the top and bottom colors, it's the same as the sides reversed, too (hence all duplicates). That leaves 5! = 120 permutations.
    cubes = [c for c in permutations(CUBE_COLORS) if c[0] == "Y"]
    
    # The cubes where the top and bottom are the same but the sides rotated (spinning the cube) are duplicate cubes,
    # so divide by 4. That leaves 30 permutations.
    for i in range(0,30):
        c = cubes[i]
        c1 = spin_cube_clockwise(c)
        c2 = spin_cube_clockwise(c1)
        c3 = spin_cube_clockwise(c2)
        safe_remove_cube_from_list(cubes, c1)
        safe_remove_cube_from_list(cubes, c2)
        safe_remove_cube_from_list(cubes, c3)

    return cubes

def get_corners(cube):
    """Get list of the 8 corners in the given cube."""
    top = cube[1]
    bottom = cube[0]
    return [
        top    + cube[2] + cube[3],
        top    + cube[3] + cube[4],
        top    + cube[4] + cube[5],
        top    + cube[5] + cube[2],
        bottom + cube[2] + cube[3],
        bottom + cube[3] + cube[4],
        bottom + cube[4] + cube[5],
        bottom + cube[5] + cube[2],
    ]

def spin_corner(corner):
    """Get the same corner if the cube was spun on rotation. Example: YRP -> RPY"""
    return corner[1:] + corner[0]

def get_all_corner_names(corner):
    """Create the set of all corner names for this corner by spinning it."""
    corner1 = spin_corner(corner)
    corner2 = spin_corner(corner1)
    return { corner, corner1, corner2 }

def is_corner_matching(corner1, corner2):
    """Determine if two corners match. The corner may need to be spun to find a match."""
    return any(get_all_corner_names(corner1).intersection(get_all_corner_names(corner2)))

def has_matching_corners(cube1, cube2):
    """"Get the set of corners that match between the given cubes."""
    corners1 = set(get_corners(cube1))
    corners2 = set(get_corners(cube2))
    for corner1 in corners1:
        for corner2 in corners2:
            if is_corner_matching(corner1, corner2):
                return True
    return False

def has_a_matching_corner(corner1, cube2):
    """Determine whether a given corner matches any corners of the given cube."""
    for corner2 in set(get_corners(cube2)):
        if is_corner_matching(corner1, corner2):
            return True
    return False

def generate_exclusions(possible_cubes):
    """Build a dictionary of cube index to list of cube indices that have no corners in common."""
    exclusions = {}
    for i, cube_key in enumerate(possible_cubes):
        exclusion_list = {j for j, cube_value in enumerate(possible_cubes) if not has_matching_corners(cube_key, cube_value)}
        exclusions[i] = exclusion_list
    return exclusions

def generate_chessboard(cubes, oracle_cube):
    """
    Generate the chess board with the rows and columns.
    Rows are the 8 cubes.
    Columns are the corners of the 2x2x2 cube if it were completed.
    """
    # A cube is represented as a Tuple of colors; for example ('Y', 'B', 'G', 'P', 'R', 'W')
    oracle_corners = get_corners(oracle_cube)
    chessboard = {}
    for c in cubes:
        top = oracle_cube[1]
        bottom = oracle_cube[0]
        chessboard[''.join(c)] = { corner : has_a_matching_corner(corner, c) for corner in oracle_corners }
    return chessboard

def print_chessboard(chessboard, oracle_cube):
    """Print the chessboard to console."""
    # print oracle cube
    print("oracle cube:", "".join(oracle_cube))
    # print column headers: the corners of the oracle cube
    print("       " + " ".join(next(iter(chessboard.values())).keys()))
    # print the row: cube + value
    for cube in chessboard:
        values = [str(int(v)) for v in chessboard[cube].values()]
        print(cube + "  " + "   ".join(values))

def get_oracle_cubes(possible_cubes, exclusions, game_cube_numbers):
    """Determine the set of oracle cubes for the given game cubes. This only checks for exclusions,
    so it is possible that an oracle cube has no solution."""
    # For each possible cube, if none of the game cubes are in its exclusion list, it's an oracle cube.
    g = set(game_cube_numbers)
    oracles = []
    for c, _ in enumerate(possible_cubes):
        if not any(g.intersection(exclusions[c])):
            oracles.append(c)
    return oracles


def main():
    # Create the set of 30 possible small cubes
    possible_cubes = generate_cubes()

    # TODO: Delete this. This is just so Moshe can verify that I did this correctly.
    print()
    print("The set of unique cubes:")
    for i, x in enumerate(possible_cubes):
        print(f"    {i}:{x}")

    # Create the set of exclusions by cube
    exclusions = generate_exclusions(possible_cubes)

    # TODO: Delete this. This is just so Moshe can verify that I did this correctly.
    print()
    print("Exclusion sets are:")
    for k in exclusions:
        print(f"    {k}:{exclusions[k]}")

    # Pick a random set of 8 cubes to play with
    game_cube_numbers = set()
    while len(game_cube_numbers) < 8:
        game_cube_numbers.add(randint(0, 29))
    game_cubes = [possible_cubes[c] for c in game_cube_numbers]
    
    print()
    print("game cubes are:")
    for c in game_cube_numbers:
        print("   ", c, possible_cubes[c])
    

    # Calculate the oracle_cube
    oracle_cubes = get_oracle_cubes(possible_cubes, exclusions, game_cube_numbers)

    print()
    print("oracle cubes are:")
    print("   ", oracle_cubes)
    if not oracle_cubes:
        print("There are no possible oracle cubes.")
    else:
        oracle_cube_number = oracle_cubes[0]
        oracle_cube = possible_cubes[oracle_cube_number]
        
        chessboard = generate_chessboard(game_cubes, oracle_cube)
        print()
        print("chessboard:")
        print_chessboard(chessboard, oracle_cube)


if __name__ == "__main__":
    main()