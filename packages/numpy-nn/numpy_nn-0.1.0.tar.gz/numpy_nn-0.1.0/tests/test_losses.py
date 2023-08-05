from numpy_nn.losses import MAE, MSE
import numpy as np

def test_mae_basic1():
    y_pred = np.array([[1,2],[3,4]])
    y = np.array([[2,3],[4,5]])
    mae = MAE()
    true_list = (mae(y_pred, y) == np.array([1,1]))
    assert list(true_list) == [True, True]

def test_mse_basic1():
    y_pred = np.array([1,2,3,4,5])
    y = np.array([2,3,4,5,6])
    mse = MSE()
    assert mse(y_pred,y) == 1