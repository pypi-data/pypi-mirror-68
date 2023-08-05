"""
Utilities for rock chemistry and mineral abundance classification.

Todo
-------

* Petrological classifiers: QAPF (aphanitic/phaneritic),
  gabbroic Pyroxene-Olivine-Plagioclase,
  ultramafic Olivine-Orthopyroxene-Clinopyroxene
"""
import os
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import logging
import joblib
from pyrolite.util.meta import pyrolite_datafolder

logging.getLogger(__name__).addHandler(logging.NullHandler())
logger = logging.getLogger(__name__)


class ClassifierModel(object):
    def __init__(self, rebuild=False, deterministic=False):
        """
        Build a ClassifierModel

        Parameters
        -----------
        rebuild : :class:`bool`
            Whether to rebuild a classifer which already exists from source files.
        deterministic : :class:`bool`
            Whether the classifier is deterministic.
        """
        self.clsf_modelname = str(type(self).__name__)
        if __name__ == "__main__":
            modeldir = Path(os.getcwd()) / "models"
        else:
            modeldir = pyrolite_datafolder(subfolder="models")
        self.diskname = modeldir / str(self.clsf_modelname)
        self.deterministic = deterministic
        self.clsf = None
        # Try load classifer
        if rebuild:
            self.rebuild_clsf()
        try:
            self.clsf = self.load_clsf(self.diskname.with_suffix(".clsf.gz"))
            # logger.info(f'Loaded {self.diskname}')
        except (FileNotFoundError, AssertionError):
            self.rebuild_clsf()

    def rebuild_clsf(self):
        self.clsf = self.build_clsf()
        self.dump_clsf(self.diskname.with_suffix(".clsf.gz"))
        # logger.info(f'Built {self.clsf_modelname}')

    def load_clsf(self, file):
        assert file.exists() and file.is_file()
        # logger.info(f'Loading {self.diskname}')
        return joblib.load(file)

    def build_clsf(self):
        # logger.info(f'Building {self.clsf_modelname}')
        clsf = None
        return clsf

    def dump_clsf(self, filename):
        joblib.dump(self.clsf, filename, compress=("gzip", 3))
        # logger.info(f'Dumped {filename}')
        assert filename.exists() and filename.is_file()

    def classify(self, df: pd.DataFrame):
        return self.clsf.predict(df)

    def __str__(self):
        pass

    def __repr__(self):
        pass


class SimpleDeterministicClassifer(object):
    def __init__(self, parent: ClassifierModel):
        self.parent = parent
        self.fields = None
        self.load_fields()

    def load_fields(self):
        if self.parent:
            self.clsf_modelname = str(self.parent.clsf_modelname)
            self.modeldir = self.parent.diskname.resolve()
            af = self.modeldir / str(self.clsf_modelname + ".modelfields")
            if af.exists() and af.is_file():
                # logger.info(f'''Loading {self.clsf_modelname} classifer fields from "allfile".''')
                loadup = joblib.load(af)
                self.fclasses = [k for (k, v) in loadup.items()]
                self.fields = {c: loadup[c] for ix, c in enumerate(self.fclasses)}
            else:
                # logger.info(f'Loading {self.clsf_modelname} classifer fields from files.')
                fieldfiles = self.modeldir.glob(self.clsf_modelname + ".*.modelfield")
                loadup = [joblib.load(f) for f in fieldfiles]
                self.fclasses = [f.suffix.replace(".", "") for f in loadup]
                self.fields = {c: loadup[ix] for ix, c in enumerate(self.fclasses)}
            # logger.info(f'''Loaded {self.clsf_modelname} classifer fields.''')
        else:
            pass

    def add_to_axes(self, ax=None, fill=False, **kwargs):
        polys = [(c, self.fields[c]) for c in self.fclasses if self.fields[c]["poly"]]
        if ax is None:
            fig, ax = plt.subplots(1)
        pgns = []
        for c, f in polys:
            label = f["names"]
            if not fill:
                kwargs["facecolor"] = "none"
            pg = Polygon(f["poly"], closed=True, edgecolor="k", **kwargs)
            pgns.append(pg)
            x, y = pg.get_xy().T
            ax.annotate(c, xy=(np.nanmean(x), np.nanmean(y)))
            ax.add_patch(pg)
        # ax.add_collection(PatchCollection(pgns), autolim=True)

    def predict(self, df: pd.DataFrame, cols: list = ["x", "y"]):
        points = df.loc[:, cols].values
        polys = [
            Polygon(self.fields[c]["poly"], closed=True) for c in self.fclasses
        ]  # if self.fields[c]['poly']
        indexes = np.array([p.contains_points(points) for p in polys]).T
        notfound = np.logical_not(indexes.sum(axis=-1))
        out = pd.Series(index=df.index)
        outlist = list(map(lambda ix: self.fclasses[ix], np.argmax(indexes, axis=-1)))
        out.loc[:] = outlist
        out.loc[(notfound)] = "none"
        return out


class PeralkalinityClassifier(object):
    def __init__(self, parent: ClassifierModel):
        self.parent = parent
        self.fields = None

    def predict(self, df: pd.DataFrame):
        TotalAlkali = df.Na2O + df.K2O
        perkalkaline_where = (df.Al2O3 < (TotalAlkali + df.CaO)) & (
            TotalAlkali > df.Al2O3
        )
        metaluminous_where = (df.Al2O3 > (TotalAlkali + df.CaO)) & (
            TotalAlkali < df.Al2O3
        )
        peraluminous_where = (df.Al2O3 < (TotalAlkali + df.CaO)) & (
            TotalAlkali < df.Al2O3
        )
        out = pd.Series(index=df.index)
        out.loc[peraluminous_where] = "Peraluminous"
        out.loc[metaluminous_where] = "Metaluminous"
        out.loc[perkalkaline_where] = "Peralkaline"
        return out


class Geochemistry(object):
    class peralkalinity(ClassifierModel):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, deterministic=True, **kwargs)

        def build_clsf(self):
            return PeralkalinityClassifier(self)

    class TAS(ClassifierModel):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, deterministic=True, **kwargs)

        def build_clsf(self):
            return SimpleDeterministicClassifer(self)

        def add_to_axes(self, ax=None, **kwargs):
            if ax is None:
                fig, ax = plt.subplots(1)
            self.clsf.add_to_axes(ax=ax, **kwargs)
            ax.set_xlim((35, 85))
            ax.set_ylim((0, 20))
            ax.set_ylabel("$Na_2O + K_2O$")
            ax.set_xlabel("$SiO_2$")

        def classify(self, df: pd.DataFrame):
            return self.clsf.predict(df, cols=["SiO2", "TotalAlkali"])
