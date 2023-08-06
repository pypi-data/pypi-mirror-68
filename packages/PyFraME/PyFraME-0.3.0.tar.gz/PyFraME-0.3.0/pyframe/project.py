# Copyright (C) 2017-2020  Jógvan Magnus Haugaard Olsen
#
# This file is part of PyFraME.
#
# PyFraME is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PyFraME is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PyFraME.  If not, see <https://www.gnu.org/licenses/>.
#

"""Contains the Project class"""

import os
import shutil
import socket
import tempfile
import numpy as np
import h5py

from .system import MolecularSystem
from .fragments import find_nearest_atom
from .potentials import Potential
from .readers import OutputReaders, read_standard_potential
from .writers import InputWriters, ScriptWriters
from .process import run, process_jobs

__all__ = ['Project']


class Project(object):
    """Project class"""

    def __init__(self, **kwargs):
        if 'SCRATCH' in os.environ:
            self._scratch_dir = os.environ['SCRATCH']
        elif os.path.isdir('/scratch'):
            self._scratch_dir = '/scratch'
        elif os.path.isdir('/scr'):
            self._scratch_dir = '/scr'
        elif os.path.isdir('/tmp'):
            self._scratch_dir = '/tmp'
        elif os.path.isdir('/usr/tmp'):
            self._scratch_dir = '/usr/tmp'
        elif os.path.isdir(os.path.join(os.getcwd(), 'scratch')):
            self._scratch_dir = os.path.join(os.getcwd(), 'scratch')
        elif os.path.isdir(os.path.join(os.getcwd(), 'scr')):
            self._scratch_dir = os.path.join(os.getcwd(), 'scr')
        elif os.path.isdir(os.path.join(os.getcwd(), 'tmp')):
            self._scratch_dir = os.path.join(os.getcwd(), 'tmp')
        elif os.path.isdir(os.path.join(os.getcwd(), 'temp')):
            self._scratch_dir = os.path.join(os.getcwd(), 'temp')
        else:
            self._scratch_dir = os.getcwd()
        self._work_dir = os.getcwd()
        if os.environ.get('PBS_NODEFILE'):
            with open(os.environ['PBS_NODEFILE'], 'r') as node_file:
                nodes = node_file.read().splitlines()
        elif os.environ.get('SLURM_NODELIST'):
            cmd = 'scontrol show hostname $SLURM_NODELIST'
            nodes, error = run(cmd)
            nodes = nodes.decode().split()
            if error:
                print('SLURM_NODELIST is defined but could not fetch node list')
                print('The following error message was received:')
                print('{0}\n'.format(error))
                print('Please specify nodes manually')
        else:
            hostname = socket.gethostname()
            nodes = [hostname]
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.bind(('', 0))
                self._comm_port = sock.getsockname()[1]
        except OSError:
            self._comm_port = 5000
        self._node_list = list(set(nodes))
        self._jobs_per_node = 1
        self._memory_per_job = 2048
        self._mpi_procs_per_job = 1
        self._omp_threads_per_job = 1
        for key in kwargs.keys():
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            else:
                raise TypeError(key)

    @property
    def scratch_dir(self):
        """Get or set the name of the scratch directory."""
        return self._scratch_dir

    @scratch_dir.setter
    def scratch_dir(self, scratch_dir):
        assert isinstance(scratch_dir, str)
        self._scratch_dir = os.path.expanduser(os.path.expandvars(os.path.normpath(scratch_dir)))

    @property
    def work_dir(self):
        """Get or set the name of the work directory."""
        return self._work_dir

    @work_dir.setter
    def work_dir(self, work_dir):
        assert isinstance(work_dir, str)
        self._work_dir = os.path.expanduser(os.path.expandvars(os.path.normpath(work_dir)))

    @property
    def node_list(self):
        """Get or set the list of node names that will be used for calculations."""
        return self._node_list

    @node_list.setter
    def node_list(self, nodelist):
        assert isinstance(nodelist, list)
        assert all(isinstance(node, str) for node in nodelist)
        self._node_list = nodelist

    @property
    def jobs_per_node(self):
        """Get or set the number of jobs to run on each node."""
        return self._jobs_per_node

    @jobs_per_node.setter
    def jobs_per_node(self, jobs_per_node):
        assert isinstance(jobs_per_node, int)
        self._jobs_per_node = jobs_per_node

    @property
    def memory_per_job(self):
        """Get or set the amount of memory to use for each job."""
        return self._memory_per_job

    @memory_per_job.setter
    def memory_per_job(self, mem_per_job):
        assert isinstance(mem_per_job, int)
        self._memory_per_job = mem_per_job

    @property
    def mpi_procs_per_job(self):
        """Get or set the number of MPI processes that each job will use."""
        return self._mpi_procs_per_job

    @mpi_procs_per_job.setter
    def mpi_procs_per_job(self, mpi_procs_per_job):
        assert isinstance(mpi_procs_per_job, int)
        self._mpi_procs_per_job = mpi_procs_per_job

    @property
    def omp_threads_per_job(self):
        """Get or set the number of OpenMP threads for each job (or each MPI process)."""
        return self._omp_threads_per_job

    @omp_threads_per_job.setter
    def omp_threads_per_job(self, omp_threads_per_job):
        assert isinstance(omp_threads_per_job, int)
        self._omp_threads_per_job = omp_threads_per_job

    @property
    def comm_port(self):
        """Get or set the communication port."""
        return self._comm_port

    @comm_port.setter
    def comm_port(self, comm_port):
        assert isinstance(comm_port, int)
        self._comm_port = comm_port

    def print_info(self):
        """Print settings."""
        print('INFO: work directory set to {0}'.format(self.work_dir))
        print('INFO: scratch directory set to {0}'.format(self.scratch_dir))
        print('INFO: running {0} job per node'.format(self.jobs_per_node))
        print('INFO: number of MPI processes per job set to {0}'.format(self.mpi_procs_per_job))
        print('INFO: number of OpenMP threads per job set to {0}'.format(self.omp_threads_per_job))
        print('INFO: memory per job set to {0} MB'.format(self.memory_per_job))
        print('INFO: memory per MPI process set to {0} MB'.format(self.memory_per_job / self.mpi_procs_per_job))
        print('INFO: communication port set to {0}'.format(self.comm_port))
        print('INFO: using node(s): {0}'.format(self.node_list))

    def create_embedding_potential(self, system):
        """Create embedding potential."""
        # TODO check if required properties are available
        assert isinstance(system, MolecularSystem)
        if not system.regions:
            # TODO replace with exception
            exit('ERROR: no regions have been added')
        temp_dir = tempfile.mkdtemp(prefix='PyFraME_', dir=self.scratch_dir)
        system_dir = os.path.join(self.work_dir, system.name)
        if not os.path.isdir(system_dir):
            os.makedirs(system_dir)
        os.chdir(system_dir)
        directories = []
        filenames = []
        fragment_sizes = []
        readers = {}
        for region in system.regions.values():
            if region.use_standard_potentials:
                region.create_mfcc_fragments()
                continue
            writers = []
            combine_calc = False
            if region.use_mfcc:
                if region.use_multipoles and not region.atomic_multipoles:
                    # TODO replace with exception
                    exit('ERROR: MFCC only works with atom-centered properties')
                if region.use_polarizabilities and not region.atomic_polarizabilities:
                    # TODO replace with exception
                    exit('ERROR: MFCC only works with atom-centred properties')
                region.create_mfcc_fragments()
                fragments = region.mfcc_fragments
            else:
                fragments = region.fragments
            if region.use_multipoles and region.use_polarizabilities:
                same_program = (region.multipole_program == region.polarizability_program)
                same_model = (region.multipole_model == region.polarizability_model)
                same_method = (region.multipole_method == region.polarizability_method and
                               region.multipole_xcfun == region.polarizability_xcfun)
                same_basis = (region.multipole_basis == region.polarizability_basis)
                both_atomic = region.use_multipoles and region.atomic_multipoles
                combine_calc = (same_program and same_model and same_method and same_basis and both_atomic)
            if region.use_multipoles and not combine_calc:
                writers.append(region.multipole_program + '_' + region.multipole_model + '_multipoles')
            if region.use_polarizabilities and not combine_calc:
                writers.append(region.polarizability_program + '_' + region.polarizability_model + '_polarizability')
            if region.use_multipoles and region.use_polarizabilities and combine_calc:
                writers.append(region.multipole_program + '_' + region.multipole_model)
            for writer in writers:
                if not hasattr(InputWriters, writer) or not hasattr(ScriptWriters, writer):
                    # TODO replace with exception
                    exit('ERROR: input writer {0} does not exist'.format(writer))
                for fragment in fragments.values():
                    readers[fragment.identifier] = []
                for fragment in fragments.values():
                    os.chdir(system_dir)
                    filename = fragment.identifier + '_' + writer
                    readers[fragment.identifier].append(writer)
                    if os.path.isfile(filename + '.out'):
                        continue
                    if not os.path.isdir(filename):
                        os.mkdir(filename)
                    os.chdir(filename)
                    getattr(InputWriters, writer)(fragment, region, system.core_region, filename)
                    getattr(ScriptWriters, writer)(filename, system_dir, temp_dir, self.mpi_procs_per_job,
                                                   self.omp_threads_per_job, self.memory_per_job)
                    directories.append(os.path.join(system_dir, filename))
                    filenames.append('{0}.sh'.format(filename))
                    fragment_sizes.append(fragment.number_of_atoms)
                    os.chdir(system_dir)
        shutil.rmtree(temp_dir)
        os.chdir(system_dir)
        if directories and filenames:
            fragment_sizes, directories, filenames = zip(*sorted(zip(fragment_sizes, directories, filenames),
                                                                 reverse=True))
            process_jobs(directories, filenames, self.node_list, self.jobs_per_node, self.comm_port)
            for filename, directory in zip(filenames, directories):
                if os.path.isfile(filename.replace('.sh', '.out')):
                    if os.path.getsize(filename.replace('.sh', '.out')) > 0:
                        shutil.rmtree(directory)
        atom2site = {}
        site2atom = {}
        site_index = 1
        for region in system.regions.values():
            for fragment in region.fragments.values():
                for atom in fragment.atoms:
                    site = Potential()
                    system.potential[site_index] = site
                    atom2site[atom.number] = site_index
                    site2atom[site_index] = atom.number
                    site.coordinate = atom.coordinate
                    site.element = atom.element
                    site_index += 1
        for region in system.regions.values():
            if region.use_standard_potentials:
                potential = read_standard_potential(region.standard_potential_model)
                for fragment in region.fragments.values():
                    fragment_prefix = ''
                    if fragment.name in potential and np.all([atom.name in potential[fragment.name] for atom in fragment.atoms]):
                        fragment_prefix = ''
                    elif 'N' + fragment.name in potential and np.all([atom.name in potential['N' + fragment.name] for atom in fragment.atoms]):
                        fragment_prefix = 'N'
                    elif 'n' + fragment.name in potential and np.all([atom.name in potential['n' + fragment.name] for atom in fragment.atoms]):
                        fragment_prefix = 'n'
                    elif 'C' + fragment.name in potential and np.all([atom.name in potential['C' + fragment.name] for atom in fragment.atoms]):
                        fragment_prefix = 'C'
                    elif 'c' + fragment.name in potential and np.all([atom.name in potential['c' + fragment.name] for atom in fragment.atoms]):
                        fragment_prefix = 'c'
                    elif 'A' + fragment.name in potential and np.all([atom.name in potential['A' + fragment.name] for atom in fragment.atoms]):
                        fragment_prefix = 'A'
                    elif 'B' + fragment.name in potential and np.all([atom.name in potential['B' + fragment.name] for atom in fragment.atoms]):
                        fragment_prefix = 'B'
                    try:
                        potential[fragment_prefix + fragment.name]
                    except KeyError:
                        # TODO replace with exception
                        exit('ERROR: fragment {0} is not available in {1}.'.format(fragment.name, region.standard_potential_model))
                    for atom in fragment.atoms:
                        try:
                            potential[fragment_prefix + fragment.name][atom.name]
                        except KeyError:
                            # TODO replace with exception
                            exit('ERROR: atom {0} in fragment {1} is not available in {2}.'.format(atom.name, fragment.name, region.standard_potential_model))
                        site = system.potential[atom2site[atom.number]]
                        for key, value in potential[fragment_prefix + fragment.name][atom.name].items():
                            if not hasattr(site, key):
                                # TODO replace with exception
                                exit('ERROR: {0} parameter is not implemented'.format(key))
                            setattr(site, key, value)
                if region.standard_potential_exclusion_type == 'mfcc':
                    for fragment in region.fragments.values():
                        for atom in fragment.atoms:
                            exclusion_list = []
                            for other_atom in fragment.capped_fragment.atoms:
                                if 'link' in other_atom.name:
                                    continue
                                if other_atom.number not in atom2site:
                                    continue
                                exclusion_list.append(atom2site[other_atom.number])
                            for neighbour in fragment.bonded_fragments:
                                # if neighbour is not in current region, we skip it
                                # because MFCC does not cross into other regions
                                if neighbour.identifier not in region.fragments:
                                    continue
                                if atom.number in neighbour.capped_fragment.atoms:
                                    if 'link' in neighbour.capped_fragment.atoms.get(atom.number).name:
                                        continue
                                    for other_atom in neighbour.capped_fragment.atoms:
                                        if 'link' in other_atom.name:
                                            continue
                                        if other_atom.number not in atom2site:
                                            continue
                                        exclusion_list.append(atom2site[other_atom.number])
                            exclusion_list = sorted(list(set(exclusion_list)))
                            exclusion_list.pop(exclusion_list.index(atom2site[atom.number]))
                            system.potential[atom2site[atom.number]].exclusion_list = exclusion_list
                elif region.standard_potential_exclusion_type == 'fragment':
                    for fragment in region.fragments.values():
                        for atom in fragment.atoms:
                            exclusion_list = []
                            for other_atom in fragment.capped_fragment.atoms:
                                if 'link' in other_atom.name:
                                    continue
                                if other_atom.number not in atom2site:
                                    continue
                                exclusion_list.append(atom2site[other_atom.number])
                            exclusion_list = sorted(list(set(exclusion_list)))
                            exclusion_list.pop(exclusion_list.index(atom2site[atom.number]))
                            system.potential[atom2site[atom.number]].exclusion_list = exclusion_list
            elif region.use_mfcc:
                for fragment in region.fragments.values():
                    for atom in fragment.atoms:
                        exclusion_list = []
                        for other_atom in fragment.capped_fragment.atoms:
                            if 'link' in other_atom.name:
                                continue
                            if other_atom.number not in atom2site:
                                continue
                            exclusion_list.append(atom2site[other_atom.number])
                        for neighbour in fragment.bonded_fragments:
                            # if neighbour is not in current region, we skip it
                            # because MFCC does not cross into other regions
                            if neighbour.identifier not in region.fragments:
                                continue
                            if atom.number in neighbour.capped_fragment.atoms:
                                if 'link' in neighbour.capped_fragment.atoms.get(atom.number).name:
                                    continue
                                for other_atom in neighbour.capped_fragment.atoms:
                                    if 'link' in other_atom.name:
                                        continue
                                    if other_atom.number not in atom2site:
                                        continue
                                    exclusion_list.append(atom2site[other_atom.number])
                        exclusion_list = sorted(list(set(exclusion_list)))
                        exclusion_list.pop(exclusion_list.index(atom2site[atom.number]))
                        system.potential[atom2site[atom.number]].exclusion_list = exclusion_list
                    capped_fragment = fragment.capped_fragment
                    for reader in readers[capped_fragment.identifier]:
                        filename = '{0}_{1}'.format(capped_fragment.identifier, reader)
                        potential = getattr(OutputReaders, reader)(filename)
                        if len(potential.values()) != capped_fragment.number_of_atoms:
                            # TODO replace with custom exception
                            raise ValueError('ERROR: number of sites in {filename}.out does not'.format(filename=filename) +
                                             ' match the number of atoms in fragment {identifier}.'.format(identifier=fragment.identifier))
                        for atom, params in zip(capped_fragment.atoms, potential.values()):
                            # for now we assume atomic parameters and same ordering
                            # assert 'coordinate' in params
                            # if not np.allclose(atom.coordinate, params['coordinate']):
                            #     # TODO handle if coordinates are in different order
                            #     exit('ERROR: the ordering of the sites is not correct')
                            if atom.number not in fragment.atoms:
                                # TODO make optional
                                # if 'M0' not in params:
                                #     continue
                                # in_region = False
                                # for other_fragment in region.fragments.values():
                                #     if atom.number in other_fragment.atoms:
                                #         in_region = True
                                #         break
                                # if not in_region:
                                #     nearest_atom = find_nearest_atom(atom, fragment)
                                #     site = system.potential[atom2site[nearest_atom.number]]
                                #     if getattr(site, 'M0'):
                                #         site.M0[0] += params['M0'][0]
                                #     else:
                                #         site.M0[0] = params['M0'][0]
                                continue
                            site = system.potential[atom2site[atom.number]]
                            for key, value in params.items():
                                if key == 'coordinate' or key == 'element':
                                    continue
                                if not hasattr(site, key):
                                    # TODO replace with exception
                                    exit('ERROR: {0} is not implemented'.format(key))
                                if getattr(site, key):
                                    new_value = []
                                    for old, new in zip(getattr(site, key), value):
                                        new_value.append(old + new)
                                else:
                                    new_value = value
                                setattr(site, key, new_value)
                    for neighbour in fragment.bonded_fragments:
                        if neighbour.identifier not in region.fragments:
                            continue
                        capped_fragment = neighbour.capped_fragment
                        for reader in readers[capped_fragment.identifier]:
                            filename = '{0}_{1}'.format(capped_fragment.identifier, reader)
                            potential = getattr(OutputReaders, reader)(filename)
                            if len(potential.values()) != capped_fragment.number_of_atoms:
                                # TODO replace with custom exception
                                raise ValueError('ERROR: number of sites in {filename}.out does not'.format(filename=filename) +
                                                 ' match the number of atoms in fragment {identifier}.'.format(identifier=neighbour.identifier))
                            for atom, params in zip(capped_fragment.atoms, potential.values()):
                                if atom.number not in fragment.atoms:
                                    continue
                                # TODO handle if coordinates are in different order
                                if 'link' in atom.name:
                                    # nearest_atom = find_nearest_atom(atom, fragment)
                                    # site = system.potential[atom2site[nearest_atom.number]]
                                    # for key, value in params.items():
                                    #     if key == 'coordinate' or key == 'element':
                                    #         continue
                                    #     new_value = []
                                    #     for old, new in zip(getattr(site, key), value):
                                    #         new_value.append(old + new)
                                    #     setattr(site, key, new_value)
                                    if 'M0' in params:
                                        nearest_atom = find_nearest_atom(atom, fragment)
                                        site = system.potential[atom2site[nearest_atom.number]]
                                        site.M0[0] += params['M0'][0]
                                    continue
                                site = system.potential[atom2site[atom.number]]
                                for key, value in params.items():
                                    if key == 'coordinate' or key == 'element':
                                        continue
                                    new_value = []
                                    for old, new in zip(getattr(site, key), value):
                                        new_value.append(old + new)
                                    setattr(site, key, new_value)
                    for concap in fragment.concaps.values():
                        for reader in readers[concap.identifier]:
                            filename = '{0}_{1}'.format(concap.identifier, reader)
                            potential = getattr(OutputReaders, reader)(filename)
                            if len(potential.values()) != concap.number_of_atoms:
                                # TODO replace with custom exception
                                raise ValueError('ERROR: number of sites in {filename}.out does not'.format(filename=filename) +
                                                 ' match the number of atoms in fragment {identifier}.'.format(identifier=concap.identifier))
                            for atom in concap.atoms:
                                if atom.number not in fragment.atoms:
                                    continue
                                params = None
                                for test_params in potential.values():
                                    if np.allclose(atom.coordinate, test_params['coordinate'], atol=1.0e-4):
                                        params = test_params
                                        break
                                if 'link' in atom.name:
                                    # nearest_atom = find_nearest_atom(atom, fragment)
                                    # site = system.potential[atom2site[nearest_atom.number]]
                                    # for key, value in params.items():
                                    #     if key == 'coordinate' or key == 'element':
                                    #         continue
                                    #     new_value = []
                                    #     for old, new in zip(getattr(site, key), value):
                                    #         new_value.append(old - new)
                                    #     setattr(site, key, new_value)
                                    if 'M0' in params:
                                        nearest_atom = find_nearest_atom(atom, fragment)
                                        site = system.potential[atom2site[nearest_atom.number]]
                                        site.M0[0] -= params['M0'][0]
                                    continue
                                site = system.potential[atom2site[atom.number]]
                                for key, value in params.items():
                                    if key == 'coordinate' or key == 'element':
                                        continue
                                    new_value = []
                                    for old, new in zip(getattr(site, key), value):
                                        new_value.append(old - new)
                                    setattr(site, key, new_value)
                # for fragment in region.fragments.values():
                #     for bonded_fragment in fragment.bonded_fragments:
                #         if bonded_fragment.identifier in region.fragments.keys():
                #             continue
                #         total_charge = 0.0
                #         for atom in fragment.atoms:
                #             total_charge += system.potential[atom2site[atom.number]].M0[0]
                #         capped_fragment = fragment.capped_fragment
                #         for reader in readers[capped_fragment.identifier]:
                #             filename = '{0}_{1}'.format(capped_fragment.identifier, reader)
                #             potential = getattr(OutputReaders, reader)(filename)
                #             cap_charge = 0.0
                #             for atom, params in zip(capped_fragment.atoms, potential.values()):
                #                 if atom.number not in bonded_fragment.atoms:
                #                     continue
                #                 if 'M0' in params:
                #                     cap_charge += params['M0'][0]
                #         excess_charge = cap_charge - round(cap_charge)
                #         print('Fragment:')
                #         print(fragment.identifier)
                #         print('Formal charge:')
                #         print(fragment.charge)
                #         print('Actual charge:')
                #         print(total_charge)
                #         print('Cap charge:')
                #         print(cap_charge)
                #         print('Excess charge:')
                #         print(excess_charge)
                #         excess_charge /= float(fragment.number_of_atoms)
                #         for atom in fragment.atoms:
                #             site = system.potential[atom2site[atom.number]]
                #             site.M0[0] -= excess_charge
                #         total_charge = 0.0
                #         for atom in fragment.atoms:
                #             total_charge += system.potential[atom2site[atom.number]].M0[0]
                #         print('Charge after equilibration:')
                #         print(total_charge)
            else:
                if region.atomic_polarizabilities and region.atomic_multipoles:
                    for fragment in region.fragments.values():
                        for atom in fragment.atoms:
                            exclusion_list = []
                            for other_atom in fragment.atoms:
                                exclusion_list.append(atom2site[other_atom.number])
                            exclusion_list = sorted(list(set(exclusion_list)))
                            exclusion_list.pop(exclusion_list.index(atom2site[atom.number]))
                            system.potential[atom2site[atom.number]].exclusion_list = exclusion_list
                    for fragment in region.fragments.values():
                        for reader in readers[fragment.identifier]:
                            filename = '{0}_{1}'.format(fragment.identifier, reader)
                            potential = getattr(OutputReaders, reader)(filename)
                            if len(potential.values()) != fragment.number_of_atoms:
                                # TODO replace with custom exception
                                raise ValueError('ERROR: number of sites in {filename}.out does not'.format(filename=filename) +
                                                 ' match the number of atoms in fragment {identifier}.'.format(identifier=fragment.identifier))
                            for atom, params in zip(fragment.atoms, potential.values()):
                                site = system.potential[atom2site[atom.number]]
                                for key, value in params.items():
                                    if key == 'coordinate' or key == 'element':
                                        continue
                                    if not hasattr(site, key):
                                        # TODO replace with exception
                                        exit('ERROR: {0} is not implemented'.format(key))
                                    setattr(site, key, value)
                else:
                    # TODO replace with exception
                    exit('ERROR: only atom-centered properties are supported')
                    # TODO separate site creation and place it together with
                    #      other types of site creation in previous region loop
                    for fragment in region.fragments.values():
                        exclusion_list = []
                        for reader in readers[fragment.identifier]:
                            filename = '{0}_{1}'.format(fragment.identifier, reader)
                            potential = getattr(OutputReaders, reader)(filename)
                            for params in potential.values():
                                assert 'coordinate' in params
                                assert 'element' in params
                                # TODO better way to test for existing sites
                                site_exists = False
                                test_index = False
                                for test_index, test_site in system.potential.items():
                                    if np.allclose(params['coordinate'], test_site.coordinate):
                                        site_exists = True
                                        break
                                if site_exists and test_index:
                                    site = system.potential[test_index]
                                else:
                                    site = Potential()
                                    system.potential[site_index] = site
                                    exclusion_list.append(site_index)
                                    site_index += 1
                                for key, value in params.items():
                                    if not hasattr(site, key):
                                        # TODO replace with exception
                                        exit('ERROR: {0} is not implemented'.format(key))
                                    setattr(site, key, value)
                        for index in exclusion_list:
                            other_indices = []
                            other_indices.extend(exclusion_list)
                            other_indices.pop(other_indices.index(index))
                            system.potential[index].exclusion_list.extend(other_indices)
        os.chdir(self.work_dir)
        formal_charge = 0.0
        for region in system.regions.values():
            for fragment in region.fragments.values():
                formal_charge += fragment.charge
        print('INFO: total formal charge: {0:12.8f}'.format(formal_charge))
        for region in system.regions.values():
            if region.use_standard_potentials:
                for fragment in region.fragments.values():
                    fragment_charge = 0.0
                    for atom in fragment.atoms:
                        site = system.potential[atom2site[atom.number]]
                        fragment_charge += site.M0[0]
                    if abs(fragment_charge - float(round(fragment_charge))) > 1.0e-8:
                        print('WARNING: sum of partial charges of {0} is: {1:12.8f}'.format(fragment.identifier,
                                                                                            fragment_charge))
            elif region.use_mfcc and region.use_multipoles:
                region_formal_charge = 0
                region_num_atoms = 0
                region_charge = 0.0
                # get reported formal charge and actual sum of partial charges
                for fragment in region.fragments.values():
                    region_formal_charge += fragment.charge
                    fragment_charge = 0.0
                    for atom in fragment.atoms:
                        site = system.potential[atom2site[atom.number]]
                        fragment_charge += site.M0[0]
                        region_num_atoms += 1
                    region_charge += fragment_charge
                # redistribute the surplus charge across all atoms of the region
                surplus_charge = region_charge - region_formal_charge
                print('INFO: surplus charge: {0:12.8f} in region {1} has been redistributed'.format(surplus_charge,
                                                                                                    region.name))
                for fragment in region.fragments.values():
                    for atom in fragment.atoms:
                        site = system.potential[atom2site[atom.number]]
                        site.M0[0] -= surplus_charge / region_num_atoms
        charge = 0.0
        number_of_sites = 0
        for site in system.potential.values():
            try:
                charge += site.M0[0]
                number_of_sites += 1
            except IndexError:
                continue
        print('INFO: sum of partial charges: {0:12.8f}'.format(charge))
        surplus_charge = formal_charge - charge
        if abs(surplus_charge) > 1.0e-8:
            print('INFO: surplus charge: {0:12.8f}'.format(surplus_charge))
            print('WARNING: this may indicate that an error has occurred')

        # TODO temporary (but probably ends up being permanent) hack to run PDE calculations
        temp_dir = tempfile.mkdtemp(prefix='PyFraME_', dir=self.scratch_dir)
        system_dir = os.path.join(self.work_dir, system.name)
        if not os.path.isdir(system_dir):
            os.makedirs(system_dir)
        os.chdir(system_dir)
        system.write_potential(filename='temp')
        directories = []
        filenames = []
        fragment_sizes = []
        readers = {}
        for region in system.regions.values():
            if not region.use_fragment_densities:
                continue
            writers = []
            combine_calc = False
            if region.use_mfcc:
                fragments = region.mfcc_fragments
            else:
                fragments = region.fragments
            if region.use_fragment_densities and region.use_exchange_repulsion:
                same_program = (region.fragment_density_program == region.exchange_repulsion_program)
                same_model = (region.fragment_density_model == region.exchange_repulsion_model)
                same_method = (
                        region.fragment_density_method == region.exchange_repulsion_method and region.fragment_density_xcfun == region.exchange_repulsion_xcfun)
                same_basis = (region.fragment_density_basis == region.exchange_repulsion_basis)
                combine_calc = (same_program and same_model and same_method and same_basis)
            # TODO handle fragment density only and exchange repulsion only
            if region.use_fragment_densities and region.use_polarizabilities and combine_calc:
                writers.append(f'{region.fragment_density_program}_{region.fragment_density_model}')
            else:
                raise NotImplementedError('Fragment density and exchange repulsion settings must be the same')
            for writer in writers:
                if not hasattr(InputWriters, writer) or not hasattr(ScriptWriters, writer):
                    # TODO replace with exception
                    exit('ERROR: input writer {0} does not exist'.format(writer))
                for fragment in fragments.values():
                    readers[fragment.identifier] = []
                for fragment in fragments.values():
                    os.chdir(system_dir)
                    filename = fragment.identifier + '_' + writer
                    readers[fragment.identifier].append(writer)
                    if os.path.isfile(filename + '.h5'):
                        continue
                    if not os.path.isdir(filename):
                        os.mkdir(filename)
                    os.chdir(filename)
                    getattr(InputWriters, writer)(fragment, region, system.core_region, filename)
                    getattr(ScriptWriters, writer)(filename, system_dir, temp_dir, self.mpi_procs_per_job,
                                                   self.omp_threads_per_job, self.memory_per_job)
                    directories.append(os.path.join(system_dir, filename))
                    filenames.append('{0}.sh'.format(filename))
                    fragment_sizes.append(fragment.number_of_atoms)
                    os.chdir(system_dir)
        shutil.rmtree(temp_dir)
        os.chdir(system_dir)
        if directories and filenames:
            fragment_sizes, directories, filenames = zip(*sorted(zip(fragment_sizes, directories, filenames),
                                                                 reverse=True))
            process_jobs(directories, filenames, self.node_list, self.jobs_per_node, self.comm_port)
            for filename, directory in zip(filenames, directories):
                if os.path.isfile(filename.replace('.sh', '.h5')):
                    if os.path.getsize(filename.replace('.sh', '.h5')) > 0:
                        shutil.rmtree(directory)
        os.remove('temp.pot')
        # PDE post process
        fd_fragments = []
        fd_prefactors = []
        repulsion_factors = []
        # get regions with PDE
        for region in system.regions.values():
            if not region.use_fragment_densities:
                continue
            if region.use_fragment_densities:
                if region.use_mfcc:
                    for fragment in region.fragments.values():
                        fd_fragments.append(fragment.capped_fragment)
                        fd_prefactors.append(1.0)
                        repulsion_factors.append(region.exchange_repulsion_factor)
                        for concap in fragment.concaps.values():
                            if concap in fd_fragments:
                                continue
                            fd_fragments.append(concap)
                            fd_prefactors.append(-1.0)
                            repulsion_factors.append(region.exchange_repulsion_factor)
                else:
                    fd_fragments += region.fragments.values()
                    fd_prefactors += [1.0] * len(fd_fragments)
                    repulsion_factors += [region.exchange_repulsion_factor] * len(fd_fragments)
        # get info for final h5 (dimensions of fock matrix etc.)
        nucel_energy = 0.0
        nuclear_coordinates = []
        nuclear_charges = []
        if fd_fragments:
            # get dimension info for final h5
            with h5py.File(f'{fd_fragments[0].identifier}_dalton_pde.h5', 'r') as fragment_h5:
                num_bas = fragment_h5['core_fragment']['num_bas'][0]
                repulsion_matrix = np.zeros(num_bas*(num_bas+1)//2)
                electrostatic_matrix = np.zeros(num_bas*(num_bas+1)//2)
                num_pols = fragment_h5['fragment']['num_pols'][0]
                fd_static_field = np.zeros(3*num_pols)
            # assemble final h5
            for fragment, prefactor, repulsion_scale_factor in zip(fd_fragments, fd_prefactors, repulsion_factors):
                with h5py.File(f'{fragment.identifier}_dalton_pde.h5', 'r') as fragment_h5:
                    nuclear_coordinates += fragment_h5['fragment']['coordinates']
                    nuclear_charges += [prefactor * charge for charge in fragment_h5['fragment']['charges']]
                    nucel_energy += prefactor * fragment_h5['core_fragment']['nuclear-electron energy'][()]
                    electrostatic_matrix += prefactor * fragment_h5['core_fragment']['electrostatic matrix'][()]
                    repulsion_matrix += prefactor * repulsion_scale_factor * fragment_h5['core_fragment']['exchange-repulsion matrix'][()]
                    fd_static_field += prefactor * fragment_h5['fragment']['electric fields'][()]
            with h5py.File(f'{system.name}.h5', 'w') as combined_h5:
                combined_h5['num_bas'] = num_bas
                combined_h5['electrostatic matrix'] = electrostatic_matrix
                combined_h5['exchange-repulsion matrix'] = repulsion_matrix
                combined_h5['num_nuclei'] = np.int32(len(nuclear_charges))
                combined_h5['nuclear charges'] = nuclear_charges
                combined_h5['nuclear coordinates'] = nuclear_coordinates
                combined_h5['nuclear-electron energy'] = nucel_energy
                combined_h5['num_fields'] = num_pols
                combined_h5['electric fields'] = fd_static_field

    def write_potential(self, system):
        """Write potential file."""
        system_dir = os.path.join(self.work_dir, system.name)
        os.chdir(system_dir)
        system.write_potential()
        os.chdir(self.work_dir)

    def write_core(self, system):
        """Write core region to file."""
        system_dir = os.path.join(self.work_dir, system.name)
        os.chdir(system_dir)
        system.write_core()
        os.chdir(self.work_dir)
