from websockets.asyncio.client import connect
import asyncio
import pyautogui
import numpy as np


async def trackMouse():
  async with connect('ws://localhost:8000/ws/input/pose') as websocket:
    prev_x = -1
    prev_y = -1

    screen_size = pyautogui.size()
    screen_width = screen_size.width
    screen_height = screen_size.height
    screen_half_width = screen_width / 2
    screen_half_height = screen_height / 2

    while True:
      position = pyautogui.position()

      if prev_x != position.x or prev_y != position.y:
        prev_x = position.x
        prev_y = position.y

        x = (screen_half_width - position.x) / screen_half_width * np.pi
        y = (screen_half_height - position.y) / screen_half_height * np.pi

        position = np.array([x, y, 0], dtype=np.float32)
        await websocket.send(position.tobytes())

      await asyncio.sleep(0.01)


if __name__ == '__main__':
  asyncio.run(trackMouse())
