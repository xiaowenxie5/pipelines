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

import json

# TODO(IronPan) This library can be removed once ifPresent is supported within concat[] in component YAML V2.
# Currently the component YAML will generate the payload with all API fields presented, 
# and those fields will be left empty if user doesn't specify them in the Python.
def __remove_empty(j):
    """Remove the empty fields in the Json."""
    final_dict = {}
    for k, v in j.items():
      if v:
        if isinstance(v, dict):
          final_dict[k] = __remove_empty(v)
        elif isinstance(v, list):
          final_dict[k] = list(filter(None, [__remove_empty(i) for i in v]))
        else:
          final_dict[k] = v
    return final_dict

def recursive_remove_empty(j):
    """Recursively remove the empty fields in the Json until there is no empty fields and sub-fields."""
    needs_update = True
    while needs_update:
        new_j = __remove_empty(j)
        needs_update = json.dumps(new_j)!=json.dumps(j)
        j = new_j
    return j
