"""
Configuration parameters.

Copyright (c) 2017, Lior P. Abitbol <liorabitbol@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

#
# vRO Default TCP Port
#
VRO_TCP_PORT = 8281

#
# vRO Config files
#
VRO_CONFIG_FILE = "/etc/vmwvro2/vro.yml"
VRO_CREDENTIALS_FILE = "/etc/vmwvro2/vro-credentials.yml"



#
# vRO URL templates
#
URL_GET_WORKFLOW_BY_ID = "{{base_url}}/vco/api/workflows/{{id}}"
URL_RUN_WORKFLOW_BY_ID = "{{base_url}}/vco/api/workflows/{{id}}/executions/"

WORKFLOW_GETFWLOGS_ID = "1d8c12ce-a551-4a03-aa54-2165f9a0f525"

ENV_VROENDPOINT = "UNITTEST_ENDPOINTSERVER"


FINISHED_STATES = ["completed", "failed"]
SIMPLE_TYPES = ["boolean", "string", "number"]
