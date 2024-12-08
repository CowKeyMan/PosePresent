# type: ignore
import tensorflow_hub as hub
import tensorflow as tf
import numpy as np


class Model:
    def __init__(
        self,
        model_path: str,
        input_size: int,
        keypoint_names: list[str],
        threshold: float = 0.2,
    ):
        self.model: tf.Module = hub.load(model_path).signatures["serving_default"]
        self.input_size = input_size
        self.keypoint_names = keypoint_names
        self.threshold = threshold

    def forward(
        self, image: np.ndarray
    ) -> tf.Tensor:  # input has size: [height, width, 3]
        height, width, _ = image.shape
        image = tf.expand_dims(image, axis=0)
        image = tf.image.resize_with_pad(image, self.input_size, self.input_size)
        image = tf.cast(image, dtype=tf.int32)
        outputs = self.model(image)
        keypoints_with_scores = outputs["output_0"].numpy()
        result = {}
        for n, (y, x, score) in zip(
            self.keypoint_names, keypoints_with_scores.squeeze()
        ):
            if score > self.threshold:
                result[n] = (int(x * width), int(y * height))
        return result

    __call__ = forward
