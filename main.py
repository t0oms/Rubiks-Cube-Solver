# Toms Pētersons tp22016
# Rubik's cube scrambler and solver

from ursina import *
from rubiks.cube import Cube

def update():
    """Checks if any of the faces should be rotating and then rotates them by a little bit every frame"""
    if cube.rotateForwards['Y'] == True:
        if cube.origin.rotation_y <= 90:  # rotates the face 90 degreees
            cube.origin.rotation_y += time.dt * cube.rotationSpeed
        else:
            cube.origin.rotation_y = 0
            cube.rotateForwards['Y'] = False
            cube.resetParents()
            cube.rotateForwardsData('Y')
            cube.updateColors()
            cube.insideStat1.visible = False  # makes the inside elements invisisible again
            cube.insideRot1.visible = False

    if cube.rotateBackwards['Y'] == True:
        if cube.origin.rotation_y >= -90:
            cube.origin.rotation_y -= time.dt * cube.rotationSpeed
        else:
            cube.origin.rotation_y = 0
            cube.rotateBackwards['Y'] = False
            cube.resetParents()
            cube.rotateBackwardsData('Y')
            cube.updateColors()
            cube.insideStat1.visible = False
            cube.insideRot1.visible = False

    if cube.rotateForwards['W'] == True:
        if cube.origin.rotation_y >= -90:
            cube.origin.rotation_y -= time.dt * cube.rotationSpeed
        else:
            cube.origin.rotation_y = 0
            cube.rotateForwards['W'] = False
            cube.resetParents()
            cube.rotateForwardsData('W')
            cube.updateColors()
            cube.insideStat2.visible = False
            cube.insideRot2.visible = False

    if cube.rotateBackwards['W'] == True:
        if cube.origin.rotation_y <= 90:
            cube.origin.rotation_y += time.dt * cube.rotationSpeed
        else:
            cube.origin.rotation_y = 0
            cube.rotateBackwards['W'] = False
            cube.resetParents()
            cube.rotateBackwardsData('W')
            cube.updateColors()
            cube.insideStat2.visible = False
            cube.insideRot2.visible = False

    if cube.rotateForwards['B'] == True:
        if cube.origin.rotation_z <= 90:
            cube.origin.rotation_z += time.dt * cube.rotationSpeed
        else:
            cube.origin.rotation_z = 0
            cube.rotateForwards['B'] = False
            cube.resetParents()
            cube.rotateForwardsData('B')
            cube.updateColors()
            cube.insideStat3.visible = False
            cube.insideRot3.visible = False

    if cube.rotateBackwards['B'] == True:
        if cube.origin.rotation_z >= -90:
            cube.origin.rotation_z -= time.dt * cube.rotationSpeed
        else:
            cube.origin.rotation_z = 0
            cube.rotateBackwards['B'] = False
            cube.resetParents()
            cube.rotateBackwardsData('B')
            cube.updateColors()
            cube.insideStat3.visible = False
            cube.insideRot3.visible = False

    if cube.rotateForwards['R'] == True:
        if cube.origin.rotation_x <= 90:
            cube.origin.rotation_x += time.dt * cube.rotationSpeed
        else:
            cube.origin.rotation_x = 0
            cube.rotateForwards['R'] = False
            cube.resetParents()
            cube.rotateForwardsData('R')
            cube.updateColors()
            cube.insideStat4.visible = False
            cube.insideRot4.visible = False

    if cube.rotateBackwards['R'] == True:
        if cube.origin.rotation_x >= -90:
            cube.origin.rotation_x -= time.dt * cube.rotationSpeed
        else:
            cube.origin.rotation_x = 0
            cube.rotateBackwards['R'] = False
            cube.resetParents()
            cube.rotateBackwardsData('R')
            cube.updateColors()
            cube.insideStat4.visible = False
            cube.insideRot4.visible = False

    if cube.rotateForwards['G'] == True:
        if cube.origin.rotation_z >= -90:
            cube.origin.rotation_z -= time.dt * cube.rotationSpeed
        else:
            cube.origin.rotation_z = 0
            cube.rotateForwards['G'] = False
            cube.resetParents()
            cube.rotateForwardsData('G')
            cube.updateColors()
            cube.insideStat5.visible = False
            cube.insideRot5.visible = False

    if cube.rotateBackwards['G'] == True:
        if cube.origin.rotation_z <= 90:
            cube.origin.rotation_z += time.dt * cube.rotationSpeed
        else:
            cube.origin.rotation_z = 0
            cube.rotateBackwards['G'] = False
            cube.resetParents()
            cube.rotateBackwardsData('G')
            cube.updateColors()
            cube.insideStat5.visible = False
            cube.insideRot5.visible = False

    if cube.rotateForwards['O'] == True:
        if cube.origin.rotation_x >= -90:
            cube.origin.rotation_x -= time.dt * cube.rotationSpeed
        else:
            cube.origin.rotation_x = 0
            cube.rotateForwards['O'] = False
            cube.resetParents()
            cube.rotateForwardsData('O')
            cube.updateColors()
            cube.insideStat6.visible = False
            cube.insideRot6.visible = False

    if cube.rotateBackwards['O'] == True:
        if cube.origin.rotation_x <= 90:
            cube.origin.rotation_x += time.dt * cube.rotationSpeed
        else:
            cube.origin.rotation_x = 0
            cube.rotateBackwards['O'] = False
            cube.resetParents()
            cube.rotateBackwardsData('O')
            cube.updateColors()
            cube.insideStat6.visible = False
            cube.insideRot6.visible = False


def input(key):
    """The user input function"""

    # when the user presses space the program enters or exits the soliving mode
    if key == "space":
        if cube.solvingModeOn:
            cube.solvingModeOn = False

            # show the need text elements for the soliving mode
            for i in [c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11]:
                i.enabled = True

            # hide the not needed elements for the solving mode
            c12.enabled = False
            c13.enabled = False
            c14.enabled = False
            solivingText.enabled = False
            for i in [s1, s2, s3, s4, s5, s6, s7, s8, s9]:
                i.enabled = False
        else:
            # if the cube is solved the solving steps should be green. Else red
            if cube.isCubeSolved():
                for i in [s1, s2, s3, s4, s5, s6, s7, s8, s9]:
                    i.color = color.green
            else:
                for i in [s1, s2, s3, s4, s5, s6, s7, s8, s9]:
                    i.color = color.red

            cube.solvingModeOn = True
            cube.solve()

            # show the needed text elements and  hide the unneeded.
            for i in [c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11]:
                i.enabled = False
            c12.enabled = True
            c13.enabled = True
            c14.enabled = True
            solivingText.enabled = True
            for i in [s1, s2, s3, s4, s5, s6, s7, s8, s9]:
                i.enabled = True

    # when the  solving mode is off accept the other input
    if cube.solvingModeOn == False:
        cube.reverse = held_keys['shift']  # when shift is held rotation is reverse
        positions = cube.getFacePositions(camera)

        if cube.rotateForwards['Y'] == False and cube.rotateBackwards['Y'] == False and cube.rotateForwards[
            'W'] == False and cube.rotateBackwards['W'] == False and cube.rotateForwards['B'] == False and \
                cube.rotateBackwards['B'] == False and cube.rotateForwards['O'] == False and cube.rotateBackwards[
            'O'] == False and cube.rotateForwards['G'] == False and cube.rotateBackwards['G'] == False and \
                cube.rotateForwards['R'] == False and cube.rotateBackwards['R'] == False:

            # scramble the cube
            if key == 'r':
                cube.randomCube()
                cube.updateColors()

            # rotate top
            if key == 'up arrow' and cube.reverse == False:
                cube.rotateForwards['Y'] = True
                cube.rotateDraw('Y')

            if key == 'up arrow' and cube.reverse:
                cube.rotateBackwards['Y'] = True
                cube.rotateDraw('Y')

            # rotate bottom
            if key == 'down arrow' and cube.reverse == False:
                cube.rotateForwards['W'] = True
                cube.rotateDraw('W')

            if key == 'down arrow' and cube.reverse:
                cube.rotateBackwards['W'] = True
                cube.rotateDraw('W')

            # rotate front side
            if key == 's' and cube.reverse == False:
                cube.rotateForwards[positions["front"]] = True
                cube.rotateDraw(positions["front"])

            if key == 's' and cube.reverse:
                cube.rotateBackwards[positions["front"]] = True
                cube.rotateDraw(positions["front"])

            # rotate left side
            if key == 'a' and cube.reverse == False:
                cube.rotateForwards[positions["left"]] = True
                cube.rotateDraw(positions["left"])

            if key == 'a' and cube.reverse:
                cube.rotateBackwards[positions["left"]] = True
                cube.rotateDraw(positions["left"])

            # rotate back side
            if key == 'w' and cube.reverse == False:
                cube.rotateForwards[positions["back"]] = True
                cube.rotateDraw(positions["back"])

            if key == 'w' and cube.reverse:
                cube.rotateBackwards[positions["back"]] = True
                cube.rotateDraw(positions["back"])

            # rotate right side
            if key == 'd' and cube.reverse == False:
                cube.rotateForwards[positions["right"]] = True
                cube.rotateDraw(positions["right"])

            if key == 'd' and cube.reverse:
                cube.rotateBackwards[positions["right"]] = True
                cube.rotateDraw(positions["right"])

    # when the solving mode is on accept only direction arrow input for moving throught steps
    elif cube.rotateForwards['Y'] == False and cube.rotateBackwards['Y'] == False and cube.rotateForwards[
        'W'] == False and cube.rotateBackwards['W'] == False and cube.rotateForwards['B'] == False and \
            cube.rotateBackwards['B'] == False and cube.rotateForwards['O'] == False and cube.rotateBackwards[
        'O'] == False and cube.rotateForwards['G'] == False and cube.rotateBackwards['G'] == False and \
            cube.rotateForwards['R'] == False and cube.rotateBackwards['R'] == False:
        # move forwards in solving steps
        if key == "right arrow":
            if cube.solvingPosition < len(cube.solveMoveList):
                cube.solivingMove(cube.solveMoveList[cube.solvingPosition])
                cube.solvingPosition += 1
            # colors the solving step green when it is reached
            if cube.flowerSolvedPoistion == cube.solvingPosition:
                s1.color = color.green

            if cube.whiteCrossSolvedPosition == cube.solvingPosition:
                s2.color = color.green

            if cube.bottomSolvedPosition == cube.solvingPosition:
                s3.color = color.green

            if cube.middleSolvedPosition == cube.solvingPosition:
                s4.color = color.green

            if cube.yellowCrossSolvedPosition == cube.solvingPosition:
                s5.color = color.green

            if cube.yellowSolvedPosition == cube.solvingPosition:
                s6.color = color.green

            if cube.CornersSolvedPosition == cube.solvingPosition:
                s7.color = color.green

            if cube.EdgesSolvedPosition == cube.solvingPosition:
                s8.color = color.green

            if cube.cubeSolvedPosition == cube.solvingPosition:
                s9.color = color.green

        # move backwards in solving steps
        if key == "left arrow":
            if cube.solvingPosition > 0:
                cube.solvingPosition -= 1
                cube.solivingMove(cube.solveMoveListBack[cube.solvingPosition])

            # colors the solving step red when you when it is no longer true
            if cube.flowerSolvedPoistion == cube.solvingPosition + 1:
                s1.color = color.red

            if cube.whiteCrossSolvedPosition == cube.solvingPosition + 1:
                s2.color = color.red

            if cube.bottomSolvedPosition == cube.solvingPosition + 1:
                s3.color = color.red

            if cube.middleSolvedPosition == cube.solvingPosition + 1:
                s4.color = color.red

            if cube.yellowCrossSolvedPosition == cube.solvingPosition + 1:
                s5.color = color.red

            if cube.yellowSolvedPosition == cube.solvingPosition + 1:
                s6.color = color.red

            if cube.CornersSolvedPosition == cube.solvingPosition + 1:
                s7.color = color.red

            if cube.EdgesSolvedPosition == cube.solvingPosition + 1:
                s8.color = color.red

            if cube.cubeSolvedPosition == cube.solvingPosition + 1:
                s9.color = color.red


app = Ursina()

window.fps_counter.enabled = False
window.entity_counter.enabled = False
window.collider_counter.enabled = False
window.cog_button.enabled = False

camera = EditorCamera(move_speed=0)

cube = Cube()

# all of the text elements
controlsText = Text('Controls:', x=-.87, y=.475)
c1 = Text("'right mouse' - rotate cube", scale=0.75, x=-.87, y=.44, color=color.rgb(186, 186, 186))
c2 = Text("'W' - rotate Back side", scale=0.75, x=-.87, y=.41, color=color.rgb(186, 186, 186))
c3 = Text("'A' - rotate Left side", scale=0.75, x=-.87, y=.38, color=color.rgb(186, 186, 186))
c4 = Text("'S' - rotate Front side", scale=0.75, x=-.87, y=.35, color=color.rgb(186, 186, 186))
c5 = Text("'D' - rotate Right side", scale=0.75, x=-.87, y=.32, color=color.rgb(186, 186, 186))
c6 = Text("'UP arrow' - rotate Top side", scale=0.75, x=-.87, y=.29, color=color.rgb(186, 186, 186))
c7 = Text("'DOWN arrow' - rotate Bottom side", scale=0.75, x=-.87, y=.26, color=color.rgb(186, 186, 186))
c8 = Text("hold 'SHIFT' - rotate side backwards", scale=0.75, x=-.87, y=.23, color=color.rgb(186, 186, 186))
c9 = Text("'SCROLL mouse' - zoom in/out", scale=0.75, x=-.87, y=.20, color=color.rgb(186, 186, 186))
c10 = Text("'R' - randomly scramble cube", scale=0.75, x=-.87, y=.17, color=color.rgb(186, 186, 186))
c11 = Text("'SPACE' - enter soliving mode", scale=0.75, x=-.87, y=.14, color=color.rgb(186, 186, 186))
c12 = Text("'SPACE' - exit soliving mode", scale=0.75, x=-.87, y=.44, color=color.rgb(186, 186, 186), enabled=False)
c13 = Text("'RIGHT arrow' - next solving move", scale=0.75, x=-.87, y=.41, color=color.rgb(186, 186, 186),
           enabled=False)
c14 = Text("'LEFT arrow' - previous solving move", scale=0.75, x=-.87, y=.38, color=color.rgb(186, 186, 186),
           enabled=False)

solivingText = Text('Soliving steps:', x=-.87, y=-0.18, enabled=False)
s1 = Text("Flower solved", scale=0.75, x=-.87, y=-0.21, color=color.red, enabled=False)
s2 = Text("White cross solved", scale=0.75, x=-.87, y=-0.24, color=color.red, enabled=False)
s3 = Text("Bottom layer solved", scale=0.75, x=-.87, y=-0.27, color=color.red, enabled=False)
s4 = Text("Middle layer solved", scale=0.75, x=-.87, y=-0.3, color=color.red, enabled=False)
s5 = Text("Yellow cross solved", scale=0.75, x=-.87, y=-0.33, color=color.red, enabled=False)
s6 = Text("Yellow face solved", scale=0.75, x=-.87, y=-0.36, color=color.red, enabled=False)
s7 = Text("Corners solved", scale=0.75, x=-.87, y=-0.39, color=color.red, enabled=False)
s8 = Text("Edges solved", scale=0.75, x=-.87, y=-0.42, color=color.red, enabled=False)
s9 = Text("Rubik's cube solved", scale=0.75, x=-.87, y=-0.45, color=color.red, enabled=False)

app.run()