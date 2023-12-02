import os
import cv2
import random
import time

from tqdm import tqdm
def load_images_from_folder(folder_path):
    images = []
    with tqdm(total=len(os.listdir(folder_path))) as pbar:
        for filename in os.listdir(folder_path):
            if filename.endswith(('.png', '.jpg', '.jpeg')):
                img_path = os.path.join(folder_path, filename)
                img = cv2.imread(img_path)
                if img is not None:
                    images.append(img)
                    pbar.update(1)
    return images

def load_images_from_folders(parent_folder):
    folders = [folder for folder in os.listdir(parent_folder) if os.path.isdir(os.path.join(parent_folder, folder))]
    folder_images = {folder: load_images_from_folder(os.path.join(parent_folder, folder)) for folder in folders}
    return folder_images

def pad_image(img, target_height):
    height, width = img.shape[:2]
    pad_top = (target_height - height) // 2
    pad_bottom = target_height - height - pad_top
    return cv2.copyMakeBorder(img, pad_top, pad_bottom, 0, 0, cv2.BORDER_CONSTANT, value=[0, 0, 0])

def main(parent_folder, num_frames):
    folder_images = load_images_from_folders(parent_folder)
    print(type(folder_images))
    print(folder_images.keys())
    selected_folders = folder_images.keys()[:2]
    if not folder_images:
        print("No valid folders found.")
        return

    while True:
        for i in range(num_frames):
            # Choose a random folder
            random_folder = random.choice(list(folder_images.keys()))

            # Select a random image from the chosen folder
            images = folder_images[random_folder]
            if images:
                img = random.choice(images)

                # Pad the image to match the maximum height
                max_height = max(img.shape[0] for images in folder_images.values() for img in images)
                padded_img = pad_image(img, max_height)

                cv2.imshow('Random Images', padded_img)
                cv2.waitKey(100)  # Adjust the delay (in milliseconds) based on your preference
            break

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()




if __name__ == "__main__":
    parent_folder = "./frames"
    num_frames = 5  # You can adjust the number of frames as needed
    main(parent_folder, num_frames)
