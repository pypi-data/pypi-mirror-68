"""A biochemical compound microspecies module."""
# The MIT License (MIT)
#
# Copyright (c) 2018 Institute for Molecular Systems Biology, ETH Zurich
# Copyright (c) 2018 Novo Nordisk Foundation Center for Biosustainability,
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


import typing

from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer

from ..thermodynamic_constants import (
    Q_,
    default_pMg,
    default_RT,
    default_T,
    legendre_transform,
    ureg,
)
from . import Base
from .compound import Compound
from .mixins import TimeStampMixin


class CompoundMicrospecies(TimeStampMixin, Base):
    """Model a microspecies' thermodynamic information."""

    __tablename__ = "compound_microspecies"

    # SQLAlchemy column descriptors.
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    compound_id: int = Column(Integer, ForeignKey(Compound.id), nullable=False)
    charge: int = Column(Integer, default=0, nullable=False)
    number_protons: int = Column(Integer, default=0, nullable=False)
    number_magnesiums: int = Column(Integer, default=0, nullable=False)
    is_major: bool = Column(Boolean, default=False, nullable=False)
    ddg_over_rt: typing.Optional[float] = Column(
        Float, default=None, nullable=True
    )

    def __repr__(self) -> str:
        """Return a representation string for this object."""
        return (
            f"{type(self).__name__}(compound_id={self.compound_id}, "
            f"charge={self.charge}, number_protons={self.number_protons})"
        )

    @property
    def ddg(self) -> Q_:
        """Return the energy difference between this and the base MS."""
        return default_RT * self.ddg_over_rt

    @ureg.check(None, "", "[concentration]", "[temperature]", "")
    def transform(
        self,
        p_h: Q_,
        ionic_strength: Q_,
        temperature: Q_ = default_T,
        p_mg: Q_ = default_pMg,
    ) -> Q_:
        r"""Calculate the Legendre transform for a microspecies.

        Use the Legendre transform to convert the `ddG` to the
        difference in the transformed energies of this MS and the major MS.

        Parameters
        ----------
        p_h : Quantity
            The pH value, i.e., the logarithmic scale for the molar
            concentration of hydrogen ions :math:`-log10([H+])`
        ionic_strength : Quantity
            Set the ionic strength
        temperature : Quantity
            Set the temperature, (Default value = default_T)
        p_mg : Quantity, optional
            The logarithmic molar concentration of magnesium ions
            :math:`-log10([Mg2+])`, (Default value = default_pMg)

        Returns
        -------
        Quantity
            The transformed relative :math:`\Delta G` of this microspecies.

        """
        ddg_prime = self.ddg + legendre_transform(
            p_h=p_h,
            ionic_strength=ionic_strength,
            temperature=temperature,
            num_protons=self.number_protons,
            charge=self.charge,
            p_mg=p_mg,
            num_magnesiums=self.number_magnesiums,
        )
        assert ddg_prime.check("[energy]/[substance]")
        return ddg_prime
