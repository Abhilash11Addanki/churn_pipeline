import functools
import absl
import os
from typing import List, Text

import kerastuner
import tensorflow as tf
import tensorflow_model_analysis as tfma
import tensorflow_transform as tft
from tensorflow_transform.tf_metadata import schema_utils

from tfx.components.trainer.executor import TrainerFnArgs
from tfx.components.trainer.fn_args_utils import DataAccessor
from tfx.components.tuner.component import TunerFnResult
from tfx_bsl.tfxio import dataset_options

import features

numeric_columns = ['tenure', 'active_member', 'balance', 'products_number', 'age', 'estimated_salary', 'customer_id', 'credit_score', 'credit_card']

EPOCHS = 1
TRAIN_BATCH_SIZE = 64
EVAL_BATCH_SIZE = 64


def _gzip_reader_fn(filenames):
    return tf.data.TFRecordDataset(filenames, compression_type='GZIP')


def _get_serve_tf_examples_fn(model, tf_transform_output):
    
    model.tft_layer = tf_transform_output.transform_features_layer()

    @tf.function
    def serve_tf_examples_fn(serialized_tf_examples):
        """Returns the output to be used in the serving signature."""
        feature_spec = tf_transform_output.raw_feature_spec()
        feature_spec.pop('churn')
        parsed_features = tf.io.parse_example(serialized_tf_examples, feature_spec)

        transformed_features = model.tft_layer(parsed_features)

        return model(transformed_features)

    return serve_tf_examples_fn


def _input_fn(file_pattern: List[Text],
              data_accessor: DataAccessor,
              tf_transform_output: tft.TFTransformOutput,
              batch_size: int = 200) -> tf.data.Dataset:
    
    dataset = data_accessor.tf_dataset_factory(
        file_pattern,
        dataset_options.TensorFlowDatasetOptions(
            batch_size=batch_size, label_key=features.transformed_name('churn')),
        tf_transform_output.transformed_metadata.schema)
    
    return dataset


def _get_hyperparameters() -> kerastuner.HyperParameters:
    hp = kerastuner.HyperParameters()
    # Defines search space.
    hp.Choice('learning_rate', [1e-2, 1e-3, 1e-4], default=1e-3)
    hp.Int('n_layers', 1, 2, default=1)
    with hp.conditional_scope('n_layers', 1):
        hp.Int('n_units_1', min_value=8, max_value=128, step=8, default=8)
    with hp.conditional_scope('n_layers', 2):
        hp.Int('n_units_1', min_value=8, max_value=128, step=8, default=8)
        hp.Int('n_units_2', min_value=8, max_value=128, step=8, default=8)        

    return hp


def _build_keras_model(hparams: kerastuner.HyperParameters, 
                       tf_transform_output: tft.TFTransformOutput) -> tf.keras.Model:
  
    deep_columns = [
        tf.feature_column.numeric_column(
            key=features.transformed_name(key), 
            shape=())
        for key in numeric_columns
    ]
    
    input_layers = {
        column.key: tf.keras.layers.Input(name=column.key, shape=(), dtype=tf.float32)
        for column in deep_columns
    }    

    categorical_columns = [
        tf.feature_column.categorical_column_with_identity(
            key=features.transformed_name(key), 
            num_buckets=tf_transform_output.num_buckets_for_transformed_feature(features.transformed_name(key)), 
            default_value=0)
        for key in features.CATEGORICAL_FEATURE_KEYS
    ]

    wide_columns = [
        tf.feature_column.indicator_column(categorical_column)
        for categorical_column in categorical_columns
    ]
    
    input_layers.update({
        column.categorical_column.key: tf.keras.layers.Input(name=column.categorical_column.key, shape=(), dtype=tf.int32)
        for column in wide_columns
    })


    deep = tf.keras.layers.DenseFeatures(deep_columns)(input_layers)
    for n in range(int(hparams.get('n_layers'))):
        deep = tf.keras.layers.Dense(units=hparams.get('n_units_' + str(n + 1)))(deep)

    wide = tf.keras.layers.DenseFeatures(wide_columns)(input_layers)

    output = tf.keras.layers.Dense(1, activation='sigmoid')(
               tf.keras.layers.concatenate([deep, wide]))

    model = tf.keras.Model(input_layers, output)
    model.compile(
      loss='binary_crossentropy',
      optimizer=tf.keras.optimizers.Adam(lr=hparams.get('learning_rate')),
      metrics=[tf.keras.metrics.BinaryAccuracy()])
    model.summary(print_fn=absl.logging.info)

    return model    


# TFX Tuner will call this function.
def tuner_fn(fn_args: TrainerFnArgs) -> TunerFnResult:
    
    transform_graph = tft.TFTransformOutput(fn_args.transform_graph_path)
  
  # Construct a build_keras_model_fn that just takes hyperparams from get_hyperparameters as input.
    build_keras_model_fn = functools.partial(
      _build_keras_model, tf_transform_output=transform_graph)  

  # BayesianOptimization is a subclass of kerastuner.Tuner which inherits from BaseTuner.    
    tuner = kerastuner.BayesianOptimization(
      build_keras_model_fn,
      max_trials=10,
      hyperparameters=_get_hyperparameters(),
      # New entries allowed for n_units hyperparameter construction conditional on n_layers selected.
#       allow_new_entries=True,
#       tune_new_entries=True,
      objective=kerastuner.Objective('val_binary_accuracy', 'max'),
      directory=fn_args.working_dir,
      project_name='churn_tuning')
  
    train_dataset = _input_fn(
      fn_args.train_files,
      fn_args.data_accessor,
      transform_graph,
      batch_size=TRAIN_BATCH_SIZE)

    eval_dataset = _input_fn(
      fn_args.eval_files,
      fn_args.data_accessor,
      transform_graph,
      batch_size=EVAL_BATCH_SIZE)

    return TunerFnResult(
      tuner=tuner,
      fit_kwargs={
          'x': train_dataset,
          'validation_data': eval_dataset,
          'steps_per_epoch': fn_args.train_steps,
          'validation_steps': fn_args.eval_steps
      })


# TFX Trainer will call this function.
def run_fn(fn_args: TrainerFnArgs):
    
    tf_transform_output = tft.TFTransformOutput(fn_args.transform_output)
    
    train_dataset = _input_fn(
      fn_args.train_files, 
      fn_args.data_accessor, 
      tf_transform_output, 
      TRAIN_BATCH_SIZE)

    eval_dataset = _input_fn(
      fn_args.eval_files, 
      fn_args.data_accessor,
      tf_transform_output, 
      EVAL_BATCH_SIZE)

    if fn_args.hyperparameters:
        hparams = kerastuner.HyperParameters.from_config(fn_args.hyperparameters)
    else:
    # This is a shown case when hyperparameters is decided and Tuner is removed
    # from the pipeline. User can also inline the hyperparameters directly in
    # _build_keras_model.
        hparams = _get_hyperparameters()
    absl.logging.info('HyperParameters for training: %s' % hparams.get_config())
  
  # Distribute training over multiple replicas on the same machine.
    mirrored_strategy = tf.distribute.MirroredStrategy()
    with mirrored_strategy.scope():
        model = _build_keras_model(
            hparams=hparams,
            tf_transform_output=tf_transform_output)

    tensorboard_callback = tf.keras.callbacks.TensorBoard(
      log_dir=fn_args.model_run_dir, update_freq='batch')

    model.fit(
      train_dataset,
      epochs=EPOCHS,
      steps_per_epoch=fn_args.train_steps,
      validation_data=eval_dataset,
      validation_steps=fn_args.eval_steps,
      callbacks=[tensorboard_callback])
    
    signatures = {
        'serving_default':
          _get_serve_tf_examples_fn(model,
                                    tf_transform_output).get_concrete_function(
                                        tf.TensorSpec(
                                            shape=[None],
                                            dtype=tf.string,
                                            name='examples')),
    }
  
    model.save(fn_args.serving_model_dir, save_format='tf', signatures=signatures)