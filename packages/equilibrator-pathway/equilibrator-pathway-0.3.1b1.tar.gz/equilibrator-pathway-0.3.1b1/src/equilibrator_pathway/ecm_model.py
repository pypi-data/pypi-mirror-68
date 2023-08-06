# The MIT License (MIT)
#
# Copyright (c) 2013 Weizmann Institute of Science
# Copyright (c) 2018-2020 Institute for Molecular Systems Biology,
# ETH Zurich
# Copyright (c) 2018-2020 Novo Nordisk Foundation Center for Biosustainability,
# Technical University of Denmark
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import logging
from typing import List, Optional, Tuple, Union

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from equilibrator_api import Q_, ComponentContribution
from sbtab import SBtab

from .cost_function import EnzymeCostFunction
from .errors import ThermodynamicallyInfeasibleError
from .pathway import Pathway
from .util import ECF_DEFAULTS, PlotCorrelation


class ECMmodel(object):

    DATAFRAME_NAMES = {
        "Compound",
        "Reaction",
        "ConcentrationConstraint",
        "Parameter",
        "Flux",
    }

    def __init__(self, pathway: Pathway, param_df: pd.DataFrame):
        self.config_dict = dict(ECF_DEFAULTS)
        self.config_dict.update(pathway.config_dict)

        # TODO: use the stdev_factor (and the uncertainty estimates for the
        #  Gibbs energies, to somehow weigh the ECF
        #  stdev_factor = self.config_dict.get("stdev_factor", 1.0)

        (
            rid2crc_gmean,
            rid2crc_fwd,
            rid2crc_rev,
            rid_cid2KMM,
            rid2mw,
            cid2mw,
        ) = ECMmodel.ReadParameters(param_df, self.config_dict)

        self.reaction_ids = list(pathway.reaction_ids)
        self.compound_ids = list(pathway.compound_names)
        assert pathway.standard_dg_primes.check("kJ/mol")
        standard_dg_primes = np.reshape(
            pathway.standard_dg_primes, (len(self.reaction_ids), 1)
        )

        KMM = ECMmodel._GenerateKMM(
            self.compound_ids, self.reaction_ids, rid_cid2KMM
        )

        # we need all fluxes to be positive, so for every negative flux,
        # we multiply it and the corresponding column in S by (-1)
        dir_mat = np.diag(np.sign(pathway.fluxes.magnitude + 1e-10).flat)
        flux = dir_mat @ pathway.fluxes
        S = pathway.S.values @ dir_mat
        standard_dg = dir_mat @ standard_dg_primes

        # we only need to define get kcat in the direction of the flux
        # if we use the 'gmean' option, that means we assume we only know
        # the geometric mean of the kcat, and we distribute it between
        # kcat_fwd and kcat_bwd according to the Haldane relationship
        # if we use the 'fwd' option, we just take the kcat in the
        # direction of flux (as is) and that would mean that our
        # thermodynamic rate law would be equivalent to calculating the
        # reverse kcat using the Haldane relationship
        assert self.config_dict["kcat_source"] in ["gmean", "fwd"], (
            "unrecognized kcat source: " + self.config_dict["kcat_source"]
        )

        kcat = []
        for rid, d in zip(pathway.reaction_ids, np.diag(dir_mat).flat):
            if self.config_dict["kcat_source"] == "gmean":
                # TODO: calculate the forward kcat using the Haldane relation
                #  and using the KMM matrix
                crc = rid2crc_gmean[rid]
            elif d >= 0:  # the flux in this reaction is forward
                crc = rid2crc_fwd[rid]
            else:  # the flux in this reaction is backward
                crc = rid2crc_rev[rid]
            kcat.append(crc.m_as("1/s"))
        kcat = Q_(kcat, "1/s")

        # TODO: turn this into a warning, if the MW data is missing, try to
        #  assign a default value
        mw_enz = []
        for rid in self.reaction_ids:
            if rid not in rid2mw:
                raise KeyError(f"This reaction is missing an enzyme MW: {rid}")
            mw_enz.append(rid2mw[rid].m_as("Da"))
        mw_enz = Q_(mw_enz, "Da")

        # TODO: fill gaps in MW data by using the equilibrator-cache
        mw_met = []
        for cid in self.compound_ids:
            if cid not in cid2mw:
                raise KeyError(f"This compound is missing a MW: {cid}")
            mw_met.append(cid2mw[cid].m_as("Da"))
        mw_met = Q_(mw_met, "Da")

        # we must remove H2O from the model, since it should not be considered
        # as a "normal" metabolite in terms of the enzyme and metabolite costs
        idx_water = pathway.S.index.tolist().index(pathway.water)

        self.compound_ids.pop(idx_water)
        S = np.delete(S, idx_water, axis=0)

        # numpy.delete does not support Quantity ndarrays as input
        KMM = np.vstack([KMM[:idx_water, :], KMM[idx_water + 1 :, :]])

        ln_conc_lb = np.delete(pathway.ln_conc_lb, idx_water, axis=0)
        ln_conc_ub = np.delete(pathway.ln_conc_ub, idx_water, axis=0)
        mw_met = np.hstack([mw_met[:idx_water], mw_met[idx_water + 1 :]])

        self.ecf = EnzymeCostFunction(
            S,
            fluxes=flux,
            kcat=kcat,
            standard_dg=standard_dg,
            KMM=KMM,
            ln_conc_lb=ln_conc_lb,
            ln_conc_ub=ln_conc_ub,
            mw_enz=mw_enz,
            mw_met=mw_met,
            params=self.config_dict,
        )

        self._val_df_dict = None

    @staticmethod
    def from_sbtab(
        filename: Union[str, SBtab.SBtabDocument],
        comp_contrib: Optional[ComponentContribution] = None,
    ) -> "ECMModel":
        if isinstance(filename, str):
            sbtabdoc = SBtab.read_csv(filename, "pathway")
        elif isinstance(filename, SBtab.SBtabDocument):
            sbtabdoc = filename

        pathway = Pathway.from_sbtab(sbtabdoc, comp_contrib)

        param_sbtab = sbtabdoc.get_sbtab_by_id("Parameter")
        assert param_sbtab, "Missing table 'Parameter' in the SBtab document"
        param_df = param_sbtab.to_data_frame()

        return ECMmodel(pathway, param_df)

    def AddValidationData(
        self, filename: Union[str, SBtab.SBtabDocument]
    ) -> None:
        if isinstance(filename, str):
            sbtabdoc = SBtab.read_csv(filename, "pathway")
        elif isinstance(filename, SBtab.SBtabDocument):
            sbtabdoc = filename

        conc_sbtab = sbtabdoc.get_sbtab_by_id("Concentration")
        self._met_conc_unit = Q_(conc_sbtab.get_attribute("Unit"))
        assert self._met_conc_unit.check("[concentration]"), (
            f"Metabolite concentration unit is not a [concentration] quantity",
            self._met_conc_unit,
        )

        enzyme_sbtab = sbtabdoc.get_sbtab_by_id("EnzymeConcentration")
        self._enz_conc_unit = Q_(enzyme_sbtab.get_attribute("Unit"))
        assert self._enz_conc_unit.check("[concentration]"), (
            f"Enzyme concentration unit is not a [concentration] quantity",
            self._enz_conc_unit,
        )

        self._val_df_dict = {
            sbtab.table_id: sbtab.to_data_frame() for sbtab in sbtabdoc.sbtabs
        }

    @staticmethod
    def ReadParameters(
        parameter_df: pd.DataFrame, ecf_params: dict
    ) -> Tuple[dict, ...]:
        cols = ["QuantityType", "Value", "Compound", "Reaction", "Unit"]

        rid2mw = dict()
        cid2mw = dict()
        rid2crc_gmean = dict()  # catalytic rate constant geomertic mean
        rid2crc_fwd = dict()  # catalytic rate constant forward
        rid2crc_rev = dict()  # catalytic rate constant reverse
        crctype2dict = {
            "catalytic rate constant geometric mean": rid2crc_gmean,
            "substrate catalytic rate constant": rid2crc_fwd,
            "product catalytic rate constant": rid2crc_rev,
        }

        rid_cid2KMM = {}  # Michaelis-Menten constants

        for i, row in parameter_df.iterrows():
            try:
                typ, val, cid, rid, unit = [row[c] for c in cols]
                val = Q_(float(val), unit)

                if typ in crctype2dict:
                    assert val.check(
                        "1/[time]"
                    ), f"rate constants must have inverse time units"
                    val.ito("1/s")
                    crctype2dict[typ][rid] = val
                elif typ == "Michaelis constant":
                    assert val.check(
                        "[concentration]"
                    ), f"Michaelis constants must have concentration units"
                    val.ito("molar")
                    rid_cid2KMM[rid, cid] = val
                elif typ == "protein molecular mass":
                    assert val.check("[mass]"), f"'{typ}' must have mass units"
                    val.ito("Da")
                    rid2mw[rid] = val
                elif typ == "molecular mass":
                    assert val.check("[mass]"), f"'{typ}' must have mass units"
                    val.ito("Da")
                    cid2mw[cid] = val
                else:
                    raise AssertionError(
                        "unrecognized Rate Constant Type: " + typ
                    )
            except AssertionError:
                raise ValueError(
                    "Syntax error in Parameter table, row %d - %s" % (i, row)
                )
        # make sure not to count water as contributing to the volume or
        # cost of a reaction
        return (
            rid2crc_gmean,
            rid2crc_fwd,
            rid2crc_rev,
            rid_cid2KMM,
            rid2mw,
            cid2mw,
        )

    @staticmethod
    def _GenerateKMM(
        cids: List[str], rids: List[str], rid_cid2KMM: dict
    ) -> np.array:
        KMM = np.ones((len(cids), len(rids)))
        for i, cid in enumerate(cids):
            for j, rid in enumerate(rids):
                kmm = rid_cid2KMM.get((rid, cid), Q_(1, "M"))
                KMM[i, j] = kmm.m_as("M")
        return KMM * Q_(1, "M")

    def MDF(self):
        mdf, ln_conc0 = self.ecf.MDF()

        if np.isnan(mdf) or mdf < 0.0:
            logging.error("Negative MDF value: %s" % mdf)
            raise ThermodynamicallyInfeasibleError()
        return ln_conc0

    def ECM(self, ln_conc0=None, n_iter=10):
        if ln_conc0 is None:
            ln_conc0 = self.MDF()
            logging.info("initializing ECM using MDF result")

        return self.ecf.ECM(ln_conc0, n_iter=n_iter)

    def ECF(self, ln_conc):
        return self.ecf.ECF(ln_conc)

    @staticmethod
    def _nanfloat(x):
        if type(x) == float:
            return x
        if type(x) == int:
            return float(x)
        if type(x) == str:
            if x.lower() in ["", "nan"]:
                return np.nan
            else:
                return float(x)
        else:
            raise ValueError("unrecognized type for value: " + str(type(x)))

    @staticmethod
    def _MappingToCanonicalEnergyUnits(unit):
        """
            Assuming the canonical units for concentration are Molar

            Returns:
                A function that converts a single number or string to the
                canonical units
        """
        if unit == "kJ/mol":
            return lambda x: ECMmodel._nanfloat(x)
        if unit == "kcal/mol":
            return lambda x: ECMmodel._nanfloat(x) * 4.184

        raise ValueError("Cannot convert these units to kJ/mol: " + unit)

    def _GetMeasuredMetaboliteConcentrations(self) -> Q_:
        assert (
            self._val_df_dict is not None
        ), "cannot validate results because no validation data was given"

        met_conc_df = self._val_df_dict["Concentration"].set_index("Compound")
        met_concentrations = Q_(
            pd.to_numeric(met_conc_df.Value)[self.compound_ids].values,
            self._met_conc_unit,
        )
        return met_concentrations

    def _GetMeasuredEnzymeConcentrations(self) -> Q_:
        assert (
            self._val_df_dict is not None
        ), "cannot validate results because no validation data was given"

        enz_conc_df = self._val_df_dict["EnzymeConcentration"].set_index(
            "Reaction"
        )
        enz_concentrations = Q_(
            pd.to_numeric(enz_conc_df.Value)[self.reaction_ids].values,
            self._met_conc_unit,
        )
        return enz_concentrations

    def _GetVolumeDataForPlotting(self, ln_conc):
        enz_vols, met_vols = self.ecf.GetVolumes(ln_conc)

        enz_data = sorted(zip(enz_vols.flat, self.reaction_ids), reverse=True)
        enz_vols, enz_labels = zip(*enz_data)
        enz_colors = [(0.5, 0.8, 0.3)] * len(enz_vols)

        met_data = zip(met_vols.flat, self.compound_ids)
        # remove H2O from the list and sort by descending volume
        met_data = sorted(filter(lambda x: x[1] != "h2o", met_data))
        met_vols, met_labels = zip(*met_data)
        met_colors = [(0.3, 0.5, 0.8)] * len(met_vols)

        return (
            enz_vols + met_vols,
            enz_labels + met_labels,
            enz_colors + met_colors,
        )

    def PlotVolumes(self, ln_conc: np.array, ax: plt.axes) -> None:
        width = 0.8
        vols, labels, colors = self._GetVolumeDataForPlotting(ln_conc)

        ax.bar(np.arange(len(vols)), vols, width, color=colors)
        ax.set_xticklabels(labels, size="medium", rotation=90)
        ax.set_ylabel("total weight [g/L]")

    def PlotVolumesPie(self, ln_conc: np.array, ax: plt.axes) -> None:
        vols, labels, colors = self._GetVolumeDataForPlotting(ln_conc)
        ax.pie(vols, labels=labels, colors=colors)
        ax.set_title("total weight [g/L]")

    def PlotThermodynamicProfile(self, ln_conc: np.array, ax: plt.axes) -> None:
        """
            Plot a cumulative line plot of the dG' values given the solution
            for the metabolite levels. This was originally designed for showing
            MDF results, but is also a useful tool for ECM.
        """
        driving_forces = self.ecf._DrivingForce(ln_conc)

        dgs = [0] + list((-driving_forces).flat)
        cumulative_dgs = np.cumsum(dgs)

        xticks = np.arange(0, len(cumulative_dgs)) - 0.5
        xticklabels = [""] + self.reaction_ids
        ax.plot(cumulative_dgs)
        ax.set_xticks(xticks)
        ax.set_xticklabels(xticklabels, rotation=45, ha="right")
        ax.set_xlim(0, len(cumulative_dgs) - 1)
        ax.set_xlabel("")
        ax.set_ylabel(r"Cumulative $\Delta_r G'$ (kJ/mol)", family="sans-serif")

    def PlotEnzymeDemandBreakdown(
        self,
        ln_conc: np.array,
        ax: plt.Axes,
        top_level: int = 3,
        plot_measured: bool = False,
    ) -> None:
        """
            A bar plot in log-scale showing the partitioning of cost between
            the levels of kinetic costs:
            1 - capacity
            2 - thermodynamics
            3 - saturation
            4 - allosteric
        """
        assert top_level in range(1, 5)

        meas_conc = self._GetMeasuredEnzymeConcentrations()

        costs = self.ecf.GetEnzymeCostPartitions(ln_conc)

        # give all reactions with zero cost a base value, which we will
        # also set as the bottom ylim, which will simulate a "minus infinity"
        # when we plot it in log-scale
        base = min(filter(None, costs[:, 0])) / 2.0
        idx_zero = costs[:, 0] == 0
        costs[idx_zero, 0] = base
        costs[idx_zero, 1:] = 1.0

        bottoms = np.hstack(
            [np.ones((costs.shape[0], 1)) * base, np.cumprod(costs, 1)]
        )
        steps = np.diff(bottoms)

        labels = EnzymeCostFunction.ECF_LEVEL_NAMES[0:top_level]

        ind = range(costs.shape[0])  # the x locations for the groups
        width = 0.8
        ax.set_yscale("log")

        if plot_measured:
            ax.plot(
                ind,
                meas_conc.m_as("M"),
                label="measured",
                color="gold",
                marker="d",
                markersize=7,
                linewidth=0,
                markeredgewidth=0.3,
                markeredgecolor=(0.3, 0.3, 0.3),
            )
        colors = ["tab:blue", "tab:orange", "tab:brown"]
        for i, label in enumerate(labels):
            ax.bar(
                ind,
                steps[:, i].flat,
                width,
                bottom=bottoms[:, i].flat,
                color=colors[i],
                label=label,
            )

        ax.set_xticks(ind)
        xticks = self.reaction_ids
        ax.set_xticklabels(xticks, size="medium", rotation=90)
        ax.legend(loc="best", framealpha=0.2)
        ax.set_ylabel("enzyme demand [M]")
        ax.set_ylim(bottom=base)

    def ValidateMetaboliteConcentrations(
        self, ln_conc: np.array, ax: plt.Axes, scale: str = "log"
    ) -> None:
        pred_conc = Q_(np.exp(ln_conc.flatten()), "M")

        meas_conc = self._GetMeasuredMetaboliteConcentrations()

        # remove NaNs and zeros
        mask = np.nan_to_num(meas_conc) > 0
        mask &= np.nan_to_num(pred_conc) > 0

        # remove compounds with fixed concentrations
        mask &= (self.ecf.ln_conc_ub - self.ecf.ln_conc_lb) > 1e-9

        PlotCorrelation(
            ax,
            meas_conc.m_as("M"),
            pred_conc.m_as("M"),
            self.compound_ids,
            mask,
            scale=scale,
        )
        ax.set_xlabel("measured [M]")
        ax.set_ylabel("predicted [M]")

    def ValidateEnzymeConcentrations(
        self, ln_conc: np.array, ax: plt.Axes, scale: str = "log"
    ) -> None:
        pred_conc = Q_(self.ecf.ECF(ln_conc).flatten(), "M")
        meas_conc = self._GetMeasuredEnzymeConcentrations()

        labels = self.reaction_ids
        PlotCorrelation(
            ax, meas_conc.m_as("M"), pred_conc.m_as("M"), labels, scale=scale
        )

        ax.set_xlabel("measured [M]")
        ax.set_ylabel("predicted [M]")

    def to_sbtab(self, ln_conc: np.array) -> SBtab.SBtabDocument:
        met_data = []
        for i, cid in enumerate(self.compound_ids):
            met_data.append(("concentration", cid, np.exp(ln_conc[i, 0])))
        met_df = pd.DataFrame(
            columns=["QuantityType", "Compound", "ecm"], data=met_data
        )

        enz_conc = self.ecf.ECF(ln_conc)
        enz_data = []
        for i, rid in enumerate(self.reaction_ids):
            enz_data.append(("concentration of enzyme", rid, enz_conc[i, 0]))
        enz_df = pd.DataFrame(
            columns=["QuantityType", "Reaction", "ecm"], data=enz_data
        )

        sbtabdoc = SBtab.SBtabDocument("report")
        met_sbtab = SBtab.SBtabTable.from_data_frame(
            met_df,
            table_id="Predicted concentrations",
            table_type="Quantity",
            unit="M",
        )

        enz_sbtab = SBtab.SBtabTable.from_data_frame(
            enz_df,
            table_id="Predicted enzyme levels",
            table_type="Quantity",
            unit="M",
        )

        sbtabdoc.add_sbtab(met_sbtab)
        sbtabdoc.add_sbtab(enz_sbtab)
        return sbtabdoc
