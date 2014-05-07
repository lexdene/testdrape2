# -*- coding: utf-8 -*-

import drape

from . import frame
import app


def index(request):
    return frame.default_frame(
        request,
        {
            'title': '首页',
            'testdrape_version': app.version,
            'drape_version': drape.version
        },
        'index/Index'
    )
