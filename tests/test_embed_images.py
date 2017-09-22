import os
import sys
import base64
import unittest

import mistune

import mei.embed_images


class TestEmbedImages(unittest.TestCase):
    def test_get_http3(self):
        ie = mei.embed_images._ImageEmbedder()

        if sys.version_info[0] == 3:
            ie._get_http3()
        else:
            try:
                ie._get_http3()
            except ImportError:
                pass
            else:
                raise Exception("Expected an exception for Python3 support under Python2.")

    def test_get_http2(self):
        ie = mei.embed_images._ImageEmbedder()

        if sys.version_info[0] == 2:
            ie._get_http2()
        else:
            try:
                ie._get_http2()
            except ImportError:
                pass
            else:
                raise Exception("Expected an exception for Python2 support.")

    def test_http(self):
        ie = mei.embed_images._ImageEmbedder()

        def fake_get_http2():
            def fake_http(url):
                return 'faker2', 'content_type'

            return fake_http

        ie._get_http2 = fake_get_http2

        def fake_get_http3():
            def fake_http(url):
                return 'faker3', 'content_type'

            return fake_http

        ie._get_http3 = fake_get_http3

        content, content_type = ie._http('http://aa.bb')

        if sys.version_info[0] == 2:
            self.assertEquals(content, 'faker2')
        elif sys.version_info[0] == 3:
            self.assertEquals(content, 'faker3')

        self.assertEquals(content_type, 'content_type')

    def test_http__instance_cached(self):
        ie = mei.embed_images._ImageEmbedder()
        ie._http_requestor = lambda x: ('test_data', 'content-type')

        content, content_type = ie._http('http://host/image')

        self.assertEquals(content, 'test_data')
        self.assertEquals(content_type, 'content-type')

    def test_embed_images_url(self):
        class TestImageEmbedder(mei.embed_images._ImageEmbedder):
            def _get_base64_with_image_url(self, url):
                return 'png_data', 'image/png'

        tie = TestImageEmbedder()

        renderer = mei.embed_images.EmbedImagesRenderer(ie=tie)
        m = mistune.Markdown(renderer=renderer)

        markdown = """\
![alt text](https://some.domain/some_image.png)"""

        actual = m.render(markdown)

        expected = '<p><img src="data:image/png;base64,png_data" alt="alt text"></p>\n'

        self.assertEquals(actual, expected)

    def test_embed_images_local(self):
        renderer = mei.embed_images.EmbedImagesRenderer(embed_local_images=True)

        m = mistune.Markdown(renderer=renderer)

        filepath = os.path.join(os.path.dirname(__file__), 'image.png')
        markdown = "![alt text]({filepath})".format(filepath=filepath)

        actual = m.render(markdown)

        expected = '<p><img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAIAAAACACAMAAAD04JH5AAAAY1BMVEX///8AAADy8vLDw8OGhoYJCQnf398EBAQdHR3s7OwPDw/7+/uioqIkJCQnJye6urrJyckbGxtlZWWwsLBvb29BQUE6Ojrk5OR+fn4WFhYvLy/W1tZqampVVVV4eHiUlJQ1NTVSAT8kAAABJ0lEQVR4nO3XWXKDMBBFUZpBgJjBgDGe9r/K2EkqcRHpL9VUKvds4D0EtKQgAAAAAAAAAAAA+NPC2Zg53Cs9Hw5jnWXV1Jdmj/jbPZFPaX1UrxCNqbw6DYVqfpnJho01G5TLNl8kUWwQ/Xj+9walVn4+uvJFqlWpwC11F5CzzkvI75586XSWYEh8BSRWKXDw5suoMZZDzyf4lGkMxLn2F7CtQgHjHAIfkuY/FJirnV9BOPkLdCq7cu8vMKmcjkrfJBa5auQHxvsf2kilQHD0FbgonQjMyZ2/KC3AYzuyrvxUZyt6KmLXhtgrXhAcDdI+18t/NCg383CJtS9I6/nlZGwvat/ft2KNx8wmie2ma6R7K/kSmrZpWrPb7RQAAAAAAAAAAOBXvAGvzwnuz+x0kQAAAABJRU5ErkJggg==" alt="alt text"></p>\n'

        if actual != expected:
            raise Exception("Local image not embedded properly:\nACTUAL:\n=======\n{}\n\nEXPECTED:\n=========\n{}\n".format(actual, expected))

    def test_get_base64_with_image_filepath(self):
        ie = mei.embed_images._ImageEmbedder()

        filepath = os.path.join(os.path.dirname(__file__), 'image.png')
        content, content_type = ie._get_base64_with_image_filepath(filepath)

        expected = "iVBORw0KGgoAAAANSUhEUgAAAIAAAACACAMAAAD04JH5AAAAY1BMVEX///8AAADy8vLDw8OGhoYJCQnf398EBAQdHR3s7OwPDw/7+/uioqIkJCQnJye6urrJyckbGxtlZWWwsLBvb29BQUE6Ojrk5OR+fn4WFhYvLy/W1tZqampVVVV4eHiUlJQ1NTVSAT8kAAABJ0lEQVR4nO3XWXKDMBBFUZpBgJjBgDGe9r/K2EkqcRHpL9VUKvds4D0EtKQgAAAAAAAAAAAA+NPC2Zg53Cs9Hw5jnWXV1Jdmj/jbPZFPaX1UrxCNqbw6DYVqfpnJho01G5TLNl8kUWwQ/Xj+9walVn4+uvJFqlWpwC11F5CzzkvI75586XSWYEh8BSRWKXDw5suoMZZDzyf4lGkMxLn2F7CtQgHjHAIfkuY/FJirnV9BOPkLdCq7cu8vMKmcjkrfJBa5auQHxvsf2kilQHD0FbgonQjMyZ2/KC3AYzuyrvxUZyt6KmLXhtgrXhAcDdI+18t/NCg383CJtS9I6/nlZGwvat/ft2KNx8wmie2ma6R7K/kSmrZpWrPb7RQAAAAAAAAAAOBXvAGvzwnuz+x0kQAAAABJRU5ErkJggg=="
        self.assertEquals(content, expected)

        self.assertEquals(content_type, 'image/png')

    def test_get_base64_with_image_url(self):
        ie = mei.embed_images._ImageEmbedder()

        ie._http = lambda x: (b'image-content', 'image-type')

        encoded, content_type = ie._get_base64_with_image_url('http://host/image')

        content = base64.b64decode(encoded)

        expected = b'image-content'
        self.assertEquals(content, expected)

        self.assertEquals(content_type, 'image-type')

    def test_get_embedded_image_url(self):
        ie = mei.embed_images._ImageEmbedder()

        ie._http = lambda x: (b'image-content', 'image-type')

        content = ie.get_embedded_image('http://aa.com/image')

        expected = '<img src="data:image-type;base64,aW1hZ2UtY29udGVudA==">'

        self.assertEquals(content, expected)

    def test_get_embedded_image_url__xhtml(self):
        ie = mei.embed_images._ImageEmbedder()

        ie._http = lambda x: (b'image-content', 'image-type')

        content = ie.get_embedded_image('http://aa.com/image', use_xhtml=True)

        expected = '<img src="data:image-type;base64,aW1hZ2UtY29udGVudA==" />'

        self.assertEquals(content, expected)

    def test_get_embedded_image_filepath(self):
        ie = mei.embed_images._ImageEmbedder()

        filepath = os.path.join(os.path.dirname(__file__), 'image.png')
        content = ie.get_embedded_image(filepath, allow_local=True)

        expected = """\
<img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAIAAAACACAMAAAD04JH5AAAAY1BMVEX///8AAADy8vLDw8OGhoYJCQnf398EBAQdHR3s7OwPDw/7+/uioqIkJCQnJye6urrJyckbGxtlZWWwsLBvb29BQUE6Ojrk5OR+fn4WFhYvLy/W1tZqampVVVV4eHiUlJQ1NTVSAT8kAAABJ0lEQVR4nO3XWXKDMBBFUZpBgJjBgDGe9r/K2EkqcRHpL9VUKvds4D0EtKQgAAAAAAAAAAAA+NPC2Zg53Cs9Hw5jnWXV1Jdmj/jbPZFPaX1UrxCNqbw6DYVqfpnJho01G5TLNl8kUWwQ/Xj+9walVn4+uvJFqlWpwC11F5CzzkvI75586XSWYEh8BSRWKXDw5suoMZZDzyf4lGkMxLn2F7CtQgHjHAIfkuY/FJirnV9BOPkLdCq7cu8vMKmcjkrfJBa5auQHxvsf2kilQHD0FbgonQjMyZ2/KC3AYzuyrvxUZyt6KmLXhtgrXhAcDdI+18t/NCg383CJtS9I6/nlZGwvat/ft2KNx8wmie2ma6R7K/kSmrZpWrPb7RQAAAAAAAAAAOBXvAGvzwnuz+x0kQAAAABJRU5ErkJggg==">"""

        self.assertEquals(content, expected)

    def test_get_embedded_image_filepath__xhtml(self):
        ie = mei.embed_images._ImageEmbedder()

        filepath = os.path.join(os.path.dirname(__file__), 'image.png')
        content = ie.get_embedded_image(filepath, allow_local=True, use_xhtml=True)

        expected = """\
<img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAIAAAACACAMAAAD04JH5AAAAY1BMVEX///8AAADy8vLDw8OGhoYJCQnf398EBAQdHR3s7OwPDw/7+/uioqIkJCQnJye6urrJyckbGxtlZWWwsLBvb29BQUE6Ojrk5OR+fn4WFhYvLy/W1tZqampVVVV4eHiUlJQ1NTVSAT8kAAABJ0lEQVR4nO3XWXKDMBBFUZpBgJjBgDGe9r/K2EkqcRHpL9VUKvds4D0EtKQgAAAAAAAAAAAA+NPC2Zg53Cs9Hw5jnWXV1Jdmj/jbPZFPaX1UrxCNqbw6DYVqfpnJho01G5TLNl8kUWwQ/Xj+9walVn4+uvJFqlWpwC11F5CzzkvI75586XSWYEh8BSRWKXDw5suoMZZDzyf4lGkMxLn2F7CtQgHjHAIfkuY/FJirnV9BOPkLdCq7cu8vMKmcjkrfJBa5auQHxvsf2kilQHD0FbgonQjMyZ2/KC3AYzuyrvxUZyt6KmLXhtgrXhAcDdI+18t/NCg383CJtS9I6/nlZGwvat/ft2KNx8wmie2ma6R7K/kSmrZpWrPb7RQAAAAAAAAAAOBXvAGvzwnuz+x0kQAAAABJRU5ErkJggg==" />"""

        self.assertEquals(content, expected)

    def test_markdown(self):
        filepath = os.path.join(os.path.dirname(__file__), 'image.png')
        markdown = "![alt text]({filepath})".format(filepath=filepath)

        actual = mei.embed_images.markdown(markdown, embed_local_images=True)

        expected = '<p><img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAIAAAACACAMAAAD04JH5AAAAY1BMVEX///8AAADy8vLDw8OGhoYJCQnf398EBAQdHR3s7OwPDw/7+/uioqIkJCQnJye6urrJyckbGxtlZWWwsLBvb29BQUE6Ojrk5OR+fn4WFhYvLy/W1tZqampVVVV4eHiUlJQ1NTVSAT8kAAABJ0lEQVR4nO3XWXKDMBBFUZpBgJjBgDGe9r/K2EkqcRHpL9VUKvds4D0EtKQgAAAAAAAAAAAA+NPC2Zg53Cs9Hw5jnWXV1Jdmj/jbPZFPaX1UrxCNqbw6DYVqfpnJho01G5TLNl8kUWwQ/Xj+9walVn4+uvJFqlWpwC11F5CzzkvI75586XSWYEh8BSRWKXDw5suoMZZDzyf4lGkMxLn2F7CtQgHjHAIfkuY/FJirnV9BOPkLdCq7cu8vMKmcjkrfJBa5auQHxvsf2kilQHD0FbgonQjMyZ2/KC3AYzuyrvxUZyt6KmLXhtgrXhAcDdI+18t/NCg383CJtS9I6/nlZGwvat/ft2KNx8wmie2ma6R7K/kSmrZpWrPb7RQAAAAAAAAAAOBXvAGvzwnuz+x0kQAAAABJRU5ErkJggg==" alt="alt text"></p>\n'

        if actual != expected:
            raise Exception("Local image not embedded properly:\nACTUAL:\n=======\n{}\n\nEXPECTED:\n=========\n{}\n".format(actual, expected))
