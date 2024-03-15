from PIL import Image, ImageDraw

def create_circular_image(image_path, output_path):
    # Open the image
    img = Image.open(image_path)
    
    # Create a circular mask
    mask = Image.new("L", img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, img.size[0], img.size[1]), fill=255)
    
    # Apply the circular mask
    circular_image = Image.new("RGB", img.size, (255, 255, 255))
    circular_image.paste(img, mask=mask)
    
    # Save the result
    circular_image.save(output_path)

# Example usage
input_image_path = "static\Garlic - Copy.jpg"
output_image_path = input_image_path
create_circular_image(input_image_path, output_image_path)
