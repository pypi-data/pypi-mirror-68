import pytest
from astropy import constants as c, units as u
from astropy.tests.helper import assert_quantity_allclose

from poliastro.bodies import Earth
from poliastro.core import iod
from poliastro.iod import izzo, vallado


@pytest.mark.parametrize("lambert", [vallado.lambert, izzo.lambert])
def test_vallado75(lambert):
    k = Earth.k
    r0 = [15945.34, 0.0, 0.0] * u.km
    r = [12214.83399, 10249.46731, 0.0] * u.km
    tof = 76.0 * u.min

    expected_va = [2.058925, 2.915956, 0.0] * u.km / u.s
    expected_vb = [-3.451569, 0.910301, 0.0] * u.km / u.s

    va, vb = next(lambert(k, r0, r, tof))
    assert_quantity_allclose(va, expected_va, rtol=1e-5)
    assert_quantity_allclose(vb, expected_vb, rtol=1e-4)


@pytest.mark.parametrize("lambert", [vallado.lambert, izzo.lambert])
def test_curtis52(lambert):
    k = Earth.k
    r0 = [5000.0, 10000.0, 2100.0] * u.km
    r = [-14600.0, 2500.0, 7000.0] * u.km
    tof = 1.0 * u.h

    expected_va = [-5.9925, 1.9254, 3.2456] * u.km / u.s
    expected_vb = [-3.3125, -4.1966, -0.38529] * u.km / u.s

    va, vb = next(lambert(k, r0, r, tof))
    assert_quantity_allclose(va, expected_va, rtol=1e-4)
    assert_quantity_allclose(vb, expected_vb, rtol=1e-4)


@pytest.mark.parametrize("lambert", [vallado.lambert, izzo.lambert])
def test_curtis53(lambert):
    k = Earth.k
    r0 = [273378.0, 0.0, 0.0] * u.km
    r = [145820.0, 12758.0, 0.0] * u.km
    tof = 13.5 * u.h
    numiter = 100

    # ERRATA: j component is positive
    expected_va = [-2.4356, 0.26741, 0.0] * u.km / u.s

    va, vb = next(lambert(k, r0, r, tof, numiter=numiter))
    assert_quantity_allclose(va, expected_va, rtol=1e-4)


@pytest.mark.parametrize("lambert", [izzo.lambert])
def test_molniya_der_zero_full_revolution(lambert):
    k = Earth.k
    r0 = [22592.145603, -1599.915239, -19783.950506] * u.km
    r = [1922.067697, 4054.157051, -8925.727465] * u.km
    tof = 10 * u.h

    expected_va = [2.000652697, 0.387688615, -2.666947760] * u.km / u.s
    expected_vb = [-3.79246619, -1.77707641, 6.856814395] * u.km / u.s

    va, vb = next(lambert(k, r0, r, tof, M=0))
    assert_quantity_allclose(va, expected_va, rtol=1e-6)
    assert_quantity_allclose(vb, expected_vb, rtol=1e-6)


@pytest.mark.parametrize("lambert", [izzo.lambert])
def test_molniya_der_one_full_revolution(lambert):
    k = Earth.k
    r0 = [22592.145603, -1599.915239, -19783.950506] * u.km
    r = [1922.067697, 4054.157051, -8925.727465] * u.km
    tof = 10 * u.h

    expected_va_l = [0.50335770, 0.61869408, -1.57176904] * u.km / u.s
    expected_vb_l = [-4.18334626, -1.13262727, 6.13307091] * u.km / u.s

    expected_va_r = [-2.45759553, 1.16945801, 0.43161258] * u.km / u.s
    expected_vb_r = [-5.53841370, 0.01822220, 5.49641054] * u.km / u.s

    (va_l, vb_l), (va_r, vb_r) = lambert(k, r0, r, tof, M=1)

    assert_quantity_allclose(va_l, expected_va_l, rtol=1e-5)
    assert_quantity_allclose(vb_l, expected_vb_l, rtol=1e-5)
    assert_quantity_allclose(va_r, expected_va_r, rtol=1e-5)
    assert_quantity_allclose(vb_r, expected_vb_r, rtol=1e-4)


@pytest.mark.parametrize("lambert", [izzo.lambert])
def test_raises_exception_for_non_feasible_solution(lambert):
    k = Earth.k
    r0 = [22592.145603, -1599.915239, -19783.950506] * u.km
    r = [1922.067697, 4054.157051, -8925.727465] * u.km
    tof = 5 * u.h

    with pytest.raises(ValueError) as excinfo:
        next(lambert(k, r0, r, tof, M=1))
    assert "ValueError: No feasible solution, try lower M" in excinfo.exconly()


@pytest.mark.parametrize("lambert", [izzo.lambert])
def test_collinear_vectors_input(lambert):
    k = Earth.k
    r0 = [22592.145603, -1599.915239, -19783.950506] * u.km
    r = [22592.145603, -1599.915239, -19783.950506] * u.km
    tof = 5 * u.h

    with pytest.raises(ValueError) as excinfo:
        next(lambert(k, r0, r, tof, M=0))
    assert (
        "ValueError: Lambert solution cannot be computed for collinear vectors"
        in excinfo.exconly()
    )


@pytest.mark.parametrize("M", [1, 2, 3])
def test_minimum_time_of_flight_convergence(M):
    ll = -1
    x_T_min_expected, T_min_expected = iod._compute_T_min(ll, M, numiter=10, rtol=1e-8)
    y = iod._compute_y(x_T_min_expected, ll)
    T_min = iod._tof_equation_y(x_T_min_expected, y, 0.0, ll, M)
    assert T_min_expected == T_min


@pytest.mark.parametrize(
    "lambert_vallado,lambert_izzo", [(vallado.lambert, izzo.lambert)]
)
def test_issue840(lambert_vallado, lambert_izzo):
    k = c.GM_earth.to(u.km ** 3 / u.s ** 2)
    r0 = [10000.0, 0, 0] * u.km
    rf = [8000.0, -5000, 0] * u.km
    tof = 2 * u.hour

    expected_va = [0.36591277, 5.8228806, 0.0] * u.km / u.s
    expected_vb = [3.99397599, 4.78236576, 0.0] * u.km / u.s

    va_v, vb_v = next(lambert_vallado(k, r0, rf, tof, short=False))
    va_i, vb_i = next(lambert_izzo(k, r0, rf, tof))

    assert_quantity_allclose(va_v, expected_va, rtol=1e-6)
    assert_quantity_allclose(vb_v, expected_vb, rtol=1e-6)
    assert_quantity_allclose(va_i, expected_va, rtol=1e-6)
    assert_quantity_allclose(vb_i, expected_vb, rtol=1e-6)
