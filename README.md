# Image Preprocessing Agent - OpenAI Agent SDK + Multi-API Support

A professional agentic AI system built with OpenAI's Agent SDK (Swarm) supporting both OpenAI and Google's Gemini APIs for automated image dataset preprocessing, including resizing and bounding box annotation.

## 🎯 Features

- **Image Resizing**: Resize images to target dimensions with aspect ratio preservation
- **Bounding Box Annotation**: Add labeled bounding boxes to images for object detection tasks
- **Batch Processing**: Process entire datasets efficiently
- **Conversational Interface**: Natural language interaction for complex workflows
- **Flexible Configuration**: Customizable dimensions, colors, and labels
- **Dual API Support**: Works with OpenAI API or Google Gemini API (free)

## 🏗️ Architecture

The agent is built using:
- **OpenAI Swarm**: Agent orchestration framework
- **OpenAI SDK**: Primary client library (works with both OpenAI and Gemini APIs)
- **Google Gemini API**: Alternative AI model backend (free tier available)
- **OpenAI API**: Primary AI model backend (with OpenAI account)
- **Pillow (PIL)**: Image processing
- **NumPy**: Numerical operations
- **Python 3.11+**: Core runtime

### Agent Capabilities

1. **Single Image Operations**
   - Resize individual images
   - Add bounding boxes to specific images
   - Maintain aspect ratios with padding

2. **Dataset Operations**
   - Batch resize entire image folders
   - Apply annotations from JSON configurations
   - Generate processing reports

3. **Utility Functions**
   - Create sample annotations for testing
   - Validate image formats
   - Error handling and reporting

## 📦 Installation

### Prerequisites
- Python 3.11 or higher
- uv package manager (recommended) or pip
- Either:
  - **OpenAI API Key** (paid, from https://platform.openai.com/api-keys), OR
  - **Google Gemini API Key** (free, from https://aistudio.google.com/app/apikey)

### Setup Steps

1. **Clone or download the repository**
```bash
# Navigate to project directory
cd image-preprocessing-agent
```

2. **Install dependencies using uv (recommended)**
```bash
# Install uv if you don't have it
pip install uv

# Install project dependencies
uv pip install -e .
```

Or using pip:
```bash
pip install -e .
```

3. **Choose Your API Provider**

#### Option A: Using OpenAI API (Recommended for Production)

1. **Get your OpenAI API Key**
   - Visit [OpenAI API Keys](https://platform.openai.com/api-keys)
   - Sign up or log in to your OpenAI account
   - Create a new API key
   - Copy your API key

2. **Configure the API Key**
   - Edit the `.env` file and add:
   ```
   OPENAI_API_KEY=sk-...your-actual-openai-api-key
   ```

#### Option B: Using Google Gemini API (Free Alternative)

1. **Get your Gemini API Key**
   - Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
   - Sign in with your Google account
   - Click "Create API Key"
   - Copy your API key

2. **Configure the API Key**
   - Edit the `.env` file and add:
   ```
   GEMINI_API_KEY=your-actual-gemini-api-key
   ```

> **Note:** This project intelligently detects which API key is available and uses the appropriate service. If both are set, OpenAI takes precedence.

## 🚀 Usage

### Method 1: Interactive Agent (Auto-Detection)

Run the interactive agent - it will automatically detect which API key you have configured:

```bash
python image_preprocessing_agent.py
```

The system will:
- Check for OpenAI API key first
- Fall back to Gemini API if OpenAI is not available
- Display which service is being used

### Method 2: Using OpenAI API Directly

For explicit OpenAI API usage:

```bash
python image_preprocessing_openai.py
```

### Method 3: Using Gemini API Directly

For explicit Gemini API usage:

```bash
python image_preprocessing_gemini.py
```

### Example Interactions

Once the agent is running, you can use natural language commands:

```
You: Resize all images in ./raw_data to 640x640 and save to ./processed

Agent: I'll process the images in ./raw_data directory...
[Processing completed]

You: Add bounding boxes to the processed images with these coordinates...

Agent: I'll add the bounding boxes now...
```

## 📋 Configuration

### Environment Variables

Create a `.env` file in the project root:

```bash
# Choose ONE of the following:

# Option 1: OpenAI API (recommended for production)
OPENAI_API_KEY=sk-...your-key

# Option 2: Gemini API (recommended for free tier)
GEMINI_API_KEY=AIzaSy...your-key

# Optional: Customize image processing defaults
DEFAULT_WIDTH=640
DEFAULT_HEIGHT=640
BATCH_SIZE=100
MAX_WORKERS=4
LOG_LEVEL=INFO
```

### Configuration File

Edit `config.py` to customize:
- Default image dimensions
- Supported image formats
- Bounding box colors and styles
- Batch processing settings
- Font and display options
- Validation rules

## 🔄 API Comparison

| Feature | OpenAI API | Gemini API |
|---------|-----------|-----------|
| Cost | Paid | Free (with limits) |
| Setup | Requires credit card | Google account only |
| Rate Limits | Varies by plan | 15 req/min free tier |
| Model Used | GPT-4, GPT-3.5 | Gemini 1.5 Flash/Pro |
| SDK Support | Native OpenAI SDK | OpenAI SDK compatible |
| Recommended For | Production use | Testing/Development |

### Free Tier Limits (Gemini)

- 15 requests per minute
- 1 million tokens per minute
- 1,500 requests per day

Perfect for image preprocessing tasks and development!

## 🧪 Testing

Run the configuration test to verify your API setup:

```bash
python test_gemini_config.py
```

This will verify:
- Environment variables are set correctly
- OpenAI client can be configured
- Swarm agent can be initialized

## 📁 Project Structure

```
image-preprocessing-agent/
├── image_preprocessing_agent.py      # Main entry point (auto-detects API)
├── image_preprocessing_openai.py     # OpenAI API specific implementation
├── image_preprocessing_gemini.py     # Gemini API specific implementation
├── config.py                         # Configuration and constants
├── test_gemini_config.py             # Configuration test script
├── pyproject.toml                    # Project dependencies
├── .env                              # Environment variables (not in git)
├── README.md                         # This file
├── processed/                        # Output directory for processed images
├── logs/                             # Application logs
└── processed_dataset/                # Alternative output directory
```

## 🛠️ API Selection Logic

The system uses this priority:

1. **Check for OpenAI API Key** → Use OpenAI if available
2. **Check for Gemini API Key** → Use Gemini if available
3. **Error** → Exit with helpful message

You can override this by running specific files:
- `image_preprocessing_openai.py` - Forces OpenAI
- `image_preprocessing_gemini.py` - Forces Gemini
- `image_preprocessing_agent.py` - Auto-detect (recommended)

## 📝 Bounding Box Format

Bounding boxes use the following JSON format:

```json
[
    {
        "x": 100,           // Top-left x coordinate
        "y": 150,           // Top-left y coordinate
        "width": 200,       // Box width
        "height": 180,      // Box height
        "label": "Car",     // Object label (optional)
        "color": "red"      // Box color (optional, default: red)
    }
]
```

Supported colors: `red`, `blue`, `green`, `yellow`, `purple`, `orange`, `cyan`, `magenta`, or any PIL-compatible color string.

## 🔧 Available Agent Functions

### `resize_single_image()`
```python
resize_single_image(
    image_path: str,
    output_path: str,
    width: int = 640,
    height: int = 640,
    maintain_aspect: bool = True
)
```

### `add_bounding_boxes_to_image()`
```python
add_bounding_boxes_to_image(
    image_path: str,
    output_path: str,
    boxes_json: str  # JSON string of bounding boxes
)
```

### `process_image_dataset()`
```python
process_image_dataset(
    input_directory: str,
    output_directory: str,
    annotations_json: str = None,
    target_width: int = 640,
    target_height: int = 640
)
```

### `create_sample_annotations()`
```python
create_sample_annotations(
    num_boxes: int = 3,
    image_width: int = 640,
    image_height: int = 640
)
```

## 📊 Example Workflows

### Workflow 1: Object Detection Dataset Preparation

```python
# 1. Create annotations
annotations = {
    "street1.jpg": [
        {"x": 100, "y": 200, "width": 150, "height": 200, "label": "Car", "color": "red"},
        {"x": 300, "y": 150, "width": 80, "height": 180, "label": "Person", "color": "blue"}
    ],
    "street2.jpg": [
        {"x": 50, "y": 100, "width": 120, "height": 150, "label": "Bicycle", "color": "green"}
    ]
}

# 2. Process dataset
preprocessor = ImagePreprocessor(target_size=(640, 640))
result = preprocessor.preprocess_dataset(
    input_dir='./raw_images',
    output_dir='./training_data',
    annotations=annotations
)

print(f"Processed: {len(result['processed'])} images")
print(f"Failed: {len(result['failed'])} images")
```

### Workflow 2: Conversational Dataset Processing

```python
client = Swarm()
agent = create_preprocessing_agent()

conversation = [
    {"role": "user", "content": "I have 1000 images in ./dataset that need to be resized to 512x512"},
    # Agent processes...
    {"role": "user", "content": "Now add bounding boxes for detected objects using this JSON file: annotations.json"},
    # Agent processes...
    {"role": "user", "content": "Great! Can you create a summary report?"}
]
```

## 🛠️ Advanced Configuration

### Custom Image Sizes

```python
# Square images
preprocessor = ImagePreprocessor(target_size=(1024, 1024))

# Rectangular images
preprocessor = ImagePreprocessor(target_size=(1920, 1080))
```

### Batch Processing with Progress

```python
import os
from tqdm import tqdm

input_dir = './raw_data'
output_dir = './processed'
os.makedirs(output_dir, exist_ok=True)

preprocessor = ImagePreprocessor()

image_files = [f for f in os.listdir(input_dir) if f.endswith(('.jpg', '.png'))]

for img_file in tqdm(image_files, desc="Processing images"):
    input_path = os.path.join(input_dir, img_file)
    output_path = os.path.join(output_dir, img_file)
    preprocessor.resize_image(input_path, output_path)
```

## 🐛 Troubleshooting

### "API Key not set"
- Make sure you edited the `.env` file
- Ensure there are no spaces around the `=` sign
- Don't use quotes around the API key
- Restart the application after adding the key

### "Invalid API key"
- Verify your API key is correct (copy from the provider again)
- Check if the API key is enabled in your provider's dashboard
- Make sure you haven't reached rate limits

### "Authentication failed"
- **For OpenAI**: Verify you have credit or trial credits available
- **For Gemini**: Check that the API is enabled in Google Cloud

### Connection Issues
- Check your internet connection
- Verify you can reach the API endpoints
- Check your firewall/proxy settings

### Common Issues

1. **"Module 'swarm' not found"**
   ```bash
   uv pip install git+https://github.com/openai/swarm.git
   ```

2. **"No module named pip" in virtual environment**
   ```bash
   uv pip install pip
   ```

3. **Font errors on Linux**
   ```bash
   sudo apt-get install fonts-dejavu-core
   ```

4. **Memory issues with large datasets**
   - Process in smaller batches
   - Use lower resolution target sizes
   - Close images after processing

## 📈 Performance Tips

- **Batch Size**: Process 100-500 images per batch for optimal memory usage
- **Image Format**: Use JPEG for faster processing, PNG for lossless quality
- **Parallel Processing**: For large datasets, consider using multiprocessing
- **Aspect Ratio**: Set `maintain_aspect=True` to prevent distortion

## 🤝 Contributing

Contributions are welcome! Areas for enhancement:
- Support for additional annotation formats (COCO, YOLO, Pascal VOC)
- Image augmentation features
- GPU acceleration for batch processing
- Web UI for annotation

## 📄 License

MIT License - feel free to use this in your projects!

## 🔗 Resources

- [OpenAI Swarm Documentation](https://github.com/openai/swarm)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Google Gemini API Documentation](https://ai.google.dev/docs)
- [Pillow Documentation](https://pillow.readthedocs.io/)
- [Computer Vision Best Practices](https://docs.opencv.org/)

---


