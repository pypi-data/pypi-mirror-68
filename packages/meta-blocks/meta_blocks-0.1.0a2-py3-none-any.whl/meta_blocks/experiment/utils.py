"""Utility functions for running experiments."""

import collections
import contextlib
import datetime
import logging
import re
from typing import Optional

import colorlog
import tensorflow.compat.v1 as tf

from meta_blocks import (
    adaptation,
    common,
    datasets,
    models,
    networks,
    optimizers,
    tasks,
)

logger = logging.getLogger(__name__)

# Transition to V2 will happen in stages.
tf.disable_v2_behavior()
tf.enable_resource_variables()


class Experiment(
    collections.namedtuple("Experiment", ("checkpoint", "meta_learners", "task_dists"))
):
    """Represents built entities for the Experiment.

    Parameters
    ----------
    checkpoint : tf.train.Checkpoint

    meta_learners : list of meta-learners

    task_dists : list of task distributions
    """

    pass


@contextlib.contextmanager
def session(
    gpu_ids: Optional[str] = None,
    gpu_allow_growth: bool = True,
    log_device_placement: bool = False,
):
    """Sets up an experiment and returns a tf.Session.

    Parameters
    ----------
    gpu_ids : str, optional
        GPUs that will be made visible.

    gpu_allow_growth : bool (default: True)
        Used to configure tf.Session.
        See tf.ConfigProto.gpu_options.allow_growth.

    log_device_placement : bool (default: False)
        Used for debugging tensor placement on devices.
        See tf.ConfigProto.log_device_placement.
    """
    # Reset TF graph.
    tf.reset_default_graph()

    # Create and configure a tf.Session.
    config = tf.ConfigProto()
    if gpu_ids is not None:
        config.gpu_options.visible_device_list = gpu_ids
    if gpu_allow_growth:
        config.gpu_options.allow_growth = True
    if log_device_placement:
        config.log_device_placement = True
    sess = tf.Session(config=config)

    try:
        with sess.as_default():
            yield sess
    finally:
        sess.close()


def build_and_initialize(cfg, mode=common.ModeKeys.TRAIN):
    """Builds and initializes all parts of the graph.

    Parameters
    ----------
    cfg : OmegaConf
        The experiment configuration.

    mode : str, optional (default: common.ModeKeys.TRAIN)
        Defines the mode of the computation graph (TRAIN or EVAL).
        Note: this is likely to be removed from the API down the line.

    Returns
    -------
    exp : Experiment
        An object that represents the experiment.
        Contains `meta_learners`, `samplers`, and `task_dists`.
    """
    sess = tf.get_default_session()

    # Build the data source.
    data_source = datasets.get_data_source(
        name=cfg.data.name, **cfg.data.source
    ).build()

    # Build meta-datasets.
    meta_datasets = {
        task.set_name: datasets.get_meta_dataset(
            name=cfg.data.name,
            data_sources=data_source[task.set_name],
            **cfg[mode].meta_dataset,
        ).build()
        for task in cfg[mode].tasks
    }

    # Build model.
    network_builder = networks.get(**cfg.network)
    model = models.get(
        input_shapes=data_source.data_shapes,
        input_types=data_source.data_types,
        num_classes=cfg[mode].meta_dataset.num_classes,
        network_builder=network_builder,
        **cfg[mode].model,
    ).build()

    # Build optimizer.
    optimizer = optimizers.get(**cfg.train.optimizer)

    # Build checkpoint.
    checkpoint = tf.train.Checkpoint(
        model_state=model.initial_parameters, optimizer=optimizer
    )

    # Build task distributions.
    task_dists = [
        tasks.get_distribution(
            meta_dataset=meta_datasets[task.set_name],
            name_suffix=task.log_dir.replace("/", "_"),
            sampler_config=task.sampler,
            **task.config,
        ).build()
        for task in cfg[mode].tasks
    ]

    # Build meta-learners.
    meta_learners = [
        adaptation.get(
            model=model,
            optimizer=optimizer,
            tasks=task_dist.task_batch,
            mode=mode,
            **cfg[mode].adapt,
        ).build()
        for task, task_dist in zip(cfg[mode].tasks, task_dists)
    ]

    # Variable initialization.
    if mode == common.ModeKeys.TRAIN:
        # Initialize all the variables in the graph.
        sess.run(tf.global_variables_initializer())
    else:  # mode == common.ModeKeys.EVAL:
        sess.run(tf.global_variables_initializer())
        # Initialize only non-trainable variables.
        # Trainable variables are loaded from a checkpoint.
        # sess.run(tf.variables_initializer(model.non_trainable_parameters))

    # Initialize task distributions.
    for task_dist in task_dists:
        task_dist.initialize()

    return Experiment(
        checkpoint=checkpoint, meta_learners=meta_learners, task_dists=task_dists
    )


class ExperimentFormatter(colorlog.ColoredFormatter):
    """Custom log formatter that nicely indents multiline experiment logs and
    format times relative to the start of the star time of the experiment.
    """

    _COLOR_REGEX = re.compile(r"\033\[[\d;]*m")

    def formatMessage(self, record):
        # Add nice multiline identation to the message.
        original_message = record.message.strip()
        # Reformat the original experiment message if it is multiline.
        if "meta_blocks.experiment" in record.name and "\n" in original_message:
            # Determine the length of everything besides the message.
            record.message = ""
            indent = len(self._COLOR_REGEX.sub("", self._style.format(record)))
            # Indent message lines appropriately.
            original_message_parts = original_message.split("\n")
            reformatted_message = "\n".join(
                # Message separator.
                [original_message_parts[0]]
                +
                # Add extra white space indent to all lines after the first one.
                [(" " * indent) + line.strip() for line in original_message_parts[1:]]
            )
            record.message = reformatted_message
        return self._style.format(record)

    def formatTime(self, record, datefmt=None):
        """
        Return the creation time of the specified LogRecord relative to the
        start time of the experiment as formatted text.
        """
        duration = datetime.datetime.utcfromtimestamp(record.relativeCreated / 1000)
        record.delta = duration.strftime("%H:%M:%S")
        return super(ExperimentFormatter, self).formatTime(record, datefmt)
