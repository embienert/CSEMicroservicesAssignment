#!/bin/bash -eu
#
# Copyright 2018 Google LLC
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

# [START gke_discountservice_genproto]


#python grpc_tools.protoc -I../../pb --python_out=. --grpc_python_out=. ../../pb/demo.proto
python C:\Users\abadn\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.10_qbz5n2kfra8p0\LocalCache\local-packages\Python310\site-packages\grpc_tools\protoc.py -I../../pb --python_out=. --grpc_python_out=. ../../pb/demo.proto
read -p "press any button"
# [END gke_discountservice_genproto]
