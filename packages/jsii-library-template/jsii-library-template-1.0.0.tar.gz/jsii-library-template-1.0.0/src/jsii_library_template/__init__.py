"""
# jsii-library-template

Template for a jsii library project.
"""
import abc
import builtins
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from ._jsii import *


class Hello(metaclass=jsii.JSIIMeta, jsii_type="jsii-library-template.Hello"):
    """Hello class.

    stability
    :stability: experimental
    """
    def __init__(self) -> None:
        jsii.create(Hello, self, [])

    @jsii.member(jsii_name="world")
    def world(self) -> str:
        """Hey there!

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "world", [])


__all__ = [
    "Hello",
]

publication.publish()
