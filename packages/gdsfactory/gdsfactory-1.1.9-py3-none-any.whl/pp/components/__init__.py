# NOTE: import order matters. Only change the order if you know what you are doing
# level 0 components
from pp.components.waveguide import waveguide
from pp.components.waveguide_heater import waveguide_heater
from pp.components.waveguide_heater import wg_heater_connected

from pp.components.bend_circular import bend_circular
from pp.components.bend_circular import bend_circular180
from pp.components.bend_circular_heater import bend_circular_heater
from pp.components.bend_s import bend_s
from pp.components.bezier import bezier
from pp.components.euler.bend_euler import bend_euler90
from pp.components.euler.bend_euler import bend_euler180

from pp.components.coupler90 import coupler90
from pp.components.coupler_straight import coupler_straight
from pp.components.coupler_symmetric import coupler_symmetric
from pp.components.coupler_asymmetric import coupler_asymmetric
from pp.components.hline import hline

# basic shapes
from pp.components.circle import circle
from pp.components.compass import compass
from pp.components.cross import cross
from pp.components.crossing_waveguide import crossing
from pp.components.ellipse import ellipse
from pp.components.label import label
from pp.components.rectangle import rectangle
from pp.components.rectangle import rectangle_centered
from pp.components.ring import ring
from pp.components.taper import taper
from pp.components.taper import taper_strip_to_ridge
from pp.components.text import text

# optical test structures
from pp.components.pcm.litho_calipers import litho_calipers
from pp.components.pcm.litho_star import litho_star
from pp.components.pcm.litho_steps import litho_steps

from pp.components.grating_coupler.elliptical import grating_coupler_elliptical_te
from pp.components.grating_coupler.elliptical import grating_coupler_elliptical_tm
from pp.components.grating_coupler.uniform import grating_coupler_uniform
from pp.components.grating_coupler.grating_coupler_tree import grating_coupler_tree
from pp.components.grating_coupler.elliptical_trenches import grating_coupler_te
from pp.components.grating_coupler.elliptical_trenches import grating_coupler_tm
from pp.components.delay_snake import delay_snake
from pp.components.spiral_inner_io import spiral_inner_io_euler
from pp.components.spiral_inner_io import spiral_inner_io
from pp.components.spiral_external_io import spiral_external_io
from pp.components.spiral_circular import spiral_circular

# electrical
from pp.components.electrical.pad import pad
from pp.components.electrical.pad import pad_array

# electrical PCM
from pp.components.pcm.test_resistance import test_resistance
from pp.components.pcm.test_via import test_via

# level 1 components
from pp.components.coupler import coupler
from pp.components.coupler_ring import coupler_ring
from pp.components.ring_single_bus import ring_single_bus
from pp.components.ring_double_bus import ring_double_bus
from pp.components.mmi1x2 import mmi1x2
from pp.components.mmi2x2 import mmi2x2
from pp.components.mzi2x2 import mzi_arm
from pp.components.mzi2x2 import mzi2x2
from pp.components.mzi1x2 import mzi1x2
from pp.components.mzi import mzi
from pp.components.loop_mirror import loop_mirror

# level 2 components
from pp.components.component_lattice import component_lattice


# we test each factory component hash against the GDS saved in the library """
component_type2factory = {
    "bend_circular": bend_circular,
    "bend_circular180": bend_circular180,
    "bend_circular_heater": bend_circular_heater,
    "bend_euler90": bend_euler90,
    "bend_euler180": bend_euler180,
    "grating_coupler_elliptical_te": grating_coupler_elliptical_te,
    "grating_coupler_elliptical_tm": grating_coupler_elliptical_tm,
    "grating_coupler_tree": grating_coupler_tree,
    "bend_s": bend_s,
    "compass": compass,
    "coupler": coupler,
    "coupler90": coupler90,
    "coupler_straight": coupler_straight,
    "coupler_symmetric": coupler_symmetric,
    "coupler_asymmetric": coupler_asymmetric,
    "grating_coupler_uniform": grating_coupler_uniform,
    "litho_calipers": litho_calipers,
    "litho_star": litho_star,
    "litho_steps": litho_steps,
    "loop_mirror": loop_mirror,
    "mmi1x2": mmi1x2,
    "mmi2x2": mmi2x2,
    "mzi": mzi,
    "mzi2x2": mzi2x2,
    "mzi1x2": mzi1x2,
    "pad": pad,
    "pad_array": pad_array,
    "rectangle": rectangle,
    "ring": ring,
    "ring_single_bus": ring_single_bus,
    "ring_double_bus": ring_double_bus,
    "spiral_inner_io_euler": spiral_inner_io_euler,
    "spiral_inner_io": spiral_inner_io,
    "spiral_external_io": spiral_external_io,
    "taper": taper,
    "waveguide": waveguide,
    "waveguide_heater": waveguide_heater,
    "wg_heater_connected": wg_heater_connected,
}


def component_factory(component_type, **settings):
    """ returns a component with settings """
    import pp

    if isinstance(component_type, pp.Component):
        return component_type
    elif callable(component_type):
        return component_type(**settings)
    elif component_type not in component_type2factory.keys():
        raise ValueError(
            "component types available: \n {}".format(
                "\n".join(component_type2factory.keys())
            )
        )
    return component_type2factory[component_type](**settings)


# all this components are available as pp.c
__all__ = [
    "bend_circular",
    "bend_circular180",
    "bend_circular_heater",
    "bend_euler90",
    "bend_euler180",
    "bend_s",
    "bezier",
    "compass",
    "cross",
    "ring",
    "ellipse",
    "circle",
    "coupler",
    "coupler_ring",
    "coupler90",
    "coupler_straight",
    "coupler_symmetric",
    "coupler_asymmetric",
    "crossing",
    "delay_snake",
    "grating_coupler_uniform",
    "grating_coupler_te",
    "grating_coupler_tm",
    "grating_coupler_elliptical_te",
    "grating_coupler_elliptical_tm",
    "grating_coupler_tree",
    "hline",
    "label",
    "litho_calipers",
    "litho_star",
    "litho_steps",
    "loop_mirror",
    "mmi1x2",
    "mmi2x2",
    "mzi_arm",
    "mzi",
    "pad",
    "pad_array",
    "rectangle",
    "rectangle_centered",
    "ring_single_bus",
    "ring_double_bus",
    "spiral_circular",
    "spiral_inner_io",
    "spiral_inner_io_euler",
    "spiral_external_io",
    "taper",
    "taper_strip_to_ridge",
    "text",
    "test_via",
    "test_resistance",
    "waveguide",
    "waveguide_heater",
    "wg_heater_connected",
    "component_lattice",
]

leaf_components = ["bend_circular", "bend_euler90", "coupler", "mmi1x2", "mmi2x2"]

_skip_test = set(["label"])
_skip_test_ports = set(["grating_coupler_tree"])


def write_test_properties():
    """ writes a regression test for all the component properties dict"""
    with open("test_components.py", "w") as f:
        f.write(
            "# this code has been automatically generated from pp/components/__init__.py\n"
        )
        f.write("import pp\n\n")

        for c in set(__all__) - _skip_test:
            f.write(
                f"""
def test_{c}(data_regression):
    c = pp.c.{c}()
    data_regression.check(c.get_settings())

"""
            )


def write_test_ports():
    """ writes a regression test for all the ports """
    with open("test_ports.py", "w") as f:
        f.write(
            "# this code has been automatically generated from pp/components/__init__.py\n"
        )
        f.write("import pp\n\n")

        for component_function in (
            set(component_type2factory.values()) - _skip_test_ports
        ):
            c = component_function.__name__
            if component_function().ports:

                f.write(
                    f"""
def test_{c}(num_regression):
    c = pp.c.{c}()
    num_regression.check(c.get_ports_array())

    """
                )


if __name__ == "__main__":
    write_test_properties()
    write_test_ports()
