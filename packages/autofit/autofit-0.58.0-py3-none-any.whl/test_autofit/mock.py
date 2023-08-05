import inspect
import math
import typing

import autofit as af
# noinspection PyAbstractClass
import autofit.mapper.prior_model.attribute_pair
from autofit import Paths
from autofit.tools.phase import Dataset


class MockNonLinearOptimizer(object):
    def __init__(
            self,
            phase_name,
            phase_tag=None,
            phase_folders=tuple(),
            most_probable=None,
            model_mapper=None,
            max_log_likelihood=None,
            model_upper_params=None,
            model_lower_params=None,
    ):
        super(MockNonLinearOptimizer, self).__init__(
            model_mapper or af.ModelMapper(),
            Paths(
                phase_name=phase_name, phase_tag=phase_tag, phase_folders=phase_folders
            ),
        )

        self.most_probable = most_probable
        self.max_log_likelihood = max_log_likelihood
        self.model_upper_params = model_upper_params
        self.model_lower_params = model_lower_params

    def _simple_fit(self, model, fitness_function):
        raise NotImplementedError()

    def _fit(self, model, analysis):
        raise NotImplementedError()

    @property
    def most_probable_vector(self):
        """
        Read the most probable or most likely model values from the 'obj_summary.txt'
        file which nlo from a multinest lens.

        This file stores the parameters of the most probable model in the first half
        of entries and the most likely model in the second half of entries. The
        offset parameter is used to start at the desiredaf.

        """
        return self.most_probable

    @property
    def max_log_likelihood_vector(self):
        """
        Read the most probable or most likely model values from the 'obj_summary.txt'
        file which nlo from a \ multinest lens.

        This file stores the parameters of the most probable model in the first half
        of entries and the most likely model in the second half of entries. The
        offset parameter is used to start at the desiredaf.
        """
        return self.max_log_likelihood

    def vector_at_upper_sigma(self, sigma):
        return self.model_upper_params

    def vector_at_lower_sigma(self, sigma):
        return self.model_lower_params


class MockClassNLOx2:
    def __init__(self, one=1, two=2):
        self.one = one
        self.two = two


class MockClassNLOx4:
    def __init__(self, one=1, two=2, three=3, four=4):
        self.one = one
        self.two = two
        self.three = three
        self.four = four


class MockClassNLOx5:
    def __init__(self, one=1, two=2, three=3, four=4, five=5):
        self.one = one
        self.two = two
        self.three = three
        self.four = four
        self.five = five


class MockClassNLOx6:
    def __init__(self, one=(1, 2), two=(3, 4), three=3, four=4):
        self.one = one
        self.two = two
        self.three = three
        self.four = four


class MockAnalysis:
    def __init__(self):
        self.kwargs = None
        self.instance = None
        self.visualize_instance = None

    def fit(self, instance):
        self.instance = instance
        return 1.0

    # noinspection PyUnusedLocal
    def visualize(self, instance, *args, **kwargs):
        self.visualize_instance = instance


class Circle:
    def __init__(self, radius):
        self.radius = radius

    def with_circumference(self, circumference):
        self.circumference = circumference

    @property
    def circumference(self):
        return self.radius * 2 * math.pi

    @circumference.setter
    def circumference(self, circumference):
        self.radius = circumference / (2 * math.pi)


class SimpleClass:
    def __init__(self, one, two: float):
        self.one = one
        self.two = two


class ComplexClass:
    def __init__(self, simple: SimpleClass):
        self.simple = simple


class ListClass:
    def __init__(self, ls: list):
        self.ls = ls


class Distance(af.DimensionType):
    pass


class DistanceClass:
    @af.map_types
    def __init__(self, first: Distance, second: Distance):
        self.first = first
        self.second = second


class PositionClass:
    @af.map_types
    def __init__(self, position: typing.Tuple[Distance, Distance]):
        self.position = position


class DeferredClass:
    def __init__(self, one, two):
        self.one = one
        self.two = two


class Galaxy:
    def __init__(
            self,
            light_profiles: list = None,
            mass_profiles: list = None,
            redshift=None,
            **kwargs
    ):
        self.redshift = redshift
        self.light_profiles = light_profiles
        self.mass_profiles = mass_profiles
        self.kwargs = kwargs


class RelativeWidth:
    def __init__(self, one, two, three):
        self.one = one
        self.two = two
        self.three = three


class Redshift:
    def __init__(self, redshift):
        self.redshift = redshift


# noinspection PyAbstractClass
class GalaxyModel(af.AbstractPriorModel):
    def instance_for_arguments(self, arguments):
        try:
            return Galaxy(redshift=self.redshift.instance_for_arguments(arguments))
        except AttributeError:
            return Galaxy()

    def __init__(self, model_redshift=False, **kwargs):
        super().__init__()
        self.redshift = af.PriorModel(Redshift) if model_redshift else None
        print(self.redshift)
        self.__dict__.update(
            {
                key: af.PriorModel(value) if inspect.isclass(value) else value
                for key, value in kwargs.items()
            }
        )

    @property
    def instance_tuples(self):
        return []

    @property
    @autofit.mapper.prior_model.attribute_pair.cast_collection(
        autofit.mapper.prior_model.attribute_pair.PriorNameValue
    )
    def unique_prior_tuples(self):
        return (
            [item for item in self.__dict__.items() if isinstance(item[1], af.Prior)]
            + [("redshift", self.redshift.redshift)]
            if self.redshift is not None
            else []
        )

    @property
    @autofit.mapper.prior_model.attribute_pair.cast_collection(af.PriorModelNameValue)
    def flat_prior_model_tuples(self):
        return [
            item
            for item in self.__dict__.items()
            if isinstance(item[1], af.AbstractPriorModel)
        ]


class GeometryProfile:
    def __init__(self, centre=(0.0, 0.0)):
        """Abstract GeometryProfile, describing an object with y, x cartesian
        coordinates """
        self.centre = centre

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class SphericalProfile(GeometryProfile):
    def __init__(self, centre=(0.0, 0.0)):
        """ Generic circular profiles class to contain functions shared by light and
        mass profiles.

        Parameters
        ----------
        centre: (float, float)
            The (y,x) coordinates of the origin of the profile.
        """
        super(SphericalProfile, self).__init__(centre)


class EllipticalProfile(SphericalProfile):
    def __init__(self, centre=(0.0, 0.0), axis_ratio=1.0, phi=0.0):
        """ Generic elliptical profiles class to contain functions shared by light
        and mass profiles.

        Parameters
        ----------
        centre: (float, float)
            The (y,x) coordinates of the origin of the profiles
        axis_ratio : float
            Ratio of profiles ellipse's minor and major axes (b/a)
        phi : float
            Rotational angle of profiles ellipse counter-clockwise from positive x-axis
        """
        super(EllipticalProfile, self).__init__(centre)
        self.axis_ratio = axis_ratio
        self.phi = phi


class EllipticalLP(EllipticalProfile):
    """Generic class for an elliptical light profiles"""

    def __init__(self, centre=(0.0, 0.0), axis_ratio=1.0, phi=0.0):
        """  Abstract class for an elliptical light-profile.

        Parameters
        ----------
        centre: (float, float)
            The (y,x) coordinates of the origin of the profiles
        axis_ratio : float
            Ratio of light profiles ellipse's minor and major axes (b/a)
        phi : float
            Rotational angle of profiles ellipse counter-clockwise from positive x-axis
        """
        super(EllipticalLP, self).__init__(centre, axis_ratio, phi)


class AbstractEllipticalSersic(EllipticalProfile):
    def __init__(
            self,
            centre=(0.0, 0.0),
            axis_ratio=1.0,
            phi=0.0,
            intensity=0.1,
            effective_radius=0.6,
            sersic_index=4.0,
    ):
        """ Abstract base class for an elliptical Sersic profile, used for computing
        its effective radius and Sersic instance.

        Parameters
        ----------
        centre: (float, float)
            The (y,x) coordinates of the origin of the profiles
        axis_ratio : float
            Ratio of light profiles ellipse's minor and major axes (b/a)
        phi : float
            Rotational angle of profiles ellipse counter-clockwise from positive x-axis
        intensity : float
            Overall intensity normalisation in the light profiles (electrons per second)
        effective_radius : float
            The circular radius containing half the light of this model_mapper
        sersic_index : Int
            The Sersic index, which controls the light profile concentration
        """
        super(AbstractEllipticalSersic, self).__init__(centre, axis_ratio, phi)
        self.intensity = intensity
        self.effective_radius = effective_radius
        self.sersic_index = sersic_index


class MassProfile:
    def surface_density_func(self, eta):
        raise NotImplementedError("surface_density_at_radius should be overridden")

    def surface_density_from_grid(self, grid):
        pass

    def potential_from_grid(self, grid):
        pass

    def deflections_from_grid(self, grid):
        raise NotImplementedError("deflections_from_grid should be overridden")


# noinspection PyAbstractClass
class EllipticalMassProfile(EllipticalProfile, MassProfile):
    def __init__(self, centre=(0.0, 0.0), axis_ratio=1.0, phi=0.0):
        """
        Abstract class for elliptical mass profiles.

        Parameters
        ----------
        centre: (float, float)
            The origin of the profile
        axis_ratio : float
            Ellipse's minor-to-major axis ratio (b/a)
        phi : float
            Rotation angle of profile's ellipse counter-clockwise from positive x-axis
        """
        super(EllipticalMassProfile, self).__init__(centre, axis_ratio, phi)
        self.axis_ratio = axis_ratio
        self.phi = phi


# noinspection PyAbstractClass
class EllipticalCoredPowerLaw(EllipticalMassProfile, MassProfile):
    def __init__(
            self,
            centre=(0.0, 0.0),
            axis_ratio=1.0,
            phi=0.0,
            einstein_radius=1.0,
            slope=2.0,
            core_radius=0.01,
    ):
        """
        Represents a cored elliptical power-law density distribution

        Parameters
        ----------
        centre: (float, float)
            The image_grid of the origin of the profiles
        axis_ratio : float
            Elliptical mass profile's minor-to-major axis ratio (b/a)
        phi : float
            Rotation angle of mass profile's ellipse counter-clockwise from positive
            x-axis
        einstein_radius : float
            Einstein radius of power-law mass profiles
        slope : float
            power-law density slope of mass profiles
        core_radius : float
            The radius of the inner core
        """
        super(EllipticalCoredPowerLaw, self).__init__(centre, axis_ratio, phi)
        self.einstein_radius = einstein_radius
        self.slope = slope
        self.core_radius = core_radius


# noinspection PyAbstractClass
class EllipticalCoredIsothermal(EllipticalCoredPowerLaw):
    def __init__(
            self,
            centre=(0.0, 0.0),
            axis_ratio=1.0,
            phi=0.0,
            einstein_radius=1.0,
            core_radius=0.05,
    ):
        """
        Represents a cored elliptical isothermal density distribution, which is
        equivalent to the elliptical power-law
        density distribution for the value slope=2.0

        Parameters
        ----------
        centre: (float, float)
            The image_grid of the origin of the profiles
        axis_ratio : float
            Elliptical mass profile's minor-to-major axis ratio (b/a)
        phi : float
            Rotation angle of mass profile's ellipse counter-clockwise from positive
            x-axis
        einstein_radius : float
            Einstein radius of power-law mass profiles
        core_radius : float
            The radius of the inner core
        """

        super(EllipticalCoredIsothermal, self).__init__(
            centre, axis_ratio, phi, einstein_radius, 2.0, core_radius
        )


class EllipticalSersic(AbstractEllipticalSersic, EllipticalLP):
    def __init__(
            self,
            centre=(0.0, 0.0),
            axis_ratio=1.0,
            phi=0.0,
            intensity=0.1,
            effective_radius=0.6,
            sersic_index=4.0,
    ):
        """ The elliptical Sersic profile, used for fitting a model_galaxy's light.

        Parameters
        ----------
        centre: (float, float)
            The (y,x) origin of the light profile.
        axis_ratio : float
            Ratio of light profiles ellipse's minor and major axes (b/a).
        phi : float
            Rotation angle of light profile counter-clockwise from positive x-axis.
        intensity : float
            Overall intensity normalisation of the light profiles (electrons per
            second).
        effective_radius : float
            The circular radius containing half the light of this profile.
        sersic_index : Int
            Controls the concentration of the of the light profile.
        """
        super(EllipticalSersic, self).__init__(
            centre, axis_ratio, phi, intensity, effective_radius, sersic_index
        )


class EllipticalCoreSersic(EllipticalSersic):
    def __init__(
            self,
            centre=(0.0, 0.0),
            axis_ratio=1.0,
            phi=0.0,
            intensity=0.1,
            effective_radius=0.6,
            sersic_index=4.0,
            radius_break=0.01,
            intensity_break=0.05,
            gamma=0.25,
            alpha=3.0,
    ):
        """ The elliptical cored-Sersic profile, used for fitting a model_galaxy's
        light.

        Parameters
        ----------
        centre: (float, float)
            The (y,x) origin of the light profile.
        axis_ratio : float
            Ratio of light profiles ellipse's minor and major axes (b/a).
        phi : float
            Rotation angle of light profile counter-clockwise from positive x-axis.
        intensity : float
            Overall intensity normalisation of the light profiles (electrons per
            second).
        effective_radius : float
            The circular radius containing half the light of this profile.
        sersic_index : Int
            Controls the concetration of the of the light profile.
        radius_break : Float
            The break radius separating the inner power-law (with logarithmic slope
            gamma) and outer Sersic function.
        intensity_break : Float
            The intensity at the break radius.
        gamma : Float
            The logarithmic power-law slope of the inner core profiles
        alpha :
            Controls the sharpness of the transition between the inner core / outer
            Sersic profiles.
        """
        super(EllipticalCoreSersic, self).__init__(
            centre, axis_ratio, phi, intensity, effective_radius, sersic_index
        )
        self.radius_break = radius_break
        self.intensity_break = intensity_break
        self.alpha = alpha
        self.gamma = gamma


class EllipticalExponential(EllipticalSersic):
    def __init__(
            self,
            centre=(0.0, 0.0),
            axis_ratio=1.0,
            phi=0.0,
            intensity=0.1,
            effective_radius=0.6,
    ):
        """ The elliptical exponential profile, used for fitting a model_galaxy's light.

        This is a subset of the elliptical Sersic profile, specific to the case that
        sersic_index = 1.0.

        Parameters
        ----------
        centre: (float, float)
            The (y,x) origin of the light profile.
        axis_ratio : float
            Ratio of light profiles ellipse's minor and major axes (b/a).
        phi : float
            Rotation angle of light profile counter-clockwise from positive x-axis.
        intensity : float
            Overall intensity normalisation of the light profiles (electrons per
            second).
        effective_radius : float
            The circular radius containing half the light of this profile.
        """
        super(EllipticalExponential, self).__init__(
            centre, axis_ratio, phi, intensity, effective_radius, 1.0
        )


class EllipticalGaussian(EllipticalLP):
    def __init__(
            self, centre=(0.0, 0.0), axis_ratio=1.0, phi=0.0, intensity=0.1, sigma=0.01
    ):
        """ The elliptical Gaussian profile.

        Parameters
        ----------
        centre: (float, float)
            The (y,x) origin of the light profile.
        axis_ratio : float
            Ratio of light profiles ellipse's minor and major axes (b/a).
        phi : float
            Rotation angle of light profile counter-clockwise from positive x-axis.
        intensity : float
            Overall intensity normalisation of the light profiles (electrons per
            second).
        sigma : float
            The full-width half-maximum of the Gaussian.
        """
        super(EllipticalGaussian, self).__init__(centre, axis_ratio, phi)

        self.intensity = intensity
        self.sigma = sigma


class Tracer:
    def __init__(self, lens_galaxy: Galaxy, source_galaxy: Galaxy, grid):
        self.lens_galaxy = lens_galaxy
        self.source_galaxy = source_galaxy
        self.grid = grid


class Result:
    def __init__(self, instance=None, model=None):
        self.instance = instance
        self.model = model

    def model_absolute(self, absolute):
        return self.model

    def model_relative(self, relative):
        return self.model


class HyperGalaxy:
    pass


class MockDataset(Dataset):
    @property
    def metadata(self) -> dict:
        return dict()

    @property
    def name(self) -> str:
        return "name"


class MockClassGaussian:
    def __init__(self, one, two):
        self.one = one
        self.two = two


class MockClassInf:
    def __init__(self, one, two):
        self.one = one
        self.two = two
