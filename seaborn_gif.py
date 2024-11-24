import imageio
import os

def main():
    """
    This creates a gif of all images in the 'sns' folder, comparing the current frame against the heatmap of color change magnitude vs the previous frame.

    This is just for visualization purposes
    """
    images = []
    for file in os.listdir('./sns'):
        if file.endswith('.png'):
            images.append(file)

    images.sort(key=lambda x: os.path.getmtime('./sns/' + x))

    with imageio.get_writer('./sns.gif', mode='I', loop=0, duration=0.2) as writer:
        for filename in images:
            image = imageio.imread('./sns/' + filename)
            writer.append_data(image)

    print('gif created')

if __name__ == "__main__":
    main()