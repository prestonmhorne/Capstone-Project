import pygame
import random
import math

pygame.init()

sw = 1170
sh = 780
TILE_SIZE = 60
win = pygame.display.set_mode((sw, sh))
pygame.display.set_caption('Traffic Simulator')
clock = pygame.time.Clock()

settings_x = 780 #variable used for making grass not overlap settings menu

RoadImages = {
    "VerticalRoad": pygame.image.load("twoLaneRoadVerticalTile.png"),
    "HorizontalRoad": pygame.image.load("twoLaneRoadHorizontalTile.png"),
    "FourWay": pygame.image.load("fourWayStop.png"),
    "StopLightHorizontalGo": pygame.image.load("stopLightHorizontalGo.png"),
    "StopLightVerticalGo": pygame.image.load("stopLightVerticalGo.png"),
    "StopLightHorizontalSlow": pygame.image.load("stopLightHorizontalSlow.png"),
    "StopLightVerticalSlow": pygame.image.load("stopLightVerticalSlow.png"),
    "StopLightAllStop": pygame.image.load("stopLightAllStop.png"),
    "SpawnTunnelNORTH": pygame.image.load("spawnTunnelNorth.png"),
    "SpawnTunnelEAST": pygame.image.load("spawnTunnelEast.png"),
    "SpawnTunnelSOUTH": pygame.image.load("spawnTunnelSouth.png"),
    "SpawnTunnelWEST": pygame.image.load("spawnTunnelWest.png")
}

BlueCarImages = {
    "NORTH": pygame.image.load("northCarBlue.png"),
    "EAST": pygame.image.load("eastCarBlue.png"),
    "SOUTH": pygame.image.load("southCarBlue.png"),
    "WEST": pygame.image.load("westCarBlue.png")
}

RedCarImages = {
    "NORTH": pygame.image.load("northCarRed.png"),
    "EAST": pygame.image.load("eastCarRed.png"),
    "SOUTH": pygame.image.load("southCarRed.png"),
    "WEST": pygame.image.load("westCarRed.png")
}

CarImages = [RedCarImages, BlueCarImages]

SettingsImages = [
    pygame.image.load("settings.jpg")
]

GrassImage = pygame.image.load("grass.png")

flower_images = [
    pygame.image.load('flower1.png'),
    pygame.image.load('flower2.png'),
]

DIRECTIONS = ["NORTH", "EAST", "SOUTH", "WEST"]

NORTH = "NORTH"
EAST = "EAST"
SOUTH = "SOUTH"
WEST = "WEST"

GREEN = 0
YELLOW = 1
RED = 2

STOP_DIST = 25

HORIZONTAL = False
VERTICAL = True

CARSPEED = 1
STOPSIGN_TIME_MAX = 200
LIGHT_TIME = 1000
TRAFFIC_DENSITY = 10
LAYOUT = 3

# =============================ROAD SEGMENT CLASS===============================
class RoadSegment():
    def __init__(self, x, y, direction = None):
        #self.image = image
        self.width = 60
        self.height = 60
        self.direction = direction
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.type = self.__class__.__name__
        self.paths = {
            "NORTHEAST": [],
            "WESTNORTH": [],
            "SOUTHWEST": [],
            "EASTSOUTH": [],
            "EASTNORTH": [],
            "NORTHWEST" : [],
            "WESTSOUTH": [],
            "SOUTHEAST" : []}

    # draws the road segment to the screen
    def draw(self):
        win.blit(self.image, (self.x, self.y))
        #for xy in self.paths["WESTNORTH"]:
            #pygame.draw.rect(win, (255,0,0), (xy[0], xy[1], 1, 1))

    # updates list of cars that are on the road segment
    def updateTrafficQueue(self, carsList):
        pass 
        '''
        for car in carsList:
            if car.rect.colliderect(self.rect):
                if car not in self.TrafficQueue:
                    self.TrafficQueue.append(car)
            else:
                if car in self.TrafficQueue:
                    self.TrafficQueue.remove(car)
        '''

class SpawnTunnel(RoadSegment):
    def __init__(self, x, y, direction):
        RoadSegment.__init__(self, x, y, direction)
        self.type = self.__class__.__name__
        self.image = RoadImages[self.type+direction]
   	 #methods & attributes

#twoLaneRoadVertical
class VerticalRoad(RoadSegment):
    def __init__(self, x, y, direction = None):
        RoadSegment.__init__(self, x, y, direction = None)
        self.type = self.__class__.__name__
        self.image = RoadImages[self.type]
   	 #methods & attributes


#twoLaneRoadHorizontal
class HorizontalRoad(RoadSegment):
    def __init__(self, x, y, direction = None):
       RoadSegment.__init__(self, x, y, direction = None)
       self.type = self.__class__.__name__
       self.image = RoadImages[self.type]


class Intersection(RoadSegment):
    def __init__(self, x, y, direction=None):
        RoadSegment.__init__(self, x, y, direction=None)
        self.TrafficQueue = []
        self.getPaths()

    # get paths for cars to follow when turning
    # get paths for cars to follow when turning
    def getPaths(self):
        # NORTH to EAST
        for i in range(24):
            self.paths["NORTHEAST"].append((37 + self.x, self.width - i + self.y))

        for i in range(24):
            self.paths["NORTHEAST"].append((37 + i + self.x, 37 + self.y))

        # SOUTH to WEST
        for i in range(8):
            self.paths["SOUTHWEST"].append((7 + self.x, i + self.y))

        for i in range(8):
            self.paths["SOUTHWEST"].append((7 - i + self.x, 7 + self.y))

        # WEST to NORTH
        for i in range(12):
            self.paths["WESTNORTH"].append((self.x - i * 2 + self.width, self.y + 12 - i))

        # EAST to SOUTH
        for i in range(8):
            self.paths["EASTSOUTH"].append((self.x + i + 7, self.y + 37))

        for i in range(22):
            self.paths["EASTSOUTH"].append((self.x + 14, self.y + 37 + i))

        # SOUTH to EAST
        for i in range(15):
            self.paths["SOUTHEAST"].append((10 + self.x, i + self.y + 1))
        for i in range(20):
            self.paths["SOUTHEAST"].append((self.x + i + 24, self.y + i + 16))
        for i in range(18):
            self.paths["SOUTHEAST"].append((self.x + i + 44, self.y + 36))

        # EAST to NORTH
        for i in range(38):
            self.paths["EASTNORTH"].append((self.x + i, self.y + 37 - i))

        # WEST to SOUTH
        for i in range(7, 60):
            self.paths["WESTSOUTH"].append((self.x + 66 - i, self.y + i))

        # NORTH to WEST
        for i in range(15):
            self.paths["NORTHWEST"].append((self.x + 37, self.y + 59 - i))
        for i in range(38):
            self.paths["NORTHWEST"].append((self.x + 37 - i, self.y + 44 - i))

   	 #methods & attributes
class FourWay(Intersection):
    def __init__(self, x, y, direction=None):
        Intersection.__init__(self, x, y, direction=None)
        self.type = self.__class__.__name__
        self.image = RoadImages[self.type]
        #self.TrafficQueue = []


class StopLight(Intersection):
    def __init__(self, x, y, direction=None):
        Intersection.__init__(self, x, y, direction=None)
        self.type = self.__class__.__name__
        self.image = RoadImages[self.type + "HorizontalGo"]
        self.horizontalLight = GREEN
        self.verticalLight = RED
        self.lastDirection = HORIZONTAL
        self.currentDirection = HORIZONTAL
        self.lightTime = 0
        self.carWait = [None, None, None, None]  # 0 is North, 1 is East, 2 is South and 3 is West

    # increment the counter for how long it has been since light changed and if long
    # enough switch direction of light
    def incrementLight(self):
        if self.lightTime == LIGHT_TIME and (
                (self.currentDirection == HORIZONTAL and not (
                        self.carWait[0] is not None or self.carWait[2] is not None))
                or (self.currentDirection == VERTICAL and not (self.carWait[1] is not None or self.carWait[
            3]) is not None)):
            self.lightTime = 0
        elif self.lightTime == LIGHT_TIME:
            if self.verticalLight == GREEN:
                self.verticalLight = YELLOW
                self.image = RoadImages["StopLightVerticalSlow"]
            else:
                self.horizontalLight = YELLOW
                self.image = RoadImages["StopLightHorizontalSlow"]

        elif math.ceil(LIGHT_TIME * 1.2) <= self.lightTime < math.ceil(LIGHT_TIME * 1.5):
            self.verticalLight = RED
            self.horizontalLight = RED
            self.image = RoadImages["StopLightAllStop"]
        elif self.lightTime == math.ceil(LIGHT_TIME * 1.5):
            if self.lastDirection == VERTICAL:
                self.lastDirection = HORIZONTAL
                self.currentDirection = HORIZONTAL
                self.horizontalLight = GREEN
                self.carWait[1] = None
                self.carWait[3] = None
                self.image = RoadImages["StopLightHorizontalGo"]
            else:
                self.lastDirection = VERTICAL
                self.currentDirection = VERTICAL
                self.verticalLight = GREEN
                self.carWait[0] = None
                self.carWait[2] = None
                self.image = RoadImages[("StopLightVerticalGo")]
            self.lightTime = 0
        self.lightTime += 1


#===================================CAR CLASS===================================


class Car():
    total_stop_time = 0  # Static variable to track total stop time for all cars
    cars_spawned = 0  # Static variable to track total number of cars spawned
    def __init__(self, spawnsList, carsList, images):
        self.direction = random.choice(DIRECTIONS)
        self.newDirection = None
        self.nextRoad = None
        self.currentRoad = None
        self.previousRoad = None
        self.images = images
        self.image = None
        self.stopSignTime = 0
        self.spawnsList = spawnsList
        self.spawned = False
        self.carsList = carsList
        self.height = 20
        self.width = 16
        self.x = -10
        self.y = -10
        self.column = math.floor(self.x / 60)
        self.row = math.floor(self.y / 60)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.hitBoxRect = pygame.Rect(self.x, self.y, self.width, self.height)

        # experimenting with realistic acceleration and braking
        self.maxSpeed = 3  # Maximum speed of the car
        self.speed = 0  # Current speed of the car
        self.acceleration = 0.01  # Acceleration rate
        self.braking = self.speed / 100.0  # Braking rate
        self.delay = 0

        #turning
        self.turning = False
        self.progress = 0
        self.angle = 0

        #driving route
        self.route = []
        self.routeDirections = []
        self.routeProgress = 0

        
        self.stopped_time = 0 # Time in milliseconds the car has been stopped

    # draws the car to the screen
    def draw(self):
        if self.currentRoad is not None:

            if not self.turning:
                self.image = self.images[self.direction]
                win.blit(self.image, (self.x, self.y))
            #if self == self.carsList[0]:
                #pygame.draw.rect(win, (255,0,0), self.hitBoxRect) #draws hitBox
                


    # updates the rect of the car to be used for collision detections
    def updateRect(self):
        if self.direction == SOUTH or self.direction == NORTH:
            self.height = 20
            self.width = 16
        else:
            self.height = 16
            self.width = 20

        if self.direction == NORTH:
            self.hitBoxRect = pygame.Rect(self.x, self.y - int(self.height / 1.5), self.width, int(self.height / 1.5))
            if (0 <= math.floor(self.x / 60) <= 12) and (0 <= math.floor(self.y / 60) <= 12):
                self.column = math.floor(self.x / 60)
                self.row = math.floor(self.y / 60)
                self.visionRow = self.row - 1

        elif self.direction == SOUTH:
            self.hitBoxRect = pygame.Rect(self.x, self.y + self.height, self.width, int(self.height / 1.5))
            if (0 <= math.floor(self.x / 60) <= 12) and (0 <= math.floor((self.y + self.height) / 60) <= 12):
                self.column = math.floor(self.x / 60)
                self.row = math.floor((self.y + self.height) / 60)
                self.visionRow = self.row + 1

        elif self.direction == EAST:
            self.hitBoxRect = pygame.Rect(self.x + self.width, self.y, int(self.width / 1.5), self.height)
            if (0 <= math.floor(self.x / 60) <= 12) and (0 <= math.floor(self.y / 60) <= 12):
                self.column = math.floor((self.x + self.width) / 60)
                self.row = math.floor(self.y / 60)
                self.visionCol = self.column + 1

        elif self.direction == WEST:
            self.hitBoxRect = pygame.Rect(self.x - int(self.width / 1.5), self.y, int(self.width / 1.5), self.height)
            if ((0 <= math.floor(self.x / 60) <= 12)
                    and (0 <= math.floor(self.y / 60) <= 12)):
                self.column = math.floor(self.x / 60)
                self.row = math.floor(self.y / 60)
                self.visionCol = self.column - 1

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    # spawns car at a possible spawn location
    def spawn(self, spawnsList):
        self.route.clear()
        self.routeDirections.clear()
        self.routeProgress = 0

        if len(spawnsList) > 0:
            option = random.choice(self.spawnsList)
            self.direction = option.direction

            if option.direction == NORTH:
                self.x = option.x + 37
                self.y = option.y
                self.updateRect()
                self.getRoad()
                self.getRoute()

                return True

            elif option.direction == SOUTH:
                self.x = option.x + 7
                self.y = option.y
                self.updateRect()
                self.getRoad()
                self.getRoute()

                return True

            elif option.direction == WEST:
                self.x = option.x
                self.y = option.y + 7
                self.updateRect()
                self.getRoad()
                self.getRoute()
                return True

            elif option.direction == EAST:
                self.x = option.x
                self.y = option.y + 37
                self.updateRect()
                self.getRoad()
                self.getRoute()
                return True

        return False

    #get route for car to drive
    def getRoute(self):
        
        segment = self.currentRoad
        direction = self.direction
        column = self.column
        row = self.row
        if segment != None:
            while segment.type != "SpawnTunnel" or len(self.route) == 0:
                self.route.append(segment)

                if segment.type == "FourWay" or segment.type == "StopLight":
                    prevDirection = direction
                    if direction == NORTH or direction == SOUTH:
                        direction = random.choice((EAST,WEST,direction))
                    elif direction == EAST or direction == WEST:
                        direction = random.choice((NORTH,SOUTH,direction))


                self.routeDirections.append(direction)   

                if direction == NORTH:
                    row -= 1
                    segment = simMatrix[column][row]
                if direction == SOUTH:
                    row += 1
                    segment = simMatrix[column][row]

                if direction == EAST:
                    column += 1
                    segment = simMatrix[column][row]
                if direction == WEST:
                    column -= 1
                    segment = simMatrix[column][row]

    # makes the car go forward if no obstacle in front and not at an intersection
    def drive(self):
        self.getRoad()
        
        if self.currentRoad is not None:
            if not self.passFourWayStop():
                self.brake()
                self.delay = 0

            if not self.passStopLight():
                self.brake()
                self.delay = 0

            if not self.obstacleInFront(self.carsList) and self.passFourWayStop() and self.passStopLight():
                self.accelerate()
                self.turn() #working on this
            else:
                self.brake()
                self.delay = 0

            # move the car according to its current speed and direction
            if self.direction == NORTH:
                self.y -= self.speed
            elif self.direction == SOUTH:
                self.y += self.speed
            elif self.direction == WEST:
                self.x -= self.speed
            elif self.direction == EAST:
                self.x += self.speed
            self.delay += 1

        

        if not self.spawned:
            self.spawned = self.spawn(self.spawnsList)

        elif self.currentRoad is not None and self.previousRoad is not None:
            if self.currentRoad.type == "SpawnTunnel" and not self.previousRoad.type == "SpawnTunnel":
                self.spawned = False
            else:
                self.spawned = True

        self.updateRect()
        self.braking = math.ceil(self.speed / 100.0)

        if self.speed == 0:
            # Increment stopped time if the car is stopped
            self.stopped_time += 1  # Increment by 1 assuming drive() is called every frame

    def accelerate(self):
        if self.speed < self.maxSpeed:
            self.speed += self.acceleration
            self.speed = min(self.speed, self.maxSpeed)

    def brake(self):
        self.speed = 0
        if self.speed > 0:
            self.speed -= 1
            self.speed = max(self.speed, 0)

    def needStop(self):
        if (self.direction == NORTH and math.fabs(self.y - (self.nextRoad.y + self.nextRoad.height)) < STOP_DIST or
                self.direction == SOUTH and math.fabs(self.nextRoad.y - (self.y + self.height)) < STOP_DIST or
                self.direction == EAST and math.fabs(self.nextRoad.x - (self.x + self.width)) < STOP_DIST or
                self.direction == WEST and math.fabs(self.x - (self.nextRoad.x + self.nextRoad.width)) < STOP_DIST):
            return True
        else:
            return False

    # tells the car what to do at a four way stop
    def passFourWayStop(self):
        go = True
        if self.nextRoad is not None and self.nextRoad.type == "FourWay":
            if self.stopSignTime < STOPSIGN_TIME_MAX:
                if self.needStop():
                    go = False
                    if self not in self.nextRoad.TrafficQueue:
                        self.nextRoad.TrafficQueue.append(self)
                self.stopSignTime += 1
            elif len(self.nextRoad.TrafficQueue) > 0:
                if self != self.nextRoad.TrafficQueue[0]:
                    if self.needStop():
                        go = False
                        if self not in self.nextRoad.TrafficQueue:
                            self.nextRoad.TrafficQueue.append(self)
                    self.stopSignTime = 0

        elif self.nextRoad is not None and self.nextRoad.type != "FourWay":
            if self.currentRoad.type == "FourWay" and self in self.currentRoad.TrafficQueue:
                self.currentRoad.TrafficQueue.remove(self)
            self.stopSignTime = 0

        return go

    # tells the car what to do at a stop light
    def passStopLight(self):
        go = True
        if self.nextRoad is not None and self.nextRoad.type == "StopLight":
            if (self.routeProgress + 1 < len(self.routeDirections) and
                    (
                    (self.direction == NORTH and self.routeDirections[self.routeProgress + 1] == WEST)
                    or (self.direction == SOUTH and self.routeDirections[self.routeProgress + 1] == EAST)
                    or (self.direction == EAST and self.routeDirections[self.routeProgress + 1] == NORTH)
                    or (self.direction == WEST and self.routeDirections[self.routeProgress + 1] == SOUTH)
                    )
                    and self not in self.nextRoad.TrafficQueue):
                self.nextRoad.TrafficQueue.append(self)

            if self.needStop():
                if ((self.nextRoad.verticalLight == RED or self.nextRoad.verticalLight == YELLOW) and
                        (self.direction == NORTH or self.direction == SOUTH)):
                    go = False
                    if self.direction == NORTH:
                        self.nextRoad.carWait[0] = self
                    else:
                        self.nextRoad.carWait[2] = self
                elif ((self.nextRoad.horizontalLight == RED or self.nextRoad.horizontalLight == YELLOW) and
                      (self.direction == EAST or self.direction == WEST)):
                    go = False

                    if self.direction == EAST:
                        self.nextRoad.carWait[1] = self
                    else:
                        self.nextRoad.carWait[3] = self

            if go:
                for c in cars:
                    if ( c != self and
                            (c.nextRoad == self.nextRoad or c.currentRoad == self.nextRoad) and
                            (self.routeProgress + 1 < len(self.routeDirections) and (
                                    (self.direction == NORTH and self.routeDirections[self.routeProgress + 1] == WEST)
                                    or (self.direction == SOUTH and self.routeDirections[self.routeProgress + 1] == EAST)
                                    or (self.direction == EAST and self.routeDirections[self.routeProgress + 1] == NORTH)
                                    or (self.direction == WEST and self.routeDirections[self.routeProgress + 1] == SOUTH)
                            )
                            ) and
                            (self.direction == NORTH and c.direction == SOUTH or
                             self.direction == SOUTH and c.direction == NORTH or
                             self.direction == EAST and c.direction == WEST or
                             self.direction == WEST and c.direction == EAST) and
                            ((c.routeProgress + 1 < len(c.routeDirections) and
                              (c.direction == c.routeDirections[c.routeProgress + 1] or
                               (c.direction == NORTH and c.routeDirections[c.routeProgress + 1] == EAST)
                               or (c.direction == SOUTH and c.routeDirections[c.routeProgress + 1] == WEST)
                               or (c.direction == EAST and (c.routeDirections[c.routeProgress + 1] == SOUTH)
                                   or (c.direction == WEST and c.routeDirections[c.routeProgress + 1] == NORTH)
                               ))
                             ) or
                             (c.routeProgress + 1 < len(c.routeDirections) and
                              (
                                      (c.direction == NORTH and c.routeDirections[c.routeProgress + 1] == WEST)
                                      or (c.direction == SOUTH and c.routeDirections[c.routeProgress + 1] == EAST)
                                      or (c.direction == EAST and (c.routeDirections[c.routeProgress + 1] == NORTH)
                                          or (c.direction == WEST and c.routeDirections[
                                          c.routeProgress + 1] == SOUTH)
                                      )) and
                              self.nextRoad.TrafficQueue.index(self) > self.nextRoad.TrafficQueue.index(c)))):
                        go = False
                        if self.direction == NORTH:
                            self.nextRoad.carWait[0] = self
                        elif self.direction == EAST:
                            self.nextRoad.carWait[1] = self
                        elif self.direction == SOUTH:
                            self.nextRoad.carWait[2] = self
                        else:
                            self.nextRoad.carWait[3] = self

        if self.previousRoad is not None and self.previousRoad.type == "StopLight":
            if len(self.previousRoad.TrafficQueue) != 0 and self in self.previousRoad.TrafficQueue:
                self.previousRoad.TrafficQueue.remove(self)
        return go

    # updates the road that the car is currently on
    def getRoad(self):
        if self.currentRoad != simMatrix[self.column][self.row]:
            self.previousRoad = self.currentRoad
            self.currentRoad = simMatrix[self.column][self.row]
            self.routeProgress += 1
            if self.direction == NORTH:

                if self.row - 1 < 0 or self.row - 1 > len(simMatrix)-1:
                    pass #self.nextRoad = None
                else:
                    self.nextRoad = simMatrix[self.column][self.row-1]
            elif self.direction == SOUTH:

                if self.row + 1 < 0 or self.row + 1 > len(simMatrix)-1:
                    pass #self.nextRoad = None
                else:
                    self.nextRoad = simMatrix[self.column][self.row+1]
            elif self.direction == EAST:

                if self.column + 1 < 0 or self.column + 1 > len(simMatrix)-1:
                    pass #self.nextRoad = None
                else:
                    self.nextRoad = simMatrix[self.column+1][self.row]
            elif self.direction == WEST:

                if self.column- 1 < 0 or self.column - 1 > len(simMatrix)-1:
                    pass #self.nextRoad = None
                else:
                    self.nextRoad = simMatrix[self.column-1][self.row]

    # checks if there is something in front of the car
    def obstacleInFront(self, obstacleList):
        isObstacle = False
        for obstacle in obstacleList:
            if obstacle.rect.colliderect(self.hitBoxRect):
                if obstacle != self:
                    isObstacle = True
        return isObstacle

    #turning
    def turn(self):
        #print(len(self.nextRoad.paths[5]))
        directionChange = None
        if self.currentRoad.type == "FourWay" or self.currentRoad.type == "StopLight":
            #print("route progress: ",self.routeProgress)
            #print("route length",len(self.routeDirections))
            self.newDirection = self.routeDirections[self.routeProgress]
            if self.newDirection != self.direction: 
                directionChange = self.direction + self.newDirection
            
            if directionChange != None:
                if self.angle < 90 and self.progress < len(simMatrix[self.column][self.row].paths[directionChange]):
                    self.rotate(directionChange)
                    self.angle += 2
                    self.progress += 1
            
                if self.progress >= len(simMatrix[self.column][self.row].paths[directionChange]) or self.angle >= 90:
                    self.direction = self.routeDirections[self.routeProgress]           
                    self.angle = 0
                    self.progress = 0
                    self.turning = False

    def rotate(self, directionChange):
        
        if self.direction == NORTH:
            if self.newDirection == EAST:
                self.x = simMatrix[self.column][self.row].paths[directionChange][self.progress][0]
                self.y = simMatrix[self.column][self.row].paths[directionChange][self.progress][1]
               
                offset_center_to_pivot = pygame.math.Vector2((self.x+(self.width/2),self.y)) - self.rect.center
                # roatated offset from pivot to center
                rotated_offset = offset_center_to_pivot.rotate(-self.angle)

                # roatetd image center
                rotated_image_center = (self.x - rotated_offset.x+(self.width/2), self.y - rotated_offset.y)
                rotated_image = pygame.transform.rotate(self.image, -self.angle)
                rotated_image_rect = rotated_image.get_rect(center = rotated_image_center) 
                win.blit(rotated_image, rotated_image_rect)
                  
                self.turning = True

                                
            if self.newDirection == WEST:
                self.x = simMatrix[self.column][self.row].paths[directionChange][self.progress][0]
                self.y = simMatrix[self.column][self.row].paths[directionChange][self.progress][1] - self.width/2
               
                offset_center_to_pivot = pygame.math.Vector2((self.x+(self.width/2),self.y)) - self.rect.center
                # roatated offset from pivot to center
                rotated_offset = offset_center_to_pivot.rotate(self.angle)

                # roatetd image center
                rotated_image_center = (self.x - rotated_offset.x+(self.width/2), self.y - rotated_offset.y)
                rotated_image = pygame.transform.rotate(self.image, self.angle)
                rotated_image_rect = rotated_image.get_rect(center = rotated_image_center)  
                win.blit(rotated_image, rotated_image_rect)
                  
                self.turning = True
        elif self.direction == SOUTH:
            if self.newDirection == EAST:
                #print(self.progress)
                self.x = simMatrix[self.column][self.row].paths[directionChange][self.progress][0]
                self.y = simMatrix[self.column][self.row].paths[directionChange][self.progress][1]
                #print(self.progress)
               
                offset_center_to_pivot = pygame.math.Vector2((self.x,self.y)) - self.rect.center
                # roatated offset from pivot to center
                rotated_offset = offset_center_to_pivot.rotate(self.angle)

                # roatetd image center
                rotated_image_center = (self.x - rotated_offset.x+(self.width/2), self.y - rotated_offset.y)
                rotated_image = pygame.transform.rotate(self.image, self.angle)
                rotated_image_rect = rotated_image.get_rect(center = rotated_image_center)  
                win.blit(rotated_image, rotated_image_rect)
                  
                self.turning = True

            if self.newDirection == WEST:
                self.x = simMatrix[self.column][self.row].paths[directionChange][self.progress][0]
                self.y = simMatrix[self.column][self.row].paths[directionChange][self.progress][1]
                #print(self.progress)
               
                offset_center_to_pivot = pygame.math.Vector2((self.x+(self.width/2),self.y)) - self.rect.center
                # roatated offset from pivot to center
                rotated_offset = offset_center_to_pivot.rotate(-self.angle)

                # roatetd image center
                rotated_image_center = (self.x - rotated_offset.x+(self.width/2), self.y - rotated_offset.y)
                rotated_image = pygame.transform.rotate(self.image, -self.angle)
                rotated_image_rect = rotated_image.get_rect(center = rotated_image_center)  
                win.blit(rotated_image, rotated_image_rect)
                  
                self.turning = True
            
        elif self.direction == WEST:
            if self.newDirection == SOUTH:
                self.x = simMatrix[self.column][self.row].paths[directionChange][self.progress][0] -self.width/2
                self.y = simMatrix[self.column][self.row].paths[directionChange][self.progress][1]
                #print(self.progress)
               
                offset_center_to_pivot = pygame.math.Vector2((self.x,self.y)) - self.rect.center
                # roatated offset from pivot to center
                rotated_offset = offset_center_to_pivot.rotate(self.angle)

                # roatetd image center
                rotated_image_center = (self.x - rotated_offset.x+(self.width/2), self.y - rotated_offset.y)
                rotated_image = pygame.transform.rotate(self.image, self.angle)
                rotated_image_rect = rotated_image.get_rect(center = rotated_image_center)  
                win.blit(rotated_image, rotated_image_rect)
                  
                self.turning = True
            if self.newDirection == NORTH:
                self.x = simMatrix[self.column][self.row].paths[directionChange][self.progress][0]
                self.y = simMatrix[self.column][self.row].paths[directionChange][self.progress][1]
                #print(self.progress)
               
                offset_center_to_pivot = pygame.math.Vector2((self.x+(self.width/2),self.y)) - self.rect.center
                # roatated offset from pivot to center
                rotated_offset = offset_center_to_pivot.rotate(-self.angle)

                # roatetd image center
                rotated_image_center = (self.x - rotated_offset.x+(self.width/2), self.y - rotated_offset.y)
                rotated_image = pygame.transform.rotate(self.image, -self.angle)
                rotated_image_rect = rotated_image.get_rect(center = rotated_image_center)  
                win.blit(rotated_image, rotated_image_rect)
                  
                self.turning = True

        elif self.direction == EAST:
            if self.newDirection == SOUTH:
                self.x  = simMatrix[self.column][self.row].paths[directionChange][self.progress][0] - self.width/2
                self.y = simMatrix[self.column][self.row].paths[directionChange][self.progress][1]
                #print(self.progress)

                offset_center_to_pivot = pygame.math.Vector2((self.x,self.y)) - self.rect.center
                # roatated offset from pivot to center
                rotated_offset = offset_center_to_pivot.rotate(-self.angle)

                # roatetd image center
                rotated_image_center = (self.x - rotated_offset.x , self.y - rotated_offset.y)
                rotated_image = pygame.transform.rotate(self.image, -self.angle)
                rotated_image_rect = rotated_image.get_rect(center = rotated_image_center)  
                win.blit(rotated_image, rotated_image_rect)
    
                self.turning = True
                            
            if self.newDirection == NORTH:
                self.x = simMatrix[self.column][self.row].paths[directionChange][self.progress][0]
                self.y = simMatrix[self.column][self.row].paths[directionChange][self.progress][1]
                #print(self.progress)
               
                offset_center_to_pivot = pygame.math.Vector2((self.x+(self.width/2),self.y)) - self.rect.center
                # roatated offset from pivot to center
                rotated_offset = offset_center_to_pivot.rotate(self.angle)

                # roatetd image center
                rotated_image_center = (self.x - rotated_offset.x+(self.width/2), self.y - rotated_offset.y)
                rotated_image = pygame.transform.rotate(self.image, self.angle)
                rotated_image_rect = rotated_image.get_rect(center = rotated_image_center)  
                win.blit(rotated_image, rotated_image_rect)
                  
                self.turning = True


# ==============================================================================

# creates list of road segments that form the road's layout
def createRoad():
    #roadType(x,y,direction)

    # straight road
    segmentList0 = [
        SpawnTunnel(TILE_SIZE * 6, TILE_SIZE * 0, SOUTH),
        VerticalRoad(TILE_SIZE * 6,TILE_SIZE * 1),
        VerticalRoad(TILE_SIZE * 6,TILE_SIZE * 2),
        VerticalRoad(TILE_SIZE * 6,TILE_SIZE * 3),
        VerticalRoad(TILE_SIZE * 6,TILE_SIZE * 4),
        VerticalRoad(TILE_SIZE * 6,TILE_SIZE * 5),
        VerticalRoad(TILE_SIZE * 6,TILE_SIZE * 6),
        VerticalRoad(TILE_SIZE * 6,TILE_SIZE * 7),
        VerticalRoad(TILE_SIZE * 6,TILE_SIZE * 8),
        VerticalRoad(TILE_SIZE * 6,TILE_SIZE * 9),
        VerticalRoad(TILE_SIZE * 6,TILE_SIZE * 10),
        VerticalRoad(TILE_SIZE * 6,TILE_SIZE * 11),
        SpawnTunnel(TILE_SIZE * 6, TILE_SIZE * 12, NORTH)]

    # single 4 way stop
    segmentList1 = [
        SpawnTunnel(TILE_SIZE * 6, TILE_SIZE * 0, SOUTH),
        VerticalRoad(TILE_SIZE * 6, TILE_SIZE * 1),
        VerticalRoad(TILE_SIZE * 6, TILE_SIZE * 2),
        VerticalRoad(TILE_SIZE * 6, TILE_SIZE * 3),
        VerticalRoad(TILE_SIZE * 6, TILE_SIZE * 4),
        VerticalRoad(TILE_SIZE * 6, TILE_SIZE * 5),
        StopLight(TILE_SIZE * 6, TILE_SIZE * 6),
        VerticalRoad(TILE_SIZE * 6, TILE_SIZE * 7),
        VerticalRoad(TILE_SIZE * 6, TILE_SIZE * 8),
        VerticalRoad(TILE_SIZE * 6, TILE_SIZE * 9),
        VerticalRoad(TILE_SIZE * 6, TILE_SIZE * 10),
        VerticalRoad(TILE_SIZE * 6, TILE_SIZE * 11),
        SpawnTunnel(TILE_SIZE * 6, TILE_SIZE * 12, NORTH),
        SpawnTunnel(TILE_SIZE * 0, TILE_SIZE * 6, EAST),
        HorizontalRoad(TILE_SIZE * 1, TILE_SIZE * 6),
        HorizontalRoad(TILE_SIZE * 2, TILE_SIZE * 6),
        HorizontalRoad(TILE_SIZE * 3, TILE_SIZE * 6),
        HorizontalRoad(TILE_SIZE * 4, TILE_SIZE * 6),
        HorizontalRoad(TILE_SIZE * 5, TILE_SIZE * 6),
        HorizontalRoad(TILE_SIZE * 7, TILE_SIZE * 6),
        HorizontalRoad(TILE_SIZE * 8, TILE_SIZE * 6),
        HorizontalRoad(TILE_SIZE * 9, TILE_SIZE * 6),
        HorizontalRoad(TILE_SIZE * 10, TILE_SIZE * 6),
        HorizontalRoad(TILE_SIZE * 11, TILE_SIZE * 6),
        SpawnTunnel(TILE_SIZE * 12, TILE_SIZE * 6, WEST)]

    # double 4 way stop
    segmentList2 = [
        SpawnTunnel(TILE_SIZE * 6, TILE_SIZE * 0,SOUTH),
        VerticalRoad(TILE_SIZE * 6,TILE_SIZE * 1),
        VerticalRoad(TILE_SIZE * 6,TILE_SIZE * 2),
        FourWay(TILE_SIZE * 6, TILE_SIZE * 3),
        VerticalRoad(TILE_SIZE * 6,TILE_SIZE * 4),
        VerticalRoad(TILE_SIZE * 6,TILE_SIZE * 5),
        VerticalRoad(TILE_SIZE * 6,TILE_SIZE * 6),
        VerticalRoad(TILE_SIZE * 6,TILE_SIZE * 7),
        VerticalRoad(TILE_SIZE * 6,TILE_SIZE * 8),
        FourWay(TILE_SIZE * 6, TILE_SIZE * 9),
        VerticalRoad(TILE_SIZE * 6,TILE_SIZE * 10),
        VerticalRoad(TILE_SIZE * 6,TILE_SIZE * 11),
        SpawnTunnel(TILE_SIZE * 6, TILE_SIZE * 12, NORTH),
        SpawnTunnel(TILE_SIZE * 0, TILE_SIZE * 3, EAST),
        HorizontalRoad(TILE_SIZE * 1,TILE_SIZE * 3),
        HorizontalRoad(TILE_SIZE * 2,TILE_SIZE * 3),
        HorizontalRoad(TILE_SIZE * 3,TILE_SIZE * 3),
        HorizontalRoad(TILE_SIZE * 4,TILE_SIZE * 3),
        HorizontalRoad(TILE_SIZE * 5,TILE_SIZE * 3),
        HorizontalRoad(TILE_SIZE * 7,TILE_SIZE * 3),
        HorizontalRoad(TILE_SIZE * 8,TILE_SIZE * 3),
        HorizontalRoad(TILE_SIZE * 9,TILE_SIZE * 3),
        HorizontalRoad(TILE_SIZE * 10,TILE_SIZE * 3),
        HorizontalRoad(TILE_SIZE * 11,TILE_SIZE * 3),
        SpawnTunnel(TILE_SIZE * 12, TILE_SIZE * 3, WEST),
        SpawnTunnel(TILE_SIZE * 0, TILE_SIZE * 9, EAST),
        HorizontalRoad(TILE_SIZE * 1,TILE_SIZE * 9),
        HorizontalRoad(TILE_SIZE * 2,TILE_SIZE * 9),
        HorizontalRoad(TILE_SIZE * 3,TILE_SIZE * 9),
        HorizontalRoad(TILE_SIZE * 4,TILE_SIZE * 9),
        HorizontalRoad(TILE_SIZE * 5,TILE_SIZE * 9),
        HorizontalRoad(TILE_SIZE * 7,TILE_SIZE * 9),
        HorizontalRoad(TILE_SIZE * 8,TILE_SIZE * 9),
        HorizontalRoad(TILE_SIZE * 9,TILE_SIZE * 9),
        HorizontalRoad(TILE_SIZE * 10,TILE_SIZE * 9),
        HorizontalRoad(TILE_SIZE * 11,TILE_SIZE * 9),
        SpawnTunnel(TILE_SIZE * 12, TILE_SIZE * 9, WEST)]
    
    # quad 4 way stops
    segmentList3 = [
        SpawnTunnel(TILE_SIZE * 3, TILE_SIZE * 0,SOUTH),
        VerticalRoad(TILE_SIZE * 3,TILE_SIZE * 1),
        VerticalRoad(TILE_SIZE * 3,TILE_SIZE * 2),
        StopLight(TILE_SIZE * 3, TILE_SIZE * 3),
        VerticalRoad(TILE_SIZE * 3,TILE_SIZE * 4),
        VerticalRoad(TILE_SIZE * 3,TILE_SIZE * 5),
        VerticalRoad(TILE_SIZE * 3,TILE_SIZE * 6),
        VerticalRoad(TILE_SIZE * 3,TILE_SIZE * 7),
        VerticalRoad(TILE_SIZE * 3,TILE_SIZE * 8),
        FourWay(TILE_SIZE * 3, TILE_SIZE * 9),
        VerticalRoad(TILE_SIZE * 3,TILE_SIZE * 10),
        VerticalRoad(TILE_SIZE * 3,TILE_SIZE * 11),
        SpawnTunnel(TILE_SIZE * 3, TILE_SIZE * 12,NORTH),
        SpawnTunnel(TILE_SIZE * 9, TILE_SIZE * 0,SOUTH),
        VerticalRoad(TILE_SIZE * 9,TILE_SIZE * 1),
        VerticalRoad(TILE_SIZE * 9,TILE_SIZE * 2),
        StopLight(TILE_SIZE * 9, TILE_SIZE * 3),
        VerticalRoad(TILE_SIZE * 9,TILE_SIZE * 4),
        VerticalRoad(TILE_SIZE * 9,TILE_SIZE * 5),
        VerticalRoad(TILE_SIZE * 9,TILE_SIZE * 6),
        VerticalRoad(TILE_SIZE * 9,TILE_SIZE * 7),
        VerticalRoad(TILE_SIZE * 9,TILE_SIZE * 8),
        FourWay(TILE_SIZE * 9, TILE_SIZE * 9),
        VerticalRoad(TILE_SIZE * 9,TILE_SIZE * 10),
        VerticalRoad(TILE_SIZE * 9,TILE_SIZE * 11),
        SpawnTunnel(TILE_SIZE * 9, TILE_SIZE * 12,NORTH),
        SpawnTunnel(TILE_SIZE * 0, TILE_SIZE * 3, EAST),
        HorizontalRoad(TILE_SIZE * 1,TILE_SIZE * 3),
        HorizontalRoad(TILE_SIZE * 2,TILE_SIZE * 3),
        HorizontalRoad(TILE_SIZE * 6,TILE_SIZE * 3),
        HorizontalRoad(TILE_SIZE * 4,TILE_SIZE * 3),
        HorizontalRoad(TILE_SIZE * 5,TILE_SIZE * 3),
        HorizontalRoad(TILE_SIZE * 7,TILE_SIZE * 3),
        HorizontalRoad(TILE_SIZE * 8,TILE_SIZE * 3),
        HorizontalRoad(TILE_SIZE * 10,TILE_SIZE * 3),
        HorizontalRoad(TILE_SIZE * 11,TILE_SIZE * 3),
        SpawnTunnel(TILE_SIZE * 12, TILE_SIZE * 3, WEST),
        SpawnTunnel(TILE_SIZE * 0, TILE_SIZE * 9, EAST),
        HorizontalRoad(TILE_SIZE * 1,TILE_SIZE * 9),
        HorizontalRoad(TILE_SIZE * 2,TILE_SIZE * 9),
        HorizontalRoad(TILE_SIZE * 6,TILE_SIZE * 9),
        HorizontalRoad(TILE_SIZE * 4,TILE_SIZE * 9),
        HorizontalRoad(TILE_SIZE * 5,TILE_SIZE * 9),
        HorizontalRoad(TILE_SIZE * 7,TILE_SIZE * 9),
        HorizontalRoad(TILE_SIZE * 8,TILE_SIZE * 9),
        HorizontalRoad(TILE_SIZE * 10,TILE_SIZE * 9),
        HorizontalRoad(TILE_SIZE * 11,TILE_SIZE * 9),
        SpawnTunnel(TILE_SIZE * 12, TILE_SIZE * 9, WEST)]

    matrix = [[None] * 13 for _ in range(13)]

    if LAYOUT == 0:

        for s in segmentList0:
            matrix[math.floor(s.x / 60)][math.floor(s.y / 60)] = s

        return matrix

    elif LAYOUT == 1:
        for s in segmentList1:
            matrix[math.floor(s.x / 60)][math.floor(s.y / 60)] = s

        return matrix

    elif LAYOUT == 2:
        for s in segmentList2:
            matrix[math.floor(s.x / 60)][math.floor(s.y / 60)] = s

        return matrix

    elif LAYOUT == 3:
        for s in segmentList3:
            matrix[math.floor(s.x / 60)][math.floor(s.y / 60)] = s

        return matrix


# ==============================================================================

# creates an initial list of all cars based on number specified (density)
def generateTraffic(spawnsList):
    carsList = []
    for i in range(TRAFFIC_DENSITY):
        carsList.append(Car(spawnsList, carsList, CarImages[random.randrange(2)]))
    return carsList

# ==============================================================================

def getRoads(matrix):
    roads = []
    for column in matrix:
        for i in column:
            if i is not None:
                roads.append(i)

    return roads


# ==============================================================================

# gets the possible spawn points for the cars (if the road segment is off-screen)
def getSpawns(roads):
    spawnsList = []
    for road in roads:
        if road.type == "SpawnTunnel":
            spawnsList.append(road)
    return spawnsList


# ==============================================================================

# draws grid to screen
def drawGrid():
    for i in range(TILE_SIZE, sw, TILE_SIZE):
        pygame.draw.rect(win, (255, 255, 255), (i, 0, 1, sh))
        pygame.draw.rect(win, (255, 255, 255), (0, i, sw, 1))


# ===================================LISTS======================================

simMatrix = createRoad()
roads = getRoads(simMatrix)
spawns = getSpawns(roads)
cars = generateTraffic(spawns)

#====================================TREE========================================
def generate_trees(number_of_trees, tree_image_path, area_width, area_height, exclusion_zone):

    tree_width = 60  # Adjust based on your tree image size
    tree_height = 60  # Adjust based on your tree image size
    tree_positions = []
    tree_image = pygame.image.load(tree_image_path)

    for _ in range(number_of_trees):
        x = random.randint(0, area_width - tree_width)
        y = random.randint(0, area_height - tree_height)

        # Check if the tree overlaps with the exclusion zone
        if not (x + tree_width > exclusion_zone[0] and x < exclusion_zone[0] + exclusion_zone[2] and
                y + tree_height > exclusion_zone[1] and y < exclusion_zone[1] + exclusion_zone[3]):
            tree_positions.append((x, y, tree_image))

    return tree_positions

# =============================SETTINGS BUTTONS=================================
win.blit(SettingsImages[0], (780, 0))
start_button = pygame.Rect(796, 70, 81, 65)
stop_button = pygame.Rect(894, 70, 81, 65)
reset_button = pygame.Rect(796, 151, 81, 65)
fullscreen_button = pygame.Rect(894, 151, 81, 65)
layout1_button = pygame.Rect(992, 70, 167, 65)
layout2_button = pygame.Rect(992, 151, 167, 65)
layout3_button = pygame.Rect(992, 232, 167, 65)
layout4_button = pygame.Rect(992, 313, 167, 65)

# ===============================FLOWERS=======================================

flower_width = 40  # Example flower image width
flower_height = 40  # Example flower image height
number_of_flowers = 70  # Decide on the number of flowers

# List to hold flower positions
# Initialize flower positions with styles
# List to hold flower positions
flower_positions = []

# Generate flower positions with associated images
for _ in range(number_of_flowers):
    x = random.randint(0, settings_x - flower_width)
    y = random.randint(0, sh - flower_height)

    # Choose a flower image for this position
    flower_image = random.choice(flower_images)

    # Store both position and image together
    flower_positions.append((x, y, flower_image))

#generating trees
exclusion_zone = (settings_x, 0, sw - settings_x, sh) 
tree_positions = generate_trees(20, "tree.png", sw, sh, exclusion_zone)


#trying to make an exclusion zone for spawning 
exclusion_zones = []
for road in roads:
    exclusion_zones.append((road.x, road.y, road.width, road.height))

# =================================MAIN LOOP====================================

run = True
start = False
fullscreen = False
timer_start_time = 0  # Time when the timer was started
timer_running = False  # Whether the timer is currently running
elapsed_time = 0  # The amount of time elapsed since the timer started
while run:
    clock.tick(60)
    mouse_pos = pygame.mouse.get_pos()
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        # Tile the grass texture
    for x in range(0, sw, TILE_SIZE):
        for y in range(0, sh, TILE_SIZE):
            if x < settings_x:
                win.blit(GrassImage, (x, y))

    for pos in flower_positions:
        # Use the pre-selected flower image
        lower_image = pos[2]  # Assuming the image is the third item in the tuple
        win.blit(lower_image, (pos[0], pos[1]))

    for tree_pos in tree_positions:
        win.blit(tree_pos[2], (tree_pos[0], tree_pos[1]))


    if keys[pygame.K_SPACE]:
        if event.type == pygame.KEYUP:
            start = not start

    # make start/stop button work    
    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:
            if start_button.collidepoint(event.pos):
                start = True
                if not timer_running:  # Start the timer if not already running
                    timer_start_time = pygame.time.get_ticks()  # Get the current time
                    timer_running = True
            elif stop_button.collidepoint(event.pos):
                start = False
                if timer_running:  # Stop the timer
                    elapsed_time += pygame.time.get_ticks() - timer_start_time  # Update elapsed time
                    timer_running = False
            elif layout1_button.collidepoint(event.pos):
                spawns = getSpawns(roads)
                simMatrix = createRoad()
                roads = getRoads(simMatrix)
                LAYOUT = 0
                cars = []
                start = False
                timer_start_time = 0
                timer_running = False
                elapsed_time = 0
            elif layout2_button.collidepoint(event.pos):
                spawns = getSpawns(roads)
                simMatrix = createRoad()
                roads = getRoads(simMatrix)
                LAYOUT = 1
                cars = []
                start = False
                timer_start_time = 0
                timer_running = False
                elapsed_time = 0
            elif layout3_button.collidepoint(event.pos):
                spawns = getSpawns(roads)
                simMatrix = createRoad()
                roads = getRoads(simMatrix)
                LAYOUT = 2
                cars = []
                start = False
                timer_start_time = 0
                timer_running = False
                elapsed_time = 0
            elif layout4_button.collidepoint(event.pos):
                spawns = getSpawns(roads)
                simMatrix = createRoad()
                roads = getRoads(simMatrix)
                LAYOUT = 3
                cars = []
                start = False
                timer_start_time = 0
                timer_running = False
                elapsed_time = 0
            elif reset_button.collidepoint(event.pos):
                cars = []
                # Reset the total stop time and cars spawned for average stop time calculation
                Car.total_stop_time = 0
                Car.cars_spawned = 0
                start = False
                timer_start_time = 0
                timer_running = False
                elapsed_time = 0
            elif fullscreen_button.collidepoint(event.pos) and fullscreen == False:
                win = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
                win.blit(SettingsImages[0], (780, 0))
                fullscreen = True
            elif fullscreen_button.collidepoint(event.pos) and fullscreen == True:
                win = pygame.display.set_mode((sw, sh))
                win.blit(SettingsImages[0], (780, 0))
                fullscreen = False   


    #change cursor when hovering over buttons
    if(start_button.collidepoint(mouse_pos) or stop_button.collidepoint(mouse_pos) 
       or reset_button.collidepoint(mouse_pos) or fullscreen_button.collidepoint(mouse_pos)
       or layout1_button.collidepoint(mouse_pos) or layout2_button.collidepoint(mouse_pos) 
       or layout3_button.collidepoint(mouse_pos) or layout4_button.collidepoint(mouse_pos)): 
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
    else:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    if not cars:
        cars = generateTraffic(spawns)

    for road in roads:
        road.draw()
        if road.type== "FourWay":
            road.updateTrafficQueue(cars)
        if road.type == "StopLight" and start:
            road.incrementLight()

    for car in cars:
        if start:
            car.drive()
        car.draw()

    for road in roads:
        if road.type == "SpawnTunnel":
            road.draw()

    # Calculate timer
    if timer_running:
        current_time = pygame.time.get_ticks() - timer_start_time + elapsed_time
    else:
        current_time = elapsed_time

    # Convert current_time to seconds for display
    current_time_seconds = current_time / 1000.0

    # Display the current timer
    font = pygame.font.SysFont(None, 24)
    timer_text = font.render(f'Elapsed Time: {current_time_seconds:.2f}s', True, (255, 255, 255))
    win.blit(timer_text, (10, 10))  # Adjust position as needed

    # Calculate stop time / elapsed time
    total_stopped_time = sum(car.stopped_time for car in cars) / 60 # Assuming 60 FPS for conversion to seconds

    if current_time_seconds > 0:  # Avoid division by zero
        stopped_ratio = total_stopped_time / current_time_seconds
    else:
        stopped_ratio = 0

    # Display the ratio
    ratio_text = font.render(f'Avg Stop Time: {stopped_ratio:.2f}s', True, (255, 255, 255))
    win.blit(ratio_text, (10, 30))  # Adjust position as needed

    # Count the number of cars that are stopped
    num_stopped_cars = sum(1 for car in cars if car.speed == 0)
    font = pygame.font.SysFont(None, 24)
    stopped_cars_text = font.render(f'Stopped Cars: {num_stopped_cars}', True, (255, 255, 255))
    win.blit(stopped_cars_text, (10, 50))  # Adjust position as needed
    

    # drawGrid()
    pygame.display.flip()

pygame.quit()

# ================================END MAIN LOOP=================================
