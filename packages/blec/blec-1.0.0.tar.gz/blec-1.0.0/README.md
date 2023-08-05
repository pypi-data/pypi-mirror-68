blec: alpha blending calculator
===============================
This is a tool to calculate a resulting color of the alpha blending process.
A gamma correction is enabled and the default gamma value is 2.2.

Usage
-----
Just enumerate colors from the bottom to the top

    $ blec 555555dd ffffffcc 00000011
    #e4e4e4f8

You may use ARGB instead of RGBA

    $ blec --argb dd555555 ccffffff 11000000
    #f8e4e4e4

You may change gamma value (set it to 1 to disable)

    $ blec --gamma 3 555555dd ffffffcc 00000011
    #eaeaeaf8

Installation
------------

    pip3 install blec

