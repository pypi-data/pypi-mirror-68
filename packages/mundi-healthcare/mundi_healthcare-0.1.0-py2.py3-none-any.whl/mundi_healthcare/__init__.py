"""
A Mundi plugin with healthcare statistics.
"""
__author__ = "Fábio Mendes"
__version__ = "0.1.0"

from .functions import hospital_capacity, hospital_capacity_public, icu_capacity, icu_capacity_public

FUNCTIONS = {
    "hospital_capacity": hospital_capacity,
    "hospital_capacity_public": hospital_capacity_public,
    "icu_capacity": icu_capacity,
    "icu_capacity_public": icu_capacity_public,
}


def register(check_environ=False):
    """
    Enable plugin.

    This is executed automatically
    """
    from mundi.loader import register
    from mundi.types.region import REGION_PLUGINS

    if check_environ:
        import os
        if os.environ.get("MUNDI_DEMOGRAPHY", "on").lower() in ("off", "false", "no"):
            return

    for k, v in FUNCTIONS.items():
        register(k, v)

    REGION_PLUGINS["hospital_capacity"] = lambda x: hospital_capacity(x.id)
    REGION_PLUGINS["hospital_capacity_public"] = lambda x: hospital_capacity_public(x.id)
    REGION_PLUGINS["icu_capacity"] = lambda x: icu_capacity(x.id)
    REGION_PLUGINS["icu_capacity_public"] = lambda x: icu_capacity_public(x.id)


def unregister():
    """
    Disable plugin.
    """
    from mundi.loader import unregister

    for k, v in FUNCTIONS.items():
        unregister(k, function=v)


register(check_environ=True)
