import numpy as np

def dist(x, y, norm=2):
    # x: N x D
    # y: M x D
    n = x.shape[0]
    m = y.shape[0]
    d = x.shape[1]
    assert d == y.shape[1]

    x = np.expand_dims(x, axis=1)  # (n,d)->(n,1,d)
    y = np.expand_dims(y, axis=0)  # (m,d)->(1,m,d)
    # x = np.repeat(x, m, axis=1)   # (n,1,d)->(n,m,d)
    # y = np.repeat(y, n, axis=0)   # (1,m,d)->(n,m,d)
    temp = x - y                    # broadcast to (n,m,d)
    if norm == 2:
        return np.power(temp, norm).sum(-1)  # (n,m,d)->(n,m)
    elif norm == 1:
        return np.abs(temp).sum(-1)
    else:
        raise ValueError(f"Arg '{norm}' only supporting L2 & L1 norm temporarily, either 1 or 2.")

# One-Hot 
def one_hot(y, nb_classes=None):
    """Converts a class vector (integers) to binary class matrix.
    E.g. for use with categorical_crossentropy.
    # Arguments
        y: 数字标签(integers from 0 to nb_classes).
        nb_classes: 类别总数. 
    # Returns
        A binary matrix representation of the input.
    """
    y = np.array(y, dtype='int').ravel()
    if not nb_classes:
        nb_classes = np.max(y) + 1
    n = y.shape[0]
    categorical = np.zeros((n, nb_classes))
    categorical[np.arange(n), y] = 1
    return categorical


# convert probability to classes
def probas_to_classes(y_pred):
    if len(y_pred.shape) > 1 and y_pred.shape[1] > 1: # 2阶以上，第二阶维度大于1
        return np.argmax(y_pred, axis=1)
    return np.array([1 if p > 0.5 else 0 for p in y_pred])


