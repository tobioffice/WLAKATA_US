# WLAKATA_US - Automated Object Quality Control System

An intelligent computer vision system for automated object detection and quality assessment using OpenCV and Python. This system captures images, detects objects, analyzes their properties, and determines quality based on burned state classification.

## 🚀 Features

- **Real-time Object Detection**: Detects presence of objects using advanced computer vision techniques
- **Quality Assessment**: Analyzes area, angle, and burned state of detected objects
- **Multi-state Classification**: Classifies objects into 4 burned states (unBurned, underBurned, good, overBurned)
- **Serial Communication**: Interfaces with hardware for automated processing
- **Image Processing Pipeline**: Complete workflow from capture to quality decision

## 📁 Project Structure

```
WLAKATA_US/
├── main.py                     # Main execution script
├── pyproject.toml             # Project dependencies
├── rgbMap.json               # RGB reference values for burned states
├── images/                   # Image storage directory
│   ├── no_object.png         # Background reference image
│   ├── pra*.png             # Sample/processed images
│   └── burnedStates/        # Reference images for each burned state
│       ├── good.png
│       ├── overBurned.png
│       ├── unBurned.png
│       └── underBurned.png
└── utils/                   # Core utility modules
    ├── captureImages.py     # Image capture and preprocessing
    ├── checkObject.py       # Object detection algorithms
    ├── getBurnedState.py    # Burned state classification
    ├── checkAreaAndAngle.py # Geometric property analysis
    └── pickBadAndPlace.py   # Hardware control for object handling
```

## 🛠️ Installation

### Prerequisites

- Python 3.8+
- OpenCV
- NumPy
- PySerial
- UV (Python package manager)

### Setup

1. Clone the repository:

```bash
git clone <repository-url>
cd WLAKATA_US
```

2. Install dependencies using UV:

```bash
uv sync
```

3. Ensure your camera is connected (default: camera index 2)

4. Connect serial device to `/dev/ttyUSB0` (or update the port in `main.py`)

## 🎯 Usage

### Basic Execution

Run the main quality control loop:

```bash
uv run main.py
```

### Individual Module Testing

#### Test Object Detection

```bash
uv run utils/checkObject.py
```

#### Test Burned State Classification

```bash
uv run utils/getBurnedState.py
```

#### Test Image Capture

```bash
uv run utils/captureImages.py
```

## 🔍 How It Works

### 1. Image Capture (`captureImages.py`)

- Captures images from connected camera
- Performs preprocessing (cropping, grayscale conversion, binary thresholding)
- Saves processed images for analysis

### 2. Object Detection (`checkObject.py`)

Uses multiple detection methods for robust object identification:

- **Difference Detection**: Compares current image with background
- **Edge Detection**: Uses Canny edge detection for dark objects
- **Adaptive Thresholding**: Handles local variations in lighting
- **Statistical Analysis**: Compares image properties (mean, std deviation)

**Key Parameters:**

- `CHANGE_THRESHOLD = 20`: Sensitivity for difference detection
- `MIN_OBJECT_AREA = 300`: Minimum area for valid object detection
- `EDGE_THRESHOLD = 50`: Threshold for edge-based detection

### 3. Burned State Classification (`getBurnedState.py`)

Classifies objects into four burned states based on RGB color analysis:

- **unBurned**: Light grayish colors `(R>125, G>125, B>120)`
- **underBurned**: Yellow/bright tones `(high R,G, low B)`
- **good**: Orange/brown tones `(R>G>B with specific ratios)`
- **overBurned**: Dark colors `(R<90, G<90, B<90)`

**RGB Reference Values** (from `rgbMap.json`):

```json
{
  "unBurned": [
    [254, 255, 254],
    [253, 255, 252],
    [254, 255, 254]
  ],
  "underBurned": [
    [254, 238, 86],
    [254, 236, 92],
    [255, 255, 97]
  ],
  "overBurned": [
    [26, 27, 26],
    [107, 103, 98],
    [60, 60, 59]
  ],
  "good": [
    [254, 148, 61],
    [255, 181, 80],
    [255, 136, 48]
  ]
}
```

### 4. Quality Assessment Workflow

```python
# Main processing loop (simplified)
while attempt <= max_attempts:
    processImagesAndSave()           # Capture and preprocess
    objectDetected = idObjectPresent()  # Detect object presence

    if objectDetected:
        areaAngleGood = isAreaAndAngleGood()     # Check geometry
        if areaAngleGood:
            goodBurnedState = check_burned_state()  # Check quality
            badFound = not goodBurnedState
        else:
            badFound = True
    else:
        badFound = False

    pickBadAndPlace(badFound)        # Handle based on quality
```

## 🎨 Burned State Examples

| State              | Description            | RGB Characteristics        |
| ------------------ | ---------------------- | -------------------------- |
| **Good** ✅        | Perfect cooking state  | Orange/brown tones (R>G>B) |
| **UnBurned** ⚪    | Undercooked, too light | Light grayish colors       |
| **UnderBurned** 🟡 | Slightly undercooked   | Yellow/bright tones        |
| **OverBurned** ⚫  | Overcooked, too dark   | Very dark colors           |

## ⚙️ Configuration

### Adjusting Detection Sensitivity

Edit `utils/checkObject.py`:

```python
CHANGE_THRESHOLD = 20    # Lower = more sensitive
MIN_OBJECT_AREA = 300    # Minimum pixels for detection
EDGE_THRESHOLD = 50      # Edge detection sensitivity
```

### Customizing Burned State Classification

Edit `utils/getBurnedState.py`:

```python
# Adjust color range thresholds
if r > 125 and g > 125 and b > 120:  # unBurned threshold
    predicted_state = "unBurned"
```

### Hardware Configuration

Edit `main.py`:

```python
serial_port = serial.Serial("/dev/ttyUSB0", 115200, timeout=1)  # Serial port
tryNO = 20  # Maximum attempts per session
```

## 🧪 Testing

### Test All Components

```bash
# Test object detection with different burned states
python3 -c "
import sys; sys.path.append('./utils')
from checkObject import idObjectPresent
print('Background:', idObjectPresent('images/no_object.png'))
print('Good:', idObjectPresent('images/burnedStates/good.png'))
print('Overburned:', idObjectPresent('images/burnedStates/overBurned.png'))
"
```

### Test Burned State Classification

```bash
# Test classification accuracy
uv run utils/getBurnedState.py
```

## 🔧 Troubleshooting

### Common Issues

1. **Camera not detected**

   - Check camera connection
   - Verify camera index in `captureImages.py` (default: 2)

2. **Serial port errors**

   - Ensure device is connected to `/dev/ttyUSB0`
   - Check permissions: `sudo chmod 666 /dev/ttyUSB0`

3. **Object detection too sensitive**

   - Increase `CHANGE_THRESHOLD` in `checkObject.py`
   - Increase `MIN_OBJECT_AREA` for larger objects only

4. **Burned state misclassification**
   - Check lighting conditions
   - Adjust color thresholds in `getBurnedState.py`
   - Verify RGB reference values in `rgbMap.json`

## 📊 Performance Metrics

The system provides detailed analysis output:

- Object detection confidence
- Color analysis scores for each burned state
- Geometric property measurements
- Processing time per image

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly with various object types
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- OpenCV community for computer vision tools
- Python scientific computing ecosystem
- Contributors to the image processing algorithms

---

For questions or support, please open an issue in the repository.
