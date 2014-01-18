# -*- coding: utf-8 -*-

import drape

import frame
import app


def Index(request):
    return frame.default_frame(
        request,
        {
            'title': u'首页',
            'testdrape_version': app.version,
            'drape_version': drape.version
        }
    )
