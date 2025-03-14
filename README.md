# Hand Gesture Control System 🤖👋

A Python-based system that uses hand gestures to control computer functions like scrolling, tab switching, zooming, and page navigation. Powered by MediaPipe and OpenCV.


## Features ✨
- **Inertial Scroll**: Natural scrolling with acceleration and smooth damping
- **Tab Management**: Switch between tabs and reopen closed tabs
- **Zoom Control**: Pinch-to-zoom functionality
- **Page Navigation**: Go back/forward in browser history
- **Multi-hand Support**: Different functions for left/right hands
- **Gesture Recognition**: Multiple simultaneous gesture detection

## Installation 📦

### Requirements
- Python 3.7+
- Webcam
- macOS or Windows (Linux untested)

### Dependencies
```bash
pip install opencv-python mediapipe pyautogui numpy 
```

## Usage 🚀

### Basic Controls

| Gesture | Action | Hand |
|---------|--------|------|
| ✋ All fingers extended (except thumb) | Scroll | Left/Right |
| 🤟 Middle + Index fingers extended | Switch tabs | Left/Right |
| 🤏 Thumb + Index pinch | Zoom in/out | Left/Right |
| 👈👉 Index + Pinky extended  | Page navigation | Either |
| 🖖 Index + Middle + Ring extended | Reopen closed tab | Either |

### Detailed Controls

#### Scroll Control (Inertial Scroll)
- **Right Hand**: Scroll down  
- **Left Hand**: Scroll up  
- Natural acceleration/deceleration

#### Tab Management
- **Right Hand**: `Ctrl/Cmd + Tab` (next tab)
- **Left Hand**: `Ctrl/Cmd + Shift + Tab` (previous tab)
- 1-second cooldown between switches

#### Zoom Control
- **Right Hand**: `Cmd/Ctrl + +` (zoom in)
- **Left Hand**: `Cmd/Ctrl + -` (zoom out)
- 0.5-second cooldown

#### Navigation
- **Point left**: `Cmd/Ctrl + ←` (back)
- **Point right**: `Cmd/Ctrl + →` (forward)

## Running the System ▶️
```bash
python script_5.py
```

## Troubleshooting 🛠️

### Webcam Issues
- Ensure camera access permissions
- Check for other apps using the camera
- Try different video capture index: `cap = cv2.VideoCapture(1)`

### Performance Tips
- Use good lighting conditions
- Keep hands within the camera frame
- Avoid complex backgrounds
- Maintain a 1-2 meter distance from the camera

### Known Limitations
- Gestures optimized for front-facing camera view
- May require calibration for different hand sizes
- High CPU usage during prolonged use

## Dependencies Acknowledgments 📚
- [MediaPipe](https://developers.google.com/mediapipe) for hand tracking
- [OpenCV](https://opencv.org/) for computer vision
- [PyAutoGUI](https://pyautogui.readthedocs.io/en/latest/) for system control

## Contributing 🤝
Contributions welcome! Please open an issue first to discuss proposed changes.

## License ⚖️
[MIT License](LICENSE)

> **Note**: Hotkeys may differ between Windows (Ctrl) and macOS (Cmd). Tested primarily on macOS - Windows users may need to adjust key combinations.
