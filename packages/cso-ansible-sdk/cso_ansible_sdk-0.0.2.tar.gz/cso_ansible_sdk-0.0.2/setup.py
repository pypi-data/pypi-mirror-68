# Copyright 2017 Redtail Consulting, LLC.
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


from setuptools import setup

setup(
    name='cso_ansible_sdk',
    version='0.0.2',
    description='CSO SDK for Ansible',
    long_description='CSO SDK for Ansible',
    author='Calvin Remsburg',
    author_email='packetferret@gmail.com',
    packages=['cso_ansible_sdk'],
    url='https://github.com/packetferret/cso_ansible_sdk/',
    download_url = 'https://github.com/packetferret/cso_ansible_sdk/archive/v0.0.2.tar.gz',
    license='Apache Software License',
    install_requires=[
        "requests >= 2.23.0",
    ],
)