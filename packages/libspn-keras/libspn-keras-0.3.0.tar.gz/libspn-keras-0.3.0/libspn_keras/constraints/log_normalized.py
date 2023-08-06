from tensorflow.keras.constraints import Constraint
import tensorflow as tf


class LogNormalized(Constraint):

    """
    Constraints the weight to be normalized in log-space by computing the log-softmax operation along ``axis``.

    Args:
        axis (int): Axis along which to normalize weights.
    """

    def __init__(self, axis=-2):
        self.axis = axis

    def __call__(self, w):
        return tf.nn.log_softmax(w, axis=self.axis)

    def get_config(self):
        return dict(axis=self.axis)
