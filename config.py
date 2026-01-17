"""
Configuration file for Image Preprocessing Agent
"""

import os
from dataclasses import dataclass
from typing import Tuple


@dataclass
class PreprocessingConfig:
    """Configuration for image preprocessing"""
    
    # Default image dimensions
    DEFAULT_WIDTH: int = 640
    DEFAULT_HEIGHT: int = 640
    
    # Supported image formats
    SUPPORTED_FORMATS: Tuple[str, ...] = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp')
    
    # Bounding box defaults
    DEFAULT_BOX_COLOR: str = 'red'
    DEFAULT_BOX_WIDTH: int = 3
    
    # Available colors for bounding boxes
    AVAILABLE_COLORS: Tuple[str, ...] = (
        'red', 'blue', 'green', 'yellow', 'purple', 
        'orange', 'cyan', 'magenta', 'white', 'black'
    )
    
    # Processing settings
    MAINTAIN_ASPECT_RATIO: bool = True
    JPEG_QUALITY: int = 95
    PNG_COMPRESSION: int = 6
    
    # Batch processing
    BATCH_SIZE: int = 100
    MAX_WORKERS: int = 4
    
    # Paths
    DEFAULT_INPUT_DIR: str = './raw_data'
    DEFAULT_OUTPUT_DIR: str = './processed'
    
    # Font settings
    FONT_SIZE: int = 16
    FONT_PATH: str = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
    
    # Validation
    MIN_IMAGE_SIZE: Tuple[int, int] = (10, 10)
    MAX_IMAGE_SIZE: Tuple[int, int] = (10000, 10000)
    
    # Agent settings
    AGENT_NAME: str = "Image Preprocessing Agent"
    AGENT_VERSION: str = "1.0.0"
    
    # Logging
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FORMAT: str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    @classmethod
    def from_env(cls):
        """Create config from environment variables"""
        return cls(
            DEFAULT_WIDTH=int(os.getenv('DEFAULT_WIDTH', 640)),
            DEFAULT_HEIGHT=int(os.getenv('DEFAULT_HEIGHT', 640)),
            BATCH_SIZE=int(os.getenv('BATCH_SIZE', 100)),
            MAX_WORKERS=int(os.getenv('MAX_WORKERS', 4)),
        )
    
    def to_dict(self):
        """Convert config to dictionary"""
        return {
            'default_width': self.DEFAULT_WIDTH,
            'default_height': self.DEFAULT_HEIGHT,
            'supported_formats': self.SUPPORTED_FORMATS,
            'default_box_color': self.DEFAULT_BOX_COLOR,
            'maintain_aspect_ratio': self.MAINTAIN_ASPECT_RATIO,
            'batch_size': self.BATCH_SIZE,
            'agent_name': self.AGENT_NAME,
            'agent_version': self.AGENT_VERSION
        }


# Create global config instance
config = PreprocessingConfig()


# Annotation format schemas
COCO_ANNOTATION_SCHEMA = {
    "type": "object",
    "properties": {
        "images": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "file_name": {"type": "string"},
                    "width": {"type": "integer"},
                    "height": {"type": "integer"}
                },
                "required": ["id", "file_name"]
            }
        },
        "annotations": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "image_id": {"type": "integer"},
                    "bbox": {
                        "type": "array",
                        "items": {"type": "number"},
                        "minItems": 4,
                        "maxItems": 4
                    },
                    "category_id": {"type": "integer"}
                },
                "required": ["id", "image_id", "bbox", "category_id"]
            }
        },
        "categories": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "name": {"type": "string"}
                },
                "required": ["id", "name"]
            }
        }
    },
    "required": ["images", "annotations", "categories"]
}


BBOX_ANNOTATION_SCHEMA = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "x": {"type": "integer"},
            "y": {"type": "integer"},
            "width": {"type": "integer"},
            "height": {"type": "integer"},
            "label": {"type": "string"},
            "color": {"type": "string"}
        },
        "required": ["x", "y", "width", "height"]
    }
}
