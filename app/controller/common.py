# -*- coding: utf-8 -*-

from drape.response import Response

from app.lib import validate_code


def validate_code_image(request):
    return Response(
        body=validate_code.create_image_body(request),
        headers={
            'Content-Type': 'image/png'
        }
    )
