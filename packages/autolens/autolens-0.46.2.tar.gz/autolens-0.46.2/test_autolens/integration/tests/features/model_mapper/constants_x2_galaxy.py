import autofit as af
import autolens as al
from test_autolens.integration.tests.imaging import runner

test_type = "model_mapper"
test_name = "instances_x2_galaxy"
data_type = "lens_light_dev_vaucouleurs"
data_resolution = "lsst"


def make_pipeline(name, phase_folders, non_linear_class=af.MultiNest):
    class MMPhase(al.PhaseImaging):
        def customize_priors(self, results):
            self.galaxies.lens_0.light.axis_ratio = 0.2
            self.galaxies.lens_0.light.phi = 90.0
            self.galaxies.lens_0.light.centre_0 = 1.0
            self.galaxies.lens_0.light.centre_1 = 2.0
            self.galaxies.lens_1.light.axis_ratio = 0.2
            self.galaxies.lens_1.light.phi = 90.0
            self.galaxies.lens_1.light.centre_0 = 1.0
            self.galaxies.lens_1.light.centre_1 = 2.0

    phase1 = MMPhase(
        phase_name="phase_1",
        phase_folders=phase_folders,
        galaxies=dict(
            lens_0=al.GalaxyModel(redshift=0.5, light=al.lp.EllipticalSersic),
            lens_1=al.GalaxyModel(redshift=0.5, light=al.lp.EllipticalSersic),
        ),
        non_linear_class=non_linear_class,
    )

    phase1.optimizer.const_efficiency_mode = True
    phase1.optimizer.n_live_points = 20
    phase1.optimizer.sampling_efficiency = 0.8

    return al.PipelineDataset(name, phase1)


if __name__ == "__main__":
    import sys

    runner.run(sys.modules[__name__])
