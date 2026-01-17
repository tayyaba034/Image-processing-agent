"""
Image Preprocessing Agent using Gemini API
Handles image resizing, preprocessing, and bounding box annotation
Uses OpenAI Agent SDK (Swarm) with Gemini API key (via OpenAI SDK compatibility)
"""

import os
import json
from pathlib import Path
from typing import List, Dict, Any, Tuple
import asyncio

# Image processing libraries
from PIL import Image, ImageDraw, ImageFont
import numpy as np

# OpenAI Agent SDK (Swarm)
from swarm import Swarm, Agent


class ImagePreprocessor:
    """Core image preprocessing functionality"""
    
    def __init__(self, target_size: Tuple[int, int] = (640, 640)):
        self.target_size = target_size
        
    def resize_image(self, image_path: str, output_path: str, maintain_aspect: bool = True) -> Dict[str, Any]:
        """
        Resize image to target size
        
        Args:
            image_path: Path to input image
            output_path: Path to save resized image
            maintain_aspect: Whether to maintain aspect ratio
            
        Returns:
            Dict with operation status and metadata
        """
        try:
            img = Image.open(image_path)
            original_size = img.size
            
            if maintain_aspect:
                img.thumbnail(self.target_size, Image.Resampling.LANCZOS)
                # Create a new image with padding
                new_img = Image.new('RGB', self.target_size, (0, 0, 0))
                paste_x = (self.target_size[0] - img.size[0]) // 2
                paste_y = (self.target_size[1] - img.size[1]) // 2
                new_img.paste(img, (paste_x, paste_y))
                img = new_img
            else:
                img = img.resize(self.target_size, Image.Resampling.LANCZOS)
            
            img.save(output_path)
            
            return {
                "status": "success",
                "original_size": original_size,
                "new_size": img.size,
                "output_path": output_path
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    def add_bounding_boxes(self, image_path: str, boxes: List[Dict], output_path: str) -> Dict[str, Any]:
        """
        Add bounding boxes to image
        
        Args:
            image_path: Path to input image
            boxes: List of bounding box dicts with format:
                   {'x': int, 'y': int, 'width': int, 'height': int, 'label': str, 'color': str}
            output_path: Path to save annotated image
            
        Returns:
            Dict with operation status
        """
        try:
            img = Image.open(image_path)
            draw = ImageDraw.Draw(img)
            
            # Try to load a font, fallback to default if not available
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
            except:
                font = ImageFont.load_default()
            
            for box in boxes:
                x, y = box['x'], box['y']
                w, h = box['width'], box['height']
                color = box.get('color', 'red')
                label = box.get('label', '')
                
                # Draw rectangle
                draw.rectangle([x, y, x + w, y + h], outline=color, width=3)
                
                # Draw label if provided
                if label:
                    # Draw label background
                    text_bbox = draw.textbbox((x, y - 20), label, font=font)
                    draw.rectangle(text_bbox, fill=color)
                    draw.text((x, y - 20), label, fill='white', font=font)
            
            img.save(output_path)
            
            return {
                "status": "success",
                "boxes_added": len(boxes),
                "output_path": output_path
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    def preprocess_dataset(self, input_dir: str, output_dir: str, 
                          annotations: Dict[str, List[Dict]] = None) -> Dict[str, Any]:
        """
        Preprocess entire dataset of images
        
        Args:
            input_dir: Directory containing input images
            output_dir: Directory to save processed images
            annotations: Optional dict mapping filenames to bounding box lists
            
        Returns:
            Dict with processing results
        """
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        results = {
            "processed": [],
            "failed": [],
            "total": 0
        }
        
        image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff'}
        
        for img_file in Path(input_dir).iterdir():
            if img_file.suffix.lower() in image_extensions:
                results["total"] += 1
                
                # First resize the image
                resized_path = Path(output_dir) / f"resized_{img_file.name}"
                resize_result = self.resize_image(str(img_file), str(resized_path))
                
                if resize_result["status"] == "error":
                    results["failed"].append({
                        "file": img_file.name,
                        "error": resize_result["error"]
                    })
                    continue
                
                # Add bounding boxes if annotations provided
                final_path = Path(output_dir) / img_file.name
                if annotations and img_file.name in annotations:
                    bbox_result = self.add_bounding_boxes(
                        str(resized_path),
                        annotations[img_file.name],
                        str(final_path)
                    )
                    os.remove(resized_path)  # Remove intermediate file
                    
                    if bbox_result["status"] == "error":
                        results["failed"].append({
                            "file": img_file.name,
                            "error": bbox_result["error"]
                        })
                        continue
                else:
                    # Just rename the resized image
                    resized_path.rename(final_path)
                
                results["processed"].append({
                    "file": img_file.name,
                    "output": str(final_path)
                })
        
        return results


# Agent Functions (Tools)
def resize_single_image(image_path: str, output_path: str, 
                       width: int = 640, height: int = 640,
                       maintain_aspect: bool = True) -> str:
    """Resize a single image to specified dimensions"""
    preprocessor = ImagePreprocessor(target_size=(width, height))
    result = preprocessor.resize_image(image_path, output_path, maintain_aspect)
    return json.dumps(result, indent=2)


def add_bounding_boxes_to_image(image_path: str, output_path: str, 
                                boxes_json: str) -> str:
    """
    Add bounding boxes to an image
    
    Args:
        image_path: Path to input image
        output_path: Path to save annotated image
        boxes_json: JSON string of bounding boxes list
    """
    preprocessor = ImagePreprocessor()
    boxes = json.loads(boxes_json)
    result = preprocessor.add_bounding_boxes(image_path, boxes, output_path)
    return json.dumps(result, indent=2)


def process_image_dataset(input_directory: str, output_directory: str,
                         annotations_json: str = None,
                         target_width: int = 640, target_height: int = 640) -> str:
    """
    Process an entire dataset of images with resizing and optional bounding boxes
    
    Args:
        input_directory: Directory containing input images
        output_directory: Directory to save processed images
        annotations_json: Optional JSON string mapping filenames to bounding boxes
        target_width: Target width for resized images
        target_height: Target height for resized images
    """
    preprocessor = ImagePreprocessor(target_size=(target_width, target_height))
    
    annotations = None
    if annotations_json:
        annotations = json.loads(annotations_json)
    
    result = preprocessor.preprocess_dataset(input_directory, output_directory, annotations)
    return json.dumps(result, indent=2)


def create_sample_annotations(num_boxes: int = 3, image_width: int = 640, 
                             image_height: int = 640) -> str:
    """Create sample bounding box annotations for testing"""
    boxes = []
    labels = ['object', 'target', 'item', 'entity', 'element']
    colors = ['red', 'blue', 'green', 'yellow', 'purple']
    
    for i in range(num_boxes):
        box = {
            'x': np.random.randint(50, image_width - 150),
            'y': np.random.randint(50, image_height - 150),
            'width': np.random.randint(80, 150),
            'height': np.random.randint(80, 150),
            'label': labels[i % len(labels)],
            'color': colors[i % len(colors)]
        }
        boxes.append(box)
    
    return json.dumps(boxes, indent=2)


# Create the Image Preprocessing Agent
def create_preprocessing_agent():
    """Create and configure the image preprocessing agent for Gemini API"""
    
    agent = Agent(
        name="Image Preprocessing Agent - Gemini",
        model="gemini-2.0-flash-exp",  # Set Gemini model as default
        instructions="""You are an expert image preprocessing agent specialized in:
        
        1. Resizing images to standard dimensions (default 640x640)
        2. Adding bounding box annotations to images
        3. Batch processing entire image datasets
        
        When a user asks you to process images, you should:
        - Clarify the input/output paths if not provided
        - Ask about target dimensions if resizing
        - Request bounding box annotations if needed
        - Provide clear feedback on processing results
        
        Always use the appropriate tool functions to complete tasks:
        - resize_single_image: For single image resizing
        - add_bounding_boxes_to_image: For adding annotations
        - process_image_dataset: For batch processing
        - create_sample_annotations: For generating test annotations
        
        Be helpful, precise, and confirm successful operations.""",
        functions=[
            resize_single_image,
            add_bounding_boxes_to_image,
            process_image_dataset,
            create_sample_annotations
        ]
    )
    
    return agent


# Main execution
def main():
    """Main function to run the agent with Gemini API"""
    
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    # Get Gemini API key from environment
    gemini_api_key = os.getenv('GEMINI_API_KEY')
    
    if not gemini_api_key or gemini_api_key == 'your-gemini-api-key-here':
        print("\n❌ Error: GEMINI_API_KEY not set!")
        print("\nPlease set your Gemini API key in the .env file:")
        print("1. Get your API key from: https://aistudio.google.com/app/apikey")
        print("2. Edit .env file and set: GEMINI_API_KEY=your-actual-api-key")
        return
    
    # Configure OpenAI client to use Gemini API
    # Note: We're using OpenAI SDK but pointing it to Gemini's endpoint
    from openai import OpenAI
    
    # Initialize OpenAI client configured for Gemini
    openai_client = OpenAI(
        api_key=gemini_api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )
    
    # Initialize Swarm client with the configured OpenAI client
    client = Swarm(client=openai_client)
    
    # Create the preprocessing agent
    agent = create_preprocessing_agent()
    
    print("=" * 70)
    print("Image Preprocessing Agent - Gemini API Edition")
    print("=" * 70)
    print("\nAgent initialized and ready to process images!")
    print("Using Google Gemini API for processing (Free Tier)")
    print("\nAvailable capabilities:")
    print("  • Resize individual images")
    print("  • Add bounding boxes to images")
    print("  • Batch process entire datasets")
    print("  • Generate sample annotations")
    print("\nExample commands:")
    print("  - 'Resize the image at /path/to/image.jpg to 800x800'")
    print("  - 'Process all images in /dataset and add bounding boxes'")
    print("  - 'Create sample annotations for testing'")
    print("\n" + "=" * 70)
    
    # Interactive conversation loop
    messages = []
    
    while True:
        user_input = input("\nYou: ").strip()
        
        if user_input.lower() in ['quit', 'exit', 'bye']:
            print("\nAgent: Goodbye! Happy preprocessing!")
            break
        
        if not user_input:
            continue
        
        messages.append({"role": "user", "content": user_input})
        
        # Run the agent with Gemini model
        response = client.run(
            agent=agent,
            messages=messages,
            model_override="gemini-2.0-flash-exp"  # Specify Gemini model
        )
        
        # Get the agent's response
        agent_message = response.messages[-1]["content"]
        messages.append({"role": "assistant", "content": agent_message})
        
        print(f"\nAgent: {agent_message}")


if __name__ == "__main__":
    main()
