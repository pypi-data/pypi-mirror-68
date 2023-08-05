import numpy as np
import pytest
from astropy import units as u
from numpy.testing import assert_allclose

from poliastro.bodies import Earth
from poliastro.twobody import Orbit
from poliastro.twobody.propagation import cowell
from poliastro.twobody.thrust import (
    change_a_inc,
    change_argp,
    change_ecc_quasioptimal,
    change_inc_ecc,
)


@pytest.mark.slow
@pytest.mark.parametrize(
    "inc_0",
    [
        np.radians(28.5),
        pytest.param(
            np.radians(90.0), marks=pytest.mark.skip(reason="too long for now")
        ),
    ],
)
def test_leo_geo_numerical(inc_0):
    f = 3.5e-7  # km / s2

    a_0 = 7000.0  # km
    a_f = 42166.0  # km
    inc_f = 0.0  # rad

    k = Earth.k.to(u.km ** 3 / u.s ** 2).value

    a_d, _, t_f = change_a_inc(k, a_0, a_f, inc_0, inc_f, f)

    # Retrieve r and v from initial orbit
    s0 = Orbit.circular(Earth, a_0 * u.km - Earth.R, inc_0 * u.rad)

    # Propagate orbit
    sf = s0.propagate(t_f * u.s, method=cowell, ad=a_d, rtol=1e-6)

    assert_allclose(sf.a.to(u.km).value, a_f, rtol=1e-3)
    assert_allclose(sf.ecc.value, 0.0, atol=1e-2)
    assert_allclose(sf.inc.to(u.rad).value, inc_f, atol=2e-3)


@pytest.mark.slow
@pytest.mark.parametrize(
    "ecc_0,ecc_f", [[0.0, 0.1245], [0.1245, 0.0]]  # Reverse-engineered from results
)
def test_sso_disposal_time_and_delta_v(ecc_0, ecc_f):
    a_0 = Earth.R.to(u.km).value + 900  # km
    f = 2.4e-7  # km / s2, assumed constant

    expected_t_f = 29.697  # days, reverse-engineered
    expected_delta_V = 0.6158  # km / s, lower than actual result
    s0 = Orbit.from_classical(
        Earth, a_0 * u.km, ecc_0 * u.one, 0 * u.deg, 0 * u.deg, 0 * u.deg, 0 * u.deg
    )
    _, delta_V, t_f = change_ecc_quasioptimal(s0, ecc_f, f)

    assert_allclose(delta_V, expected_delta_V, rtol=1e-4)
    assert_allclose(t_f / 86400, expected_t_f, rtol=1e-4)


@pytest.mark.slow
@pytest.mark.parametrize(
    "ecc_0,ecc_f", [[0.0, 0.1245], [0.1245, 0.0]]  # Reverse-engineered from results
)
def test_sso_disposal_numerical(ecc_0, ecc_f):
    a_0 = Earth.R.to(u.km).value + 900  # km
    f = 2.4e-7  # km / s2, assumed constant

    # Retrieve r and v from initial orbit
    s0 = Orbit.from_classical(
        Earth, a_0 * u.km, ecc_0 * u.one, 0 * u.deg, 0 * u.deg, 0 * u.deg, 0 * u.deg
    )
    a_d, _, t_f = change_ecc_quasioptimal(s0, ecc_f, f)

    # Propagate orbit
    sf = s0.propagate(t_f * u.s, method=cowell, ad=a_d, rtol=1e-8)

    assert_allclose(sf.ecc.value, ecc_f, rtol=1e-4, atol=1e-4)


@pytest.mark.slow
@pytest.mark.parametrize(
    "ecc_0,inc_f,expected_beta,expected_delta_V",
    [
        [0.1, 20.0, 83.043, 1.6789],
        [0.2, 20.0, 76.087, 1.6890],
        [0.4, 20.0, 61.522, 1.7592],
        [0.6, 16.0, 40.0, 1.7241],
        [0.8, 10.0, 16.304, 1.9799],
    ],
)
def test_geo_cases_beta_dnd_delta_v(ecc_0, inc_f, expected_beta, expected_delta_V):
    a = 42164  # km
    ecc_f = 0.0
    inc_0 = 0.0  # rad, baseline
    argp = 0.0  # rad, the method is efficient for 0 and 180
    f = 2.4e-7  # km / s2, unused

    inc_f = np.radians(inc_f)
    expected_beta = np.radians(expected_beta)

    s0 = Orbit.from_classical(
        Earth,
        a * u.km,
        ecc_0 * u.one,
        inc_0 * u.deg,
        0 * u.deg,
        argp * u.deg,
        0 * u.deg,
    )

    _, delta_V, beta, _ = change_inc_ecc(s0, ecc_f, inc_f, f)

    assert_allclose(delta_V, expected_delta_V, rtol=1e-2)
    assert_allclose(beta, expected_beta, rtol=1e-2)


@pytest.mark.slow
@pytest.mark.parametrize("ecc_0,ecc_f", [[0.4, 0.0], [0.0, 0.4]])
def test_geo_cases_numerical(ecc_0, ecc_f):
    a = 42164  # km
    inc_0 = 0.0  # rad, baseline
    inc_f = (20.0 * u.deg).to(u.rad).value  # rad
    argp = 0.0  # rad, the method is efficient for 0 and 180
    f = 2.4e-7  # km / s2

    # Retrieve r and v from initial orbit
    s0 = Orbit.from_classical(
        Earth,
        a * u.km,
        ecc_0 * u.one,
        inc_0 * u.deg,
        0 * u.deg,
        argp * u.deg,
        0 * u.deg,
    )
    a_d, _, _, t_f = change_inc_ecc(s0, ecc_f, inc_f, f)

    # Propagate orbit
    sf = s0.propagate(t_f * u.s, method=cowell, ad=a_d, rtol=1e-8)

    assert_allclose(sf.ecc.value, ecc_f, rtol=1e-2, atol=1e-2)
    assert_allclose(sf.inc.to(u.rad).value, inc_f, rtol=1e-1)


@pytest.mark.slow
def test_soyuz_standard_gto_delta_v():
    # Data from Soyuz Users Manual, issue 2 revision 0
    r_a = (Earth.R + 35950 * u.km).to(u.km).value
    r_p = (Earth.R + 250 * u.km).to(u.km).value

    a = (r_a + r_p) / 2  # km
    ecc = r_a / a - 1
    argp_0 = (178 * u.deg).to(u.rad).value  # rad
    argp_f = (178 * u.deg + 5 * u.deg).to(u.rad).value  # rad
    f = 2.4e-7  # km / s2

    k = Earth.k.to(u.km ** 3 / u.s ** 2).value

    _, delta_V, t_f = change_argp(k, a, ecc, argp_0, argp_f, f)

    expected_t_f = 12.0  # days, approximate
    expected_delta_V = 0.2489  # km / s

    assert_allclose(delta_V, expected_delta_V, rtol=1e-2)
    assert_allclose(t_f / 86400, expected_t_f, rtol=1e-2)


@pytest.mark.slow
def test_soyuz_standard_gto_numerical():
    # Data from Soyuz Users Manual, issue 2 revision 0
    r_a = (Earth.R + 35950 * u.km).to(u.km).value
    r_p = (Earth.R + 250 * u.km).to(u.km).value

    a = (r_a + r_p) / 2  # km
    ecc = r_a / a - 1
    argp_0 = (178 * u.deg).to(u.rad).value  # rad
    argp_f = (178 * u.deg + 5 * u.deg).to(u.rad).value  # rad
    f = 2.4e-7  # km / s2

    k = Earth.k.to(u.km ** 3 / u.s ** 2).value

    a_d, _, t_f = change_argp(k, a, ecc, argp_0, argp_f, f)

    # Retrieve r and v from initial orbit
    s0 = Orbit.from_classical(
        Earth,
        a * u.km,
        (r_a / a - 1) * u.one,
        6 * u.deg,
        188.5 * u.deg,
        178 * u.deg,
        0 * u.deg,
    )

    # Propagate orbit
    sf = s0.propagate(t_f * u.s, method=cowell, ad=a_d, rtol=1e-8)

    assert_allclose(sf.argp.to(u.rad).value, argp_f, rtol=1e-4)


@pytest.mark.slow
@pytest.mark.parametrize(
    "inc_0, expected_t_f, expected_delta_V, rtol",
    [
        [28.5, 191.26295, 5.78378, 1e-5],
        [90.0, 335.0, 10.13, 1e-3],
        [114.591, 351.0, 10.61, 1e-2],
    ],
)
def test_leo_geo_time_and_delta_v(inc_0, expected_t_f, expected_delta_V, rtol):
    f = 3.5e-7  # km / s2

    a_0 = 7000.0  # km
    a_f = 42166.0  # km
    inc_f = 0.0  # rad
    k = Earth.k.to(u.km ** 3 / u.s ** 2).value
    inc_0 = np.radians(inc_0)  # rad

    _, delta_V, t_f = change_a_inc(k, a_0, a_f, inc_0, inc_f, f)

    assert_allclose(delta_V, expected_delta_V, rtol=rtol)
    assert_allclose((t_f * u.s).to(u.day).value, expected_t_f, rtol=rtol)
