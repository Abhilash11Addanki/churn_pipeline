import tensorflow as tf
import tensorflow_model_analysis as tfma
import tensorflow_transform as tft
from tensorflow_transform.tf_metadata import schema_utils

NUMERIC_FEATURE_KEYS = [
    'tenure','active_member','balance','products_number',
    'age','estimated_salary','customer_id','credit_score',
    'credit_card'
]

CATEGORICAL_FEATURE_KEYS = ['country', 'gender']

def transformed_name(key):
  return key + '_xf'