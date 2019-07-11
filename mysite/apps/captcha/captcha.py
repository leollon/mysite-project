import os
import uuid
import random

from pathlib import Path

from django.conf import settings
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ALPHA_NUM = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
CAPATCHA_BASE = getattr(settings, "CAPTCHA_DIR")


class Captcha:
    def __init__(
        self,
        img_path=CAPATCHA_BASE,
        suffix="png",
        size=(100, 35),
        chars=ALPHA_NUM,
        mode="RGB",
        bg_color=(128, 128, 128),
        fg_color=(141, 0, 255),
        xy=None,
        font_size=25,
        font_type=None,
        length=(4, 6),
        draw_lines=True,
        num_lines=(4, 6),
        draw_points=True,
        point_frequency=5,
        draw_transform=False,
    ):
        """
        :type img_path:             str, 图片存储目录
        :type suffix:               str, 图片后缀
        :type size:                 tuple, 图片宽高
        :type chars:                str, 验证码内容
        :type mode:                 str, 图片颜色模式
        :type bg_color:             tuple, 图片背景颜色
        :type fg_color:             tuple, 字体，点，线的颜色
        :type xy:                   tuple, 验证码偏移位置（左右和上下）
        :type font_size:            int, 字体大小
        :type font_type:            str, 字体类型
        :type length:               tuple, 验证码字符长度范围
        :type draw_lines:           bool, 是否在图片中划线
        :type num_lines:            tuple, 划线的数量
        :type draw_points:          bool, 是否在图片中画点
        :type point_frequency:      int, 点出现的频率
        :type draw_transform:       bool, 是否将验证码字体进行变形
        """
        self._img_path = img_path
        self._file_name = uuid.uuid1()
        self._suffix = suffix
        self._width = size[0]
        self._height = size[1]
        self._img = Image.new(mode, size, bg_color)
        self._chars = chars
        self._fg_color = fg_color
        self._xy = xy
        self._font_size = font_size
        self._font_type = font_type
        self._length = length
        self._draw_lines = draw_lines
        self._num_lines = num_lines
        self._draw_points = draw_points
        self._point_frequency = point_frequency
        self._draw_transform = draw_transform
        self._img = Image.new(mode, size, bg_color)

    @property
    def _draw(self):
        return ImageDraw.Draw(self._img)

    @_draw.setter
    def set_draw(self):
        raise AttributeError("Can not set draw")

    def get_chars(self):
        """
        :rtype: list[str]
        """
        return random.sample(self._chars, random.randint(*self._length))

    def create_lines(self):
        """绘制干扰线
        """
        for _ in range(random.randint(*self._num_lines)):
            begin = (
                random.randint(0, self._width),
                random.randint(0, self._height),
            )
            end = (
                random.randint(0, self._width),
                random.randint(0, self._height),
            )
            self._draw.line([begin, end], fill=self._fg_color)  # 划线，并填充颜色

    def create_points(self):
        """绘制干扰点
        """
        frequency = min(100, max(0, int(self._point_frequency)))
        for w in range(self._width):
            for h in range(self._height):
                tmp = random.randint(5, 100)
                if tmp > 100 - frequency:
                    self._draw.point((w, h), fill=self._fg_color)  # 画点，并填充颜色

    def create_text(self):
        """绘制验证码字符
        """
        text = "".join(self.get_chars())
        if self._font_type is None:
            curr_path = Path(__file__).absolute().parent
            self._font_type = (
                (Path(curr_path) / "fonts" / "SourceCodeProRegular.ttf")
                .absolute()
                .as_posix()
            )
        font = ImageFont.truetype(self._font_type, self._font_size)
        if self._xy is None:
            font_width, font_height = font.getsize(text)
            self._xy = (
                (self._width - font_width) / 3,
                (self._height - font_height) / 3,
            )
        self._draw.text(
            self._xy, text, font=font, fill=self._fg_color
        )  # 写入文本，并填充颜色

        return text

    def transform(self):
        """对图片进行转换
        """
        data = [
            1 - float(random.randint(1, 2)) / 100,
            0,
            0,
            0,
            1 - float(random.randint(1, 10)) / 100,
            float(random.randint(1, 2)) / 500,
            0.001,
            float(random.randint(1, 2)) / 500,
        ]
        return self._img.transform(
            size=(self._width, self._height),
            method=Image.PERSPECTIVE,
            data=data,
        )

    def generate_captcha(self):

        if self._draw_lines:
            self.create_lines()

        if self._draw_points:
            self.create_points()

        text = self.create_text()  # 将会被放到缓存中

        if self._draw_transform:
            self._img = self.transform()
        self._img = self._img.filter(ImageFilter.EDGE_ENHANCE_MORE)  # 边界增强
        self._file_name = "%s.%s" % (
            str(self._file_name).replace("-", ""),
            self._suffix,
        )
        captcha_dir = Path(CAPATCHA_BASE)
        if not captcha_dir.exists():
            captcha_dir.mkdir(parents=True)
        file_path = captcha_dir / self._file_name
        if file_path.exists():
            file_path.unlink()
        try:
            self._img.save(file_path.as_posix())
            captcha_img_path = "/" + "/".join(
                file_path.as_posix().rsplit("/", 3)[-3:]
            )
            result_status = 0
            message = "Success"
        except PermissionError:
            text, captcha_img_path, result_status, message = (
                None,
                None,
                1,
                "No permission.",
            )
        return (text, captcha_img_path, result_status, message)

