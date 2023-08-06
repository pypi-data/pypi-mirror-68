================
Mundi Healthcare
================

The mundi-healthcare plugin provides statistics about healthcare capacity and basic indicators
for many regions in the world. Currently, this preview only provides statistics for Brazil.


Usage
=====

Install it using ``pip install mundi-healthcare`` or your method of choice. Now, you can just import
it and load the desired information. Mundi exposes collections of entries as dataframes,
which can be manipulated as usual

>>> import mundi_healthcare, mundi
>>> df = mundi.countries()
>>> df.mundi["hospital_capacity"]
...
