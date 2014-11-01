#!/usr/bin/env python

import pytest
from utils.context import Context


@pytest.fixture
def context(request):
    request.cls.context = Context()
