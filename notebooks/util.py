import os
import pathlib
import subprocess

import json
import yaml

import jupyter_client

import papermill as pm
from papermill.engines import NBClientEngine

from jinja2 import Template

import dask
from dask_jobqueue import PBSCluster
from dask.distributed import Client


def get_ClusterClient(memory="25GB", project="NCGD0011", on_hub=True):
    cluster = get_Cluster(memory, project, on_hub)
    client = Client(cluster)
    return cluster, client


def get_Cluster(memory="25GB", project="NCGD0011", on_hub=True):
    """return client and cluster"""
    USER = os.environ['USER']

    cluster = PBSCluster(
        cores=1,
        memory=memory,
        processes=1,
        queue='casper',
        local_directory=f'/glade/scratch/{USER}/dask-workers',
        log_directory=f'/glade/scratch/{USER}/dask-workers',
        resource_spec=f'select=1:ncpus=1:mem={memory}',
        project=project,
        walltime='06:00:00',
        interface='ib0',
    )

    if on_hub:
        jupyterhub_server_name = os.environ.get('JUPYTERHUB_SERVER_NAME', None)
        dashboard_link = 'https://jupyterhub.hpc.ucar.edu/stable/user/{USER}/proxy/{port}/status'
        if jupyterhub_server_name:
            dashboard_link = (
                'https://jupyterhub.hpc.ucar.edu/stable/user/'
                + '{USER}'
                + f'/{jupyterhub_server_name}/proxy/'
                + '{port}/status'
            )
    else:
        dashboard_link = 'http://localhost:8787/status'

    dask.config.set({'distributed.dashboard.link': dashboard_link})
    return cluster


class manage_conda_kernel(object):
    """Manage conda kernels so they can be see by `papermill`"""

    def __init__(self, kernel_name: str):
        self.kernel_name = kernel_name

    def getcwd(self):
        """get the directory of a conda kernel by name"""
        command = ['conda', 'env', 'list', '--json']
        output = subprocess.check_output(command).decode('ascii')
        envs = json.loads(output)['envs']

        for env in envs:
            env = pathlib.Path(env)
            if self.kernel_name == env.stem:
                return env
        else:
            return None

    def isinstalled(self):
        return self.kernel_name in jupyter_client.kernelspec.find_kernel_specs()

    def ensure_installed(self):
        """install a conda kernel in a location findable by `nbconvert` etc."""

        if self.isinstalled():
            return

        path = self.getcwd()
        if path is None:
            raise ValueError(f'conda kernel "{self.kernel_name}" not found')
        path = path / pathlib.Path('share/jupyter/kernels')

        kernels_in_conda_env = jupyter_client.kernelspec._list_kernels_in(path)
        py_kernel_key = [k for k in kernels_in_conda_env.keys() if 'python' in k][0]
        kernel_path = kernels_in_conda_env[py_kernel_key]

        jupyter_client.kernelspec.install_kernel_spec(
            kernel_path, kernel_name=self.kernel_name, user=True, replace=True
        )
        assert self.isinstalled()


class md_jinja_engine(NBClientEngine):
    @classmethod
    def execute_managed_notebook(cls, nb_man, kernel_name, **kwargs):
        jinja_data = {} if "jinja_data" not in kwargs else kwargs["jinja_data"]

        # call the papermill execution engine:
        super().execute_managed_notebook(nb_man, kernel_name, **kwargs)

        for cell in nb_man.nb.cells:
            if cell.cell_type == "markdown":
                cell["source"] = Template(cell["source"]).render(**jinja_data)


# what's the right way to register an engine?
pm.engines.papermill_engines._engines["md_jinja"] = md_jinja_engine


def get_control_dict():
    with open('_config-calc.yml', 'r') as fid:
        control = yaml.safe_load(fid)

    os.makedirs(control["output_dir"], exist_ok=True)

    default_kernel_name = control.pop('kernel_name', None) 

    if default_kernel_name is not None:
        for d in control['notebooks'].values():
            if 'kernel_name' not in d:
                d['kernel_name'] = default_kernel_name
    else:
        for nb, d in control['notebooks'].items():
            assert 'kernel_name' in d, f'kernel information missing for {nb}.ipynb'

    for nb, d in control['notebooks'].items():
        manage_conda_kernel(d['kernel_name']).ensure_installed()

    return control


