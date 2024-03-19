import numpy as np

class Face:
    """
    A class for managing the cube faces.
    """

    def __init__(self, colors):
        """Initialize the face with a 3x3 matrix of face colors"""
        self.colors = np.array(colors)

    def rotateFace(self):
        """Rotate the face matrix by 90 degrees forwards"""
        self.colors = np.rot90(self.colors, 3)

    def rotateFaceBack(self):
        """Rotate the face matrix by 90 degrees backwards"""
        self.colors = np.rot90(self.colors)

    def getTop(self):
        """Get the top row of the matrix"""
        return self.colors[0]

    def getBottom(self):
        """Get the bottom row of the matrix"""
        return self.colors[2]

    def getRight(self):
        """Get the right column of the matrix"""
        return self.colors[:, 2]

    def getLeft(self):
        """Get the left column of the matrix"""
        return self.colors[:, 0]

    def setTop(self, arr):
        """Set the top row of the matrix with the given values"""
        self.colors[0] = arr

    def setBottom(self, arr):
        """Set the bottom row of the matrix with the given values"""
        self.colors[2] = arr

    def setRight(self, arr):
        """Set the right column of the matrix with the given values"""
        self.colors[:, 2] = arr

    def setLeft(self, arr):
        """Set the left column of the matrix with the given values"""
        self.colors[:, 0] = arr