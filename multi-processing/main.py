import os
import cv2
import multiprocessing


def read_images(directory):
    images = []
    for filename in os.listdir(directory):
        if filename.endswith((".jpg", ".jpeg", ".png")):
            image_path = os.path.join(directory, filename)
            images.append(image_path)
    return images


def process_image(image_path, output_dir):
    image = cv2.imread(image_path)

    resized_image = cv2.resize(image, (0, 0), fx=0.5, fy=0.5)

    grayscale_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)

    output_path = os.path.join(output_dir, os.path.basename(image_path))
    cv2.imwrite(output_path, grayscale_image)
    print(f"Processed: {image_path}")


def parallel_process_images(images, output_dir):
    num_processes = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(processes=num_processes)
    for image_path in images:
        pool.apply_async(process_image, args=(image_path, output_dir))
    pool.close()
    pool.join()


def main():
    input_dir = "input_images"
    output_dir = "output_images"
    os.makedirs(output_dir, exist_ok=True)

    images = read_images(input_dir)
    parallel_process_images(images, output_dir)


if __name__ == "__main__":
    main()
