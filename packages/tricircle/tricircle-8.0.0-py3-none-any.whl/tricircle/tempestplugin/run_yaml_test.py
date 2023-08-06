# All Rights Reserved
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import sys

import task_runner


if __name__ == '__main__':
    (yaml_path, auth_url, project, user, password,
     project_domain_id, user_domain_id) = sys.argv[1:]
    runner = task_runner.SDKRunner(auth_url, project, user,
                                   password, project_domain_id, user_domain_id)
    engine = task_runner.RunnerEngine(yaml_path, runner)

    error_msg = engine.run_task_sets()
    if error_msg:
        sys.exit(error_msg)
