import matplotlib.pyplot as plt


def show_result(image_path, result):

    image = plt.imread(image_path)

    plt.imshow(image)

    plt.title(
        f"Identificado como: {result['identity']}"
    )

    plt.axis("off")

    plt.show()