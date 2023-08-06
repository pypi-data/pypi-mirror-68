import tensorflow as tf
from tensorflow.python.keras.engine import data_adapter


class UnsupervisedMixin(object):

    def __init__(self, *args, unsupervised=True, **kwargs):
        super().__init__(*args, **kwargs)
        self.unsupervised = unsupervised

    def _train_step_unsupervised(self, data):
        x, sample_weight, _ = data_adapter.unpack_x_y_sample_weight(data)
        with tf.GradientTape() as tape:
            out = self(x, training=True)
            loss = self.compiled_loss(out, out, sample_weight, regularization_losses=self.losses)

        trainable_variables = self.trainable_variables
        gradients = tape.gradient(loss, trainable_variables)
        self.optimizer.apply_gradients(zip(gradients, trainable_variables))

        self.compiled_metrics.update_state(out, out, sample_weight)
        return {m.name: m.result() for m in self.metrics}

    def _test_step_unsupervised(self, data):
        x, sample_weight, _ = data_adapter.unpack_x_y_sample_weight(data)
        out = self(x, training=False)
        # Updates stateful loss metrics.
        self.compiled_loss(out, sample_weight, regularization_losses=self.losses)

        self.compiled_metrics.update_state(out, sample_weight)
        return {m.name: m.result() for m in self.metrics}

    def train_step(self, data):
        if self.unsupervised:
            return self._train_step_unsupervised(data)
        else:
            return super(UnsupervisedMixin, self).train_step(data)

    def test_step(self, data):
        if self.unsupervised:
            return self._test_step_unsupervised(data)
        else:
            return super(UnsupervisedMixin, self).test_step(data)


