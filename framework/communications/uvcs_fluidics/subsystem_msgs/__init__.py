"""! @Brief This module is used to load the required dlls for the Fluidics."""

##
# @file __init__.py
#
# @brief This module is used to load the required dlls for the Fluidics
#
# @section description_subsystem_messages Description
# This module is used to load the required dlls for the Fluidics
#
# @section libraries_fluidics Libraries/Modules
# - clr module (local)
#   - Access to AddReference function.
# - System module (local)
#   - Access to the System module.
# - pathlib module (local)
#   - Access to Path class.
#
# @section notes_fluidics Notes
# - None.
#
# @section todo_fluidics TODO
# - None.
#
# @section author_fluidics Author(s)
# - Created by:
#   - Ihor Pryyma ihor.pryyma@globallogic.com on 10/07/2024.
# - Modified by:
#   - Maksym Masalov maksym.masalov@globallogic.com on 12/09/2024.
#
# Copyright (c) 2024 Alcon & GlobalLogic. All rights reserved.
import keyword
import sys

from pathlib import Path
from pythonnet import load  # type: ignore

load("coreclr")

import clr  # type: ignore # noqa: E402

bin_path = Path(__file__).parent / "bin"

dlls = [
    "NGPV.Common.AppConfig.dll",
    "NGPV.Common.Helper.dll",
    "NGPV.Common.TraceListener.dll",
    "SharedTypes.dll",
    "SubsystemMessaging.dll",
    "SubsystemMessagingResource.dll",
    "Utilities.dll",
    "VerifyTools.dll",
    "XmlTools.dll",
]

for dll in dlls:
    try:
        clr.AddReference(str(bin_path / dll))
    except Exception as e:
        print(f"Failed to load {dll}: {e}")

before_import = set(globals().keys())

from NGPV.Common.SubsystemMessagingResource import *  # type: ignore  # noqa: E402, F403
from NGPV.Common.SubsystemMessaging import *  # type: ignore  # noqa: E402, F403
from System import UInt32, Double, Boolean  # type: ignore    # noqa: E402, F403, F401

after_import = set(globals().keys())
current_module = sys.modules[__name__]

imported_names = after_import - before_import
reserved_keywords = set(keyword.kwlist)
imported_classes = []
for name in imported_names:
    obj = globals()[name]
    if isinstance(obj, type):
        imported_classes.append(obj)

for cls_ in imported_classes:
    for attr_name in dir(cls_):
        if not attr_name.startswith("__") and attr_name in reserved_keywords:
            setattr(cls_, attr_name + "_", getattr(cls_, attr_name))

__all__ = list(imported_names)
