# Copyright 2021 The Kubeflow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Test Vertex AI Model Eval Remote Runner module."""

import json
from logging import raiseExceptions
import os
import time
import unittest
from unittest import mock
from google_cloud_pipeline_components.experimental.remote.gcp_launcher import upload_model_remote_runner
from google.cloud import aiplatform
from google.cloud.aiplatform.compat.types import job_state as gca_job_state
from google_cloud_pipeline_components.experimental.proto.gcp_resources_pb2 import GcpResources
from google.protobuf import json_format

class LroResult(object):
    pass

class ModelUploadRemoteRunnerUtilsTests(unittest.TestCase):

    def setUp(self):
        super(ModelUploadRemoteRunnerUtilsTests, self).setUp()
        self._payload = '{"display_name": "ContainerComponent", "job_spec": {"worker_pool_specs": [{"machine_spec": {"machine_type": "n1-standard-4"}, "replica_count": 1, "container_spec": {"image_uri": "google/cloud-sdk:latest", "command": ["sh", "-c", "set -e -x\\necho \\"$0, this is an output parameter\\"\\n", "{{$.inputs.parameters[\'input_text\']}}", "{{$.outputs.parameters[\'output_value\'].output_file}}"]}}]}}'
        self._project = 'test_project'
        self._location = 'test_region'
        self._type = 'ModelUpload'
        self._lro_name = f'/projects/{self._project}/locations/{self._location}/operations/123'
        self._model_name = f'/projects/{self._project}/locations/{self._location}/models/123'
        self._executor_input = '{"outputs":{"artifacts":{"model":{"artifacts":[{"metadata":{},"name":"foobar","type":{"schemaTitle":"system.Model"},"uri":"gs://abc"}]}},"outputFile":"localpath/foo"}}'
        self._output_file_path = 'localpath/foo'
        self._gcp_resouces_path = 'gcp_resouces'
        self._uri_prefix = f"https://{self._location}-aiplatform.googleapis.com/v1/"

    def tearDown(self):
        if os.path.exists(self._gcp_resouces_path):
            os.remove(self._gcp_resouces_path)

    @mock.patch.object(aiplatform.gapic, 'ModelServiceClient', autospec=True)
    def test_model_upload_remote_runner_on_region_is_set_correctly_in_client_options(
            self, mock_model_service_client):
        model_client = mock.Mock()
        mock_model_service_client.return_value = model_client

        upload_model_lro = mock.Mock()
        model_client.upload_model.return_value = upload_model_lro
        upload_model_lro.operation.name = self._lro_name

        upload_model_lro.done.return_value = True
        upload_model_lro.operation.error.code = 0
        result = LroResult()
        result.model = self._model_name
        upload_model_lro.result.return_value = result

        upload_model_remote_runner.upload_model(self._type, self._project,
                                                   self._location,
                                                   self._payload,
                                                   self._gcp_resouces_path, self._executor_input)
        mock_model_service_client.assert_called_once_with(
            client_options={
                'api_endpoint': 'test_region-aiplatform.googleapis.com'
            },
            client_info=mock.ANY)

        with open(self._output_file_path) as f:
            executor_output = f.read()
            self.assertEqual(executor_output,'{"artifacts": {"model": {"artifacts": [{"metadata": {}, "name": "foobar", "type": {"schemaTitle": "system.Model"}, "uri": "https://test_region-aiplatform.googleapis.com/v1//projects/test_project/locations/test_region/models/123"}]}}}')

        with open(self._gcp_resouces_path) as f:
            serialized_gcp_resources = f.read()
            # Instantiate GCPResources Proto
            lro_resources = json_format.Parse(serialized_gcp_resources,
                                                     GcpResources())

            self.assertEqual(len(lro_resources.resources), 1)
            self.assertEqual(lro_resources.resources[0].resource_uri, self._uri_prefix+self._lro_name)

    @mock.patch.object(aiplatform.gapic, 'ModelServiceClient', autospec=True)
    def test_upload_model_remote_runner_raises_exception_on_error(
            self, mock_model_service_client):
        model_client = mock.Mock()
        mock_model_service_client.return_value = model_client

        upload_model_lro = mock.Mock()
        model_client.upload_model.return_value = upload_model_lro
        upload_model_lro.operation.name = self._lro_name

        upload_model_lro.done.return_value = True
        upload_model_lro.operation.error.code = 1

        with self.assertRaises(RuntimeError):
            upload_model_remote_runner.upload_model(self._type,
                                                       self._project,
                                                       self._location,
                                                       self._payload,
                                                       self._gcp_resouces_path, self._executor_input)

    @mock.patch.object(aiplatform.gapic, 'ModelServiceClient', autospec=True)
    @mock.patch.object(time, "sleep", autospec=True)
    def test_upload_model_remote_runner_retries_to_get_status_on_non_completed_job(
            self, mock_time_sleep, mock_model_service_client):
        model_client = mock.Mock()
        mock_model_service_client.return_value = model_client

        upload_model_lro = mock.Mock()
        model_client.upload_model.return_value = upload_model_lro
        upload_model_lro.operation.name = self._lro_name

        upload_model_lro.done.side_effect = [False, True]
        upload_model_lro.operation.error.code = 0
        result = LroResult()
        result.model = self._model_name
        upload_model_lro.result.return_value = result

        upload_model_remote_runner.upload_model(self._type, self._project,
                                                   self._location,
                                                   self._payload,
                                                   self._gcp_resouces_path, self._executor_input)
        mock_time_sleep.assert_called_once_with(
            upload_model_remote_runner._POLLING_INTERVAL_IN_SECONDS)
        self.assertEqual(upload_model_lro.done.call_count, 2)
