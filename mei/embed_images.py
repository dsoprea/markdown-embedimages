import base64
import os
import imghdr

import mistune

try:
    unicode
except NameError:
    _is_python3 = True
else:
    _is_python3 = False

_image_mime_map = {
    'gif': 'image/gif',
    'pbm': 'image/x-portable-bitmap',
    'pgm': 'image/x-portable-graymap',
    'ppm': 'image/x-portable-pixmap',
    'tiff': 'image/tiff',
    'xbm': 'image/x-xbitmap',
    'jpeg': 'image/jpeg',
    'bmp': 'image/x-ms-bmp',
    'png': 'image/png',
}


class _ImageEmbedder(object):
    def __init__(self):
        if _is_python3 is True:
            self.__string_normalize = lambda s: s.decode('utf-8')
        else:
            self.__string_normalize = lambda s: s

    def _get_http3(self):
        import urllib.request

        def read_http(url):
            r = urllib.request.urlopen(url)
            content = r.read()
            content_type = r.headers['Content-Type']

            return content, content_type

        return read_http

    def _get_http2(self):
        import urllib2

        def read_http(url):
            r = urllib2.urlopen(url)
            content = r.read()
            content_type = r.headers['Content-Type']

            return content, content_type

        return read_http

    def _http(self, url):
        try:
            requestor = self._http_requestor
        except AttributeError:
            requestor = None

        if requestor is None:
            if _is_python3 is True:
                self._http_requestor = self._get_http3()
            else:
                self._http_requestor = self._get_http2()

            requestor = self._http_requestor

        return requestor(url)

    def _get_base64_with_image_url(self, url):
        raw_image, content_type = self._http(url)

        encoded_image = base64.b64encode(raw_image)
        encoded_image = self.__string_normalize(encoded_image)

        return encoded_image, content_type

    def _get_base64_with_image_filepath(self, filepath):
        with open(filepath, 'rb') as f:
            raw_image = f.read()

        image_type = imghdr.what('', h=raw_image)
        mimetype = _image_mime_map[image_type]

        encoded_image = base64.b64encode(raw_image)
        encoded_image = self.__string_normalize(encoded_image)

        return encoded_image, mimetype

    def get_embedded_image(self, url, attributes={}, use_xhtml=False, allow_local=False):
        if use_xhtml:
            tag_tail = ' />'
        else:
            tag_tail = '>'

        if allow_local is True and os.path.exists(url) is True:
            encoded_image, content_type = self._get_base64_with_image_filepath(url)
        else:
            encoded_image, content_type = self._get_base64_with_image_url(url)

        suffix = ''
        for key, value in attributes.items():
            suffix += ' {key}="{value}"'.format(key=key, value=value)

        template = "<img src=\"data:{content_type};base64,{payload}\"{suffix}{tag_tail}"
        embedded = \
            template.format(
                content_type=content_type,
                payload=encoded_image,
                suffix=suffix,
                tag_tail=tag_tail)

        return embedded


class EmbedImagesRenderer(mistune.Renderer):
    def __init__(self, ie=None, *args, **kwargs):
        if ie is not None:
            self.__ie = ie
        else:
            self.__ie = _ImageEmbedder()

        super(EmbedImagesRenderer, self).__init__(*args, **kwargs)

    def image(self, src, title, text):
        """Rendering a image with title and text.

        :param src: source link of the image.
        :param title: title text of the image.
        :param text: alt text of the image.
        """

        allow_local_embed = self.options.get('embed_local_images', False)
        use_xhtml = self.options.get('use_xhtml')

        if title:
            title = mistune.escape(title, quote=True)

        attributes = {
            'alt': text,
        }

        if title:
            attributes['title'] = title

        html = self.__ie.get_embedded_image(
                src,
                use_xhtml=use_xhtml,
                attributes=attributes,
                allow_local=allow_local_embed)

        return html

def markdown(text, escape=True, embed_local_images=False, renderer_options={}, **kwargs):
    """Render markdown formatted text to html.

    :param text: markdown formatted text content.
    :param escape: if set to False, all html tags will not be escaped.
    :param use_xhtml: output with xhtml tags.
    :param hard_wrap: if set to True, it will use the GFM line breaks feature.
    :param parse_block_html: parse text only in block level html.
    :param parse_inline_html: parse text only in inline level html.
    """

    renderer_options['embed_local_images'] = embed_local_images

    renderer = EmbedImagesRenderer(**renderer_options)
    return mistune.Markdown(escape=escape, renderer=renderer, **kwargs)(text)
