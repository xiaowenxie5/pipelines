# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# coding: utf-8

"""
    Kubeflow Pipelines API

    This file contains REST API specification for Kubeflow Pipelines. The file is autogenerated from the swagger definition.

    Contact: kubeflow-pipelines@google.com
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest

import kfp_server_api
from kfp_server_api.api.pipeline_service_api import PipelineServiceApi  # noqa: E501
from kfp_server_api.rest import ApiException


class TestPipelineServiceApi(unittest.TestCase):
    """PipelineServiceApi unit test stubs"""

    def setUp(self):
        self.api = kfp_server_api.api.pipeline_service_api.PipelineServiceApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_create_pipeline(self):
        """Test case for create_pipeline

        Creates a pipeline.  # noqa: E501
        """
        pass

    def test_create_pipeline_version(self):
        """Test case for create_pipeline_version

        Adds a pipeline version to the specified pipeline.  # noqa: E501
        """
        pass

    def test_delete_pipeline(self):
        """Test case for delete_pipeline

        Deletes a pipeline and its pipeline versions.  # noqa: E501
        """
        pass

    def test_delete_pipeline_version(self):
        """Test case for delete_pipeline_version

        Deletes a pipeline version by pipeline version ID. If the deleted pipeline version is the default pipeline version, the pipeline's default version changes to the pipeline's most recent pipeline version. If there are no remaining pipeline versions, the pipeline will have no default version. Examines the run_service_api.ipynb notebook to learn more about creating a run using a pipeline version (https://github.com/kubeflow/pipelines/blob/master/tools/benchmarks/run_service_api.ipynb).  # noqa: E501
        """
        pass

    def test_get_pipeline(self):
        """Test case for get_pipeline

        Finds a specific pipeline by ID.  # noqa: E501
        """
        pass

    def test_get_pipeline_version(self):
        """Test case for get_pipeline_version

        Gets a pipeline version by pipeline version ID.  # noqa: E501
        """
        pass

    def test_get_pipeline_version_template(self):
        """Test case for get_pipeline_version_template

        Returns a YAML template that contains the specified pipeline version's description, parameters and metadata.  # noqa: E501
        """
        pass

    def test_get_template(self):
        """Test case for get_template

        Returns a single YAML template that contains the description, parameters, and metadata associated with the pipeline provided.  # noqa: E501
        """
        pass

    def test_list_pipeline_versions(self):
        """Test case for list_pipeline_versions

        Lists all pipeline versions of a given pipeline.  # noqa: E501
        """
        pass

    def test_list_pipelines(self):
        """Test case for list_pipelines

        Finds all pipelines.  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
