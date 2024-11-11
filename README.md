# Pose Viewer

Run viewer with:

`fastapi dev ./src/pose_viewer_server.py`

And navigate to `http://127.0.0.1:8000`.

Then stream data to the viewer with:

`python src/pose_file_reader_client.py <WHAM_pkl_output>`

For example, using the provided file:

`python src/pose_file_reader_client.py ./dataset/sit_to_stands-wham_output.pkl`
