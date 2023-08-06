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

import os
import json
import h5py
import numpy as np

from .utils import element2charge, AA2BOHR

__all__ = ['InputWriters', 'ScriptWriters']


class InputWriters(object):

    @staticmethod
    def dalton_loprop(fragment, region, core_region, filename=None):

        if region.polarizability_order != (1, 1):
            # TODO replace with exception
            exit('ERROR: only dipole-dipole polarizabilities supported with LoProp model in Dalton')
        if region.multipole_order > 2:
            # TODO replace with exception
            exit('ERROR: only up to second order multipoles supported with LoProp model in Dalton')
        if filename is None:
            filename = fragment.identifier + '_loprop'
        elements = [atom.element for atom in fragment.atoms]
        coordinates = [atom.coordinate for atom in fragment.atoms]
        InputWriters.dalton_mol(elements, coordinates, fragment.charge, region.multipole_basis, filename)
        inp = '**DALTON INPUT\n'
        inp += '.RUN RESPONSE\n'
        inp += '.DIRECT\n'
        inp += '**WAVE FUNCTIONS\n'
        inp += '.INTERFACE\n'
        if region.multipole_method == 'DFT':
            inp += '.DFT\n'
            inp += '{0}\n'.format(region.multipole_xcfun)
        elif region.multipole_method == 'HF':
            inp += '.HF\n'
        else:
            # TODO replace with exception
            exit('ERROR: only DFT or HF supported for Dalton LoProp')
        inp += '**INTEGRAL\n'
        inp += '.NOSUP\n'
        inp += '.DIPLEN\n'
        inp += '.SECMOM\n'
        inp += '**RESPONSE\n'
        inp += '*LINEAR\n'
        inp += '.DIPLEN\n'
        inp += '**END OF\n'
        with open('{0}.dal'.format(filename), 'w') as input_file:
            input_file.write(inp)

    @staticmethod
    def dalton_loprop_multipoles(fragment, region, core_region, filename=None):

        if region.multipole_order > 2:
            # TODO replace with exception
            exit('ERROR: only up to second order multipoles supported with LoProp model in Dalton')
        if filename is None:
            filename = fragment.identifier + '_loprop'
        elements = [atom.element for atom in fragment.atoms]
        coordinates = [atom.coordinate for atom in fragment.atoms]
        InputWriters.dalton_mol(elements, coordinates, fragment.charge, region.multipole_basis, filename)
        inp = '**DALTON INPUT\n'
        inp += '.RUN WAVE FUNCTION\n'
        inp += '.DIRECT\n'
        inp += '**WAVE FUNCTIONS\n'
        inp += '.INTERFACE\n'
        if region.multipole_method == 'DFT':
            inp += '.DFT\n'
            inp += '{0}\n'.format(region.multipole_xcfun)
        elif region.multipole_method == 'HF':
            inp += '.HF\n'
        else:
            # TODO replace with exception
            exit('ERROR: only DFT or HF supported for Dalton LoProp')
        inp += '**INTEGRAL\n'
        inp += '.NOSUP\n'
        inp += '.DIPLEN\n'
        inp += '.SECMOM\n'
        inp += '**END OF\n'
        with open('{0}.dal'.format(filename), 'w') as input_file:
            input_file.write(inp)

    @staticmethod
    def dalton_loprop_polarizability(fragment, region, core_region, filename=None):

        if region.polarizability_order != (1, 1):
            # TODO replace with exception
            exit('ERROR: only dipole-dipole polarizabilities supported with LoProp model in MOLCAS')
        if filename is None:
            filename = fragment.identifier + '_loprop'
        elements = [atom.element for atom in fragment.atoms]
        coordinates = [atom.coordinate for atom in fragment.atoms]
        InputWriters.dalton_mol(elements, coordinates, fragment.charge, region.polarizability_basis, filename)
        inp = '**DALTON INPUT\n'
        inp += '.RUN RESPONSE\n'
        inp += '.DIRECT\n'
        inp += '**WAVE FUNCTIONS\n'
        inp += '.INTERFACE\n'
        if region.polarizability_method == 'DFT':
            inp += '.DFT\n'
            inp += '{0}\n'.format(region.polarizability_xcfun)
        elif region.polarizability_method == 'HF':
            inp += '.HF\n'
        else:
            # TODO replace with exception
            exit('ERROR: only DFT or HF supported for Dalton LoProp')
        inp += '**INTEGRAL\n'
        inp += '.NOSUP\n'
        inp += '.DIPLEN\n'
        inp += '**RESPONSE\n'
        inp += '*LINEAR\n'
        inp += '.DIPLEN\n'
        inp += '**END OF\n'
        with open('{0}.dal'.format(filename), 'w') as input_file:
            input_file.write(inp)

    @staticmethod
    def dalton_pde(fragment, region, core_region, filename=None):
        # Monomer calculation
        input_filename = filename
        if input_filename is None:
            filename = f'{fragment.identifier}'
        else:
            filename = f'{filename}'
        monomer_elements = [atom.element for atom in fragment.atoms]
        monomer_charges = [float(element2charge[element]) for element in monomer_elements]
        monomer_coordinates = [atom.coordinate for atom in fragment.atoms]
        core_elements = [atom.element for core_fragment in core_region.fragments.values() for atom in core_fragment.atoms]
        core_charges = [float(element2charge[element]) for element in core_elements]
        core_coordinates = [atom.coordinate for core_fragment in core_region.fragments.values() for atom in core_fragment.atoms]
        InputWriters.dalton_mol(monomer_elements, monomer_coordinates, fragment.charge, region.fragment_density_basis, f'{filename}_monomer')
        with h5py.File(f'{filename}.h5', 'w') as h5:
            # groups
            h5.create_group('core_fragment')
            h5.create_group('fragment')
            h5_core = h5['core_fragment']
            h5_fragment = h5['fragment']
            # core fragment properties
            h5_core['num_nuclei'] = len(core_elements)
            h5_core['charges'] = core_charges
            h5_core['coordinates'] = np.array(core_coordinates) * AA2BOHR
            # this fragment properties
            h5_fragment['num_nuclei'] = len(monomer_elements)
            h5_fragment['coordinates'] = np.array(monomer_coordinates) * AA2BOHR
            h5_fragment['charges'] = monomer_charges
        inp = '**DALTON INPUT\n'
        inp += '.RUN WAVE FUNCTIONS\n'
        inp += '.DIRECT\n'
        inp += '*PEQM\n'
        inp += '.SAVE DENSITY\n'
        inp += f'{filename}.h5\n'
        inp += '**WAVE FUNCTIONS\n'
        if region.fragment_density_method == 'DFT':
            inp += '.DFT\n'
            inp += '{0}\n'.format(region.fragment_density_xcfun)
        elif region.fragment_density_method == 'HF':
            inp += '.HF\n'
        else:
            # TODO replace with exception
            exit('ERROR: only DFT or HF supported for Dalton LoProp')
        inp += '**END OF DALTON INPUT\n'
        with open('{0}_monomer.dal'.format(filename), 'w') as input_file:
            input_file.write(inp)
        # Dimer calculation
        dimer_elements = core_elements + monomer_elements
        dimer_coordinates = core_coordinates + monomer_coordinates
        core_charge = sum([fragment.charge for fragment in core_region.fragments.values()])
        dimer_charge = fragment.charge + core_charge
        dimer_bases = core_region.basis
        if not isinstance(dimer_bases, list):
            dimer_bases = [core_region.basis]*len(core_elements)
        dimer_bases += [region.fragment_density_basis] * len(monomer_elements)
        InputWriters.dalton_mol(dimer_elements, dimer_coordinates, dimer_charge, dimer_bases, f'{filename}_dimer')
        inp = '**DALTON INPUT\n'
        inp += '.RUN WAVE FUNCTIONS\n'
        inp += '.DIRECT\n'
        inp += '*PEQM\n'
        inp += '.TWOINT\n'
        inp += f'{filename}.h5\n'
        inp += '**WAVE FUNCTIONS\n'
        if region.exchange_repulsion_method == 'DFT':
            inp += '.DFT\n'
            inp += '{0}\n'.format(region.exchange_repulsion_xcfun)
        elif region.exchange_repulsion_method == 'HF':
            inp += '.HF\n'
        else:
            # TODO replace with exception
            exit('ERROR: only DFT or HF supported for Dalton LoProp')
        inp += '**END OF DALTON INPUT\n'
        with open('{0}_dimer.dal'.format(filename), 'w') as input_file:
            input_file.write(inp)

    @staticmethod
    def molcas_loprop(fragment, region, core_region, filename=None):

        if region.polarizability_order != (1, 1):
            # TODO replace with exception
            exit('ERROR: only dipole-dipole polarizabilities supported with LoProp model in MOLCAS')
        if filename is None:
            filename = fragment.identifier + '_loprop'
        fragment.write_xyz(filename)
        inp = '&GATEWAY\n'
        inp += 'TITLE = Generated by PyFraME\n'
        inp += 'COORD = {0}.xyz\n'.format(filename)
        inp += 'BASIS = {0}\n'.format(region.multipole_basis)
        inp += 'GROUP = C1\n'
        inp += '&SEWARD\n'
        inp += 'MULT = {0}\n'.format(max(region.multipole_order, 1))
        inp += 'MEDI\n'
        inp += '&SCF\n'
        inp += 'CHARGE = {0}\n'.format(round(fragment.charge))
        inp += 'CHOL\n'
        if region.multipole_method == 'DFT':
            inp += 'KSDFT = {0}\n'.format(region.multipole_xcfun)
        # if fragment.spin_multiplicity:
        #     inp += 'SPIN = {0}\n'.format(fragment.spin_multiplicity)
        #     inp += 'UHF\n'
        inp += '&LOPROP\n'
        inp += 'MPPROP = {0}\n'.format(region.multipole_order)
        if region.atomic_multipoles and region.atomic_polarizabilities:
            inp += 'BOND = 0.0\n'
        elif region.atomic_multipoles or region.atomic_polarizabilities:
            # TODO replace with exception
            exit('ERROR: inconsistency in choice of atomic parameters')
        with open('{0}.inp'.format(filename), 'w') as input_file:
            input_file.write(inp)

    @staticmethod
    def molcas_loprop_multipoles(fragment, region, core_region, filename=None):

        if filename is None:
            filename = fragment.identifier + '_loprop'
        fragment.write_xyz(filename)
        inp = '&GATEWAY\n'
        inp += 'TITLE = Generated by PyFraME\n'
        inp += 'COORD = {0}.xyz\n'.format(filename)
        inp += 'BASIS = {0}\n'.format(region.multipole_basis)
        inp += 'GROUP = C1\n'
        inp += '&SEWARD\n'
        inp += 'MULT = {0}\n'.format(region.multipole_order)
        inp += 'MEDI\n'
        inp += '&SCF\n'
        inp += 'CHARGE = {0}\n'.format(round(fragment.charge))
        inp += 'CHOL\n'
        if region.multipole_method == 'DFT':
            inp += 'KSDFT = {0}\n'.format(region.multipole_xcfun)
        # if fragment.spin_multiplicity:
        #     inp += 'SPIN = {0}\n'.format(fragment.spin_multiplicity)
        #     inp += 'UHF\n'
        inp += '&LOPROP\n'
        inp += 'MPPROP = {0}\n'.format(region.multipole_order)
        inp += 'NOFIELD\n'
        if region.atomic_multipoles:
            inp += 'BOND = 0.0\n'
        with open('{0}.inp'.format(filename), 'w') as input_file:
            input_file.write(inp)

    @staticmethod
    def molcas_loprop_polarizability(fragment, region, core_region, filename=None):

        if region.polarizability_order != (1, 1):
            # TODO replace with exception
            exit('ERROR: only dipole-dipole polarizabilities supported with LoProp model in MOLCAS')
        if filename is None:
            filename = fragment.identifier + '_loprop'
        fragment.write_xyz(filename)
        inp = '&GATEWAY\n'
        inp += 'TITLE = Generated by PyFraME\n'
        inp += 'COORD = {0}.xyz\n'.format(filename)
        inp += 'BASIS = {0}\n'.format(region.polarizability_basis)
        inp += 'GROUP = C1\n'
        inp += '&SEWARD\n'
        inp += 'MULT = 1\n'
        inp += 'MEDI\n'
        inp += '&SCF\n'
        inp += 'CHARGE = {0}\n'.format(round(fragment.charge))
        inp += 'CHOL\n'
        if region.polarizability_method == 'DFT':
            inp += 'KSDFT = {0}\n'.format(region.polarizability_xcfun)
        # if fragment.spin_multiplicity:
        #     inp += 'SPIN = {0}\n'.format(fragment.spin_multiplicity)
        #     inp += 'UHF\n'
        inp += '&LOPROP\n'
        inp += 'MPPROP = -1\n'
        if region.atomic_polarizabilities:
            inp += 'BOND = 0.0\n'
        with open('{0}.inp'.format(filename), 'w') as input_file:
            input_file.write(inp)

    @staticmethod
    def dalton_mol(elements, coordinates, charge, basis, filename):
        """Write Dalton molecule file"""
        if isinstance(basis, list):
            atom_basis = True
        else:
            atom_basis = False
        atom_types = 0
        coordinate_groups = []
        coordinate_group = []
        element_group = []
        basis_group = []
        previous_element = None
        previous_basis = None
        if atom_basis:
            for element, coordinate, basis in zip(elements, coordinates, basis):
                if element != previous_element or basis != previous_basis:
                    coordinate_group = [coordinate]
                    coordinate_groups.append(coordinate_group)
                    element_group.append(element)
                    basis_group.append(basis)
                    atom_types += 1
                else:
                    coordinate_group.append(coordinate)
                previous_element = element
                previous_basis = basis
        else:
            for element, coordinate in zip(elements, coordinates):
                if element != previous_element:
                    coordinate_group = [coordinate]
                    coordinate_groups.append(coordinate_group)
                    element_group.append(element)
                    atom_types += 1
                else:
                    coordinate_group.append(coordinate)
                previous_element = element
        mol = ''
        if atom_basis:
            mol += 'ATOMBASIS\n'
        else:
            mol += 'BASIS\n'
            mol += '{0}\n'.format(basis)
        mol += 'Generated by PyFraME\n'
        mol += '\n'
        mol += 'AtomTypes={0} Charge={1} NoSymmetry Angstrom\n'.format(atom_types, charge)
        if atom_basis:
            for basis, element, coordinate_group in zip(basis_group, element_group,
                                                        coordinate_groups):
                mol += 'Charge={0:.1f} Atoms={1} Basis={2}\n'.format(element2charge[element],
                                                                     len(coordinate_group),
                                                                     basis)
                for coordinate in coordinate_group:
                    mol += '{0:2} {1[0]:12.6f} {1[1]:12.6f} {1[2]:12.6f}\n'.format(element,
                                                                                   coordinate)
        else:
            for element, coordinate_group in zip(element_group, coordinate_groups):
                mol += 'Charge={0:.1f} Atoms={1}\n'.format(element2charge[element],
                                                           len(coordinate_group))
                for coordinate in coordinate_group:
                    mol += '{0:2} {1[0]:12.6f} {1[1]:12.6f} {1[2]:12.6f}\n'.format(element,
                                                                                   coordinate)
        with open('{0}.mol'.format(filename), 'w') as mol_file:
            mol_file.write(mol)

    @staticmethod
    def xyz(elements, coordinates, charge, filename):
        """Write XYZ file"""
        xyz = '{0}\n'.format(len(elements))
        xyz += 'Generated by PyFraME (fragment charge: {0})\n'.format(charge)
        # elements = [atom.element for atom in fragment.atoms]
        # coordinates = [atom.coordinate for atom in fragment.atoms]
        for element, coordinate in zip(elements, coordinates):
            xyz += ('{0} {1[0]:12.6f} {1[1]:12.6f} {1[2]:12.6f}\n'.format(element, coordinate))
        with open('{0}.xyz'.format(filename), 'w') as xyz_file:
            xyz_file.write(xyz)

    @staticmethod
    def dalton_core(system, filename=None):
        """Write Dalton molecule file for core region"""
        if filename is None:
            filename = system.name
        core_fragment = sum(system.core_region.fragments.values())
        if system.core_region.use_caps:
            core_fragment.add_cap_links()
        else:
            core_fragment.add_hydrogen_links()
        elements = [atom.element for atom in core_fragment.atoms]
        coordinates = [atom.coordinate for atom in core_fragment.atoms]
        charge = round(core_fragment.charge)
        bases = system.core_region.basis
        if isinstance(bases, list):
            atom_basis = True
            for atom in core_fragment.atoms:
                if 'link' in atom.name:
                    bases.append('STO-3G')
                elif 'cap' in atom.name:
                    bases.append('CAP ECP=CAP')
        else:
            if system.core_region.use_caps:
                bases = []
                for atom in core_fragment.atoms:
                    if 'link' in atom.name:
                        bases.append('STO-3G')
                    elif 'cap' in atom.name:
                        bases.append('CAP ECP=CAP')
                    else:
                        bases.append('{0}'.format(system.core_region.basis))
                atom_basis = True
            else:
                atom_basis = False
        atom_types = 0
        coordinate_groups = []
        coordinate_group = []
        element_group = []
        basis_group = []
        previous_element = None
        previous_basis = None
        if atom_basis:
            for element, coordinate, basis in zip(elements, coordinates, bases):
                if element != previous_element or basis != previous_basis:
                    coordinate_group = [coordinate]
                    coordinate_groups.append(coordinate_group)
                    element_group.append(element)
                    basis_group.append(basis)
                    atom_types += 1
                else:
                    coordinate_group.append(coordinate)
                previous_element = element
                previous_basis = basis
        else:
            for element, coordinate in zip(elements, coordinates):
                if element != previous_element:
                    coordinate_group = [coordinate]
                    coordinate_groups.append(coordinate_group)
                    element_group.append(element)
                    atom_types += 1
                else:
                    coordinate_group.append(coordinate)
                previous_element = element
        mol = ''
        if atom_basis:
            mol += 'ATOMBASIS\n'
        else:
            mol += 'BASIS\n'
            mol += '{0}\n'.format(bases)
        mol += 'Core region\n'
        mol += 'Generated by PyFraME\n'
        mol += 'AtomTypes={0} Charge={1} NoSymmetry Angstrom\n'.format(atom_types, charge)
        if atom_basis:
            for basis, element, coordinate_group in zip(basis_group, element_group,
                                                        coordinate_groups):
                mol += 'Charge={0:.1f} Atoms={1} Basis={2}\n'.format(element2charge[element],
                                                                     len(coordinate_group),
                                                                     basis)
                for coordinate in coordinate_group:
                    mol += '{0:2} {1[0]:12.6f} {1[1]:12.6f} {1[2]:12.6f}\n'.format(element,
                                                                                   coordinate)
        else:
            for element, coordinate_group in zip(element_group, coordinate_groups):
                mol += 'Charge={0:.1f} Atoms={1}\n'.format(element2charge[element],
                                                           len(coordinate_group))
                for coordinate in coordinate_group:
                    mol += '{0:2} {1[0]:12.6f} {1[1]:12.6f} {1[2]:12.6f}\n'.format(element,
                                                                                   coordinate)
        with open('{0}.mol'.format(filename), 'w') as mol_file:
            mol_file.write(mol)

    @staticmethod
    def pelib_potential(system, filename=None):
        """Write potential file for PyFraME"""
        if filename is None:
            filename = system.name
        elements = {}
        coordinates = {}
        multipoles = {}
        polarizabilities = {}
        exclusion_lists = {}
        for index, site in system.potential.items():
            for i in range(7):
                mx = 'M{0}'.format(i)
                if hasattr(site, mx) and getattr(site, mx):
                    if mx not in multipoles:
                        multipoles[mx] = {}
                for j in range(i + 1):
                    pxy = 'P{0}{1}'.format(j, i)
                    if hasattr(site, pxy) and getattr(site, pxy):
                        if pxy not in polarizabilities:
                            polarizabilities[pxy] = {}
        for index, site in system.potential.items():
            elements[index] = site.element
            coordinates[index] = site.coordinate
            for i in range(7):
                mx = 'M{0}'.format(i)
                if hasattr(site, mx) and getattr(site, mx):
                    multipoles[mx][index] = getattr(site, mx)
                for j in range(i + 1):
                    pxy = 'P{0}{1}'.format(j, i)
                    if hasattr(site, pxy) and getattr(site, pxy):
                        polarizabilities[pxy][index] = getattr(site, pxy)
            if site.exclusion_list:
                exclusion_lists[index] = site.exclusion_list
        length = len(str(len(elements))) + 1
        pot = '! Generated by PyFraME\n'
        # TODO write system info
        pot += '@COORDINATES\n'
        pot += '{0}\n'.format(len(elements))
        pot += 'AA\n'
        indices = sorted(elements.keys())
        for index in indices:
            pot += '{0:2} {1[0]:14.8f} {1[1]:14.8f} {1[2]:14.8f}'.format(elements[index],
                                                                         coordinates[index])
            pot += ' {0:{1}d}\n'.format(index, length+4)
        if multipoles:
            pot += '@MULTIPOLES\n'
            for i in range(7):
                mx = 'M{0}'.format(i)
                if mx in multipoles:
                    pot += 'ORDER {0}\n'.format(i)
                    pot += '{0}\n'.format(len(multipoles[mx]))
                    indices = sorted(multipoles[mx].keys())
                    for index in indices:
                        pot += '{0:<{1}d}'.format(index, length)
                        for comp in multipoles[mx][index]:
                            pot += ' {0:14.8f}'.format(comp)
                        pot += '\n'
        if polarizabilities:
            pot += '@POLARIZABILITIES\n'
            for i in range(7):
                for j in range(i + 1):
                    pxy = 'P{0}{1}'.format(j, i)
                    if pxy in polarizabilities:
                        pot += 'ORDER {0} {1}\n'.format(j, i)
                        pot += '{0}\n'.format(len(polarizabilities[pxy]))
                        indices = sorted(polarizabilities[pxy].keys())
                        for index in indices:
                            pot += '{0:<{1}d}'.format(index, length)
                            for comp in polarizabilities[pxy][index]:
                                pot += ' {0:14.8f}'.format(comp)
                            pot += '\n'
            if exclusion_lists:
                # TODO padding with zeros
                exc_list_length = 0
                for exc_list in exclusion_lists.values():
                    if exc_list_length < len(exc_list):
                        exc_list_length = len(exc_list)
                for exc_list in exclusion_lists.values():
                    exc_diff = exc_list_length - len(exc_list)
                    if exc_diff:
                        exc_list.extend([0] * exc_diff)
                pot += 'EXCLISTS\n'
                pot += '{0} {1}\n'.format(len(exclusion_lists), exc_list_length + 1)
                for index, exc_list in exclusion_lists.items():
                    pot += '{0:<{1}d}'.format(index, length)
                    for exc in exc_list:
                        pot += ' {0:{1}d}'.format(exc, length)
                    pot += '\n'
        with open('{0}.pot'.format(filename), 'w') as pot_file:
            pot_file.write(pot)

    @staticmethod
    def frame_potential(system, filename=None):
        """Write potential file for FraME"""
        if filename is None:
            filename = system.name
        elements = {}
        coordinates = {}
        multipoles = {}
        polarizabilities = {}
        exclusion_lists = {}
        for index, site in system.potential.items():
            for i in range(7):
                mx = 'M{0}'.format(i)
                if hasattr(site, mx) and getattr(site, mx):
                    if mx not in multipoles:
                        multipoles[mx] = {}
                for j in range(i + 1):
                    pxy = 'P{0}{1}'.format(j, i)
                    if hasattr(site, pxy) and getattr(site, pxy):
                        if pxy not in polarizabilities:
                            polarizabilities[pxy] = {}
        for index, site in system.potential.items():
            elements[index] = site.element
            coordinates[index] = site.coordinate
            for i in range(7):
                mx = 'M{0}'.format(i)
                if hasattr(site, mx) and getattr(site, mx):
                    multipoles[mx][index] = getattr(site, mx)
                for j in range(i + 1):
                    pxy = 'P{0}{1}'.format(j, i)
                    if hasattr(site, pxy) and getattr(site, pxy):
                        polarizabilities[pxy][index] = getattr(site, pxy)
            if site.exclusion_list:
                exclusion_lists[index] = site.exclusion_list
        length = len(str(len(elements))) + 1
        pot = '! Generated by PyFraME\n'
        # TODO write system info
        pot += '@COORDINATES\n'
        pot += '{0}\n'.format(len(elements))
        pot += 'AA\n'
        indices = sorted(elements.keys())
        for index in indices:
            pot += '{0:2} {1[0]:14.8f} {1[1]:14.8f} {1[2]:14.8f}'.format(elements[index],
                                                                         coordinates[index])
            pot += ' {0:{1}d}\n'.format(index, length + 4)
        if multipoles:
            pot += '@MULTIPOLES\n'
            for i in range(7):
                mx = 'M{0}'.format(i)
                if mx in multipoles:
                    pot += 'ORDER {0}\n'.format(i)
                    pot += '{0}\n'.format(len(multipoles[mx]))
                    indices = sorted(multipoles[mx].keys())
                    for index in indices:
                        pot += '{0:<{1}d}'.format(index, length)
                        for comp in multipoles[mx][index]:
                            pot += ' {0:14.8f}'.format(comp)
                        pot += '\n'
        if polarizabilities:
            pot += '@POLARIZABILITIES\n'
            for i in range(7):
                for j in range(i + 1):
                    pxy = 'P{0}{1}'.format(j, i)
                    if pxy in polarizabilities:
                        pot += 'ORDER {0} {1}\n'.format(j, i)
                        pot += '{0}\n'.format(len(polarizabilities[pxy]))
                        indices = sorted(polarizabilities[pxy].keys())
                        for index in indices:
                            pot += '{0:<{1}d}'.format(index, length)
                            for comp in polarizabilities[pxy][index]:
                                pot += ' {0:14.8f}'.format(comp)
                            pot += '\n'
        if exclusion_lists:
            # TODO padding with zeros
            exc_list_length = 0
            for exc_list in exclusion_lists.values():
                if exc_list_length < len(exc_list):
                    exc_list_length = len(exc_list)
            for exc_list in exclusion_lists.values():
                exc_diff = exc_list_length - len(exc_list)
                if exc_diff:
                    exc_list.extend([0] * exc_diff)
            pot += 'EXCLISTS\n'
            pot += '{0} {1}\n'.format(len(exclusion_lists), exc_list_length + 1)
            for index, exc_list in exclusion_lists.items():
                pot += '{0:<{1}d}'.format(index, length)
                for exc in exc_list:
                    pot += ' {0:{1}d}'.format(exc, length)
                pot += '\n'
        with open('{0}.pot'.format(filename), 'w') as pot_file:
            json.dump(pot, pot_file, ensure_ascii=False)


class ScriptWriters(object):

    @staticmethod
    def dalton_loprop(filename, work_dir, scratch_dir, mpi_procs, omp_threads, memory):
        """Writes run script for Dalton LoProp calculation"""
        temp_dir = os.path.join(scratch_dir, filename)
        script = '#!/usr/bin/env bash\n'
        script += 'export PATH={0}\n'.format(os.environ['PATH'])
        if 'LD_LIBRARY_PATH' in os.environ:
            script += 'export LD_LIBRARY_PATH={0}\n'.format(os.environ['LD_LIBRARY_PATH'])
        script += 'export DALTON_NUM_MPI_PROCS={0:d}\n'.format(mpi_procs)
        script += 'export OMP_NUM_THREADS={0:d}\n'.format(omp_threads)
        script += 'export DALTON_TMPDIR={0}\n'.format(temp_dir)
        script += 'mkdir -p $DALTON_TMPDIR\n'
        script += 'cd {0}\n'.format(os.path.join(work_dir, filename))
        script += 'dalton -d -noarch -nobackup -mb {0:d}'.format(int(memory / mpi_procs))
        script += ' -get "AOONEINT DALTON.BAS SIRIFC AOPROPER RSPVEC"'
        script += ' -o ../{0}.log -dal {0}.dal -mol {0}.mol\n'.format(filename)
        script += 'bzip2 --best {1}/{0}.log\n'.format(filename, work_dir)
        script += 'mv {0}.AOONEINT AOONEINT\n'.format(filename)
        script += 'mv {0}.DALTON.BAS DALTON.BAS\n'.format(filename)
        script += 'mv {0}.SIRIFC SIRIFC\n'.format(filename)
        script += 'mv {0}.AOPROPER AOPROPER\n'.format(filename)
        script += 'mv {0}.RSPVEC RSPVEC\n'.format(filename)
        script += 'loprop -v -t . -A -a 2 --decimal 10 > {0}/{1}.out\n'.format(work_dir, filename)
        script += 'rm -f AOONEINT DALTON.BAS SIRIFC AOPROPER RSPVEC\n'
        with open('{0}.sh'.format(filename), 'w') as script_file:
            script_file.write(script)

    @staticmethod
    def dalton_loprop_polarizability(filename, work_dir, scratch_dir, mpi_procs, omp_threads, memory):
        """Writes run script for Dalton LoProp calculation"""
        temp_dir = os.path.join(scratch_dir, filename)
        script = '#!/usr/bin/env bash\n'
        script += 'export PATH={0}\n'.format(os.environ['PATH'])
        if 'LD_LIBRARY_PATH' in os.environ:
            script += 'export LD_LIBRARY_PATH={0}\n'.format(os.environ['LD_LIBRARY_PATH'])
        script += 'export DALTON_NUM_MPI_PROCS={0:d}\n'.format(mpi_procs)
        script += 'export OMP_NUM_THREADS={0:d}\n'.format(omp_threads)
        script += 'export DALTON_TMPDIR={0}\n'.format(temp_dir)
        script += 'mkdir -p $DALTON_TMPDIR\n'
        script += 'cd {0}\n'.format(os.path.join(work_dir, filename))
        script += 'dalton -d -noarch -nobackup -mb {0:d}'.format(int(memory / mpi_procs))
        script += ' -get "AOONEINT DALTON.BAS SIRIFC AOPROPER RSPVEC"'
        script += ' -o ../{0}.log -dal {0}.dal -mol {0}.mol\n'.format(filename)
        script += 'bzip2 --best {1}/{0}.log\n'.format(filename, work_dir)
        script += 'mv {0}.AOONEINT AOONEINT\n'.format(filename)
        script += 'mv {0}.DALTON.BAS DALTON.BAS\n'.format(filename)
        script += 'mv {0}.SIRIFC SIRIFC\n'.format(filename)
        script += 'mv {0}.AOPROPER AOPROPER\n'.format(filename)
        script += 'mv {0}.RSPVEC RSPVEC\n'.format(filename)
        script += 'loprop -v -t . -A -a 2 -l -1 --decimal 10 > {0}/{1}.out\n'.format(work_dir, filename)
        script += 'rm -f AOONEINT DALTON.BAS SIRIFC AOPROPER RSPVEC\n'
        with open('{0}.sh'.format(filename), 'w') as script_file:
            script_file.write(script)

    @staticmethod
    def dalton_loprop_multipoles(filename, work_dir, scratch_dir, mpi_procs, omp_threads, memory):
        """Writes run script for Dalton LoProp calculation"""
        temp_dir = os.path.join(scratch_dir, filename)
        script = '#!/usr/bin/env bash\n'
        script += 'export PATH={0}\n'.format(os.environ['PATH'])
        if 'LD_LIBRARY_PATH' in os.environ:
            script += 'export LD_LIBRARY_PATH={0}\n'.format(os.environ['LD_LIBRARY_PATH'])
        script += 'export DALTON_NUM_MPI_PROCS={0:d}\n'.format(mpi_procs)
        script += 'export OMP_NUM_THREADS={0:d}\n'.format(omp_threads)
        script += 'export DALTON_TMPDIR={0}\n'.format(temp_dir)
        script += 'mkdir -p $DALTON_TMPDIR\n'
        script += 'cd {0}\n'.format(os.path.join(work_dir, filename))
        script += 'dalton -d -noarch -nobackup -mb {0:d}'.format(int(memory / mpi_procs))
        script += ' -get "AOONEINT DALTON.BAS SIRIFC AOPROPER"'
        script += ' -o ../{0}.log -dal {0}.dal -mol {0}.mol\n'.format(filename)
        script += 'bzip2 --best {1}/{0}.log\n'.format(filename, work_dir)
        script += 'mv {0}.AOONEINT AOONEINT\n'.format(filename)
        script += 'mv {0}.DALTON.BAS DALTON.BAS\n'.format(filename)
        script += 'mv {0}.SIRIFC SIRIFC\n'.format(filename)
        script += 'mv {0}.AOPROPER AOPROPER\n'.format(filename)
        script += 'mv {0}.RSPVEC RSPVEC\n'.format(filename)
        script += 'loprop -v -t . -A --decimal 10 > {0}/{1}.out\n'.format(work_dir, filename)
        script += 'rm -f AOONEINT DALTON.BAS SIRIFC AOPROPER RSPVEC\n'
        with open('{0}.sh'.format(filename), 'w') as script_file:
            script_file.write(script)

    @staticmethod
    def dalton_pde(filename, work_dir, scratch_dir, mpi_procs, omp_threads, memory):
        """Writes run script for Dalton PDE calculation"""
        temp_dir = os.path.join(scratch_dir, filename)
        script = '#!/usr/bin/env bash\n'
        script += 'export PATH={0}\n'.format(os.environ['PATH'])
        if 'LD_LIBRARY_PATH' in os.environ:
            script += 'export LD_LIBRARY_PATH={0}\n'.format(os.environ['LD_LIBRARY_PATH'])
        script += 'export DALTON_NUM_MPI_PROCS={0:d}\n'.format(mpi_procs)
        script += 'export OMP_NUM_THREADS={0:d}\n'.format(omp_threads)
        script += 'export DALTON_TMPDIR={0}\n'.format(temp_dir)
        script += 'mkdir -p $DALTON_TMPDIR\n'
        script += 'cd {0}\n'.format(os.path.join(work_dir, filename))
        script += f'cp {work_dir}/temp.pot {work_dir}/{filename}/{filename}_monomer.pot\n'
        script += 'dalton -d -noarch -nobackup -mb {0:d}'.format(int(memory / mpi_procs))
        script += f' -put {filename}.h5'
        script += f' -get {filename}.h5'
        script += f' -o ../{filename}_monomer.log -dal {filename}_monomer.dal -mol {filename}_monomer.mol -pot {filename}_monomer.pot\n'
        script += f'bzip2 --best {work_dir}/{filename}_monomer.log\n'
        script += f'mv {filename}_monomer.{filename}.h5 {filename}.h5\n'
        script += 'dalton -d -noarch -nobackup -mb {0:d}'.format(int(memory / mpi_procs))
        script += f' -put {filename}.h5'
        script += f' -get {filename}.h5'
        script += f' -o ../{filename}_dimer.log -dal {filename}_dimer.dal -mol {filename}_dimer.mol\n'
        script += f'bzip2 --best {work_dir}/{filename}_dimer.log\n'
        script += f'mv {filename}_dimer.{filename}.h5 {work_dir}/{filename}.h5'
        with open(f'{filename}.sh', 'w') as script_file:
            script_file.write(script)

    @staticmethod
    def molcas_loprop(filename, work_dir, scratch_dir, mpi_procs, omp_threads, memory):
        """Writes run script for MOLCAS LoProp calculation"""
        temp_dir = os.path.join(scratch_dir, filename)
        script = '#!/usr/bin/env bash\n'
        script += 'export PATH={0}\n'.format(os.environ['PATH'])
        if 'LD_LIBRARY_PATH' in os.environ:
            script += 'export LD_LIBRARY_PATH={0}\n'.format(os.environ['LD_LIBRARY_PATH'])
        script += 'export MOLCAS={0}\n'.format(os.environ['MOLCAS'])
        if 'MOLCAS_LICENSE' in os.environ:
            script += 'export MOLCAS_LICENSE={0}\n'.format(os.environ['MOLCAS_LICENSE'])
        script += 'export MOLCAS_MEM={0}\n'.format(int(memory / mpi_procs))
        script += 'export MOLCAS_CPUS={0:d}\n'.format(mpi_procs)
        script += 'export MOLCAS_NEW_WORKDIR="YES"\n'
        script += 'export MOLCAS_OUTPUT="WORKDIR"\n'
        script += 'export OMP_NUM_THREADS={0:d}\n'.format(omp_threads)
        script += 'export WorkDir={0}\n'.format(temp_dir)
        script += 'mkdir -p $WorkDir\n'
        script += 'cd {0}\n'.format(os.path.join(work_dir, filename))
        script += 'molcas {0}.inp > {1}/{0}.log\n'.format(filename, work_dir)
        script += 'bzip2 --best {1}/{0}.log\n'.format(filename, work_dir)
        script += 'cp {0}/{1}.MpProp {2}/{1}.out\n'.format(temp_dir, filename, work_dir)
        with open('{0}.sh'.format(filename), 'w') as script_file:
            script_file.write(script)

    @staticmethod
    def molcas_loprop_polarizability(*args):
        ScriptWriters.molcas_loprop(*args)

    @staticmethod
    def molcas_loprop_multipoles(*args):
        ScriptWriters.molcas_loprop(*args)
