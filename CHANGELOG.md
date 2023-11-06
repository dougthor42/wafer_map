# Changelog
This document highlights high-level changes made to this program.


## Unreleased
+ Modernization: Switch from `setup.py` to `pyproject.toml`; drop support for Python
  3.7 and below; move to `src` dir.
+ Migrated CI from Travis + GitLab + Appveyor CIs to Github.
+ Added `pre-commit` config.
+ Removed now-unnecessary `build_reqs` directory; moved tests to external package.
+ Formatted code with `black`.


## 1.1.2 / 2019-10-14
+ Fix x-position of gridlines (#38)
+ The die center dots can now be toggled on and off. (#82)


## 1.1.1 / 2018-10-12
+ Make `DiscreteLegend.create_colors` a static method. (#67)


## 1.1.0 / 2018-10-12
+ Use enums for `data_type`. (#61)
+ Use enums for `coord_type`.
+ Use an ordered dict internally for `DiscreteLegend`.
+ Add a `discrete_legend_colors` arg to the WaferMapPanel constructor.
+ Minor updates to docstring formatting (#44)


## 1.0.25 / 2018-10-10
+ Fixed rendering in README.rst (for PyPI's `long_description`). Again.


## 1.0.24 / 2018-10-10
+ Fixed rendering in README.rst (for PyPI's `long_description`).


## 1.0.23 / 2018-10-10
+ Python requirements are now pinned (#59)
+ Docs for wm_core.WaferMapPanel have been updated (#60)
+ Updated `.gitlab-ci.yml` to use the correct runner since we've changed
  names. (#64)
+ Switched to using `pytest` instead of `green` (#65)
+ Updated CI to no longer use the wxPython snapshots (#66)
+ Fixed pypi long_description (hopefully).
+ Updated PyPI trove classifiers to reflect supported python versions.


## 1.0.22 / 2017-02-20
+ More attempts to fix the gitlab CI.


## 1.0.21 / 2017-02-20
+ Moved deploy to a rendezvousing build stage in gitlab ci.


## 1.0.20 / 2017-02-20
+ Updated gitlab CI to auto-deploy to local PyPI on tags
+ Updated formatting in Changelog.


## 1.0.19 / 2017-02-03
+ Fixed PyPI package name.


## 1.0.18 / 2017-02-03
+ Added Sphinx auto-documentation. So far it's only hosted locally. Sorry
  everyone! I plan to put it on ReadTheDocs soon.
+ Cleaned up imports 'cause they were crap.
+ Monkeypatched `wx.Colour`. Now you don't have to muck with your wxPython
  installation, yay!
+ Fixed Appveyor CI.


## 1.0.17 / 2016-04-11
+ Fixed bug in toggle_die_gridlines()


## 1.0.16 / 2016-04-11
+ Fixed imports for Py3


## 1.0.15 / 2016-04-11
+ Version bump because of a messed up PyPI release.


## 1.0.14 / 2016-04-11
+ Added option to display die gridlines.


## 1.0.11 / 2015-10-28
+ Implemented #31 - added radius of die and mouse to status bar.


## 1.0.10 / 2015-05-04
+ Playing around with imports. Trying to make it so that if I'm running
  a file from my development directory, it imports all the development
  modules and if I'm running something else, it imports from the
  released (site-packages) directory.
+ Fixed Issue #30


## 1.0.9 / 2015-05-04
+ Fixed flicker issue.


## 1.0.8 / 2015-05-04
+ I messed up on the PyPI release, so I have to release under a new file
  name. Oh well...


## 1.0.7 / 2015-05-04
+ Minor import refactoring
+ Added some docstrings


## 1.0.6 / 2015-04-01
+ Refactored wm_core.draw_wafer_outline so that there are fewer branches
+ Added wm_core.calc_flat_coords to reduce code duplication. This function
  calculates the start and end coordinates of a horizontal chord below
  the circle origin whos length spans a given angle. See doctring on
  wm_core.calc_flat_coords for more info.
+ Fixed issue where a flat exclusion of 0 would not work
+ Fixed issue where an exclusion of 0 would prevent the flat exclusion from
  being drawn.


## 1.0.5 / 2015-03-30
+ Added optional "grid_center" input to gen_fake_data
+ Fixed Issue #28: Updated wm_utils.linear_gradient to act on HSL data
  rather than on RGB data.
+ Updated documentation for items in wm_utils.
+ Added option to plot the die centers as small red dots.
+ Added option to have the wafer map use a constant number of items for
  discrete legend.


## 1.0.4 / 2014-12-29
+ Changed import statements to not be weird.


## 1.0.3 / 2014-12-17
+ Fixed Issue #9: Users can now change the high and low colors for
  continuous data by passing in arguements or by using the app menu:
  ``Options --> Set High Color`` or ``Set Low Color``
+ Fixed Issue #26
+ Fixed Issue #25: Continuous data now generates colors from a single
  algorithm.
+ Fixed Issue #14: Discrete Data now uses an acceptable algorithm for
  determining colors.
+ Fixed Issue #16: The plot now zooms to fit upon first draw. However,
  this created issue #21.
+ Started to add unit tests
+ Updated fake data generator to accept parameter inputs. Any missing
  parameter is randomly generated.
+ The legend for continuous data now fills the entire available vertical
  area.
+ Added a color for invalid data points such as NaN or Inf.
+ Plot range can now be set manually. If it's not set, then it uses the
  2nd and 98th percentiles.
+ Added yellow circle representing the wafer as if the flat did not exist.
+ Created wm_constants.py to contain various default values such as colors.
+ Some other changes that I can't remember and foolishly didn't write
  down.


## 1.0.0 / 2014-12-05
+ Official release.
+ The Legend should now work as intended.


## 0.6.0 / 2014-12-04
+ Closed issues #1, 2, 3, 4, and 6 in the tracker.
+ Updated gen_fake_data to use better algorithm and actually output
  correct data.
+ Updated wm_core.WaferMapPanel so that the status bar text displays
  the correct grid values. Verified working with all sorts of
  grid_center values.
+ **Last Update before release, yay!** All that's left is to get the
  legend working.


## 0.5.0 / 2014-12-02
+ renamed wafer_map.py to wm_core.py.
+ Finally figured out the imports for running in development from my
  own dev directory vs running in "production" from the site-packages
  directory.


## 0.4.0 / 2014-12-02
+ Massive change to package hierarchy - separated app, frame, info, and fake
  data into individual modules.


## 0.3.0 / 2014-12-01
+ Added kb shortcuts and menu items for display toggle
  of wafer outline and crosshairs.
+ Added placeholder for legend and kb shortcut for display toggle.
+ Added option for plotting discrete data.


## 0.2.0 / 2014-11-26
+ Made it so a wafer map can be plotted with a single
  command.
+ Updated example.py to demo single-command usage.


## 0.1.0 / 2014-11-25
+ First working code. Added example file.


## 0.0.1 / 2014-11-25
+ Project Creation
