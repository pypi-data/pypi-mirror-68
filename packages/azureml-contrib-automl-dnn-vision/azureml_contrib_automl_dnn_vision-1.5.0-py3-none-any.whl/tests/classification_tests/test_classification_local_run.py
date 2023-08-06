import os
import pytest
import sys
from azureml.contrib.automl.dnn.vision.classification.common.constants import ArtifactsLiterals
import azureml.contrib.automl.dnn.vision.classification.runner as runner


data_folder = 'classification_data/images'
labels_root = 'classification_data/'


def _get_settings(csv_file):
    return {
        'images_folder': '.',
        'labels_file': csv_file,
        'seed': 47,
    }


@pytest.mark.usefixtures('new_clean_dir')
def test_binary_classification_local_run(monkeypatch):
    settings = _get_settings('binary_classification.csv')

    with monkeypatch.context() as m:
        m.setattr(sys, 'argv', ['runner.py', '--data-folder', data_folder, '--labels-file-root', labels_root])
        runner.run(settings)
    assert os.path.exists(os.path.join(ArtifactsLiterals.OUTPUT_DIRECTORY, ArtifactsLiterals.MODEL_WRAPPER_PKL))


@pytest.mark.usefixtures('new_clean_dir')
def test_multiclassification_local_run(monkeypatch):
    settings = _get_settings('multiclass.csv')

    with monkeypatch.context() as m:
        m.setattr(sys, 'argv', ['runner.py', '--data-folder', data_folder, '--labels-file-root', labels_root])
        runner.run(settings)

    assert os.path.exists(os.path.join(ArtifactsLiterals.OUTPUT_DIRECTORY, ArtifactsLiterals.MODEL_WRAPPER_PKL))


@pytest.mark.usefixtures('new_clean_dir')
def test_multilabel_local_run(monkeypatch):
    settings = _get_settings('multilabel.csv')

    with monkeypatch.context() as m:
        m.setattr(sys, 'argv', ['runner.py', '--data-folder', data_folder, '--labels-file-root', labels_root])
        runner.run(settings, multilabel=True)

    assert os.path.exists(os.path.join(ArtifactsLiterals.OUTPUT_DIRECTORY, ArtifactsLiterals.MODEL_WRAPPER_PKL))
