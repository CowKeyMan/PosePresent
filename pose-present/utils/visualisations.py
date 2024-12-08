import cv2
import numpy as np


def show_full_pose(
    personwise_keypoints: list[dict[str, tuple[int, int]]],
    image: np.ndarray,
    part_pairs: list[tuple[str, str]],
    window_name: str,
    part_to_colour: dict[str, tuple[int, int, int]],
    pose_colours: np.ndarray,
    resize_dimensions=None
) -> None:
    for i, pk in enumerate(personwise_keypoints):
        for part, position in pk.items():
            if position != -1:
                cv2.circle(
                    image, position, 5, part_to_colour[part], -1, cv2.LINE_AA
                )
        for part_1, part_2 in part_pairs:
            if part_1 in pk and part_2 in pk:
                cv2.line(
                    image,
                    pk[part_1],
                    pk[part_2],
                    pose_colours[i % len(pose_colours)],
                    3
                )
    if resize_dimensions is not None:
        image = cv2.resize(image, resize_dimensions)
    cv2.imshow(window_name, image)


def show_keypoints(
    personwise_keypoints: list[dict[str, tuple[int, int]]],
    image: np.ndarray,
    window_name: str,
    part_to_colour: dict[str, tuple[int, int, int]],
    resize_dimensions=None,
) -> None:
    for i, pk in enumerate(personwise_keypoints):
        for part, position in pk.items():
            colour = part_to_colour[part]
            cv2.circle(image, position, 5, colour, -1, cv2.LINE_AA)
            cv2.putText(
                image,
                part,
                position,
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                colour,
                1
            )
    if resize_dimensions is not None:
        image = cv2.resize(image, resize_dimensions)
    cv2.imshow(window_name, image)


def show_heatmap(
    image: np.ndarray,
    nn_output: np.ndarray,
    part_to_index: dict[str, int],
    window_name: str,
    part='Nose',
) -> None:
    heatmap = nn_output[0, part_to_index[part], :, :]
    heatmap = np.uint8(cv2.resize(heatmap, image.shape[:2][::-1]) * 255)
    heatmap_confidence = heatmap
    heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)  # pyright: ignore
    heatmap[heatmap_confidence < (0.1 * 255)] = 0
    image = cv2.addWeighted(image, 0.6, heatmap, 0.3, 0)
    cv2.imshow(window_name, image)
