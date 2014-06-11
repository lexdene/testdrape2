# -*- coding: utf-8 -*-
'validate code image and validate'

import io
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

from drape import config
from drape.util import md5sum

# 字符
# 小写字母，去除可能干扰的i，l，o，z
_LETTER_CASES = "abcdefghjkmnpqrstuvwxy"
# 大写字母
_UPPER_CASES = _LETTER_CASES.upper()
# 数字
_NUMBERS = ''.join((str(i) for i in range(3, 10)))
# 全部可用字符
CHARS_COLLECTION = ''.join((_LETTER_CASES, _UPPER_CASES, _NUMBERS))

# session key
SESSION_KEY = 'validate_code_session_key'

# 图片参数
WIDTH = 120
HEIGHT = 30
# 图片保存格式
IMAGE_TYPE = 'PNG'
# 图片模式
IMAGE_MODE = 'RGB'
# 背景色
BG_COLOR = (255, 255, 255)
# 前景色
FG_COLOR = (0, 0, 255)
# 字体文件路径
FONT_FILE = config.FONT_FILE_PATH  # pylint: disable=no-member
# 字体大小
FONT_SIZE = 18
# 是否画干扰线
DRAW_LINES = True
# 干扰线的条数范围
LINE_NUM_RANGE = (1, 3)
# 是否画干扰点
DRAW_POINTS = True
# 干扰点出现的概率, 大小范围[0, 100]
POINT_CHANCE = 1


def _draw_lines(draw):
    ''' 画干扰线 '''
    # pylint: disable=star-args
    for _ in range(random.randint(*LINE_NUM_RANGE)):
        draw.line(
            [
                (
                    random.randint(0, WIDTH),
                    random.randint(0, HEIGHT),
                ),
                (
                    random.randint(0, WIDTH),
                    random.randint(0, HEIGHT),
                )
            ],
            fill=(0, 0, 0)
        )


def _draw_points(draw):
    ''' 画干扰点 '''
    assert 0 <= POINT_CHANCE <= 100

    for i in range(WIDTH):
        for j in range(HEIGHT):
            tmp = random.randint(0, 100)
            if tmp < POINT_CHANCE:
                draw.point(
                    (i, j),
                    fill=(0, 0, 0)
                )


def _draw_text(draw, text):
    ''' 画文本 '''
    # 混入空格
    text = ' '.join(list(text))

    # font
    font = ImageFont.truetype(FONT_FILE, FONT_SIZE)
    font_width, font_height = font.getsize(text)

    # draw
    draw.text(
        (
            (WIDTH - font_width) / 3,
            (HEIGHT - font_height) / 3
        ),
        text,
        font=font,
        fill=FG_COLOR
    )


def _create_image(code):
    'create validate image by code'
    # 创建图形
    img = Image.new(IMAGE_MODE, (WIDTH, HEIGHT), BG_COLOR)
    # 创建画笔
    draw = ImageDraw.Draw(img)

    # 干扰线
    if DRAW_LINES:
        _draw_lines(draw)

    # 干扰点
    if DRAW_POINTS:
        _draw_points(draw)

    # 画文字
    _draw_text(draw, code)

    # 图形扭曲
    img = img.transform(
        (WIDTH, HEIGHT),
        Image.PERSPECTIVE,
        [
            1 - random.randint(1, 2) * 0.01,
            0,
            0,
            0,
            1 - random.randint(1, 10) * 0.01,
            random.randint(1, 2) * 0.002,
            0.001,
            random.randint(1, 2) * 0.002
        ]
    )
    # 滤镜, 边界加强
    img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)

    return img


def create_image_body(request):
    'create validate image response body'
    code = ''.join(random.sample(
        CHARS_COLLECTION,
        4
    ))

    session = request.session
    session.set(
        SESSION_KEY,
        md5sum(code.lower())
    )

    img = _create_image(code)
    output = io.BytesIO()
    img.save(output, format='PNG')
    return output.getvalue()


def validate(request, code):
    'validate by code'
    session = request.session
    hashed_code = session.get(SESSION_KEY)
    session.remove(SESSION_KEY)

    return md5sum(code.lower()) == hashed_code
