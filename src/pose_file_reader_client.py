from websockets.asyncio.client import connect
import asyncio
import sys

from pose_utils import loadPoses, FRAME_RATE


async def readPoseFile(pose_file):
  pose_faces, pose_vertices = loadPoses(pose_file)

  async with connect('ws://localhost:8000/ws/input/pose') as websocket:
    await websocket.send(pose_faces.tobytes())

    for vertices in pose_vertices:
      await websocket.send(vertices.tobytes())
      await asyncio.sleep(1./FRAME_RATE)


if __name__ == '__main__':
  input_file = sys.argv[1]
  asyncio.run(readPoseFile(input_file))
