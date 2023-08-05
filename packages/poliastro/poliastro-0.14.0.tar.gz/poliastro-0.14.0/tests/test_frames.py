import numpy as np
import pytest
from astropy import units as u
from astropy.coordinates import (
    CartesianRepresentation,
    get_body_barycentric,
    solar_system_ephemeris,
)
from astropy.tests.helper import assert_quantity_allclose
from astropy.time import Time

from poliastro.bodies import (
    Earth,
    Jupiter,
    Mars,
    Mercury,
    Neptune,
    Saturn,
    Sun,
    Uranus,
    Venus,
)
from poliastro.constants import J2000
from poliastro.frames.ecliptic import GeocentricSolarEcliptic
from poliastro.frames.equatorial import (
    GCRS,
    HCRS,
    ICRS,
    JupiterICRS,
    MarsICRS,
    MercuryICRS,
    NeptuneICRS,
    SaturnICRS,
    UranusICRS,
    VenusICRS,
)
from poliastro.frames.fixed import (
    ITRS,
    JupiterFixed,
    MarsFixed,
    MercuryFixed,
    NeptuneFixed,
    SaturnFixed,
    SunFixed,
    UranusFixed,
    VenusFixed,
)


@pytest.mark.parametrize(
    "body, frame",
    [
        (Mercury, MercuryICRS),
        (Venus, VenusICRS),
        (Mars, MarsICRS),
        (Jupiter, JupiterICRS),
        (Saturn, SaturnICRS),
        (Uranus, UranusICRS),
        (Neptune, NeptuneICRS),
    ],
)
def test_planetary_frames_have_proper_string_representations(body, frame):
    coords = frame()

    assert body.name in repr(coords)


@pytest.mark.parametrize(
    "body, frame",
    [
        (Sun, HCRS),
        (Mercury, MercuryICRS),
        (Venus, VenusICRS),
        (Earth, GCRS),
        (Mars, MarsICRS),
        (Jupiter, JupiterICRS),
        (Saturn, SaturnICRS),
        (Uranus, UranusICRS),
        (Neptune, NeptuneICRS),
    ],
)
def test_planetary_icrs_frame_is_just_translation(body, frame):
    with solar_system_ephemeris.set("builtin"):
        epoch = J2000
        vector = CartesianRepresentation(x=100 * u.km, y=100 * u.km, z=100 * u.km)
        vector_result = (
            frame(vector, obstime=epoch)
            .transform_to(ICRS)
            .represent_as(CartesianRepresentation)
        )

        expected_result = get_body_barycentric(body.name, epoch) + vector

    assert_quantity_allclose(vector_result.xyz, expected_result.xyz)


@pytest.mark.parametrize(
    "body, frame",
    [
        (Sun, HCRS),
        (Mercury, MercuryICRS),
        (Venus, VenusICRS),
        (Earth, GCRS),
        (Mars, MarsICRS),
        (Jupiter, JupiterICRS),
        (Saturn, SaturnICRS),
        (Uranus, UranusICRS),
        (Neptune, NeptuneICRS),
    ],
)
def test_icrs_body_position_to_planetary_frame_yields_zeros(body, frame):
    with solar_system_ephemeris.set("builtin"):
        epoch = J2000
        vector = get_body_barycentric(body.name, epoch)

        vector_result = (
            ICRS(vector)
            .transform_to(frame(obstime=epoch))
            .represent_as(CartesianRepresentation)
        )

    assert_quantity_allclose(vector_result.xyz, [0, 0, 0] * u.km, atol=1e-7 * u.km)


@pytest.mark.parametrize(
    "body, fixed_frame, inertial_frame",
    [
        (Sun, SunFixed, HCRS),
        (Mercury, MercuryFixed, MercuryICRS),
        (Venus, VenusFixed, VenusICRS),
        (Earth, ITRS, GCRS),
        (Mars, MarsFixed, MarsICRS),
        (Jupiter, JupiterFixed, JupiterICRS),
        (Saturn, SaturnFixed, SaturnICRS),
        (Uranus, UranusFixed, UranusICRS),
        (Neptune, NeptuneFixed, NeptuneICRS),
    ],
)
def test_planetary_fixed_inertial_conversion(body, fixed_frame, inertial_frame):
    with solar_system_ephemeris.set("builtin"):
        epoch = J2000
        fixed_position = fixed_frame(
            0 * u.deg, 0 * u.deg, body.R, obstime=epoch, representation_type="spherical"
        )
        inertial_position = fixed_position.transform_to(inertial_frame(obstime=epoch))
        assert_quantity_allclose(
            fixed_position.spherical.distance, body.R, atol=1e-7 * u.km
        )
        assert_quantity_allclose(
            inertial_position.spherical.distance, body.R, atol=1e-7 * u.km
        )


@pytest.mark.parametrize(
    "body, fixed_frame, inertial_frame",
    [
        (Sun, SunFixed, HCRS),
        (Mercury, MercuryFixed, MercuryICRS),
        (Venus, VenusFixed, VenusICRS),
        (Earth, ITRS, GCRS),
        (Mars, MarsFixed, MarsICRS),
        (Jupiter, JupiterFixed, JupiterICRS),
        (Saturn, SaturnFixed, SaturnICRS),
        (Uranus, UranusFixed, UranusICRS),
        (Neptune, NeptuneFixed, NeptuneICRS),
    ],
)
def test_planetary_inertial_fixed_conversion(body, fixed_frame, inertial_frame):
    with solar_system_ephemeris.set("builtin"):
        epoch = J2000
        inertial_position = inertial_frame(
            0 * u.deg, 0 * u.deg, body.R, obstime=epoch, representation_type="spherical"
        )
        fixed_position = inertial_position.transform_to(fixed_frame(obstime=epoch))
        assert_quantity_allclose(
            fixed_position.spherical.distance, body.R, atol=1e-7 * u.km
        )
        assert_quantity_allclose(
            inertial_position.spherical.distance, body.R, atol=1e-7 * u.km
        )


@pytest.mark.parametrize(
    "body, fixed_frame, inertial_frame",
    [
        (Sun, SunFixed, HCRS),
        (Mercury, MercuryFixed, MercuryICRS),
        (Venus, VenusFixed, VenusICRS),
        (Earth, ITRS, GCRS),
        (Mars, MarsFixed, MarsICRS),
        (Jupiter, JupiterFixed, JupiterICRS),
        (Saturn, SaturnFixed, SaturnICRS),
        (Uranus, UranusFixed, UranusICRS),
        (Neptune, NeptuneFixed, NeptuneICRS),
    ],
)
def test_planetary_inertial_roundtrip_vector(body, fixed_frame, inertial_frame):
    with solar_system_ephemeris.set("builtin"):
        epoch = J2000
        sampling_time = 10 * u.s
        fixed_position = fixed_frame(
            np.broadcast_to(0 * u.deg, (1000,), subok=True),
            np.broadcast_to(0 * u.deg, (1000,), subok=True),
            np.broadcast_to(body.R, (1000,), subok=True),
            representation_type="spherical",
            obstime=epoch + np.arange(1000) * sampling_time,
        )
        inertial_position = fixed_position.transform_to(
            inertial_frame(obstime=epoch + np.arange(1000) * sampling_time)
        )
        fixed_position_roundtrip = inertial_position.transform_to(
            fixed_frame(obstime=epoch + np.arange(1000) * sampling_time)
        )
        assert_quantity_allclose(
            fixed_position.cartesian.xyz,
            fixed_position_roundtrip.cartesian.xyz,
            atol=1e-7 * u.km,
        )


def test_round_trip_from_GeocentricSolarEcliptic_gives_same_results():
    gcrs = GCRS(ra="02h31m49.09s", dec="+89d15m50.8s", distance=200 * u.km)
    gse = gcrs.transform_to(GeocentricSolarEcliptic(obstime=Time("J2000")))
    gcrs_back = gse.transform_to(GCRS(obstime=Time("J2000")))
    assert_quantity_allclose(gcrs_back.dec.value, gcrs.dec.value, atol=1e-7)
    assert_quantity_allclose(gcrs_back.ra.value, gcrs.ra.value, atol=1e-7)


def test_GeocentricSolarEcliptic_against_data():
    gcrs = GCRS(ra="02h31m49.09s", dec="+89d15m50.8s", distance=200 * u.km)
    gse = gcrs.transform_to(GeocentricSolarEcliptic(obstime=J2000))
    lon = 233.11691362602866
    lat = 48.64606410986667
    assert_quantity_allclose(gse.lat.value, lat, atol=1e-7)
    assert_quantity_allclose(gse.lon.value, lon, atol=1e-7)


def test_GeocentricSolarEcliptic_raises_error_nonscalar_obstime():
    with pytest.raises(ValueError) as excinfo:
        gcrs = GCRS(ra="02h31m49.09s", dec="+89d15m50.8s", distance=200 * u.km)
        gcrs.transform_to(GeocentricSolarEcliptic(obstime=Time(["J3200", "J2000"])))
    assert (
        "To perform this transformation the "
        "obstime Attribute must be a scalar." in str(excinfo.value)
    )
