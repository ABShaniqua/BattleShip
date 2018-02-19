import unittest

boardWidth = 10
boardHeight = 10

class Ship():
  ships = {'carrier':5, 'battleship':4, 'cruiser':3, 'submarine':3, 'destroyer':2}
  def __init__(self, location = 0, type ='carrier', direction="horizontal"):
    self._loc = location
    self._len = self.ships[type]
    self.calculateOffset(direction)
    if not self.checkValidLocation():
      raise ValueError('Out of bounds _loc: ' + str(location) + ' in creation, ' 
        + str(self._len * self._offset + self._loc) + '<=' + str(boardWidth*boardHeight))
    self.assignCells(location)

  def calculateOffset(self, direction):
    if direction == "horizontal":
      self._offset = 1
    else:
      self._offset = boardWidth

  def assignCells(self, location):
    self._cells = []
    for i in range(0, self._len):
      self._cells.append(self._loc + self._offset*i)

  def checkValidLocation(self):
    return (self._loc < boardWidth * boardHeight 
      and self._loc >= 0 
      and (((self._len + (self._loc % boardWidth) < boardWidth) 
          and self._offset == 1) 
        or ((self._len * self._offset + self._loc <= boardWidth*boardHeight) 
          and  self._offset == boardWidth)))

  def checkExists(self, location):
    return location in self._cells

  def hit(self, location):
    if self.checkExists(location):
      self._cells.remove(location)
      return True
    return False

  def dead(self):
    return len(self._cells) == 0

  def collision(self, ship):
    for cell in self._cells:
      if ship.checkExists(cell):
        return True
    return False

class Game():
  player1 = []
  player2 = []
  def __init__(self):
    pass

  def addShip(self, player_id, ship):

    if player_id == 1:
      player = self.player1
    else:
      player = self.player2
    if not self.checkIfColliding(player, ship):
      self.player1.append(ship)
      return True

  def checkIfColliding(self, player, ship):
    for existingShip in player:
      if ship.collision(existingShip):
        raise ValueError('Collision with existing ship')
    return False



class TestBattleship(unittest.TestCase):
  def testShipCreation(self):
    self.assertEqual(Ship()._loc, 0)
    self.assertEqual(Ship(4)._loc, 4)
    with self.assertRaises(ValueError):
       Ship(200)
    self.assertEqual(Ship(10, 'destroyer')._len,2)
    self.assertTrue(Ship(50, direction="horizontal").checkExists(54))
    self.assertTrue(Ship(50, direction="vertical").checkExists(90))
    self.assertFalse(Ship(50).checkExists(55))
    with self.assertRaises(ValueError):
       Ship(99)
    with self.assertRaises(ValueError):
       Ship(80, direction="vertical")

  def testShipHits(self):
    testShip = Ship(50)
    self.assertFalse(testShip.hit(1))
    self.assertTrue(testShip.hit(51))
    self.assertFalse(testShip.checkExists(51))
    self.assertFalse(testShip.hit(51))
    testShip.hit(50)
    testShip.hit(52)
    testShip.hit(53)
    testShip.hit(54)
    self.assertTrue(testShip.dead())

  def testBattleshipGame(self):
    testShip = Ship(50)
    testGame = Game()
    self.assertTrue(testGame.addShip(1, testShip))
    with self.assertRaises(ValueError):
      testGame.addShip(1, testShip)


def main():
  unittest.main()

if __name__ == '__main__':
  main()
