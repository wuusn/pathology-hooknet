import numpy as np

def clean_weights(masks):
    return np.clip(np.sum(masks, axis=-1), 0, 1)

class HookNetReshape():
    def __init__(self, multi_loss=False):
        self._multi_loss = multi_loss

    def __call__(self, x: np.ndarray, y: np.ndarray, sample_weight=None):
        x_list_batch = [[], []]
        y_list_batch = [[], []]

        for batch_sample in x:
            batch_sample = dict(sorted(batch_sample.items()))
            for idx, (key, value) in enumerate(batch_sample.items()):
                x_list_batch[idx].append(value)

        for batch_sample in y:
            batch_sample = dict(sorted(batch_sample.items()))
            for idx, (key, value) in enumerate(batch_sample.items()):
                y_list_batch[idx].append(value)

        x_list_batch[0] = np.array(x_list_batch[0])
        x_list_batch[1] = np.array(x_list_batch[1])
        y_list_batch[0] = np.array(y_list_batch[0])
        y_list_batch[1] = np.array(y_list_batch[1])
        if self._multi_loss:
            return (
                x_list_batch,
                y_list_batch,
                [clean_weights(y_list_batch[0]), clean_weights(y_list_batch[1])],
            )

        return {'x': x_list_batch, 'y': y_list_batch[0], 'sample_weight': clean_weights(y_list_batch[0])}