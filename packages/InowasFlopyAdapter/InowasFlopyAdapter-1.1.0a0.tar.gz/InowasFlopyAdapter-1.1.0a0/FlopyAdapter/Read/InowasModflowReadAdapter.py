import flopy as fp
import geojson
import glob
import numpy as np
import os
import rasterio.features
import sys
import utm
from pyproj import Transformer


class InvalidArgumentException(Exception):
    pass


class InowasModflowReadAdapter:
    _ws = None
    _mf = None

    @staticmethod
    def load(path):

        abspath = os.path.abspath(os.path.join(path))
        if not os.path.exists(abspath):
            raise FileNotFoundError('Path not found: ' + path)

        if len(glob.glob1(abspath, "*.nam")) == 0 and len(glob.glob1(abspath, "*.mfn")) == 0:
            raise FileNotFoundError('Modflow name file with ending .nam or .mfn not found')

        orig_stdout = sys.stdout
        f = open(os.path.join(abspath, 'load.log'), 'w')
        sys.stdout = f

        instance = InowasModflowReadAdapter()
        instance._ws = path

        name_file = ''
        if len(glob.glob1(abspath, "*.nam")) > 0:
            name_file = glob.glob1(abspath, "*.nam")[0]

        if len(glob.glob1(abspath, "*.mfn")) > 0:
            name_file = glob.glob1(abspath, "*.mfn")[0]

        try:
            instance._mf = fp.modflow.Modflow.load(
                os.path.join(abspath, name_file),
                check=True,
                forgive=True,
                model_ws=abspath,
                verbose=True,
            )

            sys.stdout = orig_stdout
            f.close()

            return instance

        except:
            sys.stdout = orig_stdout
            f.close()
            raise

    def __init__(self):
        pass

    def get_ibound(self):
        if not isinstance(self._mf, fp.modflow.Modflow):
            raise FileNotFoundError('Model not loaded')

        bas_package = None
        package_list = self._mf.get_package_list()

        if 'BAS' in package_list:
            bas_package = self._mf.get_package('BAS')

        if 'BAS6' in package_list:
            bas_package = self._mf.get_package('BAS6')

        if not isinstance(bas_package, fp.modflow.ModflowBas):
            raise Exception('Bas package could not be loaded.')

        return bas_package.ibound.array

    @staticmethod
    def wgs82ToUtm(x, y):
        easting, northing, zone_number, zone_letter = utm.from_latlon(y, x)
        return easting, northing, zone_number, zone_letter

    @staticmethod
    def utmToWgs82XY(easting, northing, zone_number, zone_letter):
        latitude, longitude = utm.to_latlon(easting, northing, zone_number, zone_letter)
        return longitude, latitude

    def model_geometry(self, xll=None, yll=None, origin_epsg=4326, angrot=None, layer=0):
        if not isinstance(self._mf, fp.modflow.Modflow):
            raise FileNotFoundError('Model not loaded')

        if xll is None:
            raise InvalidArgumentException('xll not set')

        if yll is None:
            raise InvalidArgumentException('yll not set')

        if origin_epsg != 4326:
            tf = Transformer.from_crs(origin_epsg, 4326, always_xy=True)
            xll, yll = tf.transform(xll, yll)

        xoff, yoff, zone_number, zone_letter = self.wgs82ToUtm(xll, yll)

        # We should create a new grid with updated coordinate-references
        mg = self._mf.modelgrid

        # new model grid
        from flopy.discretization import StructuredGrid
        nmg = StructuredGrid(
            mg.delc,
            mg.delr,
            mg.top,
            mg.botm,
            mg.idomain,
            mg.lenuni,
            xoff=xoff,
            yoff=yoff,
            angrot=angrot if angrot is not None else mg.angrot
        )

        iBound = self.get_ibound()

        if layer >= len(iBound):
            raise Exception('Layer with key ' + str(layer) + 'not found. Max: ' + str(len(iBound)))

        layer = iBound[layer]

        mask = np.array(np.ma.masked_values(layer, 1, shrink=False), dtype=bool)
        mpoly_cells = []
        for vec in rasterio.features.shapes(layer, mask=mask):
            mpoly_cells.append(geojson.Polygon(vec[0]["coordinates"]))

        mpoly_cells = mpoly_cells[0]

        def get_cell_centers(grid, c):

            xcz = grid.xcellcenters
            ycz = grid.ycellcenters

            nx, ny = int(c[0]), int(c[1])
            return [xcz[ny][nx], ycz[ny][nx]]

        mpoly_coordinates_utm = geojson.utils.map_tuples(lambda c: get_cell_centers(nmg, c), mpoly_cells)

        mpoly_coordinates_wgs84 = geojson.utils.map_tuples(
            lambda c: self.utmToWgs82XY(c[0], c[1], zone_number, zone_letter), mpoly_coordinates_utm
        )

        # noinspection PyTypeChecker
        polygon = geojson.Polygon(mpoly_coordinates_wgs84['coordinates'])
        return polygon
