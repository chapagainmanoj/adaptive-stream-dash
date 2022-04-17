# Video Stream

## installation

### With docker

```
docker docker build -t video-stream .
docker run -p 8000:8000 --name video_stream_server video-stream
```

### Without docker

#### Requried Dependency:

- ffmpeg

```
source venv.sh
pip install -r requirements/prod.txt
serve
```

### Possible Improvements:

- background worker/task for DASH files creation
- server sent events or websocket implementation for new uploads
- better ui

### Screenshorts

![App Screenshort](/ScreenShot.png?raw=true "App Screenshort")
