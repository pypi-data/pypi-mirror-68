import os
import sys
import base64
import logging
import zipfile
import textwrap
import pywren_ibm_cloud.compute.backends.vm
from . import config as ibmcf_config
from pywren_ibm_cloud.utils import version_str
from pywren_ibm_cloud.version import __version__
from pywren_ibm_cloud.utils import is_pywren_function

logger = logging.getLogger(__name__)


class IBMGen2VMBackend:
    """
    A wrap-up around VM backend.
    """

    def __init__(self, ibm_vm_config):
        logger.debug("Creating VM client")
        self.log_level = os.getenv('PYWREN_LOGLEVEL')
        self.name = 'vm'
        self.ibm_vm_config = ibm_vm_config
        self.is_pywren_function = is_pywren_function()

        self.user_agent = ibm_vm_config['user_agent']
        self.vm_host = ibm_vm_config['host']
        self.vm_user = ibm_vm_config['user']
        self.vm_password = ibm_vm_config['password']
        self.vm_client = None

        log_msg = ('PyWren v{} init for VM host {}'.format(__version__, self.vm_host))
        if not self.log_level:
            print(log_msg)
        logger.info("VM client created successfully")


    def build_runtime(self, docker_image_name, dockerfile):
        """
        Builds a new VM runtime
        """
        logger.info('Building a new IBM VM runtime')

    def create_runtime(self, docker_image_name, memory, timeout):
        """
        Creates a new runtime into IBM CF namespace from an already built Docker image
        """
        logger.info('Create a new IBM VM runtime')

    def delete_runtime(self, docker_image_name, memory):
        """
        Deletes a runtime
        """
        logger.info('Delete IBM VM runtime')

    def delete_all_runtimes(self):
        """
        Deletes all runtimes from all packages
        """
        logger.info('Delete IBM VM all runtimes')

    def list_runtimes(self, docker_image_name='all'):

        logger.info('List IBM VM runtime')

    def invoke(self, docker_image_name, runtime_memory, payload):
        """
        Invoke -- return information about this invocation
        """
        print (payload)
        logger.info('Invoke IBM VM runtime')

    def get_runtime_key(self, docker_image_name, runtime_memory):
        """
        Method that creates and returns the runtime key.
        Runtime keys are used to uniquely identify runtimes within the storage,
        in order to know which runtimes are installed and which not.
        """
        logger.info('Get IBM VM runtime')
        """
        Method that creates and returns the runtime key.
        Runtime keys are used to uniquely identify runtimes within the storage,
        in order to know which runtimes are installed and which not.
        """
        name = self._format_runtime_name(docker_image_name, runtime_memory)
        runtime_key = os.path.join(self.name, name)

        return runtime_key
    
    def _format_runtime_name(self, docker_image_name, runtime_memory):
        runtime_name = docker_image_name.replace('/', '_').replace(':', '_')
        return '{}_{}MB'.format(runtime_name, runtime_memory)
    