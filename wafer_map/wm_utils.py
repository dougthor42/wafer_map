# -*- coding: utf-8 -*-
# pylint: disable=C0103
#         C0103 = invalid variable name
"""
@name:          new_program.py
@vers:          0.1.0
@author:        dthor
@created:       Thu Dec 04 16:12:07 2014
@descr:         A new file

Usage:
    new_program.py

Options:
    -h --help           # Show this screen.
    --version           # Show version.
"""

from __future__ import print_function, division#, absolute_import
#from __future__ import unicode_literals
import numpy as np
from colour import Color


class Gradient(object):
    """
    Base class for all gradients.

    Currently does nothing.
    """
    pass


class LinearGradient(Gradient):
    """
    Linear gradient between two colors.

    Parameters:
    -----------
    initial_color :
        The starting color for the linear gradient.

    dest_color :
        sdfsd

    Attributes:
    -----------
    self.initial_color :
        asad

    self.dest_color :
        asdads

    Methods:
    --------
    get_color(self, value) :
        Returns a color that is ``value`` between self.initial_color and
        self.final_color
    """
    def __init__(self, initial_color, dest_color):
        self.initial_color = initial_color
        self.dest_color = dest_color

    def get_color(self, value):
        """ Gets a color along the gradient. Value = 0 to 1 inclusive"""
        return linear_gradient(self.initial_color, self.dest_color, value)


class PolylinearGradient(Gradient):
    """
    Polylinear Gradient between ``n`` colors.

    Acts as a LinearGradient if ``n == 2``.

    Parameters:
    -----------
    colors : iterable
        A list or tuple of RGB or RGBa tuples (or wx.Colour objects). Each
        color in this list is a vertex of the polylinear gradient.

    Attributes:
    -----------
    self.colors : iterable
        The list of colors (or wx.Colour objects) which are the verticies
        of the poly gradient.

    self.initial_color : tuple or wx.Colour object
        The starting color of the gradient.

    self.dest_color : tuple or wx.Colour object
        The final color of the gradient.

    Methods:
    --------
    get_color(self, value):
        Returns a color that is ``value`` along the gradient.
    """
    def __init__(self, *colors):
        self.colors = colors
        self.initial_color = self.colors[0]
        self.dest_color = self.colors[-1]

    def get_color(self, value):
        """ Gets a color value """
        return polylinear_gradient(self.colors, value)


class BeizerGradient(Gradient):
    """
    Beizer curve gradient between 3 colors.

    Not implemented.
    """
    def __init__(self, initial_color, arc_color, dest_color):
        self.initial_color = initial_color
        self.arc_color = arc_color
        self.dest_color = dest_color

    def get_color(self, value):
        """ Gets a color """
        pass


def linear_gradient(initial_color, dest_color, value):
    """
    Find the color that is ``value`` between initial_color and dest_color.

    Parameters:
    -----------
    initial_color : tuple
        A 3- or 4-tuple of RGB or RGBa values representing the starting
        color for the gradient. Each color channel should be
        in the range 0-255 inclusive.

    dest_color : tuple
        A 3- or 4-tuple of RGB or RGBa values representing the ending
        color for the gradient. Each color channel should be
        in the range 0-255.

    value : float
        A floating point number from 0 to 1 inclusive that determines how
        far along the color gradient the returned color should be. A value
        of ``0`` returns ``initial_color`` while a value of ``1`` returns
        ``dest_color``.

    Returns:
    --------
    (r, g, b) : tuple
        A 3-tuple representing the color that is ``value * 100`` percent
        along the gradient. Each color channel is 0-255 inclusive.

    Implementation Details:
    -----------------------
    All of this package works in the RGB colorspace. However, as is seen in
    https://www.youtube.com/watch?v=LKnqECcg6Gw and
    https://www.youtube.com/watch?v=sPiWg5jSoZI, the RGB color space does
    not blend correctly with standard averaging, which is what I do here.

    I haven't found any source for this, but experimentation has shown that
    the HSL colorspace *does* blend correctly with linear averaging. So
    I use the ``colour`` module to convert RGB to HSL. After converting, I
    take the linear average of my two colors (via ``rescale``) and then
    convert back to RGB.

    Examples:
    ---------
    Halfway between Red and Green is Yellow. This really should return
    (255, 255, 0), but it's close enough for now.

    >>> linear_gradient((255, 0, 0), (0, 255, 0), 0.5)
    (254, 255, 0)

    Red and Blue mix to make green. Standard Rainbow

    >>> linear_gradient((255, 0, 0), (0, 0, 255), 0.5)
    (0, 255, 0)

    75% of the from Red to Green is Orange.

    >>> linear_gradient((255, 0, 0), (0, 255, 0), 0.75)
    (127, 255, 0)
    """
    if value <= 0:
        return initial_color
    elif value >= 1:
        return dest_color

    # Old way, linear averaging.
#    r1, g1, b1 = (_c for _c in initial_color)
#    r2, g2, b2 = (_c for _c in dest_color)
#    r = int(rescale(value, (0, 1), (r1, r2)))
#    g = int(rescale(value, (0, 1), (g1, g2)))
#    b = int(rescale(value, (0, 1), (b1, b2)))

    # Using the ``colour`` package
    # Convert from 0-255 to 0-1 and instance the Color class
    c1 = Color(rgb=(_c / 255 for _c in initial_color))
    c2 = Color(rgb=(_c / 255 for _c in dest_color))

    # extract the HSL values
    h1, s1, l1 = c1.hsl
    h2, s2, l2 = c2.hsl

    # Perform the linear interpolation
    h = rescale(value, (0, 1), (h1, h2))
    s = rescale(value, (0, 1), (s1, s2))
    l = rescale(value, (0, 1), (l1, l2))

    # Convert back to 0-255 for wxPython
    r, g, b = (int(_c * 255) for _c in Color(hsl=(h, s, l)).rgb)

    return (r, g, b)


def polylinear_gradient(colors, value):
    """
    colors is a list or tuple of length 2 or more. If length 2, then it's
    the same as LinearGradient
    Value is the 0-1 value between colors[0] and colors[-1].
    Assumes uniform spacing between all colors.
    """
    n = len(colors)
    if n == 2:
        return linear_gradient(colors[0], colors[1], value)

    if value >= 1:
        return colors[-1]
    elif value <= 0:
        return colors[0]

    # divide up our range into n - 1 segments, where n is the number of colors
    l = 1 / (n - 1)     # float division

    # figure out which segment we're in - determines start and end colors
    m = int(value // l)      # Note floor division

    low = m * l
    high = (m + 1) * l

    # calculate where our value lies within that particular gradient
    v2 = rescale(value, (low, high), (0, 1))

    return linear_gradient(colors[m], colors[m + 1], v2)


def beizer_gradient(initial_color, arc_color, dest_color, value):
    """
    Calculates the color value along a Beizer Cuve who's control colors are
    defined by initial_color, arc_color, and final_color.
    """
    pass


def _GradientFillLinear(rect,
                        intial_color,
                        dest_color,
                        direction,
                        ):
    """
    Reimplements the ``wxDCImpl::DoGradientFillLinear`` algorithm found in
    wxWidgets-3.0.2\src\common\dcbase.cpp, line 862.

    wxWidgets uses the native MS Windows (msw) function if it can:
        wxMSIMG32DLL.GetSymbol(wxT("GradientFill")

    See function ``wxMSWDCImpl::DoGradientFillLinear`` in
    wxWidgets-3.0.2\src\msw\dc.cpp, line 2870

    Allows user to put in a value from 0 (intial_color) to 1 (dest_color).

    What will this function return? I do not know yet.

    There's not really a struct for a "continuous gradient"...

    I think that perhaps this function will just calculate the color for
    a given 0-1 value between initial_color and dest_color on the fly.

    I'm an idiot! This is just linear algebra, I can solve this!
    """
    pass
"""
    void wxDCImpl::DoGradientFillLinear(const wxRect& rect,
                                        const wxColour& initialColour,
                                        const wxColour& destColour,
                                        wxDirection nDirection)
    {
        // save old pen
        wxPen oldPen = m_pen;
        wxBrush oldBrush = m_brush;

        wxUint8 nR1 = initialColour.Red();
        wxUint8 nG1 = initialColour.Green();
        wxUint8 nB1 = initialColour.Blue();
        wxUint8 nR2 = destColour.Red();
        wxUint8 nG2 = destColour.Green();
        wxUint8 nB2 = destColour.Blue();
        wxUint8 nR, nG, nB;

        if ( nDirection == wxEAST || nDirection == wxWEST )
        {
            wxInt32 x = rect.GetWidth();
            wxInt32 w = x;              // width of area to shade
            wxInt32 xDelta = w/256;     // height of one shade bend
            if (xDelta < 1)
                xDelta = 1;   # max of 255 points - fractional colors are not defined.

            while (x >= xDelta)
            {
                x -= xDelta;
                if (nR1 > nR2)
                    nR = nR1 - (nR1-nR2)*(w-x)/w;
                else
                    nR = nR1 + (nR2-nR1)*(w-x)/w;

                if (nG1 > nG2)
                    nG = nG1 - (nG1-nG2)*(w-x)/w;
                else
                    nG = nG1 + (nG2-nG1)*(w-x)/w;

                if (nB1 > nB2)
                    nB = nB1 - (nB1-nB2)*(w-x)/w;
                else
                    nB = nB1 + (nB2-nB1)*(w-x)/w;

                wxColour colour(nR,nG,nB);
                SetPen(wxPen(colour, 1, wxPENSTYLE_SOLID));
                SetBrush(wxBrush(colour));
                if(nDirection == wxEAST)
                    DoDrawRectangle(rect.GetRight()-x-xDelta+1, rect.GetTop(),
                            xDelta, rect.GetHeight());
                else //nDirection == wxWEST
                    DoDrawRectangle(rect.GetLeft()+x, rect.GetTop(),
                            xDelta, rect.GetHeight());
            }
        }
        else  // nDirection == wxNORTH || nDirection == wxSOUTH
        {
            wxInt32 y = rect.GetHeight();
            wxInt32 w = y;              // height of area to shade
            wxInt32 yDelta = w/255;     // height of one shade bend
            if (yDelta < 1)
                yDelta = 1;  # max of 255 points - fractional colors are not defined.

            while (y > 0)
            {
                y -= yDelta;
                if (nR1 > nR2)
                    nR = nR1 - (nR1-nR2)*(w-y)/w;
                else
                    nR = nR1 + (nR2-nR1)*(w-y)/w;

                if (nG1 > nG2)
                    nG = nG1 - (nG1-nG2)*(w-y)/w;
                else
                    nG = nG1 + (nG2-nG1)*(w-y)/w;

                if (nB1 > nB2)
                    nB = nB1 - (nB1-nB2)*(w-y)/w;
                else
                    nB = nB1 + (nB2-nB1)*(w-y)/w;

                wxColour colour(nR,nG,nB);
                SetPen(wxPen(colour, 1, wxPENSTYLE_SOLID));
                SetBrush(wxBrush(colour));
                if(nDirection == wxNORTH)
                    DoDrawRectangle(rect.GetLeft(), rect.GetTop()+y,
                            rect.GetWidth(), yDelta);
                else //nDirection == wxSOUTH
                    DoDrawRectangle(rect.GetLeft(), rect.GetBottom()-y-yDelta+1,
                            rect.GetWidth(), yDelta);
            }
        }

        SetPen(oldPen);
        SetBrush(oldBrush);
}"""


def frange(start, stop, step):
    """ Generator that creates an arbitrary-stepsize range. """
    r = start
    while r < stop:
        yield r
        r += step


def coord_to_grid(coord, die_size, grid_center):
    """
    Converts a panel coordinate to a grid value.

    Parameters:
    -----------
    coord : tuple
        A 2-tuple of (x, y) floating point values for the panel coordinate

    die_size : tuple
        A 2-tuple of (x, y) floating point values for the die size

    grid_center : tuple
        A 2-tuple of (grid_x, grid_y) values that represents the origin of
        the wafer in grid coordinates.

    Returns:
    --------
    (grid_x, grid_y) : tuple
        The grid coordinates. Also known as (column, row).
    """
    # TODO: seems have a error with negative 0 grid values.
    grid_x = int(grid_center[0] + 0.5 + (coord[0] / die_size[0]))
    grid_y = int(grid_center[1] + 0.5 - (coord[1] / die_size[1]))
    return (grid_x, grid_y)


def grid_to_rect_coord(grid, die_size, grid_center):
    """
    Converts a die's grid value to the origin point of the rectangle to draw.

    Adjusts for the fact that the grid falls on the center of a die by
    subtracting die_size/2 from the coordinate.

    Adjusts for the fact that Grid +y is down while panel +y is up by
    taking ``grid_center - grid`` rather than ``grid - grid_center`` as is
    done in the X case.
    """
    _x = die_size[0] * (grid[0] - grid_center[0] - 0.5)
    _y = die_size[1] * (grid_center[1] - grid[1] - 0.5)
    return (_x, _y)


def nanpercentile(a, percentile):
    """
    Performs a numpy.percentile(a, percentile) calculation while
    ignoring NaN values.

    Only works on a 1D array.
    """
    if type(a) != np.ndarray:
        a = np.array(a)
    return np.percentile(a[np.logical_not(np.isnan(a))], percentile)


def max_dist_sqrd(center, size):
    """
    Calculates the squared distance from the orgin (0, 0) to the
    farthest corner of a rectangle, where the center of the rectangle's
    coordinates are known.

    Does not take the square of the distance for the sake of speed.

    If the rectangle's center is in the Q1, then the upper-right corner is
    the farthest away from the origin. If in Q2, then the upper-left corner
    is farthest away. Etc.

    Returns the magnitude of the largest distance.

    Used primarily for calculating if a die has any part outside of wafer's
    edge exclusion.

    Parameters:
    -----------
    center : tuple of length 2, numerics
        (x, y) tuple defining the rectangle's center coordinates

    size : tuple of length 2
        (x, y) tuple that defines the size of the rectangle.

    Returns:
    --------
    dist : numeric
        The distance from the origin (0, 0) to the farthest corner of the
        rectangle.

    See Also:
    ---------
    max_dist :
        Calculates the distance from the orgin (0, 0) to the
        farthest corner of a rectangle.
    """
    half_x = size[0]/2.
    half_y = size[1]/2.
    if center[0] < 0:
        half_x = -half_x
    if center[1] < 0:
        half_y = -half_y
    dist = (center[0] + half_x)**2 + (center[1] + half_y)**2
    return dist


def rescale(x, orig_scale, new_scale=(0, 1)):
    """
    Rescales x to run over a new range.

    Rescales x (which was part of scale original_min to original_max)
    to run over a range new_min to new_max such
    that the value x maintains position on the new scale new_min to new_max.
    If x is outside of xRange, then y will be outside of yRange.

    Default new scale range is 0 to 1 inclusive.

    Parameters:
    -----------
    x : numeric
        The value to rescale.

    orig_scale : sequence of numerics, length 2
        The (min, max) value that ``x`` typically ranges over.

    new_scale : sequence of numerics, length 2, optional
        The new (min, max) value that the rescaled ``x`` should reference

    Returns:
    --------
    result : float
        The rescaled ``x`` value

    Examples:
    ---------
    >>> rescale(5, (10, 20), (0, 1))
    -0.5
    >>> rescale(27, (0, 200), (0, 5))
    0.675
    >>> rescale(1.5, (0, 1), (0, 10))
    15.0
    """
    original_min, original_max = orig_scale
    new_min, new_max = new_scale

    part_a = x * (new_max - new_min)
    part_b = original_min * new_max - original_max * new_min
    denominator = original_max - original_min
    try:
        result = (part_a - part_b)/denominator
    except ZeroDivisionError:
        result = 0
    return float(result)


def rescale_clip(x, orig_scale, new_scale=(0, 1)):
    """
    Same as rescale, but also clips the new data. Any result that is
    below new_min or above new_max is listed as new_min or
    new_max, respectively

    Example:
    rescale_clip(5, (10, 20), (0, 1)) = 0
    rescale_clip(15, (10, 20), (0, 1)) = 0.5
    rescale_clip(25, (10, 20), (0, 1)) = 1
    """
    original_min, original_max = orig_scale
    new_min, new_max = new_scale

    result = rescale(x, (original_min, original_max), (new_min, new_max))
    if result > new_max:
        return new_max
    elif result < new_min:
        return new_min
    else:
        return result

if __name__ == "__main__":
    print("0 and 1")
    print(polylinear_gradient([(0, 0, 0), (255, 0, 0), (0, 255, 0)], 0))
    print(polylinear_gradient([(0, 0, 0), (255, 0, 0), (0, 255, 0)], 1))

    print("\n0.5:")
    print(polylinear_gradient([(0, 0, 0), (255, 0, 0), (0, 255, 0)], 0.5))

    print("\n0.25")
    print(polylinear_gradient([(0, 0, 0), (255, 0, 0), (0, 255, 0)], 0.25))
    print("\n0.75")
    print(polylinear_gradient([(0, 0, 0), (255, 0, 0), (0, 255, 0)], 0.75))

    print("\n4 colors")
    print(polylinear_gradient([(0, 0, 0),
                               (255, 0, 0),
                               (0, 255, 0),
                               (0, 0, 255),
                               ],
                              0.5))

    print(linear_gradient((0, 0, 0), (255, 255, 255), 1.5))
