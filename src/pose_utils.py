import joblib
import smplx
import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


FRAME_RATE = 30


def loadPoses(pose_file):
  pose_data = joblib.load(pose_file)
  person_id = 0
  num_people = len(pose_data)
  num_frames = len(pose_data[0]['pose'])
  print('loading:', pose_file)
  print('contains', num_frames, 'frames and', num_people, 'tracked people')

  pose_vertices = []
  for frame_id in range(num_frames):
    # 'pose' is a 1x72 array (24 keypoints * 3 dimensions)
    # `global_orient` is the pelvis (1x3)
    # `body_pose` is 1x69 (pose without the pelvis)
    global_orient = pose_data[person_id]['pose'][frame_id, :3].reshape((1, -1))
    body_pose = pose_data[person_id]['pose'][frame_id, 3:].reshape((1, -1))

    pose_model = smplx.create(
      model_path='./body_models',
      model_type='smpl',
      global_orient=global_orient,
      body_pose=body_pose
    )

    pose_output = pose_model()
    vertices = pose_output.vertices.detach().cpu().numpy().squeeze()
    pose_vertices.append(vertices)

  return pose_model.faces, pose_vertices

def wristAcceleration(pose_file, plot=False):
  """
  Computes the position, velocity, and acceleration of the right wrist joint from a given motion file 
  and optionally plots the wrist’s acceleration over time.

  The motion file should be a pickle (.pkl) file containing pose data compatible with the SMPL model format. 
  Each frame of the pose data is used to reconstruct a 3D body configuration, from which the wrist’s 3D position 
  is extracted. The velocity and acceleration are then derived by numerically differentiating the position data 
  with respect to time.

  Parameters
  ----------
  pose_file : str
    The file path to the motion data file in .pkl format.
  plot : bool, optional
    If True, plots the x, y, and z components of the wrist’s acceleration over time. 
    Defaults to False.

  Returns
  -------
  time : np.ndarray
     A 1D array of time values for each frame (in seconds).
  position_data : np.ndarray
    A 2D array (num_frames x 3) of the wrist’s 3D position at each frame.
  velocity : np.ndarray
    A 2D array (num_frames x 3) of the wrist’s 3D velocity at each frame (in units of position/second).
  acceleration : np.ndarray
    A 2D array (num_frames x 3) of the wrist’s 3D acceleration at each frame (in units of position/second²).
  """

  # Load pose data
  pose_data = joblib.load(pose_file)
  person_id = 0
  wrist_idx = 21
  num_frames = len(pose_data[0]['pose'])

  # Extract the position of the wrist for each frame
  position_data = []
  for frame_id in range(num_frames):
    global_orient = pose_data[person_id]['pose'][frame_id, :3].reshape((1, -1))
    body_pose = pose_data[person_id]['pose'][frame_id, 3:].reshape((1, -1))

    # Create the SMPL model with the given pose
    pose_model = smplx.create(
      model_path='./body_models',
      model_type='smpl',
      global_orient=global_orient,
      body_pose=body_pose
    )

    # Get the joint positions
    pose_output = pose_model()
    joints = pose_output.joints.detach().cpu().numpy().squeeze()
    position_data.append(joints[wrist_idx])

  position_data = np.array(position_data)  # Shape: (num_frames, 3)

  # Create a time array for the frames
  time = np.arange(num_frames) / FRAME_RATE

  # Compute velocity: v = dp/dt
  velocity = np.gradient(position_data, time, axis=0)

  # Compute acceleration: a = dv/dt
  acceleration = np.gradient(velocity, time, axis=0)

  # Optional: Plot the acceleration components over time
  if plot:
    _, ax = plt.subplots(3, 1, figsize=(10, 6), sharex=True)
    ax[0].plot(time, acceleration[:, 0], label='Ax')
    ax[1].plot(time, acceleration[:, 1], label='Ay')
    ax[2].plot(time, acceleration[:, 2], label='Az')

    ax[0].set_ylabel('Acceleration X (m/s²)')
    ax[1].set_ylabel('Acceleration Y (m/s²)')
    ax[2].set_ylabel('Acceleration Z (m/s²)')
    ax[2].set_xlabel('Time (s)')

    for a in ax:
      a.legend()
      a.grid(True)

    plt.tight_layout()
    plt.show()

  return time, position_data, velocity, acceleration

def plotModelWithJoints(pose_file):
  """
  Visualizes the SMPL model and its joints for the first frame of a given motion data file.
  
  This function:
  - Loads the pose data from a given `.pkl` motion file.
  - Constructs an SMPL model with the initial frame’s global orientation and body pose.
  - Extracts and visualizes the model’s mesh (vertices and faces) in 3D.
  - Plots all joints in black, and specifically highlights the right wrist joint in red.
  - Sets a viewing angle to display the model as if standing upright.

  Parameters
  ----------
  pose_file : str
    The file path to a `.pkl` motion file containing SMPL pose data.
  """

  # Load pose data
  wrist_idx = 21
  pose_data = joblib.load(pose_file)
  person_id = 0

  # We only need the first frame for a static plot
  frame_id = 0
  global_orient = pose_data[person_id]['pose'][frame_id, :3].reshape((1, -1))
  body_pose = pose_data[person_id]['pose'][frame_id, 3:].reshape((1, -1))

  # Create the SMPL model with the given pose
  pose_model = smplx.create(
    model_path='./body_models',
    model_type='smpl',
    global_orient=global_orient,
    body_pose=body_pose
  )

  # Forward pass to get vertices and joints
  pose_output = pose_model()
  vertices = pose_output.vertices.detach().cpu().numpy().squeeze()
  joints = pose_output.joints.detach().cpu().numpy().squeeze()

  # Set up the 3D figure
  fig = plt.figure(figsize=(10, 8))
  ax = fig.add_subplot(111, projection='3d')

  # Create a mesh from the model's vertices and faces
  mesh = Poly3DCollection(vertices[pose_model.faces], alpha=0.1)
  face_color = (1.0, 1.0, 0.9)  # Light, slightly off-white
  edge_color = (0, 0, 0)        # Black edges
  mesh.set_edgecolor(edge_color)
  mesh.set_facecolor(face_color)
  ax.add_collection3d(mesh)

  # Plot all joints in black
  ax.scatter(joints[:, 0], joints[:, 1], joints[:, 2], c='k', s=20, label='All Joints')

  # Highlight the wrist joint in red
  wrist_coords = joints[wrist_idx]
  ax.scatter(wrist_coords[0], wrist_coords[1], wrist_coords[2], c='r', s=60, label='Wrist Joint')

  # Set plot labels and title
  ax.set_xlabel('X')
  ax.set_ylabel('Y')
  ax.set_zlabel('Z')
  ax.set_title('3D SMPL Model and Joints at Time 0')
  ax.legend()

  # Adjust view angle
  ax.view_init(elev=180, azim=90, roll=None, vertical_axis='y')

  plt.tight_layout()
  plt.show()
