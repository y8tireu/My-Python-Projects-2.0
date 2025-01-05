from direct.showbase.ShowBase import ShowBase
from panda3d.core import WindowProperties, Camera, GraphicsPipe, GraphicsOutput
from panda3d.core import Vec3, Vec4

class ParkourGame(ShowBase):
    def __init__(self):
        super().__init__()

        # Disable the default camera
        self.disableMouse()

        # Set window title
        self.win.setTitle("2 Player 3D Parkour Game")

        # Load the environment model
        self.environment = self.loader.loadModel("models/environment")
        self.environment.reparentTo(self.render)
        self.environment.setScale(0.25, 0.25, 0.25)
        self.environment.setPos(-8, 42, 0)

        # Initialize players
        self.player1 = self.loader.loadModel("models/panda-model")
        self.player1.reparentTo(self.render)
        self.player1.setScale(0.005)
        self.player1.setPos(0, 10, 0)

        self.player2 = self.loader.loadModel("models/panda-model")
        self.player2.reparentTo(self.render)
        self.player2.setScale(0.005)
        self.player2.setPos(2, 10, 0)

        # Setup cameras
        self.setup_cameras()

        # Setup controls
        self.setup_controls()

    def setup_cameras(self):
        # Create two separate cameras for split-screen
        props = WindowProperties()
        props.setSize(1280, 720)
        self.win.requestProperties(props)

        # Left camera for Player 1
        self.cam1 = self.makeCamera(self.win, sort=1)
        self.cam1.reparentTo(self.render)
        self.cam1.setPos(self.player1.getPos() + Vec3(0, -10, 5))
        self.cam1.lookAt(self.player1)

        # Right camera for Player 2
        self.cam2 = self.makeCamera(self.win, sort=2)
        self.cam2.reparentTo(self.render)
        self.cam2.setPos(self.player2.getPos() + Vec3(0, -10, 5))
        self.cam2.lookAt(self.player2)

        # Adjust viewports for split-screen
        self.cam1.node().getDisplayRegion(0).setSort(1)
        self.cam1.node().getDisplayRegion(0).setDimensions(0, 0.5, 0, 1)
        self.cam2.node().getDisplayRegion(0).setSort(2)
        self.cam2.node().getDisplayRegion(0).setDimensions(0.5, 1, 0, 1)

    def setup_controls(self):
        # Player 1 Controls
        self.accept("w", self.move_player1, ["forward"])
        self.accept("s", self.move_player1, ["backward"])
        self.accept("a", self.move_player1, ["left"])
        self.accept("d", self.move_player1, ["right"])

        # Player 2 Controls
        self.accept("arrow_up", self.move_player2, ["forward"])
        self.accept("arrow_down", self.move_player2, ["backward"])
        self.accept("arrow_left", self.move_player2, ["left"])
        self.accept("arrow_right", self.move_player2, ["right"])

    def move_player1(self, direction):
        if direction == "forward":
            self.player1.setY(self.player1, -0.5)
        elif direction == "backward":
            self.player1.setY(self.player1, 0.5)
        elif direction == "left":
            self.player1.setX(self.player1, -0.5)
        elif direction == "right":
            self.player1.setX(self.player1, 0.5)

        # Update camera position
        self.cam1.setPos(self.player1.getPos() + Vec3(0, -10, 5))
        self.cam1.lookAt(self.player1)

    def move_player2(self, direction):
        if direction == "forward":
            self.player2.setY(self.player2, -0.5)
        elif direction == "backward":
            self.player2.setY(self.player2, 0.5)
        elif direction == "left":
            self.player2.setX(self.player2, -0.5)
        elif direction == "right":
            self.player2.setX(self.player2, 0.5)

        # Update camera position
        self.cam2.setPos(self.player2.getPos() + Vec3(0, -10, 5))
        self.cam2.lookAt(self.player2)

app = ParkourGame()
app.run()
