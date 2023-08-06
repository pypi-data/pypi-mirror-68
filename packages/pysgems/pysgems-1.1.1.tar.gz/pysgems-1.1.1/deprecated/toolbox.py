#  Copyright (c) 2020. Robin Thibaut, Ghent University

import os
import shutil
import struct
import subprocess
import time
import uuid
import xml.etree.ElementTree as ET
from os.path import join as jp

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from shapely.geometry import Point, Polygon


def datread(file=None, start=0, end=None):
    # end must be set to None and NOT -1
    """Reads space separated dat file"""
    with open(file, 'r') as fr:
        lines = np.copy(fr.readlines())[start:end]
        try:
            op = np.array([list(map(float, line.split())) for line in lines])
        except ValueError:
            op = [line.split() for line in lines]
    return op


def joinlist(j, mylist):
    """
    Function that joins an array of numbers with j as separator. For example, joinlist('^', [1,2]) returns 1^2
    """
    gp = j.join(map(str, mylist))

    return gp


def blocks_from_rc(rows, columns, layers, xo=0, yo=0, zo=0):
    """
    Yields blocks defining grid cells
    :param rows: array of x-widths along a row
    :param columns: array of y-widths along a column
    :param xo: x origin
    :param yo: y origin
    :return: generator of (cell node number, block vertices coordinates, block center)
    """
    # TODO: adapt to 3D
    nrow = len(rows)
    ncol = len(columns)
    nlay = len(layers)
    delr = rows
    delc = columns
    dell = layers
    r_sum = np.cumsum(delr) + yo
    c_sum = np.cumsum(delc) + xo
    l_sum = np.cumsum(delc) + zo

    def get_node(r, c, h):
        """
        Get node index to fix hard data
        :param r: row number
        :param c: column number
        :param h: layer number
        :return: node number
        """
        nrc = nrow*ncol
        return int((h * nrc) + (r * ncol) + c)

    for k in range(nlay):
        for i in range(nrow):
            for j in range(ncol):
                b = [
                     [c_sum[j] - delc[j], r_sum[i] - delr[i], l_sum[k] - dell[k]],
                     [c_sum[j],           r_sum[i] - delr[i], l_sum[k] - dell[k]],
                     [c_sum[j] - delc[j], r_sum[i],           l_sum[k] - dell[k]],
                     [c_sum[j],           r_sum[i],           l_sum[k] - dell[k]],

                     [c_sum[j] - delc[j], r_sum[i] - delr[i], l_sum[k]],
                     [c_sum[j],           r_sum[i] - delr[i], l_sum[k]],
                     [c_sum[j] - delc[j], r_sum[i],           l_sum[k]],
                     [c_sum[j],           r_sum[i],           l_sum[k]]
                    ]
                yield get_node(i, j, k), np.array(b), np.mean(b, axis=0)


def write_point_set(file_name, sub_dataframe, nodata=-999):
    # TODO: build similar method to save grid files.
    """
    Function to write sgems binary point set files.

    The Simulacre_input_filter class is a filter that can read the default file
    format of GsTLAppli. The format is a binary format, with big endian byte
    order. Following are a description of the file formats for the pointset and
    the cartesian grid objects. All file formats begin with magic number
    0xB211175D, a string indicating the type of object stored in the file, the
    name of the object, and a version number (Q_INT32). The rest is specific
    to the object stored:

     - point-set:
        a Q_UINT32 indicating the number of points in the object.
        a Q_UINT32 indicating the number of properties in the object
        strings containing the names of the properties
        the x,y,z coordinates of each point, as floats
        all the property values, one property at a time, in the order specified
        by the strings of names, as floats. For each property there are as many
        values as points in the point-set.

     - cartesian grid:
        3 Q_UINT32 indicating the number of cells in the x,y,z directions
        3 floats for the dimensions of a single cell
        3 floats for the origin of the grid
        a Q_UINT32 indicating the number of properties
        all the property values, one property at a time, in the order specified
        by the strings of names, as floats. For each property, there are nx*ny*nz
        values (nx,ny,nz are the number of cells in the x,y,z directions).

    :param nodata: nodata value, rows containing this value are omitted.
    :param file_name:
    :param sub_dataframe: Sub-frame of the feature to be exported [x, y, feature value]
    :return:
    """

    # First, rows with no data occurrence are popped
    sub_dataframe = sub_dataframe[(sub_dataframe != nodata).all(axis=1)]

    xyz = np.vstack(
        (sub_dataframe['x'],
         sub_dataframe['y'],
         np.zeros(len(sub_dataframe)))  # 0 column for z
    ).T  # We need X Y Z coordinates even if working in 2D

    pp = sub_dataframe.columns[-1]  # Get name of the property

    grid_name = '{}_grid'.format(pp)

    ext = '.sgems'
    if ext not in file_name:
        file_name += ext

    with open(file_name, 'wb') as wb:
        wb.write(struct.pack('i', int(1.561792946e+9)))  # Magic number
        wb.write(struct.pack('>i', 10))  # Length of 'Point_set' + 1

    with open(file_name, 'a') as wb:
        wb.write('Point_set')  # Type of file

    with open(file_name, 'ab') as wb:
        wb.write(struct.pack('>b', 0))  # Signed character 0 after str

    with open(file_name, 'ab') as wb:
        wb.write(struct.pack('>i', len(grid_name)+1))  # Length of 'grid' + 1

    with open(file_name, 'a') as wb:
        wb.write(grid_name)  # Name of the grid on which points are saved

    with open(file_name, 'ab') as wb:
        wb.write(struct.pack('>b', 0))  # Signed character 0 after str

    with open(file_name, 'ab') as wb:
        wb.write(struct.pack('>i', 100))  # version number
        wb.write(struct.pack('>i', len(xyz)))  # n data points
        wb.write(struct.pack('>i', 1))  # n property

    with open(file_name, 'ab') as wb:
        wb.write(struct.pack('>i', len(pp)+1))  # Length of property name + 1

    with open(file_name, 'a') as wb:
        wb.write(pp)  # Property name

    with open(file_name, 'ab') as wb:
        wb.write(struct.pack('>b', 0))  # Signed character 0 after str

    with open(file_name, 'ab') as wb:
        for c in xyz:
            ttt = struct.pack('>fff', c[0], c[1], c[2])  # Coordinates x, y, z
            wb.write(ttt)

    with open(file_name, 'ab') as wb:
        for v in sub_dataframe[pp]:
            wb.write(struct.pack('>f', v))  # Values


class Sgems:

    def __init__(self,
                 cwd='',
                 data_dir='',
                 file_name='',
                 res_dir=None,
                 dx=1, dy=1, dz=1,
                 xo=None, yo=None, zo=None,
                 x_lim=None, y_lim=None, z_lim=None,
                 nodata=-999):

        # Directories
        if not cwd:
            self.cwd = os.path.dirname(os.getcwd())  # Main directory
        else:
            self.cwd = cwd
        self.algo_dir = jp(self.cwd, 'algorithms')  # algorithms directory
        self.data_dir = data_dir  # data directory
        self.res_dir = res_dir  # result dir initiated when modifying xml file if none given
        self.file_name = file_name  # data file name

        # Grid geometry - use self.generate_grid() to update values
        self.dx = dx  # Block x-dimension
        self.dy = dy  # Block y-dimension
        self.dz = dz  # Block z-dimension
        self.xo = xo
        self.yo = yo
        self.zo = zo
        self.x_lim = x_lim
        self.y_lim = y_lim
        self.z_lim = z_lim
        self.nrow = 1
        self.ncol = 1
        self.nlay = 1
        self.along_r = [1]
        self.along_c = [1]
        self.along_l = [1]
        self.bounding_box = None

        # Data
        self.raw_data = None
        self.project_name = ''
        self.columns = None
        self.xyz = None
        self.dataframe = None
        if file_name:
            self.file_path = jp(self.data_dir, file_name)
            self.load_dataframe()
            self.generate_grid(xo=self.xo, yo=self.yo, zo=self.zo,
                               x_lim=self.x_lim, y_lim=self.y_lim, z_lim=self.z_lim)
            self.node_file = jp(os.path.dirname(self.file_path), 'nodes.npy')  # nodes files
            self.node_value_file = jp(os.path.dirname(self.file_path), 'fnodes.txt')
            self.dis_file = jp(os.path.dirname(self.file_path), 'dis.info')

        self.nodata = nodata
        self.hard_data_objects = []  # List of names of hard data
        self.object_file_names = []  # List containing file names of point sets that will be loaded

        # Algorithm XML
        self.tree = None
        self.root = None
        self.auto_update = False  # Experimental feature to auto fill XML and saving binary files
        dir_path = os.path.abspath(__file__ + "/../")
        self.template_file = jp(dir_path, 'script_templates/script_template.py')  # Python template file path

    # Load sgems dataset
    def loader(self):
        """Parse dataset in GSLIB format"""
        project_info = datread(self.file_path, end=2)  # Name, n features
        project_name = project_info[0][0].lower()  # Project name (lowered)
        n_features = int(project_info[1][0])  # Number of features len([x, y, f1, f2... fn])
        head = datread(self.file_path, start=2, end=2 + n_features)  # Name of features (x, y, z, f1...)
        columns_name = [h[0].lower() for h in head] # Column names (lowered)
        data = datread(self.file_path, start=2 + n_features)  # Raw data
        return data, project_name, columns_name

    def load_dataframe(self):
        """
        Loads sgems data set.
        Assumes that x, y, z are the first three columns and are labeled as such.
        """
        # At this time, considers only 2D dataset
        self.raw_data, self.project_name, self.columns = self.loader()
        self.dataframe = pd.DataFrame(data=self.raw_data, columns=self.columns)
        try:
            self.xyz = self.dataframe[['x', 'y', 'z']].to_numpy()
        except KeyError:  # Assumes 2D dataset
            self.dataframe.insert(2, 'z', np.zeros(self.dataframe.shape[0]))
            self.columns = list(self.dataframe.columns.values)
            self.xyz = self.dataframe[['x', 'y', 'z']].to_numpy()
            self.dz = 0
        self.generate_grid(xo=self.xo, yo=self.yo, zo=self.zo,
                           x_lim=self.x_lim, y_lim=self.y_lim, z_lim=self.z_lim)
        self.node_file = jp(os.path.dirname(self.file_path), 'nodes.npy')  # nodes files
        self.node_value_file = jp(os.path.dirname(self.file_path), 'fnodes.txt')
        self.dis_file = jp(os.path.dirname(self.file_path), 'dis.info')

    def generate_grid(self, xo=None, yo=None, zo=None, x_lim=None, y_lim=None, z_lim=None):
        """
        Constructs the grid geometry. The user can not control directly the number of rows and columns
        but instead inputs the cell size in x and y dimensions.
        xo, yo, x_lim, y_lim, defining the bounding box of the grid, are None by default, and are computed
        based on the data points distribution.
        :param xo:
        :param yo:
        :param zo:
        :param x_lim:
        :param y_lim:
        :param z_lim:
        """

        if x_lim is None:
            x_lim = self.dataframe['x'].max() + self.dx * 4
        if y_lim is None:
            y_lim = self.dataframe['y'].max() + self.dy * 4
        if z_lim is None:
            z_lim = self.dataframe['z'].max() + self.dz * 4

        if xo is None:
            xo = self.dataframe['x'].min() - self.dx * 4
        if yo is None:
            yo = self.dataframe['y'].min() - self.dy * 4
        if zo is None:
            zo = self.dataframe['z'].min() - self.dz * 4

        if self.dy > 0:
            nrow = int((y_lim - yo) // self.dy)  # Number of rows
        else:
            nrow = 1
        if self.dx > 0:
            ncol = int((x_lim - xo) // self.dx)  # Number of columns
        else:
            ncol = 1
        if self.dz > 0:
            nlay = int((z_lim - zo) // self.dz)  # Number of layers
        else:
            nlay = 1

        along_r = np.ones(ncol) * self.dx  # Size of each cell along y-dimension - rows
        along_c = np.ones(nrow) * self.dy  # Size of each cell along x-dimension - columns
        along_l = np.ones(nlay) * self.dz  # Size of each cell along x-dimension - columns

        self.xo = xo
        self.yo = yo
        self.zo = zo
        self.x_lim = x_lim
        self.y_lim = y_lim
        self.z_lim = z_lim
        self.nrow = nrow
        self.ncol = ncol
        self.nlay = nlay
        self.along_r = along_r
        self.along_c = along_c
        self.along_l = along_l

    def my_node(self, xyz):
        """
        Given a point coordinate xy [x, y], computes its node number by computing the euclidean distance of each cell
        center.
        :param xyz:  x, y, z coordinate of data point
        :return:
        """
        start = time.time()
        rn = np.array(xyz)
        # first check if point is within the grid
        p_xy = Point([rn[0], rn[1]])
        p_xz = Point([rn[0], rn[2]])
        poly_xy = Polygon([(self.xo, self.yo), (self.x_lim, self.yo), (self.x_lim, self.y_lim), (self.xo, self.y_lim)])
        poly_xz = Polygon([(self.xo, self.zo), (self.x_lim, self.zo), (self.x_lim, self.z_lim), (self.xo, self.z_lim)])

        if self.dz == 0:
            crit = p_xy.within(poly_xy)
        else:
            crit = p_xy.within(poly_xy) and p_xz.within(poly_xz)

        if crit:
            if self.dz > 0:
                dmin = np.min([self.dx, self.dy, self.dz]) / 2
            else:
                dmin = np.min([self.dx, self.dy]) / 2

            blocks = blocks_from_rc(self.along_c, self.along_r, self.along_l,
                                    self.xo, self.yo, self.zo)
            vmin = np.inf
            cell = None
            for b in blocks:
                c = b[2]
                dc = np.linalg.norm(rn - c)  # Euclidean distance
                if dc <= dmin:  # If point is inside cell
                    print('found 1 node in {} s'.format(time.time()-start))
                    return b[0]
                if dc < vmin:
                    vmin = dc
                    cell = b[0]
            print('found 1 node in {} s'.format(time.time() - start))
            return cell
        else:
            return self.nodata

    def compute_nodes(self):
        """
        Determines node location for each data point.
        It is necessary to know the node number to assign the hard data property to the sgems grid.
        :return: nodes number
        """
        nodes = np.array([self.my_node(c) for c in self.xyz])

        np.save(self.node_file, nodes)  # Save to nodes to avoid recomputing each time

    def get_nodes(self):

        npar = np.array([self.dx, self.dy, self.dz,
                         self.xo, self.yo, self.zo,
                         self.x_lim, self.y_lim, self.z_lim,
                         self.nrow, self.ncol, self.nlay])

        if os.path.isfile(self.dis_file):  # Check previous grid info
            pdis = np.loadtxt(self.dis_file)
            # If different, recompute data points node by deleting previous node file
            if not np.array_equal(pdis, npar):
                print('New grid found')
                try:
                    os.remove(self.node_file)
                    os.remove(self.node_value_file)
                except FileNotFoundError:
                    pass
                finally:
                    np.savetxt(self.dis_file, npar)
                    self.compute_nodes()
            else:
                print('Using previous grid')
                try:
                    np.load(self.node_file)
                except FileNotFoundError:
                    self.compute_nodes()
        else:
            np.savetxt(self.dis_file, npar)
            self.compute_nodes()

        self.export_node_idx()

    def nodes_cleanup(self, features):
        """
        Removes no-data rows from data frame and compute the mean of data points sharing the same cell.
        :param features: str or list(str) of features name to save
        :return: Filtered list of each attribute
        """
        data_nodes = np.load(self.node_file)
        unique_nodes = list(set(data_nodes))

        if not isinstance(features, list):
            features = [features]
        fn = []
        for h in features:  # For each feature
            # fixed nodes = [[node i, value i]....]
            fixed_nodes = np.array([[data_nodes[dn], self.dataframe[h][dn]] for dn in range(len(data_nodes))])
            # Deletes points where val == nodata
            hard_data = np.delete(fixed_nodes, np.where(fixed_nodes == self.nodata)[0], axis=0)
            # If data points share the same cell, compute their mean and assign the value to the cell
            for n in unique_nodes:
                where = np.where(hard_data[:, 0] == n)[0]
                if len(where) > 1:  # If more than 1 point per cell
                    mean = np.mean(hard_data[where, 1])
                    hard_data[where, 1] = mean

            fn.append(hard_data.tolist())

        return fn

    # Save node list to load it into sgems later
    def export_node_idx(self):
        """
        Export the list of shape (n features, m nodes, 2) containing the node of each point data with the corresponding
        value, for each feature
        """
        self.hard_data_objects = self.columns[3:]
        if not os.path.isfile(self.node_value_file):
            hard = self.nodes_cleanup(features=self.hard_data_objects)
            with open(self.node_value_file, 'w') as nd:
                nd.write(repr(hard))
            shutil.copyfile(self.node_value_file,
                            self.node_value_file.replace(os.path.dirname(self.node_value_file), self.res_dir))

    def xml_reader(self, algo_name):
        """
        Reads and parse XML file. It assumes the algorithm XML file is located in the algo_dir folder.
        :param algo_name: Name of the algorithm, without any extension, e.g. 'kriging', 'cokriging'...
        """
        self.algo_dir = jp(self.cwd, 'algorithms')  # ensure proper algorithm directory

        self.op_file = jp(self.algo_dir, 'temp_output.xml')  # Temporary saves a modified XML
        try:
            os.remove(self.op_file)
        except FileNotFoundError:
            pass

        self.tree = ET.parse(jp(self.algo_dir, '{}.xml'.format(algo_name)))
        self.root = self.tree.getroot()
        self.object_file_names = []  # Empty object file names if reading new algorithm

        name = self.root.find('algorithm').attrib['name']  # Algorithm name

        # result directory generated according to project and algorithm name
        if self.res_dir is None:
            # Generate result directory if none is given
            self.res_dir = jp(self.cwd, 'results', '_'.join([self.project_name, name, uuid.uuid1().hex]))
            os.makedirs(self.res_dir)

        # By default, replace the grid name by 'computation_grid', and the name by the algorithm name.
        replace = [['Grid_Name', {'value': 'computation_grid', 'region': ''}],
                   ['Property_Name', {'value': name}]]

        for r in replace:
            try:
                self.xml_update(path=r[0], new_attribute_dict=r[1])
            except AttributeError:
                pass

    def show_tree(self):
        """
        Displays the structure of the XML file, in order to get the path of updatable variables.
        """
        try:
            for element in self.root:
                print(element.tag)
                print(element.attrib)
                elems = list(element)
                c_list = [element.tag]
                while len(elems) > 0:
                    elems = list(element)
                    for e in elems:
                        c_list.append(e.tag)
                        print('//'.join(c_list))
                        print(e.attrib)
                        element = list(e)
                        if len(element) == 0:
                            c_list.pop(-1)
        except TypeError:
            print('No loaded XML file')

    def auto_fill(self):
        """
        Ensures binary file of point set are properly generated.
        In case of kriging, cokriging... ensures proper xml attribute names for feature and feature grid.
        This is still quite specific and lots of nested loops, ideally parse all Sgems default XML
        and build proper 'auto_fill' method.
        """

        try:
            elist = []
            for element in self.root:

                elems = list(element)
                c_list = [element.tag]

                elist.append(element)
                trv = list(element.attrib.values())
                trk = list(element.attrib.keys())

                for i in range(len(trv)):
                    if (trv[i] in self.columns) \
                            and ('Variable' or 'Hard_Data' in element.tag):
                        if trv[i] not in self.object_file_names:
                            self.object_file_names.append(trv[i])
                            try:
                                if trk[i-1] == 'grid':  # ensure default grid name
                                    print(element.attrib)
                                    element.attrib['grid'] = '{}_grid'.format(trv[i])
                                    self.xml_update('//'.join(c_list), 'grid', '{}_grid'.format(trv[i]))
                                    print('>>>')
                                    print(element.attrib)
                                if trk[i-1] == 'value' and trk[i] == 'property':  # ensure default grid name
                                    print(element.attrib)
                                    element.attrib['value'] = '{}_grid'.format(trv[i])
                                    self.xml_update('//'.join(c_list), 'value', '{}_grid'.format(trv[i]))
                                    print('>>>')
                                    print(element.attrib)
                            except IndexError:
                                pass
                            try:
                                if 'Grid' in elist[-2].tag:
                                    tp = list(elist[-2].attrib.keys())
                                    if 'grid' in tp:
                                        print('//'.join(c_list[:-2]))
                                        print(elist[-2].attrib)
                                        elist[-2].attrib['grid'] = '{}_grid'.format(trv[i])
                                        self.xml_update(elist[-2].tag, 'grid', '{}_grid'.format(trv[i]))
                                        print('>>>')
                                        print(elist[-2].attrib)
                                    if 'value' in tp:
                                        print('//'.join(c_list[:-2]))
                                        print(elist[-2].attrib)
                                        elist[-2].attrib['value'] = '{}_grid'.format(trv[i])
                                        self.xml_update(elist[-2].tag, 'value', '{}_grid'.format(trv[i]))
                                        print('>>>')
                                        print(elist[-2].attrib)
                            except IndexError:
                                pass

                while len(elems) > 0:
                    elems = list(element)
                    for e in elems:
                        c_list.append(e.tag)

                        trv = list(e.attrib.values())
                        trk = list(e.attrib.keys())

                        for i in range(len(trv)):
                            if trv[i] in self.columns:
                                if trv[i] not in self.object_file_names:
                                    self.object_file_names.append(trv[i])
                                    if trk[i] == 'grid':  # ensure default grid name
                                        print('//'.join(c_list))
                                        print(e.attrib)
                                        e.attrib['grid'] = '{}_grid'.format(trv[i])
                                        self.xml_update('//'.join(c_list), 'grid', '{}_grid'.format(trv[i]))
                                        print('>>>')
                                        print(e.attrib)
                                    if trk[i] == 'value':  # ensure default grid name
                                        print('//'.join(c_list))
                                        print(e.attrib)
                                        e.attrib['value'] = '{}_grid'.format(trv[i])
                                        self.xml_update('//'.join(c_list), 'value', '{}_grid'.format(trv[i]))
                                        print('>>>')
                                        print(e.attrib)

                        element = list(e)
                        if len(element) == 0:
                            c_list.pop(-1)
        except TypeError:
            print('No loaded XML file')

    def xml_update(self, path,
                   attribute_name=None,
                   value=None,
                   new_attribute_dict=None,
                   show=1):
        """
        Given a path in the algorithm XML file, changes the corresponding attribute to the new attribute
        :param path: object path
        :param attribute_name: name of the attribute to modify
        :param value: new value for attribute
        :param new_attribute_dict: dictionary defining new attribute
        :param show: whether to display updated xml or not
        """

        if new_attribute_dict is not None:
            if (self.auto_update is True) and ('property' in new_attribute_dict):
                # If one property point set needs to be used
                pp = new_attribute_dict['property']  # Name property
                if pp in self.columns:
                    ps_name = jp(self.res_dir, pp)  # Path of binary file
                    feature = os.path.basename(ps_name)  # If object not already in list
                    if feature not in self.object_file_names:
                        self.object_file_names.append(feature)
                    if 'grid' in new_attribute_dict:  # ensure default grid name
                        new_attribute_dict['grid'] = '{}_grid'.format(pp)
                    if 'value' in new_attribute_dict:  # ensure default grid name
                        new_attribute_dict['value'] = '{}_grid'.format(pp)

            self.root.find(path).attrib = new_attribute_dict
            self.tree.write(self.op_file)

        else:

            self.root.find(path).attrib[attribute_name] = value
            self.tree.write(self.op_file)

        if show:
            print('Updated')
            print(self.root.find(path).tag)
            print(self.root.find(path).attrib)

    def make_data(self, features):
        """
        Gives a list of dataset to be saved in sgems binary format and saves them to the result directory
        :param features:
        """
        if not isinstance(features, list):
            features = [features]
        for pp in features:
            subframe = self.dataframe[['x', 'y', pp]]  # Extract x, y, values
            ps_name = jp(self.res_dir, pp)  # Path of binary file
            write_point_set(ps_name, subframe)  # Write binary file
            if pp not in self.object_file_names:  # Adding features name to load them within sgems
                self.object_file_names.append(pp)

    def write_command(self):
        """
        Write python script that sgems will run.
        The sgems python script template must be located in the main folder.
        """
        if self.auto_update:
            # First creates necessary binary files
            self.auto_fill()
            self.make_data(self.object_file_names)

        run_algo_flag = ''  # This empty str will replace the # in front of the commands meant to execute sgems
        # within its python environment
        try:
            name = self.root.find('algorithm').attrib['name']  # Algorithm name
            with open(self.op_file) as alx:  # Remove unwanted \n
                algo_xml = alx.read().strip('\n')

        except AttributeError or FileNotFoundError:
            name = 'None'
            algo_xml = 'None'
            run_algo_flag = '#'  # If no algorithm loaded, then just loads the data

        sgrid = [self.ncol, self.nrow, self.nlay,
                 self.dx, self.dy, self.dz,
                 self.xo, self.yo, self.zo]  # Grid information
        grid = joinlist('::', sgrid)  # Grid in sgems format

        sgems_files = [sf + '.sgems' for sf in self.object_file_names]

        # The list below is the list of flags that will be replaced in the sgems python script
        params = [[run_algo_flag, '#'],
                  [self.res_dir.replace('\\', '//'), 'RES_DIR'],  # for sgems convention...
                  [grid, 'GRID'],
                  [self.project_name, 'PROJECT_NAME'],
                  [str(self.hard_data_objects), 'FEATURES_LIST'],
                  ['results', 'FEATURE_OUTPUT'],  # results.grid = output file
                  [name, 'ALGORITHM_NAME'],
                  [name, 'PROPERTY_NAME'],
                  [algo_xml, 'ALGORITHM_XML'],
                  [str(sgems_files), 'OBJECT_FILES'],
                  [self.node_value_file.replace('\\', '//'), 'NODES_VALUES_FILE']]

        with open(self.template_file) as sst:
            template = sst.read()
        for i in range(len(params)):  # Replaces the parameters
            template = template.replace(params[i][1], params[i][0])

        with open(jp(self.res_dir, 'simusgems.py'), 'w') as sstw:  # Write sgems python file
            sstw.write(template)

    def script_file(self):
        """Create script file"""
        run_script = jp(self.res_dir, 'sgems.script')
        rscpt = open(run_script, 'w')
        rscpt.write(' '.join(['RunScript', jp(self.res_dir, 'simusgems.py')]))
        rscpt.close()

    def bat_file(self):
        """Create bat file"""
        if not os.path.isfile(jp(self.res_dir, 'sgems.script')):
            self.script_file()

        batch = jp(self.res_dir, 'RunSgems.bat')
        bat = open(batch, 'w')
        bat.write(' '.join(['cd', self.res_dir, '\n']))
        bat.write(' '.join(['sgems', 'sgems.script']))
        bat.close()

    def run(self):
        """Call bat file, run sgems"""
        batch = jp(self.res_dir, 'RunSgems.bat')
        if not os.path.isfile(batch):
            self.bat_file()
        start = time.time()

        subprocess.call([batch])  # Opens the BAT file
        print('ran algorithm in {} s'.format(time.time()-start))

    def plot_coordinates(self):
        try:
            plt.plot(self.raw_data[:, 0], self.raw_data[:, 1], 'ko')
        except:
            pass
        try:
            plt.xticks(np.cumsum(self.along_r) + self.xo - self.dx, labels=[])
            plt.yticks(np.cumsum(self.along_c) + self.yo - self.dy, labels=[])
        except:
            pass

        plt.grid('blue')
        plt.show()

    def plot_2d(self, save=False):
        """Rudimentary 2D plot"""
        matrix = datread(jp(self.res_dir, 'results.grid'), start=3)
        matrix = np.where(matrix == -9966699, np.nan, matrix)
        matrix = matrix.reshape((self.nrow, self.ncol))
        extent = (self.xo, self.x_lim, self.yo, self.y_lim)
        plt.imshow(np.flipud(matrix), cmap='coolwarm', extent=extent)
        plt.plot(self.raw_data[:, 0], self.raw_data[:, 1], 'k+', markersize=1, alpha=.7)
        plt.colorbar()
        if save:
            plt.savefig(jp(self.res_dir, 'results.png'), bbox_inches='tight', dpi=300)
        plt.show()
