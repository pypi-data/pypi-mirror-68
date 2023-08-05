What's new
==========

poliastro 0.14.0 - 2020-05-08
-----------------------------

This major release contains crucial new features and bug fixes that have
been years in the making, and is by far the most exciting release
in the history of the project.

Highlights
..........

* **New API to retrieve ephemerides**: After a lot of iteration we introduced
  a new object, :py:class:`poliastro.ephem.Ephem`, to retrieve and represent
  **ephemerides**, as opposed to osculating orbits. Besides, we added convenience
  methods to plot them so they can be combined with
  :py:class:`~poliastro.twobody.orbit.Orbit` objects.
* **Simple API to retrieve mean elements of Solar System planets**: There are
  many use cases for approximate, mean Keplerian elements for planet orbits:
  computing Spheres of Influence, designing specialized orbits... We introduced
  a new function :py:meth:`poliastro.twobody.mean_elements.get_mean_elements`
  that makes it way easier.
* **Avoid mixing ephemerides and osculating orbits**: The ``Orbit.from_body_ephem``
  method was very convenient and it was used everywhere
  in poliastro examples because it was the simplest way to plot and analyze
  the orbits of the planets. However, it introduced a lot of confusion about the
  nature of osculating orbits and planetary ephemerides. With the introduction of
  :py:class:`~poliastro.ephem.Ephem` objects and
  :py:meth:`~poliastro.twobody.mean_elements.get_mean_elements`, this convenience
  method is no longer necessary, we removed almost all references to it
  (both in source code and examples) and we will remove it in the next release.
* **Robust propagation in all eccentricity regimes**: Two years ago we started
  working on improving our propagators for near parabolic orbits, which occur
  naturally when studying comets and reentry trajectories. Unfortunately, there were
  still problems we could not identify and we tried to compensate by adding
  other propagation algorithms, but none of them worked correctly in all
  eccentricity regimes. With a big effort and a few sleepless nights
  we finally fixed the implementation of our default propagator
  :py:meth:`poliastro.twobody.propagation.farnocchia`, and is now working
  correctly for very extreme cases and long term propagations. Give it a try!
* **New color palette**: We introduced a new color palette to improve the
  appearance of plots that include the orbits of the planets of the Solar System.
  We hope you love it as much as we do!

.. image:: _static/solar_system.png
   :align: center

New features
............

* **New plotting methods**: Check out
  :py:meth:`~poliastro.plotting.static.StaticOrbitPlotter.plot_body_orbit` and
  :py:meth:`~poliastro.plotting.static.StaticOrbitPlotter.plot_ephem`,
  available in all orbit plotter classes (both static and interactive).
* **New CZML methods**: Simple API to retrieve the document
  :py:meth:`poliastro.czml.extract_czml.CZMLExtractor.get_document` and method to add
  trajectories :py:meth:`~poliastro.czml.extract_czml.CZMLExtractor.add_trajectory`
* **Propagation events**: We added basic support for event detection when propagation
  with the Cowell method and created a :py:class:`~poliastro.twobody.events.LithobrakeEvent`
  that detects impact with the surface of an attractor. We will be adding more events
  in the future.
* **Extended atmospheric properties beyond 90 kilometers**: We completed the
  implementation of our atmospheric models,
  :py:class:`poliastro.atmosphere.coesa62.COESA62` and
  :py:class:`~poliastro.atmosphere.coesa76.COESA76`, to compute physical properties
  beyond 90 kilometers, and tested them up to approximately 700 kilometers.

Bugs fixed
..........

* `Issue #475`_: 🎉 Propagator mean_motion hangs for some r, v vectors around Earth
  (see the gory details at the `Farnocchia propagator pull request`_)
* `Issue #716`_: Prevent Orbit creation with non scalar quantities
* `Issue #726`_: Strange behaviour when plotting some orbits
* `Issue #817`_: CZML extractor: timezone issues (clock.Interval and currentTime not tz-aware)
* `Issue #824`_: Properly plot orbits in different planes
* `Issue #829`_: Long standing typo in equinoctial elements documentation
* `Issue #837`_: Fix :py:const:`R_polar_jupiter` value
* `Issue #840`_: vallado.lambert fails for long way transfers
* `Issue #841`_: RAAN from LTAN calculation off by 180 degrees
* `Issue #849`_: Changed ss.frame to ss.get_frame in documentation
* `Issue #850`_: Duplicated sphinx extension
* `Issue #859`_: Fix Binder
* `Issue #861`_: Make from_sbdb tests more robust against external changes
* `Issue #862`_: CZML tests failing locally because of non-UTC timezones
* `Issue #892`_: Error in porkchop docstrings
* `Issue #901`_: Fix sampling logic for closed orbits
* `Issue #902`_: Error while reading Halley's comet from DASTCOM5
* `Issue #907`_: Orbit.propagate_to_anomaly freezes
* `Issue #911`_: CZMLExtractor has no API documentation
* `Issue #916`_: Orbit.from_sbdb raises unhelpful error if no object was found

.. _`Issue #475`: https://github.com/poliastro/poliastro/issues/475
.. _`Farnocchia propagator pull request`: https://github.com/poliastro/poliastro/pull/908
.. _`Issue #716`: https://github.com/poliastro/poliastro/issues/716
.. _`Issue #726`: https://github.com/poliastro/poliastro/issues/726
.. _`Issue #817`: https://github.com/poliastro/poliastro/issues/817
.. _`Issue #824`: https://github.com/poliastro/poliastro/issues/824
.. _`Issue #829`: https://github.com/poliastro/poliastro/issues/829
.. _`Issue #837`: https://github.com/poliastro/poliastro/issues/837
.. _`Issue #840`: https://github.com/poliastro/poliastro/issues/840
.. _`Issue #841`: https://github.com/poliastro/poliastro/issues/841
.. _`Issue #849`: https://github.com/poliastro/poliastro/issues/849
.. _`Issue #850`: https://github.com/poliastro/poliastro/issues/850
.. _`Issue #859`: https://github.com/poliastro/poliastro/issues/859
.. _`Issue #861`: https://github.com/poliastro/poliastro/issues/861
.. _`Issue #862`: https://github.com/poliastro/poliastro/issues/862
.. _`Issue #892`: https://github.com/poliastro/poliastro/issues/892
.. _`Issue #901`: https://github.com/poliastro/poliastro/issues/901
.. _`Issue #902`: https://github.com/poliastro/poliastro/issues/902
.. _`Issue #907`: https://github.com/poliastro/poliastro/issues/907
.. _`Issue #911`: https://github.com/poliastro/poliastro/issues/911
.. _`Issue #916`: https://github.com/poliastro/poliastro/issues/916

Backwards incompatible changes
..............................

* poliastro :ref:`frames`  now must be imported from the specific submodule.
* Renamed ``kepler`` to :py:meth:`poliastro.twobody.propagation.vallado`
  and ``mean_motion`` to :py:meth:`poliastro.twobody.propagation.farnocchia`.
* Removed ``nu_to_M`` and ``M_to_nu`` functions, see the
  `Farnocchia propagator pull request`_ for discussion. We recommend users to
  use the mean anomaly only for elliptic orbits using
  :py:meth:`~poliastro.twobody.angles.E_to_M`, :py:meth:`~poliastro.twobody.angles.nu_to_E`
  and the converse functions.
* Renamed ``SolarSystemBody`` to :py:class:`poliastro.bodies.SolarSystemPlanet`.
* Removed unused ``poliastro.coordinates`` module.

Other news
..........

* Support for Python 3.8! The next release will add support for Python 3.9
  and remove support for 3.6, following `NEP 29`_.
* `Benchmarks <https://benchmarks.poliastro.space/>`_ moved to a new location!
* Switched to Azure Pipelines, so we are again testing in all operative systems.
* `Huge internal refactor of orbit plotters <https://github.com/poliastro/poliastro/pull/876>`_.
* We do not ship tests anymore! To run the tests, you will now need to
  `clone poliastro repository <https://github.com/poliastro/poliastro/>`_.

.. _`NEP 29`: https://numpy.org/neps/nep-0029-deprecation_policy.html

Contributors
............

This is a complete, alphabetic list of people that contributed to this release,
with a + sign indicating first contribution.

* Abdallah+
* Abhishek Chaurasia+
* Andrej Rode+
* Greg Lindahl+
* Ian DesJardin+
* Jorge Martínez
* Jos van 't Hof+
* Juan Luis Cano Rodríguez
* María Eugenia Cruz
* Nanubala Gnana Sai+
* Sarthak Jain+
* Shreyas Bapat
* Sundesh Gupta+
* Syed Osama Hussain+
* Tomek Mrugalski+
* Priyanshu Rohilla+

poliastro 0.13.1 - 2019-12-20
-----------------------------

This release fixes some bugs found after 0.13.0.

Bugs fixed
..........

* `Issue #715`_: Fix docs and dependencies for most recent nbsphinx release
* `Issue #761`_: Fix unnoticed doctest failures due to unit problems
* `Issue #776`_: Fix typing error in test
* `Issue #781`_: Fix broken binder embedded hyperlinks
* `Issue #821`_: Fix timezone issues in CZML extraction

* [No issue number] Avoid looking for tests in virtual environments
* [No issue number] Remove executable bit from some Python sources

.. _`Issue #715`: https://github.com/poliastro/poliastro/issues/715
.. _`Issue #761`: https://github.com/poliastro/poliastro/issues/761
.. _`Issue #776`: https://github.com/poliastro/poliastro/issues/776
.. _`Issue #781`: https://github.com/poliastro/poliastro/issues/781
.. _`Issue #821`: https://github.com/poliastro/poliastro/issues/821

Do you want to help with the remaining ones?
`Check the current list here! <https://github.com/poliastro/poliastro/issues?q=is%3Aopen+is%3Aissue+label%3Abug>`_

Contributors
............

This is the complete list of the people that contributed to this release,
with a + sign indicating first contribution.

* Juan Luis Cano
* Ole Streicher
* Shreyas Bapat

poliastro 0.13.0 - 2019-08-05
-----------------------------

This major release is packed with new features, especially the new
CZML exporting capabilities and miscellaneous additions and important fixes
on the algorithmic side. It also sets a new high in terms of contributors,
which makes us extremely proud and thankful!

Highlights
..........

* **Export Orbit objects to CZML**: There is new experimental functionality to
  export :py:class:`~poliastro.twobody.orbit.Orbit` to CZML, the JSON format used
  by the Cesium visualization system. This complements poliastro capabilities
  and allows users to produce gorgeous visualizations, like the one below.
  We also kickstarted a new project called `czml3`_ a Python 3 interface to CZML,
  to support all these new capabilities, and created a `base Cesium application`_
  so you can quickly start experimenting. Let us know your thoughts!
* **2D plots are static by default**: Getting Plotly properly installed is
  a bit more difficult than just a :code:`pip install` nowadays, and
  it turns out we alienated some of our non-Jupyter users by pushing it too soon
  (especially those of you that use Spyder). We have tried hard in this release
  to make the default plotting work everywhere by sticking again to matplotlib,
  while allowing more proficient users to install all the necessary components
  to have interactive visualizations going. If you still find issues, tell us!
* **New Lambert maneuver**: After a long time, Lambert transfers are finally
  a :py:class:`~poliastro.maneuver.Maneuver`, which means it shares the same API
  as Hohmann and bielliptic transfers among others, making it easier to use.
* **Lots of new propagators**: And when we say _lots_, we mean it! Lots of
  authors claim their propagator is "universal", but to our knowledge this is
  almost always a slight overstatement. To enrich poliastro with new propagation
  methods and allow users to test them with all kinds of crazy orbits
  (especially quasy-parabolic ones) we implemented a ton of new propagators,
  all sharing the same API. You have more information in this article about
  `the new propagators`_ in our blog.
* **Python 3.6+ only**: Python 3.5 has done a great service and will still be
  supported by Astropy a few more months, but we already wanted to move on
  and embrace fixed-order dictionaries, f-strings, and decimal separators,
  among others. This release of poliastro requires Python 3.6 or higher to work.
  We are also getting ready for Python 3.8!

.. image:: _static/cesium.gif
   :width: 675px
   :align: center

.. _`czml3`: https://github.com/poliastro/czml3/
.. _`base Cesium application`: https://github.com/poliastro/cesium-app
.. _`the new propagators`: https://blog.poliastro.space/2019/07/16/2019-07-16-new-propagators/


New features
............

* **More orbit creation methods**: Both to interface with external systems
  (:py:meth:`~poliastro.twobody.orbit.Orbit.from_sbdbs`) and to build new special orbits
  (:py:meth:`~poliastro.twobody.orbit.Orbit.frozen`).
* **Non-planar transfer maneuvers**: https://github.com/poliastro/poliastro/pull/599
* **Arrival velocity contour lines in porkchop plots**: Now porkchop plots are a bit richer
  and display arrival velocity as well.
* **Experimental Geocentric Solar Ecliptic frame**: We introduced an experimental
  implementation of a Geocentric Solar Ecliptic frame, which is used for studies of
  Near Earth Objects. Please help us validating it!
* **Plot orbit trails**: Apart from plotting orbits as solid or dashed lines, now
  it's easier to visualize the actual direction of the orbit using :code:`trail=True`.
* **New :code:`change_attractor` method**: Now it's easier to translate the origin
  of an orbit (withing the patched conics framework) to study it from a different perspective
  using the :py:meth:`~poliastro.twobody.orbit.Orbit.change_attractor` method.
* **New :code:`SpheroidLocation`**: We also added a experimental
  :py:class:`poliastro.spheroid_location.SpheroidLocation`, which tries to generalize
  :py:class:`astropy.coordinates.EarthLocation` to other bodies.
* **New orbital properties**: Angular momentum, mean anomaly, time of perifocal passage
  of :py:class:`~poliastro.twobody.orbit.Orbit` are now very easy to compute.

Bugs fixed
..........

* `Issue #348`_ and `Issue #495`_: Fix Lambert corner case
* `Issue #530`_: FigureWidget objects are not used anymore
* `Issue #542`_: Download progress is now shown for DASTCOM5
* `Issue #548`_ and `Issue #629`_: ipywidgets was not present in requirements
* `Issue #572`_: documentation CSS is no longer messed up
* `Issue #585`_: OrbitPlotter classes no longer relayout the figure
  in Plotly batch mode
* `Issue #590`_: Confusion between semimajor axis and semilatus rectum
  in docstring
* `Issue #609`_: Raise error in :py:meth:`~poliastro.twobody.orbit.Orbit.from_sbdb`
* `Issue #652`_: Editable installs now work with modern pip
  when more than one orbit is returned
* `Issue #654`_: Orbits around custom bodies can be propagated again

.. _`Issue #348`: https://github.com/poliastro/poliastro/issues/348
.. _`Issue #495`: https://github.com/poliastro/poliastro/issues/495
.. _`Issue #530`: https://github.com/poliastro/poliastro/issues/530
.. _`Issue #542`: https://github.com/poliastro/poliastro/issues/542
.. _`Issue #548`: https://github.com/poliastro/poliastro/issues/548
.. _`Issue #572`: https://github.com/poliastro/poliastro/issues/572
.. _`Issue #585`: https://github.com/poliastro/poliastro/issues/585
.. _`Issue #590`: https://github.com/poliastro/poliastro/issues/590
.. _`Issue #609`: https://github.com/poliastro/poliastro/issues/609
.. _`Issue #629`: https://github.com/poliastro/poliastro/issues/629
.. _`Issue #652`: https://github.com/poliastro/poliastro/issues/652
.. _`Issue #654`: https://github.com/poliastro/poliastro/issues/654

Backwards incompatible changes
..............................

* The :py:mod:`poliastro.neos.neows` module is gone, use
  :py:meth:`~poliastro.twobody.orbit.Orbit.from_horizons`
  or :py:meth:`~poliastro.twobody.orbit.Orbit.from_sbdb` instead.
  We were pioneers in implementing it, but now the same functionality
  can be found elsewhere, with better support.
* We removed :py:class:`~poliastro.plotting.OrbitPlotter2D.savefig`,
  check out the `Plotly exporting documentation`_ for the best way
  of doing the same thing.
* We removed the :code:`method` parameter from
  :py:meth:`~poliastro.twobody.orbit.Orbit.sample`,
  use :py:meth:`poliastro.twobody.propagation.propagate` for lower
  level control instead.
  We wanted to simplify the :code:`sample` method to avoid making
  it a catch-all function.

.. _`Plotly exporting documentation`: https://plot.ly/python/next/static-image-export/

Other news
..........

* Updated minimum Astropy version to 3.2 and Plotly to 4.0.
* Updated planetary :py:mod:`poliastro.constants`, plan to add more.
* Better development workflow, issue templates on GitHub,
  tools to reformat the code.

Contributors
............

This is a complete, alphabetic list of people that contributed to this release,
with a + sign indicating first contribution.
Again we had an all-time high number of contributors, thanks everybody ❤️

* Adam Johnson+
* Ahmada Yusril+
* Angala+
* Divyansh Raina+
* Eleftheria Chatziargyriou+
* Helge Eichhorn
* Himanshu Garg
* Iván Castro+
* Jesús Jiménez+
* Jorge Martinez
* Juan Luis Cano
* Manuel Kaufmann+
* María Eugenia Cruz+
* Ritwik Saha+
* Shreyas Bapat
* Siro Moreno+
* Sky+
* Vedang Naik+
* Emily Selwood

poliastro 0.12.0 - 2019-02-21
-----------------------------

This major release brings lots of new features, several breaking changes
that improve the overall consistency of the library, and a stronger bet
on Plotly as the default plotting backend, as well as the usual bug fixes.
This has been the biggest release in terms of contributors so far and
we feel we are reaching a tipping point, which makes us extremely proud
and also busier!

Highlights
..........

* **New defaults for plotting**: We are now switching to Plotly for the default
  plotting backend as it has better interactive capabilities in the notebook,
  while keeping the matplotlib backend for publication-quality, 2D static plots.
  There might be some rough edges in the installation or in trying to keep the
  aspect ratio still, so we ask for user feedback.
* **Reorganization of propagation capabilities**: We made some changes to the propagation
  APIs to be more coherent and flexible and simpler to understand for new contributors.
  We removed some features from :py:meth:`~poliastro.twobody.orbit.Orbit.sample` to
  keep it simpler while moving some of them to
  :py:meth:`poliastro.twobody.propagation.propagate`, and we splitted
  :py:meth:`~poliastro.twobody.orbit.Orbit.propagate` by adding
  :py:meth:`~poliastro.twobody.orbit.Orbit.propagate_to_anomaly`. At the cost of
  some breakage, we think this is a positive change that will make the library
  more maintainable in the future and reduce the number of bugs.
* **Better integration with reference frames**: We took one step further in our
  endeavor to integrate better with Astropy reference frames by adding a
  :py:meth:`~poliastro.twobody.orbit.Orbit.from_coords` method that accepts
  any frame, be it inertial or not.
* **Refactor of Orbit objects**: The :py:class:`~poliastro.twobody.orbit.Orbit`
  was designed a long time ago and some design choices prevented all its
  orbital properties to appear in the documentation, while also making people
  think that they had to use an internal property. After a simple refactor
  this is no longer the case, and the code is still fast while being
  much simpler to understand. Did you know that you can compute the
  *semilatus rectum*, the modified equinoctial elements, the eccentricity vector
  or the mean motion of an :py:class:`~poliastro.twobody.orbit.Orbit`?
  Now there are no excuses!

New features
............

* **New orbit creation methods**: We can create an
  :py:class:`~poliastro.twobody.orbit.Orbit` directly from JPL HORIZONS data using
  :py:meth:`~poliastro.twobody.orbit.Orbit.from_horizons`, from Astropy
  :code:`SkyCoord` and :code:`BaseCoordinateFrame` objects using
  :py:meth:`~poliastro.twobody.orbit.Orbit.from_coords`, and Geostationary orbits
  around an attractor using :py:meth:`~poliastro.twobody.orbit.Orbit.geostationary`.
  We plan to keep adding more in the coming releases.
* **New propagation methods**: We now have more specific methods for certain
  tasks, like :py:meth:`~poliastro.twobody.orbit.Orbit.propagate_to_anomaly` to
  propagate an :py:class:`~poliastro.twobody.orbit.Orbit` to a certain anomaly,
  and we can specify the anomaly limits when using
  :py:meth:`~poliastro.twobody.orbit.Orbit.sample`.
* **New simple plotting method**: We added a
  :py:meth:`~poliastro.twobody.orbit.Orbit.plot` to quickly plot an
  :py:class:`~poliastro.twobody.orbit.Orbit` without additional imports, in 2D or 3D.
* **Dark theme for Plotly plots**: It is now possible to create Plotly plots
  with a dark background, perfect for recreating our Solar System!
* **Computation of the Hill radius**: To complement the existing Laplace
  sphere of influence (or just Sphere of Influence) available with
  :py:meth:`poliastro.threebody.soi.laplace_radius`, we added the Hill radius
  as well with the function :py:meth:`poliastro.threebody.soi.hill_radius`.
* **Porkchop plots**: By popular demand, we can now produce *gorgeous*
  `Porkchop plots`_ to analyze launch opportunities between origin and
  destination bodies by using :py:meth:`poliastro.plotting.porkchop.porkchop`.
  We plan to expand its capabilities by being able to target any body of
  the Solar System. Stay tuned!

.. image:: _static/porkchop.png
   :width: 675px
   :align: center

.. _`Porkchop plots`: https://en.wikipedia.org/wiki/Porkchop_plot

Bugs fixed
..........

* `Issue #435`_: :py:class:`~poliastro.twobody.orbit.Orbit` properties were not
  discoverable
* `Issue #469`_: Better error for collinear points in Lambert problem
* `Issue #476`_: Representation of orbits with no frame
* `Issue #477`_: Propagator crashed when propagating a hyperbolic orbit 0 seconds
* `Issue #480`_: :py:class:`~poliastro.plotting.OrbitPlotter2D` did not have
  a :py:meth:`~poliastro.plotting.OrbitPlotter2D.set_frame` method
* `Issue #483`_: :py:class:`~poliastro.plotting.OrbitPlotter2D`OrbitPlotter2D`
  results were not correct
* `Issue #518`_: Trajectories were not redrawn when the frame was changed
* `Issue #548`_: Improve installation instructions to include interactive and test
  dependencies
* `Issue #573`_: Fix outdated matplotlib version limits

.. _`Issue #435`: https://github.com/poliastro/poliastro/issues/435
.. _`Issue #469`: https://github.com/poliastro/poliastro/issues/469
.. _`Issue #476`: https://github.com/poliastro/poliastro/issues/476
.. _`Issue #477`: https://github.com/poliastro/poliastro/issues/477
.. _`Issue #480`: https://github.com/poliastro/poliastro/issues/480
.. _`Issue #483`: https://github.com/poliastro/poliastro/issues/483
.. _`Issue #518`: https://github.com/poliastro/poliastro/issues/518
.. _`Issue #548`: https://github.com/poliastro/poliastro/issues/548
.. _`Issue #573`: https://github.com/poliastro/poliastro/issues/573

Backwards incompatible changes
..............................

* The old :code:`OrbitPlotter` has been renamed to
  :py:class:`poliastro.plotting.static.StaticOrbitPlotter`, please adjust
  your imports accordingly.
* :py:meth:`~poliastro.twobody.orbit.Orbit.propagate`,
  :py:meth:`~poliastro.twobody.orbit.Orbit.sample`,
  :py:meth:`poliastro.twobody.propagation.propagate` and all propagators in
  :py:mod:`poliastro.twobody.propagation` now have different signatures,
  and the first two lost some functionality. Check out the notebooks
  and their respective documentation.
* The :py:mod:`poliastro.threebody` has been reorganized and some functions
  moved there.

Other updates
.............

* We now follow the `Black`_ style guide 😎
* The API docs are now more organized and should be easier to browse and
  understand.
* We are working towards documenting how to use poliastro in JupyterLab,
  please tell us about anything we may have missed.
* poliastro will be presented at the `fifth PyCon Namibia`_ 🇳🇦

.. _`Black`: https://black.readthedocs.io/
.. _`fifth PyCon Namibia`: https://na.pycon.org/speakers/

Contributors
............

This is the complete list of the people that contributed to this release,
with a + sign indicating first contribution.

* Juan Luis Cano
* Shreyas Bapat
* Jorge Martínez+
* Hrishikesh Goyal+
* Sahil Orionis+
* Helge Eichhorn+
* Antonina Geryak
* Aditya Vikram+

poliastro 0.11.1 - 2018-12-27
-----------------------------

This release fixes some bugs found in 0.11.0 and prepares the ground for bigger
API and code changes.

Bugs fixed
..........

* `Issue #281`_: Plotly graphs not showing in documentation
* `Issue #469`_: :code:`OrbitPlotter.set_frame` error
* `Issue #476`_: Error when representing orbits with no reference frame
* `Issue #482`_: Non deterministic legend layout
* `Issue #492`_: Better error for collinear orbits in Lambert and corner case arithmetic

.. _`Issue #281`: https://github.com/poliastro/poliastro/issues/281
.. _`Issue #469`: https://github.com/poliastro/poliastro/issues/469
.. _`Issue #476`: https://github.com/poliastro/poliastro/issues/476
.. _`Issue #482`: https://github.com/poliastro/poliastro/issues/482
.. _`Issue #492`: https://github.com/poliastro/poliastro/issues/492

Do you want to help with the remaining ones? Check the current list here!
https://github.com/poliastro/poliastro/issues?q=is%3Aopen+is%3Aissue+label%3Abug

Contributors
............

This is the complete list of the people that contributed to this release, with a + sign indicating first contribution.

* Juan Luis Cano
* Shreyas Bapat
* Ole Streicher+
* Antoniya Karpova+

poliastro 0.11.0 - 2018-09-21
-----------------------------

This short cycle release brought some new features related to the three body problem,
as well as important changes related to how reference frames are handled in poliastro.

Highlights
..........

* **Support for Python 3.7** has been added to the library, now that all the depdendencies
  are easily available there. Currently supported versions of Python are 3.5, 3.6 and 3.7.

New features
............

* **Lagrange points**: The new experimental module :py:mod:`poliastro.threebody.restricted`
  contains functions to compute the Lagrange points in the circular restricted three body
  problem (CR3BP). It has been validated only approximately, so use it at your own risk.
* **Flybys**: New functions to compute the exit velocity and turn angle have been added to
  the new module :py:mod:`poliastro.threebody.flybys`. The B-plane aim point can be specified
  and the result will be returned in the correct reference frame. This feature was motivated
  by the Parker Solar Probe mission, and you can read an example on `how to analyze parts of
  its trajectory using poliastro`_.
* **Reference frames**: We addded experimental support for reference frames in poliastro objects.
  So far, the :py:class:`~poliastro.twobody.orbit.Orbit` objects were in some assumed reference
  frame that could not be controlled, leading to some confusion by people that wanted some
  specific coordinates. Now, **the reference frame is made out explicit**, and there is also
  the possibility to make a limited set of transformations. This framework will be further
  developed in the next release and transformations to arbitrary frames will be allowed.
  Check out the :py:mod:`poliastro.frames` module for more information.

.. _`how to analyze parts of its trajectory using poliastro`: http://docs.poliastro.space/en/latest/examples/Analyzing%20the%20Parker%20Solar%20Probe%20flybys.html

Bugs fixed
..........

* `Issue #450`_: Angles function of safe API have wrong docstrings

.. _`Issue #450`: https://github.com/poliastro/poliastro/issues/450

Do you want to help with the remaining ones? Check the current list here!
https://github.com/poliastro/poliastro/issues?q=is%3Aopen+is%3Aissue+label%3Abug

Backwards incompatible changes
..............................

* The :py:meth:`poliastro.twobody.Orbit.sample` method returns one single object again that
  contains the positions and the corresponding times.

Contributors
............

This is the complete list of the people that contributed to this release, with a + sign indicating first contribution.

* Juan Luis Cano
* Nikita Astrakhantsev
* Shreyas Bapat
* Daniel Lubián+
* Emily Selwood+

poliastro 0.10.0 - 2018-07-21
-----------------------------

This major release brings important changes from the code perspective
(including a major change in the structure of the library),
several performance improvements
and a new infrastructure for running timing benchmarks,
as well as some new features and bug fixes.

Highlights
..........

* **Major change in the structure of poliastro codebase**: We separated the high level,
  units safe functions from the low level, fast ones, with the subsequent improvement
  in code quality. With this change we effectively communicate where "core" algorithms
  should go, make easier for future contributors to add numerical functions, and
  improved the overall quality of the library.
* **Upgrade to new SciPy ODE solvers**: We wrote our own version of Dormand-Prince 8(5,3)
  based on the new IVP framework in SciPy 1.0 to take advantage of event detection,
  dense output and other fancy features. In particular,
  the :py:meth:`~poliastro.twobody.orbit.Orbit.sample` method now uses dense output when available,
  therefore removing the need to propagate the orbit repeatedly.
* **New infrastructure for benchmarks**: We started publishing timing benchmarks results
  using `Airspeed Velocity`_, a Python framework for writing, running, studying and
  publishing benchmarks. Besides, we bought a dedicated machine to run them with
  as much precision as we can.
  Please `check them out <https://poliastro.github.io/benchmarks/>`_
  and consider `adding new benchmarks`_ as well!
* **Several performance improvements**: Now that we are tracking performance, we dedicated
  some time during this release to fix some performance regressions that appeared in
  propagation, improving the behavior near parabolic orbits, and accelerating (even more!)
  the Izzo algorithm for the Lambert problem as well as some poliastro utilities.
* **New Continuous Integration infrastructure**: We started to use CircleCI for the
  Linux tests, the coverage measurements and the documentation builds. This service
  has faster machines and better support for workflows, which significantly reduced
  the build times and completely removed the timeouts that were affecting us in
  Travis CI.
* **Plotly backends now stable**: We fixed some outstanding issues with the 2D Plotly backend
  so now it's no longer experimental. We also started refactoring some parts of the plotting module
  and prepared the ground for the new interactive widgets that Plotly 3.0 brings.

.. _`Airspeed Velocity`: https://asv.readthedocs.io/
.. _`adding new benchmarks`: https://github.com/poliastro/benchmarks/

New features
............

* **New continuous thrust/low thrust guidance laws**: We brought some continuous thrust
  guidance laws for orbital maneuvers that have analytical solution, such as orbit
  raising combined with inclination change, eccentricity change and so forth. This is based on
  the Master Thesis of Juan Luis Cano, "Study of analytical solutions for low-thrust trajectories",
  which provided complete validation for all of these laws and which
  `can be found on GitHub <https://github.com/juanlu001/pfc-uc3m>`_.
* **More natural perturbations**: We finished adding the most common orbital perturbations,
  namely Solar radiation pressure and J3 perturbation. We could not reach agreement with
  the paper for the latter, so if you are considering using it please read the discussion
  `in the original pull request <https://github.com/poliastro/poliastro/pull/398>`_ and
  consider lending us a hand to validate it properly!
* **New dark mode for matplotlib plots**: We added a :code:`dark` parameter to
  :py:class:`~poliastro.plotting.OrbitPlotter` objects so the background is black.
  Handy for astronomical purposes!

Bugs fixed:
...........

Besides some installation issues due to the evolution of dependencies, these
code bugs were fixed:

* `Issue #345`_: Bodies had incorrect aspect ratio in OrbitPlotter2D
* `Issue #369`_: Orbit objects cannot be unpickled
* `Issue #382`_: Orbit.from_body_ephem returns wrong orbit for the Moon
* `Issue #385`_: Sun Incorrectly plotted in plot_solar_system

.. _`Issue #345`: https://github.com/poliastro/poliastro/issues/345
.. _`Issue #382`: https://github.com/poliastro/poliastro/issues/382
.. _`Issue #385`: https://github.com/poliastro/poliastro/issues/385

Backward incompatible changes
.............................

* Some functions have been moved to :py:mod`:poliastro.core`.

Contributors
............

This is the complete list of the people that contributed to this release,
with a + sign indicating first contribution.

* Juan Luis Cano
* Nikita Astrakhantsev
* Shreyas Bapat
* jmerskine1+

poliastro 0.9.1 - 2018-05-11
----------------------------

This is a minor release that fixes one single issue:

* `Issue #369`_:  Orbit objects cannot be unpickled

.. _`Issue #369`: https://github.com/poliastro/poliastro/issues/369

Thanks to Joan Fort Alsina for reporting.

poliastro 0.9.0 - 2018-04-25
----------------------------

This major release received lots of improvements in the 2D plotting code
and propagation functions, introduced the new perturbation framework and
paved the way for the `Python in Astronomy 2018`_ workshop and the
`Google Summer of Code 2018`_ program.

.. _`Python in Astronomy 2018`: https://openastronomy.org/pyastro/2018/
.. _`Google Summer of Code 2018`: https://summerofcode.withgoogle.com/

New features
............

* **New experimental 2D Plotly backend**: A new :py:class:`~poliastro.plotting.OrbitPlotter2D`
  class was introduced that uses Plotly instead of matplotlib for the rendering. There are
  still some issues that should be resolved when we take advantage of the latest Plotly version,
  hence the "experimental" nature.
* **New propagators**: A new Keplerian propagator :py:meth:`~poliastro.twobody.propagation.mean_motion`
  was introduced that has better convergence properties than :py:meth:`~poliastro.twobody.propagation.kepler`,
  so now the user can choose.
* **New perturbation functions**: A new module :py:mod:`poliastro.twobody.perturbations` was introduced
  that contains perturbation accelerations that can be readily used with
  :py:meth:`~poliastro.twobody.propagation.cowell`. So far we implemented J2 and atmospheric drag effects,
  and we will add more during the summer. Check out the User Guide for examples!
* **Support for different propagators in sampling**: With the introduction of new propagators and perturbation
  accelerations, now the user can easily sample over a period of time using any of them. We are eager to see
  what experiments you come up with!
* **Easy plotting of the Solar System**: A new function :py:meth:`~poliastro.plotting.plot_solar_system` was
  added to easily visualize our inner or complete Solar System in 2D plots.

Other highlights
................

* **poliastro participates in Google Summer of Code thanks to OpenAstronomy!**
  More information `in the poliastro blog <https://blog.poliastro.space/2018/02/22/2018-02-22-join-poliastro-google-summer-of-code/>`_.
* **poliastro will be presented at the Python in Astronomy 2018 workshop** to be held
  at Center for Computational Astrophysics at the Flatiron Institute in New York, USA.
  You can read `more details about the event here <https://openastronomy.org/pyastro/2018/>`_.

New contributors
................

This is the complete list of the people that contributed to this release,
with a + sign indicating first contribution.

* Juan Luis Cano
* Pablo Galindo+
* Matt Ettus+
* Shreyas Bapat+
* Ritiek Malhotra+
* Nikita Astrakhantsev+

Bugs fixed:
...........

* `Issue #294`_: Default steps 2D plots were too visible

.. _`Issue #294`: https://github.com/poliastro/poliastro/issues/294

Backward incompatible changes
.............................

* Now the :py:meth:`poliastro.twobody.Orbit.sample` method returns a tuple of (times, positions).
* All the propagator methods changed their signature
  and now accept :py:class:`~poliastro.twobody.Orbit` objects.

poliastro 0.8.0 - 2017-11-18
----------------------------

This is a new major release, focused on bringing 3D plotting functions and
preparing the material for the Open Source Cubesat Workshop.

New features
............

* **Sampling method** for :py:class:`~poliastro.twobody.Orbit` objects that returns
  an array of positions. This was already done in the plotting functions and will
  help providing other applications, such as exporting an Orbit to other formats.
* **3D plotting functions**: finally poliastro features a new high level object,
  :py:class:`poliastro.plotting.OrbitPlotter3D`, that uses Plotly to represent
  orbit and trajectories in 3D. The venerable notebook about the trajectory of
  rover Curiosity has been updated accordingly.
* **Propagation to a certain date**: now apart from specifying the total elapsed
  time for propagation or time of flight, we can directly specify a target date
  in :py:meth:`poliastro.twobody.orbit.Orbit.propagate`.
* **Hyperbolic anomaly conversion**: we implemented the conversion of hyperbolic
  to mean and true anomaly to complement the existing eccentric anomaly functions
  and improve the handling of hyperbolic orbits in :py:mod:`poliastro.twobody.angles`.

Other highlights
................

* **poliastro is now an Astropy affiliated package**, which gives the project a privileged
  position in the Python ecosystem. Thank you, Astropy core developers! You can read
  `the evaluation here <https://github.com/poliastro/poliastro/issues/279>`_.
* **poliastro will be presented at the first Open Source Cubesat Workshop** to be held
  at the European Space Operations Centre in Darmstadt, Germany. You can read
  `the full program of the event here <http://oscw.space/>`_.

New contributors
................

This is the complete list of the people that contributed to this release,
with a + sign indicating first contribution.

* Juan Luis Cano
* Antonio Hidalgo
* mattrossman+
* Roshan Jossey+

Bugs fixed:
...........

* `Issue #275`_: Converting from true to mean anomaly fails for hyperbolic orbits

.. _`Issue #275`: https://github.com/poliastro/poliastro/issues/275

Backward incompatible changes
.............................

* The :code:`ephem` module has been removed in favor of the
  :code:`astropy.coordinates.get_body_barycentric_posvel` function.

poliastro 0.7.0 - 2017-09-15
----------------------------

This is a new major release, which adds new packages and modules,
besides fixing several issues.

New features:
.............

* **NEOS package**: a new package has been added to poliastro, :py:mod:`~poliastro.neos`
  package. It provides several ways of getting NEOs (Near Earth Objects) data from NASA
  databases, online and offline.
* **New patched conics module**. New module containing a function to compute
  the radius of the Sphere of Influence (SOI).
* **Use Astropy for body ephemerides**. Instead of downloading the SPK
  files ourselves, now we use Astropy builtin capabilities. This also
  allows the user to select a builtin ephemerides that does not require
  external downloads. See `#131`_ for details.
* **Coordinates and frames modules**: new modules containing transformations between ICRS
  and body-centered frame, and perifocal to body_centered, :py:mod:`~poliastro.coordinates`
  as well as Heliocentric coordinate frame in :py:mod:`~poliastro.frames` based on Astropy
  for NEOs.
* **Pip packaging**: troublesome dependencies have been released in wheel format,
  so poliastro can now be installed using pip from all platforms.
* **Legend plotting**: now label and epoch are in a figure legend, which ends with
  the ambiguity of the epochs when having several plots in the same figure.

.. _`#131`: https://github.com/poliastro/poliastro/issues/131


Other highlights:
.................

* **Joined Open Astronomy**: we are now part of `Open Astronomy`_, a
  collaboration between open source astronomy and astrophysics projects
  to share resources, ideas, and to improve code.
* **New constants module**: poliastro has now a :py:mod:`~poliastro.constants` module,
  with GMs and radii of solar system bodies.
* **Added Jupyter examples**: poliastro examples are now available in the
  documentation as Jupyter notebooks, thanks to `nbsphinx`_.
* **New Code of Conduct**: poliastro community now has a Code of conduct.
* **Documentation update**: documentation has been updated with new installation
  ways, propagation and NEOs examples, "refactored" code and images, improved contribution
  guidelines and intersphinx extension.
* **New success stories**: two new success stories have been added to documentation.
* **Bodies now have a parent**. It is now possible to specify the attractor
  of a body.
* **Relative definition of Bodies**. Now it is possible to define Body parameters
  with respect to another body, and also add any number of properties in a simple
  way.

.. _`nbsphinx`: http://nbsphinx.readthedocs.io/en/latest/
.. _`Open Astronomy`: https://openastronomy.org/members/

New contributors
................

Thanks to the generous SOCIS grant from the European Space Agency,
Antonio Hidalgo has devoted three months developing poliastro full time
and gained write access to the repository.

This is the complete list of the people that contributed to this release,
with a + sign indicating first contribution.

* Juan Luis Cano
* MiguelHB+
* Antonio Hidalgo+
* Zac Miller+
* Fran Navarro+
* Pablo Rodríguez Robles+

Bugs fixed:
...........

* `Issue #205`_: Bug when plotting orbits with different epochs.
* `Issue #128`_: Missing ephemerides if no files on import time.
* `Issue #131`_: Slightly incorrect ephemerides results due to improper time scale.
* `Issue #130`_: Wrong attractor size when plotting different orbits.

.. _`Issue #205`: https://github.com/poliastro/poliastro/issues/205
.. _`Issue #128`: https://github.com/poliastro/poliastro/issues/128
.. _`Issue #131`: https://github.com/poliastro/poliastro/issues/131
.. _`Issue #130`: https://github.com/poliastro/poliastro/issues/130

Backward incompatible changes:
..............................

* **Non-osculating orbits**: removed support for non-osculating orbits.
  :code:`plotting.plot()` calls containing :code:`osculating` parameter should be
  replaced.

poliastro 0.6.0 - 2017-02-12
----------------------------

This major release was focused on refactoring some internal core
parts and improving the propagation functionality.

Highlights:
...........

* **Support Python 3.6**. See `#144`_.
* **Introduced ``Orbit`` objects** to replace ``State`` ones. The latter
  has been simplified, reducing some functionality, now their API
  has been moved to the former. See the User Guide and the examples for
  updated explanations. See `#135`_.
* **Allow propagation functions to receive a callback**. This paves the
  way for better plotting and storage of results. See `#140`_.

.. _`#135`: https://github.com/poliastro/poliastro/pull/135
.. _`#140`: https://github.com/poliastro/poliastro/pull/140
.. _`#144`: https://github.com/poliastro/poliastro/pull/144

poliastro 0.5.0 - 2016-03-06
----------------------------

This is a new major release, focused on expanding the initial orbit
determination capabilities and solving some infrastructure challenges.

New features:
.............

* **Izzo's algorithm for the Lambert problem**: Thanks to this algorithm
  multirevolution solutions are also returned. The old algorithm is kept
  on a separate module.

Other highlights:
.................

* **Documentation on Read the Docs**: You can now browse previous releases
  of the package and easily switch between released and development versions.
* **Mailing list**: poliastro now has a mailing list hosted on groups.io.
  Come and join!
* **Clarified scope**: poliastro will now be focused on interplanetary
  applications, leaving other features to the new `python-astrodynamics`_
  project.

.. _`python-astrodynamics`: http://python-astrodynamics.org/

Bugs fixed:
...........

* `Issue #110`_: Bug when plotting State with non canonical units

.. _`Issue #110`: https://github.com/poliastro/poliastro/issues/110

Backward incompatible changes:
..............................

* **Drop Legacy Python**: poliastro 0.5.x and later will support only
  Python 3.x. We recommend our potential users to create dedicated virtual
  environments using conda or virtualenv or to contact the developers to fund
  Python 2 support.
* **Change ``lambert`` function API**: The functions for solving Lambert's
  problem are now _generators_, even in the single revolution case.
  Check out the User Guide for specific examples.
* **Creation of orbits from classical elements**: poliastro has
  reverted the switch to the *semilatus rectum* \\(p\\) instead of the semimajor
  axis \\(a\\) made in 0.4.0, so \\(a\\) must be used again. This change is
  definitive.

poliastro 0.4.2 - 2015-12-24
----------------------------

Fixed packaging problems.

poliastro 0.4.0 - 2015-12-13
----------------------------

This is a new major release, focused on improving stability and code quality.
New angle conversion and modified equinoctial elements functions were added
and an important backwards incompatible change was introduced related to
classical orbital elements.

New features:
.............

* **Angle conversion functions**: Finally brought back from poliastro 0.1,
  new functions were added to convert between true \\(\\nu\\), eccentric
  \\(E\\) and mean \\(M\\) anomaly, see `#45`_.
* **Equinoctial elements**: Now it's possible to convert between classical
  and equinoctial elements, as well as from/to position and velocity vectors,
  see `#61`_.
* **Numerical propagation**: A new propagator using
  SciPy Dormand & Prince 8(5,3) integrator was added, see `#64`_.

.. _`#45`: https://github.com/poliastro/poliastro/pull/45
.. _`#61`: https://github.com/poliastro/poliastro/pull/61
.. _`#64`: https://github.com/poliastro/poliastro/pull/64

Other highlights:
.................

* **MIT license**: The project has been relicensed to a more popular license.
  poliastro remains commercial-friendly through a permissive, OSI-approved
  license.
* **Python 3.5 and NumPy 1.10 compatibility**. poliastro retains compatibility
  with legacy Python (Python 2) and NumPy 1.9. *Next version will be Python 3
  only*.

Bugs fixed:
...........

* `Issue #62`_: Conversion between coe and rv is not transitive
* `Issue #69`_: Incorrect plotting of certain closed orbits

.. _`Issue #62`: https://github.com/poliastro/poliastro/issues/62
.. _`Issue #69`: https://github.com/poliastro/poliastro/issues/69

Backward incompatible changes:
..............................

* **Creation of orbits from classical elements**: poliastro has
  switched to the *semilatus rectum* \\(p\\) instead of the semimajor
  axis \\(a\\) to define ``State`` objects, and the function has been renamed
  to :py:meth:`~poliastro.twobody.State.from_classical`. Please update your
  programs accordingly.
* Removed specific angular momentum \\(h\\) property to avoid a name clash
  with the fourth modified equinoctial element, use ``norm(ss.h_vec)``
  instead.

poliastro 0.3.1 - 2015-06-30
----------------------------

This is a new minor release, with some bug fixes backported from the main
development branch.

Bugs fixed:
...........

* Fixed installation problem in Python 2.
* `Issue #49`_: Fix velocity units in ``ephem``.
* `Issue #50`_: Fixed ``ZeroDivisionError`` when propagating with time zero.

.. _`Issue #49`: https://github.com/poliastro/poliastro/issues/49
.. _`Issue #50`: https://github.com/poliastro/poliastro/issues/50

poliastro 0.3.0 - 2015-05-09
----------------------------

This is a new major release, focused on switching to a pure Python codebase.
Lambert problem solving and ephemerides computation came back, and a couple
of bugs were fixed.

New features:
.............

* **Pure Python codebase**: Forget about Fortran linking problems and
  nightmares on Windows, because now poliastro is a pure Python package.
  A new dependency, numba, was introduced to accelerate the algorithms,
  but poliastro will use it only if it is installed.
* **Lambert problem solving**: New module :py:mod:`~poliastro.iod` to
  determine an orbit given two position vectors and the time of flight.
* `PR #42`_: **Planetary ephemerides computation**: New module
  :py:mod:`~poliastro.ephem` with functions to deal with SPK files and
  compute position and velocity vectors of the planets.
* `PR #38`_: New method :py:meth:`~poliastro.twobody.State.parabolic` to create parabolic orbits.
* New conda package: visit `poliastro binstar channel`_!
* New organization and logo.

.. _`PR #42`: https://github.com/poliastro/poliastro/pull/42
.. _`PR #38`: https://github.com/poliastro/poliastro/pull/38

.. _`poliastro binstar channel`: https://binstar.org/poliastro

Bugs fixed:
...........

* `Issue #19`_: Fixed plotting region for parabolic orbits.
* `Issue #37`_: Fixed creation of parabolic orbits.

.. _`Issue #19`: https://github.com/poliastro/poliastro/issues/19
.. _`Issue #37`: https://github.com/poliastro/poliastro/issues/37

poliastro 0.2.1 - 2015-04-26
----------------------------

This is a bugfix release, no new features were introduced since 0.2.0.

* Fixed `#35`_ (failing tests with recent astropy versions), thanks to
  Sam Dupree for the bug report.
* Updated for recent Sphinx versions.

.. _`#35`: https://github.com/poliastro/poliastro/issues/35

poliastro 0.2 - 2014-08-16
--------------------------

* **Totally refactored code** to provide a more pythonic API (see `PR #14`_
  and `wiki`_ for further information) heavily inspired by `Plyades`_ by
  Helge Eichhorn.

  * Mandatory use of **physical units** through :code:`astropy.units`.
  * Object-oriented approach: :py:class:`~poliastro.twobody.State` and
    :py:class:`~poliastro.maneuver.Maneuver` classes.
  * Vector quantities: results not only have magnitude now, but also direction
    (see for example maneuvers).

* Easy plotting of orbits in two dimensions using matplotlib.
* Module :code:`example` with sample data to start testing the library.

.. _`PR #14`: https://github.com/poliastro/poliastro/pull/14
.. _wiki: https://github.com/poliastro/poliastro/wiki
.. _Plyades: https://github.com/helgee/Plyades

These features were removed temporarily not to block the release and will
see the light again in poliastro 0.3:

* Conversion between anomalies.
* Ephemerides calculations, will look into Skyfield and the JPL ephemerides
  prepared by Brandon Rhodes (see `issue #4`_).
* Lambert problem solving.
* Perturbation analysis.

.. _`issue #4`: https://github.com/poliastro/poliastro/issues/4
