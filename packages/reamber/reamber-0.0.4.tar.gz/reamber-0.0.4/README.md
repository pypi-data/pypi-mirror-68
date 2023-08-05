# Reamber Base (Py)

This is a simple package to handle VSRG file, useful if you'd want to manipulate data
such as offset, column, bpm, etc.

This doesn't provide complex algorithms, only the base dataclasses and helpful basic
algorithms

## Important

### Timed Objects

All Timed Objects' Attributes use base unit time of **milliseconds** unless
otherwise explicitly stated in their name.

Shorthand Conversions can be found in reamber.base.RAConst

### Bpm

Beats per Minute, no other units unless explicitly stated

### Map Pack / Map Set / Map

A Map Pack contains Map Sets

A Map Set contains Maps / Difficulties