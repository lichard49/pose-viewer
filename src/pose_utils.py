import joblib
import smplx


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
