from ursina import *
import copy
import numpy as np
from rubiks.face import Face

class Cube():
    """"
    The main Rubik's cubes class.
    """
    origin = Entity(model="sphere")

    def __init__(self):
        """"
        Initializes the colors of the cube and draws it
        """
        self.solvingModeOn = False

        # lists for storing the cube solving moves
        self.solveMoveList = []
        self.solveMoveListBack = []

        self.solvingPosition = 0

        self.solveDirection = None

        self.reverse = False  # when the user holds down shift

        self.rotationSpeed = 600  # cube side rotation animation speed

        # dictionaries used for knowing if the faces should still be rotating in the animation
        self.rotateForwards = {}
        self.rotateBackwards = {}

        self.rotateForwards['Y'] = False
        self.rotateForwards['W'] = False
        self.rotateForwards['B'] = False
        self.rotateForwards['R'] = False
        self.rotateForwards['G'] = False
        self.rotateForwards['O'] = False

        self.rotateBackwards['Y'] = False
        self.rotateBackwards['W'] = False
        self.rotateBackwards['B'] = False
        self.rotateBackwards['R'] = False
        self.rotateBackwards['G'] = False
        self.rotateBackwards['O'] = False

        # all of the face colors.
        # in the cubeFaces dictionary face name keys are created according to each of the faces center color ([1][1] in the matrix), because they never change when rotating the cube
        self.cubeFaces = {}
        self.cubeFaces["Y"] = Face([["Y", "Y", "Y"],
                                    ["Y", "Y", "Y"],
                                    ["Y", "Y", "Y"]])

        self.cubeFaces["W"] = Face([["W", "W", "W"],
                                    ["W", "W", "W"],
                                    ["W", "W", "W"]])

        self.cubeFaces["G"] = Face([["G", "G", "G"],
                                    ["G", "G", "G"],
                                    ["G", "G", "G"]])

        self.cubeFaces["R"] = Face([["R", "R", "R"],
                                    ["R", "R", "R"],
                                    ["R", "R", "R"]])

        self.cubeFaces["B"] = Face([["B", "B", "B"],
                                    ["B", "B", "B"],
                                    ["B", "B", "B"]])

        self.cubeFaces["O"] = Face([["O", "O", "O"],
                                    ["O", "O", "O"],
                                    ["O", "O", "O"]])

        self.cubeSolved = self.isCubeSolved()  # check if the cube is already solved

        # dictionary stores the cube rendering data of each of the cube face pieces
        self.drawData = {}
        self.drawData["Y"] = np.zeros((3, 3), Entity)
        self.drawData["W"] = np.zeros((3, 3), Entity)
        self.drawData["G"] = np.zeros((3, 3), Entity)
        self.drawData["R"] = np.zeros((3, 3), Entity)
        self.drawData["B"] = np.zeros((3, 3), Entity)
        self.drawData["O"] = np.zeros((3, 3), Entity)

        # assigns positions and rotations for each of the cube face colors
        z = 1
        for i in range(3):
            x = -1
            for j in range(3):
                self.drawData["Y"][i][j] = Entity(model="quad", texture="white_cube", position=(x, 1.5, z),
                                                  rotation=(90, 0, 0))
                x += 1
            z -= 1

        z = -1
        for i in range(3):
            x = -1
            for j in range(3):
                self.drawData["W"][i][j] = Entity(model="quad", texture="white_cube", position=(x, -1.5, z),
                                                  rotation=(-90, 0, 0))
                x += 1
            z += 1

        y = 1
        for i in range(3):
            x = 1
            for j in range(3):
                self.drawData["G"][i][j] = Entity(model="quad", texture="white_cube", position=(x, y, 1.5),
                                                  rotation=(0, 180, 0))
                x -= 1
            y -= 1

        y = 1
        for i in range(3):
            z = -1
            for j in range(3):
                self.drawData["R"][i][j] = Entity(model="quad", texture="white_cube", position=(1.5, y, z),
                                                  rotation=(0, -90, 0))
                z += 1
            y -= 1

        y = 1
        for i in range(3):
            x = -1
            for j in range(3):
                self.drawData["B"][i][j] = Entity(model="quad", texture="white_cube", position=(x, y, -1.5))
                x += 1
            y -= 1

        y = 1
        for i in range(3):
            z = 1
            for j in range(3):
                self.drawData["O"][i][j] = Entity(model="quad", texture="white_cube", position=(-1.5, y, z),
                                                  rotation=(0, 90, 0))
                z -= 1
            y -= 1

        # draws black squares inside of the Rubik's cube, so when the cube sides are rotatins, you wouldn't be able to see inside of the cube. By default are invisible
        self.insideStat1 = Entity(model="quad", scale=3, color=color.black, position=(0, 0.5, 0), rotation=(90, 0, 0),
                                  visible=False)
        self.insideRot1 = Entity(model="quad", scale=3, color=color.black, position=(0, 0.5, 0), rotation=(-90, 0, 0),
                                 visible=False)

        self.insideStat2 = Entity(model="quad", scale=3, color=color.black, position=(0, -0.5, 0), rotation=(-90, 0, 0),
                                  visible=False)
        self.insideRot2 = Entity(model="quad", scale=3, color=color.black, position=(0, -0.5, 0), rotation=(90, 0, 0),
                                 visible=False)

        self.insideStat3 = Entity(model="quad", scale=3, color=color.black, position=(0, 0, -0.5), visible=False)
        self.insideRot3 = Entity(model="quad", scale=3, color=color.black, position=(0, 0, -0.5), rotation=(0, 180, 0),
                                 visible=False)

        self.insideStat4 = Entity(model="quad", scale=3, color=color.black, position=(0.5, 0, 0), rotation=(0, -90, 0),
                                  visible=False)
        self.insideRot4 = Entity(model="quad", scale=3, color=color.black, position=(0.5, 0, 0), rotation=(0, 90, 0),
                                 visible=False)

        self.insideStat5 = Entity(model="quad", scale=3, color=color.black, position=(0, 0, 0.5), rotation=(0, 180, 0),
                                  visible=False)
        self.insideRot5 = Entity(model="quad", scale=3, color=color.black, position=(0, 0, 0.5), visible=False)

        self.insideStat6 = Entity(model="quad", scale=3, color=color.black, position=(-0.5, 0, 0), rotation=(0, 90, 0),
                                  visible=False)
        self.insideRot6 = Entity(model="quad", scale=3, color=color.black, position=(-0.5, 0, 0), rotation=(0, -90, 0),
                                 visible=False)

        # assign colors specified in the cubeFaces dictionary to the drawn elements.
        self.updateColors()

        # meant for storing the solving position in the solveMoveList where each of the soliving steps were completed
        self.flowerSolvedPoistion = None
        self.whiteCrossSolvedPosition = None
        self.bottomSolvedPosition = None
        self.middleSolvedPosition = None
        self.yellowCrossSolvedPosition = None
        self.yellowSolvedPosition = None
        self.CornersSolvedPosition = None
        self.EdgesSolvedPosition = None
        self.cubeSolvedPosition = None

    def updateColors(self):
        """Updates the colors of the drawn elements according to the cubeFaces dictionary"""
        for face in self.cubeFaces:
            for i in range(3):
                for j in range(3):
                    if self.cubeFaces[face].colors[i][j][0] == "Y":
                        self.drawData[face][i][j].color = color.yellow
                    if self.cubeFaces[face].colors[i][j][0] == "W":
                        self.drawData[face][i][j].color = color.white
                    if self.cubeFaces[face].colors[i][j][0] == "G":
                        self.drawData[face][i][j].color = color.green
                    if self.cubeFaces[face].colors[i][j][0] == "R":
                        self.drawData[face][i][j].color = color.red
                    if self.cubeFaces[face].colors[i][j][0] == "B":
                        self.drawData[face][i][j].color = color.blue
                    if self.cubeFaces[face].colors[i][j][0] == "O":
                        self.drawData[face][i][j].color = color.orange

    def rotateDraw(self, face):
        """Assigns each of the specified faces drawn elements to the origin so theese elements could be rotated"""
        if face == 'Y':
            for i in range(3):
                for j in range(3):
                    self.drawData["Y"][i][j].parent = self.origin
            self.drawData["B"][0][0].parent = self.origin
            self.drawData["B"][0][1].parent = self.origin
            self.drawData["B"][0][2].parent = self.origin
            self.drawData["R"][0][0].parent = self.origin
            self.drawData["R"][0][1].parent = self.origin
            self.drawData["R"][0][2].parent = self.origin
            self.drawData["G"][0][0].parent = self.origin
            self.drawData["G"][0][1].parent = self.origin
            self.drawData["G"][0][2].parent = self.origin
            self.drawData["O"][0][0].parent = self.origin
            self.drawData["O"][0][1].parent = self.origin
            self.drawData["O"][0][2].parent = self.origin

            # makes the black inside elements which are going to be needed for the rotation visible
            self.insideStat1.visible = True
            self.insideRot1.visible = True
            self.insideRot1.parent = self.origin

        if face == 'W':
            for i in range(3):
                for j in range(3):
                    self.drawData["W"][i][j].parent = self.origin
            self.drawData["B"][2][0].parent = self.origin
            self.drawData["B"][2][1].parent = self.origin
            self.drawData["B"][2][2].parent = self.origin
            self.drawData["R"][2][0].parent = self.origin
            self.drawData["R"][2][1].parent = self.origin
            self.drawData["R"][2][2].parent = self.origin
            self.drawData["G"][2][0].parent = self.origin
            self.drawData["G"][2][1].parent = self.origin
            self.drawData["G"][2][2].parent = self.origin
            self.drawData["O"][2][0].parent = self.origin
            self.drawData["O"][2][1].parent = self.origin
            self.drawData["O"][2][2].parent = self.origin
            self.insideStat2.visible = True
            self.insideRot2.visible = True
            self.insideRot2.parent = self.origin

        if face == 'B':
            for i in range(3):
                for j in range(3):
                    self.drawData["B"][i][j].parent = self.origin
            self.drawData["Y"][2][0].parent = self.origin
            self.drawData["Y"][2][1].parent = self.origin
            self.drawData["Y"][2][2].parent = self.origin
            self.drawData["R"][0][0].parent = self.origin
            self.drawData["R"][1][0].parent = self.origin
            self.drawData["R"][2][0].parent = self.origin
            self.drawData["W"][0][0].parent = self.origin
            self.drawData["W"][0][1].parent = self.origin
            self.drawData["W"][0][2].parent = self.origin
            self.drawData["O"][0][2].parent = self.origin
            self.drawData["O"][1][2].parent = self.origin
            self.drawData["O"][2][2].parent = self.origin
            self.insideStat3.visible = True
            self.insideRot3.visible = True
            self.insideRot3.parent = self.origin

        if face == 'R':
            for i in range(3):
                for j in range(3):
                    self.drawData["R"][i][j].parent = self.origin
            self.drawData["Y"][0][2].parent = self.origin
            self.drawData["Y"][1][2].parent = self.origin
            self.drawData["Y"][2][2].parent = self.origin
            self.drawData["G"][0][0].parent = self.origin
            self.drawData["G"][1][0].parent = self.origin
            self.drawData["G"][2][0].parent = self.origin
            self.drawData["W"][0][2].parent = self.origin
            self.drawData["W"][1][2].parent = self.origin
            self.drawData["W"][2][2].parent = self.origin
            self.drawData["B"][0][2].parent = self.origin
            self.drawData["B"][1][2].parent = self.origin
            self.drawData["B"][2][2].parent = self.origin
            self.insideStat4.visible = True
            self.insideRot4.visible = True
            self.insideRot4.parent = self.origin

        if face == 'G':
            for i in range(3):
                for j in range(3):
                    self.drawData["G"][i][j].parent = self.origin
            self.drawData["Y"][0][0].parent = self.origin
            self.drawData["Y"][0][1].parent = self.origin
            self.drawData["Y"][0][2].parent = self.origin
            self.drawData["O"][0][0].parent = self.origin
            self.drawData["O"][1][0].parent = self.origin
            self.drawData["O"][2][0].parent = self.origin
            self.drawData["W"][2][0].parent = self.origin
            self.drawData["W"][2][1].parent = self.origin
            self.drawData["W"][2][2].parent = self.origin
            self.drawData["R"][0][2].parent = self.origin
            self.drawData["R"][1][2].parent = self.origin
            self.drawData["R"][2][2].parent = self.origin
            self.insideStat5.visible = True
            self.insideRot5.visible = True
            self.insideRot5.parent = self.origin

        if face == 'O':
            for i in range(3):
                for j in range(3):
                    self.drawData["O"][i][j].parent = self.origin
            self.drawData["Y"][0][0].parent = self.origin
            self.drawData["Y"][1][0].parent = self.origin
            self.drawData["Y"][2][0].parent = self.origin
            self.drawData["B"][0][0].parent = self.origin
            self.drawData["B"][1][0].parent = self.origin
            self.drawData["B"][2][0].parent = self.origin
            self.drawData["W"][0][0].parent = self.origin
            self.drawData["W"][1][0].parent = self.origin
            self.drawData["W"][2][0].parent = self.origin
            self.drawData["G"][0][2].parent = self.origin
            self.drawData["G"][1][2].parent = self.origin
            self.drawData["G"][2][2].parent = self.origin
            self.insideStat6.visible = True
            self.insideRot6.visible = True
            self.insideRot6.parent = self.origin

    def resetParents(self):
        """Resets the parent element of every drawn object to nothing, after some of them have been rotated"""
        for face in self.drawData:
            for row in self.drawData[face]:
                for quad in row:
                    quad.parent = scene

        self.insideStat1.parent = scene
        self.insideRot1.parent = scene
        self.insideStat2.parent = scene
        self.insideRot2.parent = scene
        self.insideStat3.parent = scene
        self.insideRot3.parent = scene
        self.insideStat4.parent = scene
        self.insideRot4.parent = scene
        self.insideStat5.parent = scene
        self.insideRot5.parent = scene
        self.insideStat6.parent = scene
        self.insideRot6.parent = scene

    def rotateForwardsData(self, face):
        """Rotates the specified face and also the associeated rows and columns in the near by faces"""
        if face == 'Y':
            self.cubeFaces['Y'].rotateFace()
            orangeArr = self.cubeFaces['O'].getTop().copy()
            greenArr = self.cubeFaces['G'].getTop().copy()
            redArr = self.cubeFaces['R'].getTop().copy()
            blueArr = self.cubeFaces['B'].getTop().copy()
            self.cubeFaces['G'].setTop(orangeArr)
            self.cubeFaces['R'].setTop(greenArr)
            self.cubeFaces['B'].setTop(redArr)
            self.cubeFaces['O'].setTop(blueArr)

        if face == 'W':
            self.cubeFaces['W'].rotateFace()
            orangeArr = self.cubeFaces['O'].getBottom().copy()
            greenArr = self.cubeFaces['G'].getBottom().copy()
            redArr = self.cubeFaces['R'].getBottom().copy()
            blueArr = self.cubeFaces['B'].getBottom().copy()
            self.cubeFaces['G'].setBottom(redArr)
            self.cubeFaces['R'].setBottom(blueArr)
            self.cubeFaces['B'].setBottom(orangeArr)
            self.cubeFaces['O'].setBottom(greenArr)

        if face == 'B':
            self.cubeFaces['B'].rotateFace()
            yellowArr = self.cubeFaces['Y'].getBottom().copy()
            redArr = self.cubeFaces['R'].getLeft().copy()
            whiteArr = self.cubeFaces['W'].getTop().copy()
            orangeArr = self.cubeFaces['O'].getRight().copy()
            self.cubeFaces['Y'].setBottom(orangeArr[::-1])
            self.cubeFaces['R'].setLeft(yellowArr)
            self.cubeFaces['W'].setTop(redArr[::-1])
            self.cubeFaces['O'].setRight(whiteArr)

        if face == 'R':
            self.cubeFaces['R'].rotateFace()
            yellowArr = self.cubeFaces['Y'].getRight().copy()
            blueArr = self.cubeFaces['B'].getRight().copy()
            whiteArr = self.cubeFaces['W'].getRight().copy()
            greenArr = self.cubeFaces['G'].getLeft().copy()
            self.cubeFaces['Y'].setRight(blueArr)
            self.cubeFaces['B'].setRight(whiteArr)
            self.cubeFaces['W'].setRight(greenArr[::-1])
            self.cubeFaces['G'].setLeft(yellowArr[::-1])

        if face == 'G':
            self.cubeFaces['G'].rotateFace()
            yellowArr = self.cubeFaces['Y'].getTop().copy()
            orangeArr = self.cubeFaces['O'].getLeft().copy()
            whiteArr = self.cubeFaces['W'].getBottom().copy()
            redArr = self.cubeFaces['R'].getRight().copy()
            self.cubeFaces['Y'].setTop(redArr)
            self.cubeFaces['O'].setLeft(yellowArr[::-1])
            self.cubeFaces['W'].setBottom(orangeArr)
            self.cubeFaces['R'].setRight(whiteArr[::-1])

        if face == 'O':
            self.cubeFaces['O'].rotateFace()
            yellowArr = self.cubeFaces['Y'].getLeft().copy()
            blueArr = self.cubeFaces['B'].getLeft().copy()
            whiteArr = self.cubeFaces['W'].getLeft().copy()
            greenArr = self.cubeFaces['G'].getRight().copy()
            self.cubeFaces['Y'].setLeft(greenArr[::-1])
            self.cubeFaces['B'].setLeft(yellowArr)
            self.cubeFaces['W'].setLeft(blueArr)
            self.cubeFaces['G'].setRight(whiteArr[::-1])

    def rotateBackwardsData(self, face):
        """Rotates the specified face and also the associeated rows and columns in the near by faces backwards"""
        if face == "Y":
            self.cubeFaces['Y'].rotateFaceBack()
            orangeArr = self.cubeFaces['O'].getTop().copy()
            greenArr = self.cubeFaces['G'].getTop().copy()
            redArr = self.cubeFaces['R'].getTop().copy()
            blueArr = self.cubeFaces['B'].getTop().copy()
            self.cubeFaces['G'].setTop(redArr)
            self.cubeFaces['R'].setTop(blueArr)
            self.cubeFaces['B'].setTop(orangeArr)
            self.cubeFaces['O'].setTop(greenArr)

        if face == "W":
            self.cubeFaces['W'].rotateFaceBack()
            orangeArr = self.cubeFaces['O'].getBottom().copy()
            greenArr = self.cubeFaces['G'].getBottom().copy()
            redArr = self.cubeFaces['R'].getBottom().copy()
            blueArr = self.cubeFaces['B'].getBottom().copy()
            self.cubeFaces['G'].setBottom(orangeArr)
            self.cubeFaces['R'].setBottom(greenArr)
            self.cubeFaces['B'].setBottom(redArr)
            self.cubeFaces['O'].setBottom(blueArr)

        if face == "B":
            self.cubeFaces['B'].rotateFaceBack()
            yellowArr = self.cubeFaces['Y'].getBottom().copy()
            redArr = self.cubeFaces['R'].getLeft().copy()
            whiteArr = self.cubeFaces['W'].getTop().copy()
            orangeArr = self.cubeFaces['O'].getRight().copy()
            self.cubeFaces['Y'].setBottom(redArr)
            self.cubeFaces['R'].setLeft(whiteArr[::-1])
            self.cubeFaces['W'].setTop(orangeArr)
            self.cubeFaces['O'].setRight(yellowArr[::-1])

        if face == "R":
            self.cubeFaces['R'].rotateFaceBack()
            yellowArr = self.cubeFaces['Y'].getRight().copy()
            blueArr = self.cubeFaces['B'].getRight().copy()
            whiteArr = self.cubeFaces['W'].getRight().copy()
            greenArr = self.cubeFaces['G'].getLeft().copy()
            self.cubeFaces['Y'].setRight(greenArr[::-1])
            self.cubeFaces['B'].setRight(yellowArr)
            self.cubeFaces['W'].setRight(blueArr)
            self.cubeFaces['G'].setLeft(whiteArr[::-1])

        if face == "G":
            self.cubeFaces['G'].rotateFaceBack()
            yellowArr = self.cubeFaces['Y'].getTop().copy()
            orangeArr = self.cubeFaces['O'].getLeft().copy()
            whiteArr = self.cubeFaces['W'].getBottom().copy()
            redArr = self.cubeFaces['R'].getRight().copy()
            self.cubeFaces['Y'].setTop(orangeArr[::-1])
            self.cubeFaces['O'].setLeft(whiteArr)
            self.cubeFaces['W'].setBottom(redArr[::-1])
            self.cubeFaces['R'].setRight(yellowArr)

        if face == "O":
            self.cubeFaces['O'].rotateFaceBack()
            yellowArr = self.cubeFaces['Y'].getLeft().copy()
            blueArr = self.cubeFaces['B'].getLeft().copy()
            whiteArr = self.cubeFaces['W'].getLeft().copy()
            greenArr = self.cubeFaces['G'].getRight().copy()
            self.cubeFaces['Y'].setLeft(blueArr)
            self.cubeFaces['B'].setLeft(whiteArr)
            self.cubeFaces['W'].setLeft(greenArr[::-1])
            self.cubeFaces['G'].setRight(yellowArr[::-1])

    def randomCube(self):
        """Rotaes the cube faces randomly 20 times"""
        randomMoves = [random.randint(1, 12) for i in range(20)]

        for move in randomMoves:
            if move == 1:
                self.rotateForwardsData('Y')
            if move == 2:
                self.rotateBackwardsData('Y')
            if move == 3:
                self.rotateForwardsData('W')
            if move == 4:
                self.rotateBackwardsData('W')
            if move == 5:
                self.rotateForwardsData('B')
            if move == 6:
                self.rotateBackwardsData('B')
            if move == 7:
                self.rotateForwardsData('R')
            if move == 8:
                self.rotateBackwardsData('R')
            if move == 9:
                self.rotateForwardsData('G')
            if move == 10:
                self.rotateBackwardsData('G')
            if move == 11:
                self.rotateForwardsData('O')
            if move == 12:
                self.rotateBackwardsData('O')

    def solivingMove(self, move):
        """When given a tuple where the first element is a cube face and the second is a direction (F - forwards, B- backwards), rotates the cube face in the specified direction"""
        if move == ('Y', 'F'):
            self.rotateForwards['Y'] = True
            self.rotateDraw('Y')
        if move == ('Y', 'B'):
            self.rotateBackwards['Y'] = True
            self.rotateDraw('Y')
        if move == ('W', 'F'):
            self.rotateForwards['W'] = True
            self.rotateDraw('W')
        if move == ('W', 'B'):
            self.rotateBackwards['W'] = True
            self.rotateDraw('W')
        if move == ('B', 'F'):
            self.rotateForwards['B'] = True
            self.rotateDraw('B')
        if move == ('B', 'B'):
            self.rotateBackwards['B'] = True
            self.rotateDraw('B')
        if move == ('R', 'F'):
            self.rotateForwards['R'] = True
            self.rotateDraw('R')
        if move == ('R', 'B'):
            self.rotateBackwards['R'] = True
            self.rotateDraw('R')
        if move == ('G', 'F'):
            self.rotateForwards['G'] = True
            self.rotateDraw('G')
        if move == ('G', 'B'):
            self.rotateBackwards['G'] = True
            self.rotateDraw('G')
        if move == ('O', 'F'):
            self.rotateForwards['O'] = True
            self.rotateDraw('O')
        if move == ('O', 'B'):
            self.rotateBackwards['O'] = True
            self.rotateDraw('O')

    def solve(self):
        """Solves the Rubik's cube by going through 8 smaller algorithms"""

        self.cubeSolved = False

        # Reset the variables that store the position where each of the soliving steps were completed
        self.flowerSolvedPoistion = None
        self.whiteCrossSolvedPosition = None
        self.bottomSolvedPosition = None
        self.middleSolvedPosition = None
        self.yellowCrossSolvedPosition = None
        self.yellowSolvedPosition = None
        self.CornersSolvedPosition = None
        self.EdgesSolvedPosition = None
        self.cubeSolvedPosition = None

        cubeFacesCopy = copy.deepcopy(self.cubeFaces)

        # reset the solivng move lists and the position
        self.solveMoveList = []
        self.solveMoveListBack = []
        self.solvingPosition = 0

        # check if the cube is already solved
        if self.isCubeSolved():
            self.cubeSolved = True
            return

        # go throught each of the solving steps and record the position where each of the steps were completed
        self.solveFlower()
        self.flowerSolvedPoistion = len(self.solveMoveList)

        self.solveWhiteCross()
        self.whiteCrossSolvedPosition = len(self.solveMoveList)

        self.solveBottom()
        self.bottomSolvedPosition = len(self.solveMoveList)

        self.solveMiddle()
        self.middleSolvedPosition = len(self.solveMoveList)

        self.solveYellowCross()
        self.yellowCrossSolvedPosition = len(self.solveMoveList)

        self.solveYellow()
        self.yellowSolvedPosition = len(self.solveMoveList)

        self.solveCorners()
        self.CornersSolvedPosition = len(self.solveMoveList)

        self.solveEdges()
        self.EdgesSolvedPosition = len(self.solveMoveList)

        while self.cubeFaces['B'].colors[0][0] != 'B':
            self.rotateForwardsData('Y')
            self.solveMoveList.append(('Y', 'F'))
        self.cubeSolved = True
        self.cubeSolvedPosition = len(self.solveMoveList)

        self.cubeFaces = cubeFacesCopy

        # populate the solveMoveListBack list with the reverse move for each of the moves in the solveMoveList
        for i in self.solveMoveList:
            if i[1] == 'F':
                self.solveMoveListBack.append((i[0], 'B'))
            else:
                self.solveMoveListBack.append((i[0], 'F'))

    def findWhiteEdges(self):
        """Helper function for the solveFlower() function that finds all of the white edge pieces and their positions in the side faces (not white and yellow)"""
        sideFaces = ["B", "R", "G", "O"]
        edges = {"top": [], "bottom": [], "left": [], "right": []}
        for i in sideFaces:
            if self.cubeFaces[i].colors[0][1] == 'W':
                edges["top"].append(i)
            if self.cubeFaces[i].colors[2][1] == 'W':
                edges["bottom"].append(i)
            if self.cubeFaces[i].colors[1][0] == 'W':
                edges["left"].append(i)
            if self.cubeFaces[i].colors[1][2] == 'W':
                edges["right"].append(i)
        return edges

    def solveFlower(self):
        """implements the algorithm that achieves the flower like formation on the yellow face of the rubiks cube"""
        edges = self.findWhiteEdges()

        # rotates the sides of the cube until all of the 4 white edges are in their correct positions
        while self.cubeFaces['Y'].colors[0][1] != "W" or self.cubeFaces['Y'].colors[1][0] != "W" or \
                self.cubeFaces['Y'].colors[1][2] != "W" or self.cubeFaces['Y'].colors[2][1] != "W":

            # when a white edge is found the left side of any of the side faces
            while len(edges["left"]) != 0:
                if edges["left"][0] == "B":
                    while self.cubeFaces['Y'].colors[1][0] == "W":
                        self.rotateForwardsData('Y')
                        self.solveMoveList.append(('Y', 'F'))
                    self.rotateBackwardsData('O')
                    self.solveMoveList.append(('O', 'B'))
                    edges = self.findWhiteEdges()

                elif edges["left"][0] == "R":
                    while self.cubeFaces['Y'].colors[2][1] == "W":
                        self.rotateForwardsData('Y')
                        self.solveMoveList.append(('Y', 'F'))
                    self.rotateBackwardsData('B')
                    self.solveMoveList.append(('B', 'B'))
                    edges = self.findWhiteEdges()

                elif edges["left"][0] == "G":
                    while self.cubeFaces['Y'].colors[1][2] == "W":
                        self.rotateForwardsData('Y')
                        self.solveMoveList.append(('Y', 'F'))
                    self.rotateBackwardsData('R')
                    self.solveMoveList.append(('R', 'B'))
                    edges = self.findWhiteEdges()

                elif edges["left"][0] == "O":
                    while self.cubeFaces['Y'].colors[0][1] == "W":
                        self.rotateForwardsData('Y')
                        self.solveMoveList.append(('Y', 'F'))
                    self.rotateBackwardsData('G')
                    self.solveMoveList.append(('G', 'B'))
                    edges = self.findWhiteEdges()

            # when a white edge is found the right side of any of the side faces
            while len(edges["right"]) != 0:
                if edges["right"][0] == "B":
                    while self.cubeFaces['Y'].colors[1][2] == "W":
                        self.rotateForwardsData('Y')
                        self.solveMoveList.append(('Y', 'F'))
                    self.rotateForwardsData('R')
                    self.solveMoveList.append(('R', 'F'))
                    edges = self.findWhiteEdges()

                elif edges["right"][0] == "R":
                    while self.cubeFaces['Y'].colors[0][1] == "W":
                        self.rotateForwardsData('Y')
                        self.solveMoveList.append(('Y', 'F'))
                    self.rotateForwardsData('G')
                    self.solveMoveList.append(('G', 'F'))
                    edges = self.findWhiteEdges()

                elif edges["right"][0] == "G":
                    while self.cubeFaces['Y'].colors[1][0] == "W":
                        self.rotateForwardsData('Y')
                        self.solveMoveList.append(('Y', 'F'))
                    self.rotateForwardsData('O')
                    self.solveMoveList.append(('O', 'F'))
                    edges = self.findWhiteEdges()

                elif edges["right"][0] == "O":
                    while self.cubeFaces['Y'].colors[2][1] == "W":
                        self.rotateForwardsData('Y')
                        self.solveMoveList.append(('Y', 'F'))
                    self.rotateForwardsData('B')
                    self.solveMoveList.append(('B', 'F'))
                    edges = self.findWhiteEdges()

            # when a white edge is found the top side of any of the side faces
            while len(edges["top"]) != 0:
                if edges["top"][0] == "B":
                    self.rotateForwardsData('B')
                    self.solveMoveList.append(('B', 'F'))
                    edges = self.findWhiteEdges()

                elif edges["top"][0] == "R":
                    self.rotateForwardsData('R')
                    self.solveMoveList.append(('R', 'F'))
                    edges = self.findWhiteEdges()

                elif edges["top"][0] == "G":
                    self.rotateForwardsData('G')
                    self.solveMoveList.append(('G', 'F'))
                    edges = self.findWhiteEdges()

                elif edges["top"][0] == "O":
                    self.rotateForwardsData('O')
                    self.solveMoveList.append(('O', 'F'))
                    edges = self.findWhiteEdges()

            # when a white edge is found the bottom side of any of the non yellow faces
            while len(edges["bottom"]) != 0:
                if edges["bottom"][0] == "B":
                    if self.cubeFaces['Y'].colors[2][1] == "W":
                        self.rotateForwardsData('Y')
                        self.solveMoveList.append(('Y', 'F'))
                    else:
                        self.rotateForwardsData('B')
                        self.solveMoveList.append(('B', 'F'))
                    edges = self.findWhiteEdges()

                elif edges["bottom"][0] == "R":
                    if self.cubeFaces['Y'].colors[1][2] == "W":
                        self.rotateForwardsData('Y')
                        self.solveMoveList.append(('Y', 'F'))
                    else:
                        self.rotateForwardsData('R')
                        self.solveMoveList.append(('R', 'F'))
                    edges = self.findWhiteEdges()

                elif edges["bottom"][0] == "G":
                    if self.cubeFaces['Y'].colors[0][1] == "W":
                        self.rotateForwardsData('Y')
                        self.solveMoveList.append(('Y', 'F'))
                    else:
                        self.rotateForwardsData('G')
                        self.solveMoveList.append(('G', 'F'))
                    edges = self.findWhiteEdges()

                elif edges["bottom"][0] == "O":
                    if self.cubeFaces['Y'].colors[1][0] == "W":
                        self.rotateForwardsData('Y')
                        self.solveMoveList.append(('Y', 'F'))
                    else:
                        self.rotateForwardsData('O')
                        self.solveMoveList.append(('O', 'F'))
                    edges = self.findWhiteEdges()

            # when a white edge is found on the white face in any position
            if self.cubeFaces['W'].colors[0][1] == "W":
                while self.cubeFaces['Y'].colors[2][1] == "W":
                    self.rotateForwardsData('Y')
                    self.solveMoveList.append(('Y', 'F'))
                self.rotateForwardsData('B')
                self.solveMoveList.append(('B', 'F'))
                self.rotateForwardsData('B')
                self.solveMoveList.append(('B', 'F'))

            if self.cubeFaces['W'].colors[1][0] == "W":
                while self.cubeFaces['Y'].colors[1][0] == "W":
                    self.rotateForwardsData('Y')
                    self.solveMoveList.append(('Y', 'F'))
                self.rotateForwardsData('O')
                self.solveMoveList.append(('O', 'F'))
                self.rotateForwardsData('O')
                self.solveMoveList.append(('O', 'F'))

            if self.cubeFaces['W'].colors[1][2] == "W":
                while self.cubeFaces['Y'].colors[1][2] == "W":
                    self.rotateForwardsData('Y')
                    self.solveMoveList.append(('Y', 'F'))
                self.rotateForwardsData('R')
                self.solveMoveList.append(('R', 'F'))
                self.rotateForwardsData('R')
                self.solveMoveList.append(('R', 'F'))

            if self.cubeFaces['W'].colors[2][1] == "W":
                while self.cubeFaces['Y'].colors[0][1] == "W":
                    self.rotateForwardsData('Y')
                    self.solveMoveList.append(('Y', 'F'))
                self.rotateForwardsData('G')
                self.solveMoveList.append(('G', 'F'))
                self.rotateForwardsData('G')
                self.solveMoveList.append(('G', 'F'))
            edges = self.findWhiteEdges()

    def topEdgeColor(self, face):
        """Helper function for the solveWhiteCross() and solveMiddle() functions, that checks the color of the other side of an edge piece of any specified face"""
        if face == "B":
            return self.cubeFaces["Y"].colors[2][1]
        if face == "R":
            return self.cubeFaces["Y"].colors[1][2]
        if face == "G":
            return self.cubeFaces["Y"].colors[0][1]
        if face == "O":
            return self.cubeFaces["Y"].colors[1][0]

    def solveWhiteCross(self):
        """implements the algorithm that achieves the cross like formation on the white face of the rubiks cube"""

        sideFaces = ["B", "R", "G", "O"]

        # going throught each of the side faces, rotates the yellow face until the other color of the white edge piece is the same as the center color of the side face
        for i in sideFaces:
            while self.cubeFaces[i].colors[0][1] != self.cubeFaces[i].colors[1][1] or self.topEdgeColor(i) != "W":
                self.rotateForwardsData('Y')
                self.solveMoveList.append(('Y', 'F'))
            if i == "B":
                self.rotateForwardsData('B')
                self.solveMoveList.append(('B', 'F'))
                self.rotateForwardsData('B')
                self.solveMoveList.append(('B', 'F'))
            if i == "R":
                self.rotateForwardsData('R')
                self.solveMoveList.append(('R', 'F'))
                self.rotateForwardsData('R')
                self.solveMoveList.append(('R', 'F'))
            if i == "G":
                self.rotateForwardsData('G')
                self.solveMoveList.append(('G', 'F'))
                self.rotateForwardsData('G')
                self.solveMoveList.append(('G', 'F'))
            if i == "O":
                self.rotateForwardsData('O')
                self.solveMoveList.append(('O', 'F'))
                self.rotateForwardsData('O')
                self.solveMoveList.append(('O', 'F'))

    def findWhiteCorners(self):
        """A helper function for the solveBottom() function that finds all of the white corner pieces and their positions in the side faces"""
        sideFaces = ["B", "R", "G", "O"]
        corners = {"topLeft": [], "topRight": [], "bottomLeft": [], "bottomRight": []}

        for i in sideFaces:
            if self.cubeFaces[i].colors[0][0] == 'W':
                corners["topLeft"].append(i)
            if self.cubeFaces[i].colors[0][2] == 'W':
                corners["topRight"].append(i)
            if self.cubeFaces[i].colors[2][0] == 'W':
                corners["bottomLeft"].append(i)
            if self.cubeFaces[i].colors[2][2] == 'W':
                corners["bottomRight"].append(i)
        return corners

    def cornerInPlace(self, face, position):
        """A helper function for the solveBottom() function that check a corner piece is of the correct color in the specified face and position"""
        if face == "B":
            if position == "right":
                return self.cubeFaces["R"].colors[0][0] == self.cubeFaces["R"].colors[1][1]
            if position == "left":
                return self.cubeFaces["O"].colors[0][2] == self.cubeFaces["O"].colors[1][1]
        if face == "R":
            if position == "right":
                return self.cubeFaces["G"].colors[0][0] == self.cubeFaces["G"].colors[1][1]
            if position == "left":
                return self.cubeFaces["B"].colors[0][2] == self.cubeFaces["B"].colors[1][1]
        if face == "G":
            if position == "right":
                return self.cubeFaces["O"].colors[0][0] == self.cubeFaces["O"].colors[1][1]
            if position == "left":
                return self.cubeFaces["R"].colors[0][2] == self.cubeFaces["R"].colors[1][1]
        if face == "O":
            if position == "right":
                return self.cubeFaces["B"].colors[0][0] == self.cubeFaces["B"].colors[1][1]
            if position == "left":
                return self.cubeFaces["G"].colors[0][2] == self.cubeFaces["G"].colors[1][1]

    def solveBottom(self):
        """implements the algorithm that solves the bottom layer and the white face of the rubiks cube"""
        # a dictionary of the known white corners and their positions
        corners = self.findWhiteCorners()
        sideFaces = ['B', 'R', 'G', 'O']
        while self.cubeFaces['B'].colors[2][0] != "B" or self.cubeFaces['B'].colors[2][2] != "B" or \
                self.cubeFaces['R'].colors[2][0] != "R" or self.cubeFaces['R'].colors[2][2] != "R" or \
                self.cubeFaces['G'].colors[2][0] != "G" or self.cubeFaces['G'].colors[2][2] != "G" or \
                self.cubeFaces['O'].colors[2][0] != "O" or self.cubeFaces['O'].colors[2][2] != "O":
            # if there is a corner in the top left position in a side face
            if len(corners["topLeft"]) != 0:
                i = corners["topLeft"][0]
                while self.cornerInPlace(i, "left") == False:
                    self.rotateForwardsData('Y')
                    self.solveMoveList.append(('Y', 'F'))
                    i = sideFaces[sideFaces.index(i) - 1]
                self.rotateForwardsData(i)
                self.solveMoveList.append((i, 'F'))
                self.rotateForwardsData('Y')
                self.solveMoveList.append(('Y', 'F'))
                self.rotateBackwardsData(i)
                self.solveMoveList.append((i, 'B'))

            # if there is a corner in the top right position in a side face
            elif len(corners["topRight"]) != 0:
                i = corners["topRight"][0]
                while self.cornerInPlace(i, "right") == False:
                    self.rotateBackwardsData('Y')
                    self.solveMoveList.append(('Y', 'B'))
                    i = sideFaces[(sideFaces.index(i) + 1) % 4]
                self.rotateBackwardsData(i)
                self.solveMoveList.append((i, 'B'))
                self.rotateBackwardsData('Y')
                self.solveMoveList.append(('Y', 'B'))
                self.rotateForwardsData(i)
                self.solveMoveList.append((i, 'F'))

            # if there is a corner in the bottom left position in a side face
            elif len(corners["bottomLeft"]) != 0:
                i = corners["bottomLeft"][0]
                self.rotateForwardsData(i)
                self.solveMoveList.append((i, 'F'))
                self.rotateForwardsData('Y')
                self.solveMoveList.append(('Y', 'F'))
                self.rotateBackwardsData(i)
                self.solveMoveList.append((i, 'B'))

            # if there is a corner in the bottom right position in a side face
            elif len(corners["bottomRight"]) != 0:
                i = corners["bottomRight"][0]
                self.rotateBackwardsData(i)
                self.solveMoveList.append((i, 'B'))
                self.rotateBackwardsData('Y')
                self.solveMoveList.append(('Y', 'B'))
                self.rotateForwardsData(i)
                self.solveMoveList.append((i, 'F'))

            # there is a white corner in any position on the yellow face
            elif self.cubeFaces["Y"].colors[0][0] == "W" and self.cubeFaces["W"].colors[2][0] != "W":
                self.rotateForwardsData('O')
                self.solveMoveList.append(('O', 'F'))
                self.rotateBackwardsData('Y')
                self.solveMoveList.append(('Y', 'B'))
                self.rotateBackwardsData('O')
                self.solveMoveList.append(('O', 'B'))

            elif self.cubeFaces["Y"].colors[0][2] == "W" and self.cubeFaces["W"].colors[2][2] != "W":
                self.rotateForwardsData('G')
                self.solveMoveList.append(('G', 'F'))
                self.rotateBackwardsData('Y')
                self.solveMoveList.append(('Y', 'B'))
                self.rotateBackwardsData('G')
                self.solveMoveList.append(('G', 'B'))

            elif self.cubeFaces["Y"].colors[2][0] == "W" and self.cubeFaces["W"].colors[0][0] != "W":
                self.rotateForwardsData('B')
                self.solveMoveList.append(('B', 'F'))
                self.rotateBackwardsData('Y')
                self.solveMoveList.append(('Y', 'B'))
                self.rotateBackwardsData('B')
                self.solveMoveList.append(('B', 'B'))

            elif self.cubeFaces["Y"].colors[2][2] == "W" and self.cubeFaces["W"].colors[0][2] != "W":
                self.rotateForwardsData('R')
                self.solveMoveList.append(('R', 'F'))
                self.rotateBackwardsData('Y')
                self.solveMoveList.append(('Y', 'B'))
                self.rotateBackwardsData('R')
                self.solveMoveList.append(('R', 'B'))

            # if the white face is solved but some of the edges are still not in the right positions
            elif self.cubeFaces['W'].colors[0][0] == "W" and self.cubeFaces['W'].colors[0][2] == "W" and \
                    self.cubeFaces['W'].colors[2][0] == "W" and self.cubeFaces['W'].colors[2][2] == "W":
                for i in sideFaces:
                    if self.cubeFaces[i].colors[2][0] != i:
                        left = sideFaces[sideFaces.index(i) - 1]
                        self.rotateBackwardsData(left)
                        self.solveMoveList.append((left, 'B'))
                        self.rotateBackwardsData('Y')
                        self.solveMoveList.append(('Y', 'B'))
                        self.rotateForwardsData(left)
                        self.solveMoveList.append((left, 'F'))
                        break


                    elif self.cubeFaces[i].colors[2][2] != i:
                        right = sideFaces[(sideFaces.index(i) + 1) % 4]
                        self.rotateForwardsData(right)
                        self.solveMoveList.append((right, 'F'))
                        self.rotateForwardsData('Y')
                        self.solveMoveList.append(('Y', 'F'))
                        self.rotateBackwardsData(right)
                        self.solveMoveList.append((right, 'B'))
                        break
            else:
                self.rotateForwardsData('Y')
                self.solveMoveList.append(('Y', 'F'))

            # update the corner positions
            corners = self.findWhiteCorners()

    def findColoredEdges(self):
        """A helper function for the SolveMidlle() function that returns a list of the faces that have an edge with no yellow in it"""
        faces = []
        if self.cubeFaces['B'].colors[0][1] != 'Y' and self.cubeFaces['Y'].colors[2][1] != 'Y':
            faces.append(self.cubeFaces['B'].colors[0][1])

        if self.cubeFaces['R'].colors[0][1] != 'Y' and self.cubeFaces['Y'].colors[1][2] != 'Y':
            faces.append(self.cubeFaces['R'].colors[0][1])

        if self.cubeFaces['G'].colors[0][1] != 'Y' and self.cubeFaces['Y'].colors[0][1] != 'Y':
            faces.append(self.cubeFaces['G'].colors[0][1])

        if self.cubeFaces['O'].colors[0][1] != 'Y' and self.cubeFaces['Y'].colors[1][0] != 'Y':
            faces.append(self.cubeFaces['O'].colors[0][1])

        return faces

    def solveMiddle(self):
        """implements the algorithm that solves the middle layer of the rubiks cube"""

        sideFaces = ['B', 'R', 'G', 'O']
        # finds the faces with the non yellow edges
        faces = self.findColoredEdges()

        # while all of the edges in the middle layer are not in their correct positions
        while self.cubeFaces['B'].colors[1][0] != "B" or self.cubeFaces['B'].colors[1][2] != "B" or \
                self.cubeFaces['R'].colors[1][0] != "R" or self.cubeFaces['R'].colors[1][2] != "R" or \
                self.cubeFaces['G'].colors[1][0] != "G" or self.cubeFaces['G'].colors[1][2] != "G" or \
                self.cubeFaces['O'].colors[1][0] != "O" or self.cubeFaces['O'].colors[1][2] != "O":

            if len(faces) != 0:
                # rotate the to until the edge is in the correct face
                i = faces[0]
                edgeTop = self.topEdgeColor(i)
                while self.cubeFaces[i].colors[0][1] != i or edgeTop == 'Y':
                    self.rotateForwardsData('Y')
                    self.solveMoveList.append(('Y', 'F'))
                    edgeTop = self.topEdgeColor(i)

                left = sideFaces[sideFaces.index(i) - 1]
                right = sideFaces[(sideFaces.index(i) + 1) % 4]

                # if the other color of the edge is equal to the face that is to the left of the current face
                if edgeTop == left:
                    self.rotateBackwardsData('Y')
                    self.solveMoveList.append(('Y', 'B'))
                    self.rotateBackwardsData(left)
                    self.solveMoveList.append((left, 'B'))
                    self.rotateBackwardsData('Y')
                    self.solveMoveList.append(('Y', 'B'))
                    self.rotateForwardsData(left)
                    self.solveMoveList.append((left, 'F'))
                    self.rotateForwardsData('Y')
                    self.solveMoveList.append(('Y', 'F'))
                    self.rotateForwardsData(i)
                    self.solveMoveList.append((i, 'F'))
                    self.rotateForwardsData('Y')
                    self.solveMoveList.append(('Y', 'F'))
                    self.rotateBackwardsData(i)
                    self.solveMoveList.append((i, 'B'))
                else:
                    # if the other color of the edge is equal to the face that is to the right of the current face
                    self.rotateForwardsData('Y')
                    self.solveMoveList.append(('Y', 'F'))
                    self.rotateForwardsData(right)
                    self.solveMoveList.append((right, 'F'))
                    self.rotateForwardsData('Y')
                    self.solveMoveList.append(('Y', 'F'))
                    self.rotateBackwardsData(right)
                    self.solveMoveList.append((right, 'B'))
                    self.rotateBackwardsData('Y')
                    self.solveMoveList.append(('Y', 'B'))
                    self.rotateBackwardsData(i)
                    self.solveMoveList.append((i, 'B'))
                    self.rotateBackwardsData('Y')
                    self.solveMoveList.append(('Y', 'B'))
                    self.rotateForwardsData(i)
                    self.solveMoveList.append((i, 'F'))

                faces = self.findColoredEdges()
            else:
                # if some of the edges end up in the incorret postions in the left of the right
                for i in sideFaces:
                    if self.cubeFaces[i].colors[1][0] != i:
                        left = sideFaces[sideFaces.index(i) - 1]
                        self.rotateBackwardsData(left)
                        self.solveMoveList.append((left, 'B'))
                        self.rotateBackwardsData('Y')
                        self.solveMoveList.append(('Y', 'B'))
                        self.rotateForwardsData(left)
                        self.solveMoveList.append((left, 'F'))
                        self.rotateForwardsData('Y')
                        self.solveMoveList.append(('Y', 'F'))
                        self.rotateForwardsData(i)
                        self.solveMoveList.append((i, 'F'))
                        self.rotateForwardsData('Y')
                        self.solveMoveList.append(('Y', 'F'))
                        self.rotateBackwardsData(i)
                        self.solveMoveList.append((i, 'B'))
                        faces = self.findColoredEdges()
                        break

                    elif self.cubeFaces[i].colors[1][2] != i:
                        right = sideFaces[(sideFaces.index(i) + 1) % 4]
                        self.rotateForwardsData(right)
                        self.solveMoveList.append((right, 'F'))
                        self.rotateForwardsData('Y')
                        self.solveMoveList.append(('Y', 'F'))
                        self.rotateBackwardsData(right)
                        self.solveMoveList.append((right, 'B'))
                        self.rotateBackwardsData('Y')
                        self.solveMoveList.append(('Y', 'B'))
                        self.rotateBackwardsData(i)
                        self.solveMoveList.append((i, 'B'))
                        self.rotateBackwardsData('Y')
                        self.solveMoveList.append(('Y', 'B'))
                        self.rotateForwardsData(i)
                        self.solveMoveList.append((i, 'F'))
                        faces = self.findColoredEdges()
                        break

    def yellowCrossMoves(self):
        """A helper function for the solveYellowCross() function that does the main moves the algorithm"""
        self.rotateForwardsData('B')
        self.solveMoveList.append(('B', 'F'))
        self.rotateForwardsData('Y')
        self.solveMoveList.append(('Y', 'F'))
        self.rotateForwardsData('R')
        self.solveMoveList.append(('R', 'F'))
        self.rotateBackwardsData('Y')
        self.solveMoveList.append(('Y', 'B'))
        self.rotateBackwardsData('R')
        self.solveMoveList.append(('R', 'B'))
        self.rotateBackwardsData('B')
        self.solveMoveList.append(('B', 'B'))

    def countYellowEdges(self):
        """A helper function for the solveYellowCross() function that counts the number of yellow edges on the yellow side"""
        yellowCount = 0
        if self.cubeFaces['Y'].colors[0][1] == "Y":
            yellowCount += 1
        if self.cubeFaces['Y'].colors[1][0] == "Y":
            yellowCount += 1
        if self.cubeFaces['Y'].colors[1][2] == "Y":
            yellowCount += 1
        if self.cubeFaces['Y'].colors[2][1] == "Y":
            yellowCount += 1
        return yellowCount

    def solveYellowCross(self):
        """implements the algorithm that creates the yellow cross on the yellow face of the cube"""
        yellowCount = self.countYellowEdges()
        # while all of the yellow edges are not in their correct positions on the yellow face
        while yellowCount != 4:

            if yellowCount == 0:
                self.yellowCrossMoves()
                yellowCount = self.countYellowEdges()

            # if the yellow edges are in a line formation
            if yellowCount == 2 or yellowCount == 3:
                # if edges are in a vertical line
                if self.cubeFaces['Y'].colors[0][1] == "Y" and self.cubeFaces['Y'].colors[2][1] == "Y":
                    self.yellowCrossMoves()
                # if edges are in a horizontal line
                elif self.cubeFaces['Y'].colors[1][0] == "Y" and self.cubeFaces['Y'].colors[1][2] == "Y":
                    self.rotateForwardsData('Y')
                    self.solveMoveList.append(('Y', 'F'))
                    self.yellowCrossMoves()
                else:
                    # if edges are in a hooh formation rotate until in the correct position
                    while self.cubeFaces['Y'].colors[0][1] != "Y" or self.cubeFaces['Y'].colors[1][0] != "Y":
                        self.rotateForwardsData('Y')
                        self.solveMoveList.append(('Y', 'F'))
                    self.yellowCrossMoves()
            yellowCount = self.countYellowEdges()  # update the edge count

    def solveYellowMoves(self):
        """A helper function for the solveYellow() function that does the main moves of the algorithm"""
        self.rotateForwardsData('R')
        self.solveMoveList.append(('R', 'F'))
        self.rotateForwardsData('Y')
        self.solveMoveList.append(('Y', 'F'))
        self.rotateBackwardsData('R')
        self.solveMoveList.append(('R', 'B'))
        self.rotateForwardsData('Y')
        self.solveMoveList.append(('Y', 'F'))
        self.rotateForwardsData('R')
        self.solveMoveList.append(('R', 'F'))
        self.rotateForwardsData('Y')
        self.solveMoveList.append(('Y', 'F'))
        self.rotateForwardsData('Y')
        self.solveMoveList.append(('Y', 'F'))
        self.rotateBackwardsData('R')
        self.solveMoveList.append(('R', 'B'))

    def countYellowCorners(self):
        """A helper function for the solveYellow() function that counts the number of yellow corners on the yellow face"""
        yellowCount = 0
        if self.cubeFaces['Y'].colors[0][0] == "Y":
            yellowCount += 1
        if self.cubeFaces['Y'].colors[0][2] == "Y":
            yellowCount += 1
        if self.cubeFaces['Y'].colors[2][0] == "Y":
            yellowCount += 1
        if self.cubeFaces['Y'].colors[2][2] == "Y":
            yellowCount += 1
        return yellowCount

    def solveYellow(self):
        """A function that implements the algorithm for solving the yellow face"""

        yellowCount = self.countYellowCorners()
        # until all of the yellow corner are in the correct positions on the yellow face
        while yellowCount != 4:
            if yellowCount == 1:
                # if the yellow corners are in a fish formation
                while self.cubeFaces['Y'].colors[2][0] != "Y":
                    self.rotateBackwardsData('Y')
                    self.solveMoveList.append(('Y', 'B'))
                self.solveYellowMoves()
            else:
                # rotate the yellow face until there is a yellow corner on the orange face
                while self.cubeFaces['O'].colors[0][2] != "Y":
                    self.rotateForwardsData('Y')
                    self.solveMoveList.append(('Y', 'F'))
                self.solveYellowMoves()
            yellowCount = self.countYellowCorners()  # update the yellow corner count

    def solveCornersMoves(self):
        """A helper function for the solveCorners() function that does the main moves of the algorithm"""
        self.rotateBackwardsData('O')
        self.solveMoveList.append(('O', 'B'))
        self.rotateForwardsData('Y')
        self.solveMoveList.append(('Y', 'F'))
        self.rotateForwardsData('R')
        self.solveMoveList.append(('R', 'F'))
        self.rotateBackwardsData('Y')
        self.solveMoveList.append(('Y', 'B'))
        self.rotateForwardsData('O')
        self.solveMoveList.append(('O', 'F'))
        self.rotateForwardsData('Y')
        self.solveMoveList.append(('Y', 'F'))
        self.rotateBackwardsData('R')
        self.solveMoveList.append(('R', 'B'))
        self.solveYellowMoves()

    def solveCorners(self):
        """A function that implements the algorithm for solving the corners of the top layer"""
        sideFaces = ['B', 'R', 'G', 'O']
        # while all of the corners are not in the correct positions
        while self.cubeFaces['B'].colors[0][0] != self.cubeFaces['B'].colors[0][2] or self.cubeFaces['R'].colors[0][
            0] != self.cubeFaces['R'].colors[0][2] or self.cubeFaces['G'].colors[0][0] != self.cubeFaces['G'].colors[0][
            2] or self.cubeFaces['O'].colors[0][0] != self.cubeFaces['O'].colors[0][2]:
            for i in sideFaces:
                # if two of the corners of a face are the same color
                if self.cubeFaces[i].colors[0][0] == self.cubeFaces[i].colors[0][2]:
                    color = self.cubeFaces[i].colors[0][0]
                    # rotate the yellow face until the same color corneres are on the orange face
                    while self.cubeFaces['O'].colors[0][0] != color or self.cubeFaces['O'].colors[0][2] != color:
                        self.rotateForwardsData('Y')
                        self.solveMoveList.append(('Y', 'F'))
            self.solveCornersMoves()

    def solveEdgesMoves(self):
        """A helper function for the solveEdges() function that does the main moves of the algorithm"""
        self.rotateForwardsData('B')
        self.solveMoveList.append(('B', 'F'))
        self.rotateForwardsData('B')
        self.solveMoveList.append(('B', 'F'))
        self.rotateForwardsData('Y')
        self.solveMoveList.append(('Y', 'F'))
        self.rotateBackwardsData('R')
        self.solveMoveList.append(('R', 'B'))
        self.rotateForwardsData('O')
        self.solveMoveList.append(('O', 'F'))
        self.rotateForwardsData('B')
        self.solveMoveList.append(('B', 'F'))
        self.rotateForwardsData('B')
        self.solveMoveList.append(('B', 'F'))
        self.rotateBackwardsData('O')
        self.solveMoveList.append(('O', 'B'))
        self.rotateForwardsData('R')
        self.solveMoveList.append(('R', 'F'))
        self.rotateForwardsData('Y')
        self.solveMoveList.append(('Y', 'F'))
        self.rotateForwardsData('B')
        self.solveMoveList.append(('B', 'F'))
        self.rotateForwardsData('B')
        self.solveMoveList.append(('B', 'F'))

    def solveEdges(self):
        """A function that implements the algorithm that solves the edges of the top layer"""
        sideFaces = ['B', 'R', 'G', 'O']
        # while all of the edges are not in the correct positions
        while self.cubeFaces['B'].colors[0][0] != self.cubeFaces['B'].colors[0][1] or self.cubeFaces['R'].colors[0][
            0] != self.cubeFaces['R'].colors[0][1] or self.cubeFaces['G'].colors[0][0] != self.cubeFaces['G'].colors[0][
            1] or self.cubeFaces['O'].colors[0][0] != self.cubeFaces['O'].colors[0][1]:
            for i in sideFaces:
                # if any of the faces have the same colors on the top row
                if self.cubeFaces[i].colors[0][0] == self.cubeFaces[i].colors[0][1]:
                    color = self.cubeFaces[i].colors[0][1]
                    # rotate until the row with the samve colors is on the green face
                    while self.cubeFaces['G'].colors[0][0] != color or self.cubeFaces['G'].colors[0][2] != color:
                        self.rotateForwardsData('Y')
                        self.solveMoveList.append(('Y', 'F'))
                    break
            self.solveEdgesMoves()

    def getFacePositions(self, camera):
        """Finds the front face and all the other faces according to the rotation of the camera"""
        cameraRotation = camera.rotation_y % 360

        if (cameraRotation >= 0 and cameraRotation < 45) or (cameraRotation >= 315 and cameraRotation <= 360):
            return {"front": 'B', "left": 'O', "right": 'R', "back": 'G'}
        elif cameraRotation >= 45 and cameraRotation < 135:
            return {"front": 'O', "left": 'G', "right": 'B', "back": 'R'}
        elif cameraRotation >= 135 and cameraRotation < 225:
            return {"front": 'G', "left": 'R', "right": 'O', "back": 'B'}
        elif cameraRotation >= 225 and cameraRotation < 315:
            return {"front": 'R', "left": 'B', "right": 'G', "back": 'O'}

    def isCubeSolved(self):
        """A function that checks if the rubiks cube is solved"""
        for face in self.cubeFaces:
            for row in self.cubeFaces[face].colors:
                for color in row:
                    if color != face:
                        return False
        return True
