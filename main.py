from PIL import Image
import os


def is_transparent(pixel):
    return len(pixel) == 4 and pixel[3] == 0


def all_transparent_row(image, y):
    for x in range(image.width):
        if not is_transparent(image.getpixel((x, y))):
            return False
    return True


def all_transparent_column(image, x):
    for y in range(image.height):
        if not is_transparent(image.getpixel((x, y))):
            return False
    return True


def crop_image(image):
    topmost = 0
    for y in range(image.height):
        if not all_transparent_row(image, y):
            topmost = y
            break

    bottommost = image.height - 1
    for y in range(image.height - 1, -1, -1):
        if not all_transparent_row(image, y):
            bottommost = y
            break

    leftmost = 0
    for x in range(image.width):
        if not all_transparent_column(image, x):
            leftmost = x
            break

    rightmost = image.width - 1
    for x in range(image.width - 1, -1, -1):
        if not all_transparent_column(image, x):
            rightmost = x
            break

    if topmost > bottommost or leftmost > rightmost:
        return image

    cropped_image = image.crop((leftmost, topmost, rightmost + 1, bottommost + 1))
    return cropped_image


def process_images_in_directory(source_directory, target_directory):
    if not os.path.exists(source_directory):
        print(f"The provided source directory does not exist: {source_directory}")
        return

    os.makedirs(target_directory, exist_ok=True)

    names = [file for file in os.listdir(source_directory) if file.endswith('.png')]

    for name in names:
        file_path = os.path.join(source_directory, name)
        try:
            with Image.open(file_path) as img:
                if img.mode != 'RGBA':
                    img = img.convert('RGBA')

                cropped_img = crop_image(img)
                save_path = os.path.join(target_directory, name)
                cropped_img.save(save_path)
                print(f"Cropped image saved to {save_path}")
        except Exception as ex:
            print(f"Error processing file {file_path}: {ex}")


if __name__ == "__main__":
    source_directory = input("Please enter the source directory path: ")
    target_directory = fr'{source_directory}/output'
    process_images_in_directory(source_directory, target_directory)
