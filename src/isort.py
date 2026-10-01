import sys
import time
from pathlib import Path

import keras_tuner as kt
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from src.utils import logger as log
from tensorflow.keras.layers import BatchNormalization, Dense, Input
from tensorflow.keras.models import Sequential
from tensorflow.keras.regularizers import l1, l1_l2, l2

print("hello world")
