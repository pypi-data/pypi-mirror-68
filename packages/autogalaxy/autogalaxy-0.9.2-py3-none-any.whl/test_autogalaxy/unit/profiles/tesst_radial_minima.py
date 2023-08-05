from __future__ import division, print_function

import autofit as af
import os

test_path = "{}/config/".format(os.path.dirname(os.path.realpath(__file__)))
af.conf.instance = af.conf.Config(config_path=test_path)

import numpy as np
import pytest


class TestGaussian:
    def test__transform_grid_wrapper_and_move_radial_minimum_wrappers(self):

        gaussian = ag.EllipticalGaussian(centre=(0.0, 0.0))

        image_1 = gaussian.profile_image_from_grid(grid=grid_01)
        image_0 = gaussian.profile_image_from_grid(grid=np.array([[0.000000001, 0.0]]))
        assert image_0 == pytest.approx(image_1, 1.0e-4)

        gaussian = ag.EllipticalGaussian(centre=(1.0, 1.0))

        image_1 = gaussian.profile_image_from_grid(grid=grid_22)
        image_0 = gaussian.profile_image_from_grid(grid=np.array([[1.000000001, 1.0]]))
        assert image_0 == pytest.approx(image_1, 1.0e-4)

        gaussian = ag.SphericalGaussian(centre=(0.0, 0.0))

        image_1 = gaussian.profile_image_from_grid(grid=grid_01)
        image_0 = gaussian.profile_image_from_grid(grid=np.array([[0.000000001, 0.0]]))
        assert image_0 == pytest.approx(image_1, 1.0e-4)

        gaussian = ag.SphericalGaussian(centre=(1.0, 1.0))

        image_1 = gaussian.profile_image_from_grid(grid=grid_22)
        image_0 = gaussian.profile_image_from_grid(grid=np.array([[1.000000001, 1.0]]))
        assert image_0 == pytest.approx(image_1, 1.0e-4)


class TestSersic:
    def test__transform_grid_wrapper_and_move_radial_minimum_wrappers(self):

        sersic = ag.EllipticalSersic(centre=(0.0, 0.0))

        image_1 = sersic.profile_image_from_grid(grid=grid_01)
        image_0 = sersic.profile_image_from_grid(grid=np.array([[0.000000001, 0.0]]))
        assert image_0 == pytest.approx(image_1, 1.0e-4)

        sersic = ag.EllipticalSersic(centre=(1.0, 1.0))

        image_1 = sersic.profile_image_from_grid(grid=grid_22)
        image_0 = sersic.profile_image_from_grid(grid=np.array([[1.000000001, 1.0]]))
        assert image_0 == pytest.approx(image_1, 1.0e-4)

        sersic = ag.light_profiles.SphericalSersic(centre=(0.0, 0.0))

        image_1 = sersic.profile_image_from_grid(grid=grid_01)
        image_0 = sersic.profile_image_from_grid(grid=np.array([[0.000000001, 0.0]]))
        assert image_0 == pytest.approx(image_1, 1.0e-4)

        sersic = ag.light_profiles.SphericalSersic(centre=(1.0, 1.0))

        image_1 = sersic.profile_image_from_grid(grid=grid_22)
        image_0 = sersic.profile_image_from_grid(grid=np.array([[1.000000001, 1.0]]))
        assert image_0 == pytest.approx(image_1, 1.0e-4)


class TestExponential:
    def test__transform_grid_wrapper_and_move_radial_minimum_wrappers(self):

        exponential = ag.EllipticalExponential(centre=(0.0, 0.0))

        image_1 = exponential.profile_image_from_grid(grid=grid_01)
        image_0 = exponential.profile_image_from_grid(
            grid=np.array([[0.000000001, 0.0]])
        )
        assert image_0 == pytest.approx(image_1, 1.0e-4)

        exponential = ag.EllipticalExponential(centre=(1.0, 1.0))

        image_1 = exponential.profile_image_from_grid(grid=grid_22)
        image_0 = exponential.profile_image_from_grid(
            grid=np.array([[1.000000001, 1.0]])
        )
        assert image_0 == pytest.approx(image_1, 1.0e-4)

        exponential = ag.SphericalExponential(centre=(0.0, 0.0))

        image_1 = exponential.profile_image_from_grid(grid=grid_01)
        image_0 = exponential.profile_image_from_grid(
            grid=np.array([[0.000000001, 0.0]])
        )
        assert image_0 == pytest.approx(image_1, 1.0e-4)

        exponential = ag.SphericalExponential(centre=(1.0, 1.0))

        image_1 = exponential.profile_image_from_grid(grid=grid_22)
        image_0 = exponential.profile_image_from_grid(
            grid=np.array([[1.000000001, 1.0]])
        )
        assert image_0 == pytest.approx(image_1, 1.0e-4)


class TestDevVaucouleurs:
    def test__transform_grid_wrapper_and_move_radial_minimum_wrappers(self):
        dev_vaucouleurs = ag.EllipticalDevVaucouleurs(centre=(0.0, 0.0))

        image_1 = dev_vaucouleurs.profile_image_from_grid(grid=grid_01)
        image_0 = dev_vaucouleurs.profile_image_from_grid(
            grid=np.array([[0.000000001, 0.0]])
        )
        assert image_0 == pytest.approx(image_1, 1.0e-4)

        dev_vaucouleurs = ag.EllipticalDevVaucouleurs(centre=(1.0, 1.0))

        image_1 = dev_vaucouleurs.profile_image_from_grid(grid=grid_22)
        image_0 = dev_vaucouleurs.profile_image_from_grid(
            grid=np.array([[1.000000001, 1.0]])
        )
        assert image_0 == pytest.approx(image_1, 1.0e-4)

        dev_vaucouleurs = ag.SphericalDevVaucouleurs(centre=(0.0, 0.0))

        image_1 = dev_vaucouleurs.profile_image_from_grid(grid=grid_01)
        image_0 = dev_vaucouleurs.profile_image_from_grid(
            grid=np.array([[0.000000001, 0.0]])
        )
        assert image_0 == pytest.approx(image_1, 1.0e-4)

        dev_vaucouleurs = ag.SphericalDevVaucouleurs(centre=(1.0, 1.0))

        image_1 = dev_vaucouleurs.profile_image_from_grid(grid=grid_22)
        image_0 = dev_vaucouleurs.profile_image_from_grid(
            grid=np.array([[1.000000001, 1.0]])
        )
        assert image_0 == pytest.approx(image_1, 1.0e-4)


class TestCoreSersic:
    def test__transform_grid_wrapper_and_move_radial_minimum_wrappers(self):
        core_sersic = ag.EllipticalCoreSersic(centre=(0.0, 0.0))

        image_1 = core_sersic.profile_image_from_grid(grid=grid_01)
        image_0 = core_sersic.profile_image_from_grid(
            grid=np.array([[0.000000001, 0.0]])
        )
        assert image_0 == pytest.approx(image_1, 1.0e-4)

        core_sersic = ag.EllipticalCoreSersic(centre=(1.0, 1.0))

        image_1 = core_sersic.profile_image_from_grid(grid=grid_22)
        image_0 = core_sersic.profile_image_from_grid(
            grid=np.array([[1.000000001, 1.0]])
        )
        assert image_0 == pytest.approx(image_1, 1.0e-4)

        core_sersic = ag.SphericalCoreSersic(centre=(0.0, 0.0))

        image_1 = core_sersic.profile_image_from_grid(grid=grid_01)
        image_0 = core_sersic.profile_image_from_grid(
            grid=np.array([[0.000000001, 0.0]])
        )
        assert image_0 == pytest.approx(image_1, 1.0e-4)

        core_sersic = ag.SphericalCoreSersic(centre=(1.0, 1.0))

        image_1 = core_sersic.profile_image_from_grid(grid=grid_22)
        image_0 = core_sersic.profile_image_from_grid(
            grid=np.array([[1.000000001, 1.0]])
        )
        assert image_0 == pytest.approx(image_1, 1.0e-4)


class TestPointMass:
    def test__transform_grid_wrapper_and_move_radial_minimum_wrappers(self):

        point_mass = ag.PointMass(centre=(0.0, 0.0), einstein_radius=1.0)

        deflections_1 = point_mass.deflections_from_grid(grid=grid_01)
        deflections_0 = point_mass.deflections_from_grid(
            grid=np.array([[0.00000001, 0.0]])
        )
        assert deflections_0 == pytest.approx(deflections_1, 1.0e-4)

        point_mass = ag.PointMass(centre=(1.0, 1.0), einstein_radius=1.0)

        deflections_1 = point_mass.deflections_from_grid(grid=grid_22)
        deflections_0 = point_mass.deflections_from_grid(
            grid=np.array([[1.000000001, 1.0]])
        )
        assert deflections_0 == pytest.approx(deflections_1, 1.0e-4)


class TestCoredPowerLaw:
    def test__transform_grid_wrapper_and_move_radial_minimum_wrappers(self):
        cored_power_law = ag.EllipticalCoredPowerLaw(
            centre=(0.0, 0.0), einstein_radius=1.0, slope=2.0
        )

        convergence_1 = cored_power_law.convergence_from_grid(grid=grid_01)
        convergence_0 = cored_power_law.convergence_from_grid(
            grid=np.array([[1e-8, 0.0]])
        )
        assert convergence_0 == pytest.approx(convergence_1, 1.0e-4)


class TestPowerLaw:
    def test__transform_grid_wrapper_and_move_radial_minimum_wrappers(self):

        power_law = ag.EllipticalPowerLaw(
            centre=(0.0, 0.0), einstein_radius=1.0, slope=2.0
        )

        convergence_1 = power_law.convergence_from_grid(grid=grid_01)
        convergence_0 = power_law.convergence_from_grid(grid=np.array([[1.0e-9, 0.0]]))
        assert convergence_0 == pytest.approx(convergence_1, 1.0e-4)

        power_law = ag.SphericalPowerLaw(
            centre=(-0.7, 0.5), einstein_radius=1.3, slope=1.8
        )

        mask = np.array(
            [
                [True, True, True, True, True],
                [True, False, False, False, True],
                [True, False, True, False, True],
                [True, False, False, False, True],
                [True, True, True, True, True],
            ]
        )

        mask = aa.Mask.manual(mask, real_space_pixel_scales=1.0)

        grid = aa.MaskedGrid.from_mask(mask=mask)

        regular_with_interp = grid.new_grid_with_interpolator(
            pixel_scale_interpolation_grid=0.5
        )
        interp_deflections = power_law.deflections_from_grid(grid=regular_with_interp)

        interpolator = grids.Interpolator.from_mask_grid_and_pixel_scale_interpolation_grids(
            mask=mask, grid=grid, pixel_scale_interpolation_grid=0.5
        )

        interp_deflections_values = power_law.deflections_from_grid(
            grid=interpolator.interp_grid
        )

        interp_deflections_manual_y = interpolator.interpolated_values_from_values(
            values=interp_deflections_values[:, 0]
        )
        interp_deflections_manual_x = interpolator.interpolated_values_from_values(
            values=interp_deflections_values[:, 1]
        )

        assert (interp_deflections_manual_y != interp_deflections[:, 0]).all()
        assert (interp_deflections_manual_x != interp_deflections[:, 1]).all()


class TestCoredIsothermal:
    def test__transform_grid_wrapper_and_move_radial_minimum_wrappers(self):
        cored_isothermal = ag.EllipticalCoredIsothermal(
            centre=(0.0, 0.0), einstein_radius=1.0
        )

        convergence_1 = cored_isothermal.convergence_from_grid(grid=grid_01)
        convergence_0 = cored_isothermal.convergence_from_grid(
            grid=np.array([[0.000000001, 0.0]])
        )
        assert convergence_0 == pytest.approx(convergence_1, 1.0e-4)

        cored_isothermal = ag.EllipticalCoredIsothermal(
            centre=(1.0, 1.0), einstein_radius=1.0
        )

        convergence_1 = cored_isothermal.convergence_from_grid(grid=grid_22)
        convergence_0 = cored_isothermal.convergence_from_grid(
            grid=np.array([[1.000000001, 1.0]])
        )
        assert convergence_0 == pytest.approx(convergence_1, 1.0e-4)

        cored_isothermal = ag.SphericalCoredIsothermal(
            centre=(0.0, 0.0), einstein_radius=1.0
        )

        convergence_1 = cored_isothermal.convergence_from_grid(grid=grid_01)
        convergence_0 = cored_isothermal.convergence_from_grid(
            grid=np.array([[0.000000001, 0.0]])
        )
        assert convergence_0 == pytest.approx(convergence_1, 1.0e-4)

        cored_isothermal = ag.SphericalCoredIsothermal(
            centre=(1.0, 1.0), einstein_radius=1.0
        )

        convergence_1 = cored_isothermal.convergence_from_grid(grid=grid_22)
        convergence_0 = cored_isothermal.convergence_from_grid(
            grid=np.array([[1.000000001, 1.0]])
        )
        assert convergence_0 == pytest.approx(convergence_1, 1.0e-4)

        cored_isothermal = ag.EllipticalCoredIsothermal(
            centre=(0.0, 0.0), einstein_radius=1.0
        )

        potential_1 = cored_isothermal.potential_from_grid(grid=grid_01)
        potential_0 = cored_isothermal.potential_from_grid(
            grid=np.array([[0.000000001, 0.0]])
        )
        assert potential_0 == pytest.approx(potential_1, 1.0e-4)

        cored_isothermal = ag.EllipticalCoredIsothermal(
            centre=(1.0, 1.0), einstein_radius=1.0
        )

        potential_1 = cored_isothermal.potential_from_grid(grid=grid_22)
        potential_0 = cored_isothermal.potential_from_grid(
            grid=np.array([[1.000000001, 1.0]])
        )
        assert potential_0 == pytest.approx(potential_1, 1.0e-4)

        cored_isothermal = ag.SphericalCoredIsothermal(
            centre=(0.0, 0.0), einstein_radius=1.0
        )

        potential_1 = cored_isothermal.potential_from_grid(grid=grid_01)
        potential_0 = cored_isothermal.potential_from_grid(
            grid=np.array([[0.000000001, 0.0]])
        )
        assert potential_0 == pytest.approx(potential_1, 1.0e-4)

        cored_isothermal = ag.SphericalCoredIsothermal(
            centre=(1.0, 1.0), einstein_radius=1.0
        )

        potential_1 = cored_isothermal.potential_from_grid(grid=grid_22)
        potential_0 = cored_isothermal.potential_from_grid(
            grid=np.array([[1.000000001, 1.0]])
        )
        assert potential_0 == pytest.approx(potential_1, 1.0e-4)

        cored_isothermal = ag.EllipticalCoredIsothermal(
            centre=(0.0, 0.0), einstein_radius=1.0
        )

        deflections_1 = cored_isothermal.deflections_from_grid(grid=grid_01)
        deflections_0 = cored_isothermal.deflections_from_grid(
            grid=np.array([[0.000000001, 0.0]])
        )
        assert deflections_0 == pytest.approx(deflections_1, 1.0e-4)

        cored_isothermal = ag.EllipticalCoredIsothermal(
            centre=(1.0, 1.0), einstein_radius=1.0
        )

        deflections_1 = cored_isothermal.deflections_from_grid(grid=grid_22)
        deflections_0 = cored_isothermal.deflections_from_grid(
            grid=np.array([[1.000000001, 1.0]])
        )
        assert deflections_0 == pytest.approx(deflections_1, 1.0e-4)

        cored_isothermal = ag.SphericalCoredIsothermal(
            centre=(0.0, 0.0), einstein_radius=1.0
        )

        deflections_1 = cored_isothermal.deflections_from_grid(grid=grid_01)
        deflections_0 = cored_isothermal.deflections_from_grid(
            grid=np.array([[0.000000001, 0.0]])
        )
        assert deflections_0 == pytest.approx(deflections_1, 1.0e-4)

        cored_isothermal = ag.SphericalCoredIsothermal(
            centre=(1.0, 1.0), einstein_radius=1.0
        )

        deflections_1 = cored_isothermal.deflections_from_grid(grid=grid_22)
        deflections_0 = cored_isothermal.deflections_from_grid(
            grid=np.array([[1.000000001, 1.0]])
        )
        assert deflections_0 == pytest.approx(deflections_1, 1.0e-4)


class TestIsothermal:
    def test__transform_grid_wrapper_and_move_radial_minimum_wrappers(self):
        isothermal = ag.mass_profiles.EllipticalIsothermal(
            centre=(0.0, 0.0), einstein_radius=1.0
        )

        convergence_1 = isothermal.convergence_from_grid(grid=grid_01)
        convergence_0 = isothermal.convergence_from_grid(
            grid=np.array([[0.000000001, 0.0]])
        )
        assert convergence_0 == pytest.approx(convergence_1, 1.0e-4)

        isothermal = ag.mass_profiles.EllipticalIsothermal(
            centre=(1.0, 1.0), einstein_radius=1.0
        )

        convergence_1 = isothermal.convergence_from_grid(grid=grid_22)
        convergence_0 = isothermal.convergence_from_grid(
            grid=np.array([[1.000000001, 1.0]])
        )
        assert convergence_0 == pytest.approx(convergence_1, 1.0e-4)

        isothermal = ag.mass_profiles.SphericalIsothermal(
            centre=(0.0, 0.0), einstein_radius=1.0
        )

        convergence_1 = isothermal.convergence_from_grid(grid=grid_01)
        convergence_0 = isothermal.convergence_from_grid(
            grid=np.array([[0.000000001, 0.0]])
        )
        assert convergence_0 == pytest.approx(convergence_1, 1.0e-4)

        isothermal = ag.mass_profiles.SphericalIsothermal(
            centre=(1.0, 1.0), einstein_radius=1.0
        )

        convergence_1 = isothermal.convergence_from_grid(grid=grid_22)
        convergence_0 = isothermal.convergence_from_grid(
            grid=np.array([[1.000000001, 1.0]])
        )
        assert convergence_0 == pytest.approx(convergence_1, 1.0e-4)

        isothermal = ag.mass_profiles.EllipticalIsothermal(
            centre=(0.0, 0.0), einstein_radius=1.0
        )

        potential_1 = isothermal.potential_from_grid(grid=grid_01)
        potential_0 = isothermal.potential_from_grid(
            grid=np.array([[0.000000001, 0.0]])
        )
        assert potential_0 == pytest.approx(potential_1, 1.0e-4)

        isothermal = ag.mass_profiles.EllipticalIsothermal(
            centre=(1.0, 1.0), einstein_radius=1.0
        )

        potential_1 = isothermal.potential_from_grid(grid=grid_22)
        potential_0 = isothermal.potential_from_grid(
            grid=np.array([[1.000000001, 1.0]])
        )
        assert potential_0 == pytest.approx(potential_1, 1.0e-4)

        isothermal = ag.mass_profiles.SphericalIsothermal(
            centre=(0.0, 0.0), einstein_radius=1.0
        )

        potential_1 = isothermal.potential_from_grid(grid=grid_01)
        potential_0 = isothermal.potential_from_grid(
            grid=np.array([[0.000000001, 0.0]])
        )
        assert potential_0 == pytest.approx(potential_1, 1.0e-4)

        isothermal = ag.mass_profiles.SphericalIsothermal(
            centre=(1.0, 1.0), einstein_radius=1.0
        )

        potential_1 = isothermal.potential_from_grid(grid=grid_22)
        potential_0 = isothermal.potential_from_grid(
            grid=np.array([[1.000000001, 1.0]])
        )
        assert potential_0 == pytest.approx(potential_1, 1.0e-4)

        isothermal = ag.mass_profiles.EllipticalIsothermal(
            centre=(0.0, 0.0), einstein_radius=1.0
        )

        deflections_1 = isothermal.deflections_from_grid(grid=grid_01)
        deflections_0 = isothermal.deflections_from_grid(
            grid=np.array([[0.000000001, 0.0]])
        )
        assert deflections_0 == pytest.approx(deflections_1, 1.0e-4)

        isothermal = ag.mass_profiles.EllipticalIsothermal(
            centre=(1.0, 1.0), einstein_radius=1.0
        )

        deflections_1 = isothermal.deflections_from_grid(grid=grid_22)
        deflections_0 = isothermal.deflections_from_grid(
            grid=np.array([[1.000000001, 1.0]])
        )
        assert deflections_0 == pytest.approx(deflections_1, 1.0e-4)

        isothermal = ag.mass_profiles.SphericalIsothermal(
            centre=(0.0, 0.0), einstein_radius=1.0
        )

        deflections_1 = isothermal.deflections_from_grid(grid=grid_01)
        deflections_0 = isothermal.deflections_from_grid(
            grid=np.array([[0.000000001, 0.0]])
        )
        assert deflections_0 == pytest.approx(deflections_1, 1.0e-4)

        isothermal = ag.mass_profiles.SphericalIsothermal(
            centre=(1.0, 1.0), einstein_radius=1.0
        )

        deflections_1 = isothermal.deflections_from_grid(grid=grid_22)
        deflections_0 = isothermal.deflections_from_grid(
            grid=np.array([[1.000000001, 1.0]])
        )
        assert deflections_0 == pytest.approx(deflections_1, 1.0e-4)


class TestGeneralizedNFW:
    def test__transform_grid_wrapper_and_move_radial_minimum_wrappers(self):
        gnfw = ag.mass_profiles.SphericalGeneralizedNFW(centre=(0.0, 0.0))

        convergence_1 = gnfw.convergence_from_grid(grid=grid_01)
        convergence_0 = gnfw.convergence_from_grid(grid=np.array([[0.000000001, 0.0]]))
        assert convergence_0 == pytest.approx(convergence_1, 1.0e-4)

        gnfw = ag.mass_profiles.SphericalGeneralizedNFW(centre=(1.0, 1.0))

        convergence_1 = gnfw.convergence_from_grid(grid=grid_22)
        convergence_0 = gnfw.convergence_from_grid(grid=np.array([[1.000000001, 1.0]]))
        assert convergence_0 == pytest.approx(convergence_1, 1.0e-4)

        gnfw = ag.mass_profiles.SphericalGeneralizedNFW(centre=(0.0, 0.0))

        potential_1 = gnfw.potential_from_grid(grid=grid_01)
        potential_0 = gnfw.potential_from_grid(grid=np.array([[0.000000001, 0.0]]))
        assert potential_0 == pytest.approx(potential_1, 1.0e-4)

        gnfw = ag.mass_profiles.SphericalGeneralizedNFW(centre=(1.0, 1.0))

        potential_1 = gnfw.potential_from_grid(grid=grid_22)
        potential_0 = gnfw.potential_from_grid(grid=np.array([[1.000000001, 1.0]]))
        assert potential_0 == pytest.approx(potential_1, 1.0e-4)

        gnfw = ag.mass_profiles.SphericalGeneralizedNFW(centre=(0.0, 0.0))

        deflections_1 = gnfw.deflections_from_grid(grid=grid_01)
        deflections_0 = gnfw.deflections_from_grid(grid=np.array([[0.000000001, 0.0]]))
        assert deflections_0 == pytest.approx(deflections_1, 1.0e-4)

        gnfw = ag.mass_profiles.SphericalGeneralizedNFW(centre=(1.0, 1.0))

        deflections_1 = gnfw.deflections_from_grid(grid=grid_22)
        deflections_0 = gnfw.deflections_from_grid(grid=np.array([[1.000000001, 1.0]]))
        assert deflections_0 == pytest.approx(deflections_1, 1.0e-4)


class TestTruncatedNFW:
    def test__transform_grid_wrapper_and_move_radial_minimum_wrappers(self):
        truncated_nfw = ag.mass_profiles.SphericalTruncatedNFW(centre=(0.0, 0.0))

        convergence_1 = truncated_nfw.convergence_from_grid(grid=grid_01)
        convergence_0 = truncated_nfw.convergence_from_grid(
            grid=np.array([[0.000000001, 0.0]])
        )
        assert convergence_0 == pytest.approx(convergence_1, 1.0e-4)

        truncated_nfw = ag.mass_profiles.SphericalTruncatedNFW(centre=(1.0, 1.0))

        convergence_1 = truncated_nfw.convergence_from_grid(grid=grid_22)
        convergence_0 = truncated_nfw.convergence_from_grid(
            grid=np.array([[1.000000001, 1.0]])
        )
        assert convergence_0 == pytest.approx(convergence_1, 1.0e-4)

        truncated_nfw = ag.mass_profiles.SphericalTruncatedNFW(centre=(0.0, 0.0))

        potential_1 = truncated_nfw.potential_from_grid(grid=grid_01)
        potential_0 = truncated_nfw.potential_from_grid(
            grid=np.array([[0.000000001, 0.0]])
        )
        assert potential_0 == pytest.approx(potential_1, 1.0e-4)

        truncated_nfw = ag.mass_profiles.SphericalTruncatedNFW(centre=(1.0, 1.0))

        potential_1 = truncated_nfw.potential_from_grid(grid=grid_22)
        potential_0 = truncated_nfw.potential_from_grid(
            grid=np.array([[1.000000001, 1.0]])
        )
        assert potential_0 == pytest.approx(potential_1, 1.0e-4)

        truncated_nfw = ag.mass_profiles.SphericalTruncatedNFW(centre=(0.0, 0.0))

        deflections_1 = truncated_nfw.deflections_from_grid(grid=grid_01)
        deflections_0 = truncated_nfw.deflections_from_grid(
            grid=np.array([[0.000000001, 0.0]])
        )
        assert deflections_0 == pytest.approx(deflections_1, 1.0e-4)

        truncated_nfw = ag.mass_profiles.SphericalTruncatedNFW(centre=(1.0, 1.0))

        deflections_1 = truncated_nfw.deflections_from_grid(grid=grid_22)
        deflections_0 = truncated_nfw.deflections_from_grid(
            grid=np.array([[1.000000001, 1.0]])
        )
        assert deflections_0 == pytest.approx(deflections_1, 1.0e-4)


class TestNFW:
    def test__transform_grid_wrapper_and_move_radial_minimum_wrappers(self):
        nfw = ag.mass_profiles.EllipticalNFW(centre=(0.0, 0.0))

        convergence_1 = nfw.convergence_from_grid(grid=grid_01)
        convergence_0 = nfw.convergence_from_grid(grid=np.array([[0.000000001, 0.0]]))
        assert convergence_0 == pytest.approx(convergence_1, 1.0e-4)

        nfw = ag.mass_profiles.EllipticalNFW(centre=(1.0, 1.0))

        convergence_1 = nfw.convergence_from_grid(grid=grid_22)
        convergence_0 = nfw.convergence_from_grid(grid=np.array([[1.000000001, 1.0]]))
        assert convergence_0 == pytest.approx(convergence_1, 1.0e-4)

        nfw = ag.mass_profiles.SphericalNFW(centre=(0.0, 0.0))

        convergence_1 = nfw.convergence_from_grid(grid=grid_01)
        convergence_0 = nfw.convergence_from_grid(grid=np.array([[0.000000001, 0.0]]))
        assert convergence_0 == pytest.approx(convergence_1, 1.0e-4)

        nfw = ag.mass_profiles.SphericalNFW(centre=(1.0, 1.0))

        convergence_1 = nfw.convergence_from_grid(grid=grid_22)
        convergence_0 = nfw.convergence_from_grid(grid=np.array([[1.000000001, 1.0]]))
        assert convergence_0 == pytest.approx(convergence_1, 1.0e-4)

        nfw = ag.mass_profiles.EllipticalNFW(centre=(0.0, 0.0))

        potential_1 = nfw.potential_from_grid(grid=grid_01)
        potential_0 = nfw.potential_from_grid(grid=np.array([[0.000000001, 0.0]]))
        assert potential_0 == pytest.approx(potential_1, 1.0e-4)

        nfw = ag.mass_profiles.EllipticalNFW(centre=(1.0, 1.0))

        potential_1 = nfw.potential_from_grid(grid=grid_22)
        potential_0 = nfw.potential_from_grid(grid=np.array([[1.000000001, 1.0]]))
        assert potential_0 == pytest.approx(potential_1, 1.0e-4)

        nfw = ag.mass_profiles.SphericalNFW(centre=(0.0, 0.0))

        potential_1 = nfw.potential_from_grid(grid=grid_01)
        potential_0 = nfw.potential_from_grid(grid=np.array([[0.000000001, 0.0]]))
        assert potential_0 == pytest.approx(potential_1, 1.0e-4)

        nfw = ag.mass_profiles.SphericalNFW(centre=(1.0, 1.0))

        potential_1 = nfw.potential_from_grid(grid=grid_22)
        potential_0 = nfw.potential_from_grid(grid=np.array([[1.000000001, 1.0]]))
        assert potential_0 == pytest.approx(potential_1, 1.0e-4)

        nfw = ag.mass_profiles.EllipticalNFW(centre=(0.0, 0.0))

        deflections_1 = nfw.deflections_from_grid(grid=grid_01)
        deflections_0 = nfw.deflections_from_grid(grid=np.array([[0.000000001, 0.0]]))
        assert deflections_0 == pytest.approx(deflections_1, 1.0e-4)

        nfw = ag.mass_profiles.EllipticalNFW(centre=(1.0, 1.0))

        deflections_1 = nfw.deflections_from_grid(grid=grid_22)
        deflections_0 = nfw.deflections_from_grid(grid=np.array([[1.000000001, 1.0]]))
        assert deflections_0 == pytest.approx(deflections_1, 1.0e-4)

        nfw = ag.mass_profiles.SphericalNFW(centre=(0.0, 0.0))

        deflections_1 = nfw.deflections_from_grid(grid=grid_01)
        deflections_0 = nfw.deflections_from_grid(grid=np.array([[0.000000001, 0.0]]))
        assert deflections_0 == pytest.approx(deflections_1, 1.0e-4)

        nfw = ag.mass_profiles.SphericalNFW(centre=(1.0, 1.0))

        deflections_1 = nfw.deflections_from_grid(grid=grid_22)
        deflections_0 = nfw.deflections_from_grid(grid=np.array([[1.000000001, 1.0]]))
        assert deflections_0 == pytest.approx(deflections_1, 1.0e-4)


class TestSersic:
    def test__transform_grid_wrapper_and_move_radial_minimum_wrappers(self):
        sersic = ag.EllipticalSersic(centre=(0.0, 0.0))

        convergence_1 = sersic.convergence_from_grid(grid=grid_01)
        convergence_0 = sersic.convergence_from_grid(
            grid=np.array([[0.000000001, 0.0]])
        )
        assert convergence_0 == pytest.approx(convergence_1, 1.0e-4)

        sersic = ag.EllipticalSersic(centre=(1.0, 1.0))

        convergence_1 = sersic.convergence_from_grid(grid=grid_22)
        convergence_0 = sersic.convergence_from_grid(
            grid=np.array([[1.000000001, 1.0]])
        )
        assert convergence_0 == pytest.approx(convergence_1, 1.0e-4)

        sersic = ag.SphericalSersic(centre=(0.0, 0.0))

        convergence_1 = sersic.convergence_from_grid(grid=grid_01)
        convergence_0 = sersic.convergence_from_grid(
            grid=np.array([[0.000000001, 0.0]])
        )
        assert convergence_0 == pytest.approx(convergence_1, 1.0e-4)

        sersic = ag.SphericalSersic(centre=(1.0, 1.0))

        convergence_1 = sersic.convergence_from_grid(grid=grid_22)
        convergence_0 = sersic.convergence_from_grid(
            grid=np.array([[1.000000001, 1.0]])
        )
        assert convergence_0 == pytest.approx(convergence_1, 1.0e-4)

        sersic = ag.EllipticalSersic(centre=(0.0, 0.0))

        deflections_1 = sersic.deflections_from_grid(grid=grid_01)
        deflections_0 = sersic.deflections_from_grid(
            grid=np.array([[0.000000001, 0.0]])
        )
        assert deflections_0 == pytest.approx(deflections_1, 1.0e-4)

        sersic = ag.EllipticalSersic(centre=(1.0, 1.0))

        deflections_1 = sersic.deflections_from_grid(grid=grid_22)
        deflections_0 = sersic.deflections_from_grid(
            grid=np.array([[1.000000001, 1.0]])
        )
        assert deflections_0 == pytest.approx(deflections_1, 1.0e-4)

        sersic = ag.SphericalSersic(centre=(0.0, 0.0))

        deflections_1 = sersic.deflections_from_grid(grid=grid_01)
        deflections_0 = sersic.deflections_from_grid(
            grid=np.array([[0.000000001, 0.0]])
        )
        assert deflections_0 == pytest.approx(deflections_1, 1.0e-4)

        sersic = ag.SphericalSersic(centre=(1.0, 1.0))

        deflections_1 = sersic.deflections_from_grid(grid=grid_22)
        deflections_0 = sersic.deflections_from_grid(
            grid=np.array([[1.000000001, 1.0]])
        )
        assert deflections_0 == pytest.approx(deflections_1, 1.0e-4)


class TestExponential:
    def test__transform_grid_wrapper_and_move_radial_minimum_wrappers(self):
        exponential = ag.EllipticalExponential(centre=(0.0, 0.0))

        convergence_1 = exponential.convergence_from_grid(grid=grid_01)
        convergence_0 = exponential.convergence_from_grid(
            grid=np.array([[0.000000001, 0.0]])
        )
        assert convergence_0 == pytest.approx(convergence_1, 1.0e-4)

        exponential = ag.EllipticalExponential(centre=(1.0, 1.0))

        convergence_1 = exponential.convergence_from_grid(grid=grid_22)
        convergence_0 = exponential.convergence_from_grid(
            grid=np.array([[1.000000001, 1.0]])
        )
        assert convergence_0 == pytest.approx(convergence_1, 1.0e-4)

        exponential = ag.SphericalExponential(centre=(0.0, 0.0))

        convergence_1 = exponential.convergence_from_grid(grid=grid_01)
        convergence_0 = exponential.convergence_from_grid(
            grid=np.array([[0.000000001, 0.0]])
        )
        assert convergence_0 == pytest.approx(convergence_1, 1.0e-4)

        exponential = ag.SphericalExponential(centre=(1.0, 1.0))

        convergence_1 = exponential.convergence_from_grid(grid=grid_22)
        convergence_0 = exponential.convergence_from_grid(
            grid=np.array([[1.000000001, 1.0]])
        )
        assert convergence_0 == pytest.approx(convergence_1, 1.0e-4)

        exponential = ag.EllipticalExponential(centre=(0.0, 0.0))

        deflections_1 = exponential.deflections_from_grid(grid=grid_01)
        deflections_0 = exponential.deflections_from_grid(
            grid=np.array([[0.000000001, 0.0]])
        )
        assert deflections_0 == pytest.approx(deflections_1, 1.0e-4)

        exponential = ag.EllipticalExponential(centre=(1.0, 1.0))

        deflections_1 = exponential.deflections_from_grid(grid=grid_22)
        deflections_0 = exponential.deflections_from_grid(
            grid=np.array([[1.000000001, 1.0]])
        )
        assert deflections_0 == pytest.approx(deflections_1, 1.0e-4)

        exponential = ag.SphericalExponential(centre=(0.0, 0.0))

        deflections_1 = exponential.deflections_from_grid(grid=grid_01)
        deflections_0 = exponential.deflections_from_grid(
            grid=np.array([[0.000000001, 0.0]])
        )
        assert deflections_0 == pytest.approx(deflections_1, 1.0e-4)

        exponential = ag.SphericalExponential(centre=(1.0, 1.0))

        deflections_1 = exponential.deflections_from_grid(grid=grid_22)
        deflections_0 = exponential.deflections_from_grid(
            grid=np.array([[1.000000001, 1.0]])
        )
        assert deflections_0 == pytest.approx(deflections_1, 1.0e-4)


class TestDevVaucouleurs:
    def test__transform_grid_wrapper_and_move_radial_minimum_wrappers(self):
        dev_vaucouleurs = ag.EllipticalDevVaucouleurs(centre=(0.0, 0.0))

        convergence_1 = dev_vaucouleurs.convergence_from_grid(grid=grid_01)
        convergence_0 = dev_vaucouleurs.convergence_from_grid(
            grid=np.array([[0.000000001, 0.0]])
        )
        assert convergence_0 == pytest.approx(convergence_1, 1.0e-4)

        dev_vaucouleurs = ag.EllipticalDevVaucouleurs(centre=(1.0, 1.0))

        convergence_1 = dev_vaucouleurs.convergence_from_grid(grid=grid_22)
        convergence_0 = dev_vaucouleurs.convergence_from_grid(
            grid=np.array([[1.000000001, 1.0]])
        )
        assert convergence_0 == pytest.approx(convergence_1, 1.0e-4)

        dev_vaucouleurs = ag.SphericalDevVaucouleurs(centre=(0.0, 0.0))

        convergence_1 = dev_vaucouleurs.convergence_from_grid(grid=grid_01)
        convergence_0 = dev_vaucouleurs.convergence_from_grid(
            grid=np.array([[0.000000001, 0.0]])
        )
        assert convergence_0 == pytest.approx(convergence_1, 1.0e-4)

        dev_vaucouleurs = ag.SphericalDevVaucouleurs(centre=(1.0, 1.0))

        convergence_1 = dev_vaucouleurs.convergence_from_grid(grid=grid_22)
        convergence_0 = dev_vaucouleurs.convergence_from_grid(
            grid=np.array([[1.000000001, 1.0]])
        )
        assert convergence_0 == pytest.approx(convergence_1, 1.0e-4)

        dev_vaucouleurs = ag.EllipticalDevVaucouleurs(centre=(0.0, 0.0))

        deflections_1 = dev_vaucouleurs.deflections_from_grid(grid=grid_01)
        deflections_0 = dev_vaucouleurs.deflections_from_grid(
            grid=np.array([[0.000000001, 0.0]])
        )
        assert deflections_0 == pytest.approx(deflections_1, 1.0e-4)

        dev_vaucouleurs = ag.EllipticalDevVaucouleurs(centre=(1.0, 1.0))

        deflections_1 = dev_vaucouleurs.deflections_from_grid(grid=grid_22)
        deflections_0 = dev_vaucouleurs.deflections_from_grid(
            grid=np.array([[1.000000001, 1.0]])
        )
        assert deflections_0 == pytest.approx(deflections_1, 1.0e-4)

        dev_vaucouleurs = ag.SphericalDevVaucouleurs(centre=(0.0, 0.0))

        deflections_1 = dev_vaucouleurs.deflections_from_grid(grid=grid_01)
        deflections_0 = dev_vaucouleurs.deflections_from_grid(
            grid=np.array([[0.000000001, 0.0]])
        )
        assert deflections_0 == pytest.approx(deflections_1, 1.0e-4)

        dev_vaucouleurs = ag.SphericalDevVaucouleurs(centre=(1.0, 1.0))

        deflections_1 = dev_vaucouleurs.deflections_from_grid(grid=grid_22)
        deflections_0 = dev_vaucouleurs.deflections_from_grid(
            grid=np.array([[1.000000001, 1.0]])
        )
        assert deflections_0 == pytest.approx(deflections_1, 1.0e-4)


class TestSersicMassRadialGradient:
    def test__transform_grid_wrapper_and_move_radial_minimum_wrappers(self):
        sersic = ag.EllipticalSersicRadialGradient(centre=(0.0, 0.0))

        convergence_1 = sersic.convergence_from_grid(grid=grid_01)
        convergence_0 = sersic.convergence_from_grid(
            grid=np.array([[0.000000001, 0.0]])
        )
        assert convergence_0 == pytest.approx(convergence_1, 1.0e-4)

        sersic = ag.EllipticalSersicRadialGradient(centre=(1.0, 1.0))

        convergence_1 = sersic.convergence_from_grid(grid=grid_22)
        convergence_0 = sersic.convergence_from_grid(
            grid=np.array([[1.000000001, 1.0]])
        )
        assert convergence_0 == pytest.approx(convergence_1, 1.0e-4)

        sersic = ag.SphericalSersicRadialGradient(centre=(0.0, 0.0))

        convergence_1 = sersic.convergence_from_grid(grid=grid_01)
        convergence_0 = sersic.convergence_from_grid(
            grid=np.array([[0.000000001, 0.0]])
        )
        assert convergence_0 == pytest.approx(convergence_1, 1.0e-4)

        sersic = ag.SphericalSersicRadialGradient(centre=(1.0, 1.0))

        convergence_1 = sersic.convergence_from_grid(grid=grid_22)
        convergence_0 = sersic.convergence_from_grid(
            grid=np.array([[1.000000001, 1.0]])
        )
        assert convergence_0 == pytest.approx(convergence_1, 1.0e-4)

        sersic = ag.EllipticalSersicRadialGradient(centre=(0.0, 0.0))

        deflections_1 = sersic.deflections_from_grid(grid=grid_01)
        deflections_0 = sersic.deflections_from_grid(
            grid=np.array([[0.000000001, 0.0]])
        )
        assert deflections_0 == pytest.approx(deflections_1, 1.0e-4)

        sersic = ag.EllipticalSersicRadialGradient(centre=(1.0, 1.0))

        deflections_1 = sersic.deflections_from_grid(grid=grid_22)
        deflections_0 = sersic.deflections_from_grid(
            grid=np.array([[1.000000001, 1.0]])
        )
        assert deflections_0 == pytest.approx(deflections_1, 1.0e-4)

        sersic = ag.SphericalSersicRadialGradient(centre=(0.0, 0.0))

        deflections_1 = sersic.deflections_from_grid(grid=grid_01)
        deflections_0 = sersic.deflections_from_grid(
            grid=np.array([[0.000000001, 0.0]])
        )
        assert deflections_0 == pytest.approx(deflections_1, 1.0e-4)

        sersic = ag.SphericalSersicRadialGradient(centre=(1.0, 1.0))

        deflections_1 = sersic.deflections_from_grid(grid=grid_22)
        deflections_0 = sersic.deflections_from_grid(
            grid=np.array([[1.000000001, 1.0]])
        )
        assert deflections_0 == pytest.approx(deflections_1, 1.0e-4)
        sersic = ag.SphericalSersicRadialGradient(
            centre=(-0.7, 0.5),
            intensity=5.0,
            effective_radius=0.2,
            sersic_index=2.0,
            mass_to_light_ratio=1.0,
            mass_to_light_gradient=1.5,
        )

        mask = np.array(
            [
                [True, True, True, True, True],
                [True, False, False, False, True],
                [True, False, True, False, True],
                [True, False, False, False, True],
                [True, True, True, True, True],
            ]
        )

        mask = aa.Mask.manual(mask, real_space_pixel_scales=1.0)

        grid = aa.MaskedGrid.from_mask(mask=mask)

        regular_with_interp = grid.new_grid_with_interpolator(
            pixel_scale_interpolation_grid=0.5
        )
        interp_deflections = sersic.deflections_from_grid(grid=regular_with_interp)

        interpolator = grids.Interpolator.from_mask_grid_and_pixel_scale_interpolation_grids(
            mask=mask, grid=grid, pixel_scale_interpolation_grid=0.5
        )

        interp_deflections_values = sersic.deflections_from_grid(
            grid=interpolator.interp_grid
        )

        interp_deflections_manual_y = interpolator.interpolated_values_from_values(
            values=interp_deflections_values[:, 0]
        )
        interp_deflections_manual_x = interpolator.interpolated_values_from_values(
            values=interp_deflections_values[:, 1]
        )

        assert (interp_deflections_manual_y == interp_deflections[:, 0]).all()
        assert (interp_deflections_manual_x == interp_deflections[:, 1]).all()


class TestMassSheet:
    def test__transform_grid_wrapper_and_move_radial_minimum_wrappers(self):
        mass_sheet = ag.mass_profiles.MassSheet(centre=(0.0, 0.0))

        deflections_1 = mass_sheet.deflections_from_grid(grid=grid_01)
        deflections_0 = mass_sheet.deflections_from_grid(
            grid=np.array([[0.000000001, 0.0]])
        )
        assert deflections_0 == pytest.approx(deflections_1, 1.0e-4)

        mass_sheet = ag.mass_profiles.MassSheet(centre=(1.0, 1.0))

        deflections_1 = mass_sheet.deflections_from_grid(grid=grid_22)
        deflections_0 = mass_sheet.deflections_from_grid(
            grid=np.array([[1.000000001, 1.0]])
        )
        assert deflections_0 == pytest.approx(deflections_1, 1.0e-4)


class TestExternalShear:
    def test__transform_grid_wrapper_and_move_radial_minimum_wrappers(self):
        shear = ag.mass_profiles.ExternalShear(magnitude=0.1, phi=45.0)

        deflections_1 = shear.deflections_from_grid(grid=np.array([[1e-8, 0.0]]))
        deflections_0 = shear.deflections_from_grid(grid=np.array([[1e-9, 0.0]]))
        assert deflections_0 == pytest.approx(deflections_1, 1.0e-4)
