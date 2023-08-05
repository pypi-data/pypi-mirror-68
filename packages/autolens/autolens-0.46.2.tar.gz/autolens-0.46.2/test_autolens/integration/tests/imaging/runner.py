import os

import autofit as af
import autoarray as aa
from test_autolens.integration import integration_util
from test_autolens.simulate.imaging import simulate_util


def run(
    module,
    test_name=None,
    non_linear_class=af.MultiNest,
    config_folder="config",
    mask=None,
    positions=None,
):

    test_name = test_name or module.test_name
    test_path = "{}/../..".format(os.path.dirname(os.path.realpath(__file__)))
    output_path = f"{test_path}.output/imaging"
    config_path = f"{test_path}/{config_folder}"
    af.conf.instance = af.conf.Config(config_path=config_path, output_path=output_path)
    integration_util.reset_paths(test_name=test_name, output_path=output_path)

    imaging = simulate_util.load_test_imaging(
        data_type=module.data_type,
        data_resolution=module.data_resolution,
        name="test_dataset",
        metadata={"test": 2},
    )

    if mask is None:
        mask = aa.Mask.circular(
            shape_2d=imaging.shape_2d, pixel_scales=imaging.pixel_scales, radius=3.0
        )

    module.make_pipeline(
        name=test_name,
        phase_folders=[module.test_type, test_name],
        non_linear_class=non_linear_class,
    ).run(dataset=imaging, mask=mask)


def run_a_mock(module):
    # noinspection PyTypeChecker
    run(
        module,
        test_name=f"{module.test_name}_mock",
        non_linear_class=af.MockNLO,
        config_folder="config_mock",
    )


def run_with_multi_nest(module):
    # noinspection PyTypeChecker
    run(
        module,
        test_name=f"{module.test_name}_nest",
        non_linear_class=af.MultiNest,
        config_folder="config_mock",
    )
