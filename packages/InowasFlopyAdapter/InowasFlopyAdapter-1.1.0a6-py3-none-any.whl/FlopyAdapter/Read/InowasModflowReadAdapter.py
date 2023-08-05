import flopy as fp
import geojson
import glob
import numpy as np
import os
import rasterio.features
import sys
import utm
from flopy.modflow import ModflowWel
from pyproj import Transformer


class InvalidArgumentException(Exception):
    pass


class InvalidModelUnitException(Exception):
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

    @staticmethod
    def get_cell_center(grid, c):
        xcz = grid.xcellcenters
        ycz = grid.ycellcenters
        nx, ny = int(c[0]), int(c[1])
        return [xcz[ny][nx], ycz[ny][nx]]

    def model_grid(self, xll=None, yll=None, origin_epsg=4326, angrot=None):
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
        return StructuredGrid(
            mg.delc,
            mg.delr,
            mg.top,
            mg.botm,
            mg.idomain,
            mg.lenuni,
            xoff=xoff,
            yoff=yoff,
            angrot=angrot if angrot is not None else mg.angrot
        ), zone_number, zone_letter

    def model_geometry(self, xll=None, yll=None, origin_epsg=4326, angrot=None, layer=0):
        nmg, zone_number, zone_letter = self.model_grid(xll, yll, origin_epsg, angrot)

        i_bound = self.get_ibound()
        if layer >= len(i_bound):
            raise Exception('Layer with key ' + str(layer) + 'not found. Max: ' + str(len(i_bound)))

        layer = i_bound[layer]
        mask = np.array(np.ma.masked_values(layer, 1, shrink=False), dtype=bool)
        mpoly_cells = []
        for vec in rasterio.features.shapes(layer, mask=mask):
            mpoly_cells.append(geojson.Polygon(vec[0]["coordinates"]))

        mpoly_cells = mpoly_cells[0]
        mpoly_coordinates_utm = geojson.utils.map_tuples(lambda c: self.get_cell_center(nmg, c), mpoly_cells)

        mpoly_coordinates_wgs84 = geojson.utils.map_tuples(
            lambda c: self.utmToWgs82XY(c[0], c[1], zone_number, zone_letter), mpoly_coordinates_utm
        )

        # noinspection PyTypeChecker
        polygon = geojson.Polygon(mpoly_coordinates_wgs84['coordinates'])
        return polygon

    def wel_boundaries(self, xll=None, yll=None, origin_epsg=4326, angrot=None):
        default = 0
        mg, zone_number, zone_letter = self.model_grid(xll, yll, origin_epsg, angrot)
        try:
            wel: ModflowWel = self._mf.wel
            flux = np.array(wel.stress_period_data.array["flux"])
            flux_cells = np.argwhere(~np.isnan(flux))

            well_cells = []
            for cell in flux_cells:
                sp, l, r, c = cell
                if [l, r, c] not in well_cells:
                    well_cells.append([l, r, c])

            wel_boundaries = []
            for idx, cell in enumerate(well_cells):
                l, r, c = cell
                center = self.get_cell_center(mg, [c, r])
                center = self.utmToWgs82XY(center[0], center[1], zone_number, zone_letter)
                sp_values = []
                for spd in flux:
                    value = spd[l][r][c]
                    if ~np.isnan(value):
                        sp_values.append(value)
                        continue

                    sp_values.append(default)

                wel_boundaries.append({
                    'type': 'wel',
                    'name': 'Well ' + str(idx + 1),
                    'geometry': geojson.Point(center),
                    'layers': [l],
                    'sp_values': sp_values,
                    'cells': [[c, r]]
                })

            return wel_boundaries

        except AttributeError:
            pass

    def model_grid_size(self):
        if not isinstance(self._mf, fp.modflow.Modflow):
            raise FileNotFoundError('Model not loaded.')

        nrow, ncol, nlay, nper = self._mf.get_nrow_ncol_nlay_nper()

        return {
            'n_x': ncol,
            'n_y': nrow
        }

    def model_stress_periods(self, start_datetime=None):
        if not isinstance(self._mf, fp.modflow.Modflow):
            raise FileNotFoundError('Model not loaded.')

        if not isinstance(self._mf.dis, fp.modflow.ModflowDis):
            raise FileNotFoundError('Dis-Package not loaded.')

        time_unit = self._mf.dis.itmuni

        if time_unit != 4:
            raise InvalidModelUnitException('The time unit is required to be in days (4)')

        from datetime import datetime, timedelta
        mt = self._mf.modeltime

        if start_datetime is None:
            start_datetime = datetime.strptime(mt.start_datetime, '%m-%d-%Y')

        if not isinstance(start_datetime, datetime):
            raise InvalidModelUnitException('DateTime has to be None or instance od datetime.')

        end_datetime = start_datetime + timedelta(days=sum(mt.perlen.tolist()))

        stressperiods = []
        for sp_idx in range(0, mt.nper):
            start_date_time = start_datetime + timedelta(days=sum(mt.perlen.tolist()[0:sp_idx]))
            stressperiods.append({
                'start_date_time': str(start_date_time.date()),
                'nstp': mt.nstp.tolist()[sp_idx],
                'tsmult': mt.tsmult.tolist()[sp_idx],
                'steady': mt.steady_state.array[sp_idx]
            })

        return {
            'start_date_time': str(start_datetime.date()),
            'end_date_time': str(end_datetime.date()),
            'time_unit': time_unit,
            'stressperiods': stressperiods
        }

    def model_length_unit(self):
        if not isinstance(self._mf, fp.modflow.Modflow):
            raise FileNotFoundError('Model not loaded')

        if not isinstance(self._mf.dis, fp.modflow.ModflowDis):
            raise FileNotFoundError('Dis-Package not loaded.')

        return self._mf.dis.lenuni

    def model_time_unit(self):
        if not isinstance(self._mf, fp.modflow.Modflow):
            raise FileNotFoundError('Model not loaded')

        if not isinstance(self._mf.dis, fp.modflow.ModflowDis):
            raise FileNotFoundError('Dis-Package not loaded.')

        return self._mf.dis.itmuni
