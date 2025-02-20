import os
from PIL import Image
from concurrent.futures import ThreadPoolExecutor, as_completed

def process_image(file_path, output_folder, target_size_kb):
    """Resize and compress a single image."""
    try:
        img = Image.open(file_path)

        # Reduce dimensions by 10%
        width, height = img.size
        new_width = int(width * 0.9)
        new_height = int(height * 0.9)
        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)  # Use Resampling.LANCZOS

        # Save the resized image with compression
        file_name = os.path.basename(file_path)  # Keeps original name and extension
        output_path = os.path.join(output_folder, file_name)

        quality = 85  # Initial quality setting
        img.save(output_path, quality=quality, optimize=True)
        
        # Dynamically adjust quality to meet the target size
        while os.path.getsize(output_path) > target_size_kb * 1024:
            quality -= 5
            img.save(output_path, quality=quality, optimize=True)
            if quality <= 10:  # Stop if quality is too low
                break

        print(f"Processed: {file_name} -> {os.path.getsize(output_path) / 1024:.2f} KB")
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

def resize_images_parallel(folder_path, target_size_kb, output_folder, max_workers=8):
    """
    Resize and compress images in parallel to a target size.
    
    Args:
        folder_path (str): Path to the folder containing images.
        target_size_kb (int): Target file size in kilobytes.
        output_folder (str): Path to save resized images.
        max_workers (int): Number of parallel threads.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # List all image files in the folder
    image_files = [
        os.path.join(folder_path, f)
        for f in os.listdir(folder_path)
        if f.lower().endswith(('png', 'jpg', 'jpeg'))
    ]

    # Process images using a thread pool
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(process_image, file_path, output_folder, target_size_kb): file_path
            for file_path in image_files
        }

        for future in as_completed(futures):
            file_path = futures[future]
            try:
                future.result()  # Wait for the thread to finish
            except Exception as e:
                print(f"Failed to process {file_path}: {e}")

# Example usage
folder_path = "./athlete_photos"  # Relative path to your folder
output_folder = "./resized_photos"  # Output folder on the same level as the script
target_size_kb = 100  # Target size in KB
max_workers = 8  # Adjust based on your system's capabilities

resize_images_parallel(folder_path, target_size_kb, output_folder, max_workers)
