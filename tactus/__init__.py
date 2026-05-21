#!/usr/bin/env python3
"""Package to run the Destination Earth on Demand Extremes system."""

from pathlib import Path

import tactus.meta as tactus_meta
from tactus.aux_types import QuasiConstant


class GeneralConstants(QuasiConstant):
    """General package-related constants."""

    PACKAGE_NAME = tactus_meta.PACKAGE_NAME
    VERSION = tactus_meta.PACKAGE_VERSION
    PACKAGE_DIRECTORY = Path(__file__).parent
