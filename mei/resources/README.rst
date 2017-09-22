.. image:: https://img.shields.io/pypi/v/mistune.svg
   :target: https://pypi.python.org/pypi/markdown-embedimages/
   :alt: Latest Version
.. image:: https://travis-ci.org/dsoprea/markdown-embedimages.svg?branch=master
   :target: https://travis-ci.org/dsoprea/markdown-embedimages
   :alt: Travis CI Status

Overview
========

This project allows you to translate markdown to HTML and to convert URLs or even local image file-paths to embedded images.

Local file-paths must be specifically enabled, for security reasons.

This project is Python 2 and Python 3 compatible.


Example
=======

----------
Image URLs
----------

Short usage::

    import mei

    markdown = "![Random Ingenuity](http://www.randomingenuity.com/ri72.png)"
    actual = mei.markdown(markdown)

    # <p><img src="data:image/png;base64,iVBORw0KGgoAAAANSU...kJggg==" alt="Random Ingenuity"></p>

Long usage::

    import mei.embed_images
    import mistune

    renderer = mei.embed_images.EmbedImagesRenderer()
    m = mistune.Markdown(renderer=renderer)

    markdown = "![Random Ingenuity](http://www.randomingenuity.com/ri72.png)"
    actual = m.render(markdown)

    # <p><img src="data:image/png;base64,iVBORw0KGgoAAAANSU...kJggg==" alt="Random Ingenuity"></p>


------------
Local Images
------------

Short usage::

    import mei

    markdown = "![alt text](/drawable-mdpi/ic_menu_paste.png)"
    actual = mei.markdown(markdown)

    # <p><img src="data:image/png;base64,iVBORw0KGgoAAAANSU...TkSuQCC" alt="Random Ingenuity"></p>

Long usage::

    import mei.embed_images
    import mistune

    renderer = mei.embed_images.EmbedImagesRenderer(embed_local_images=True)
    m = mistune.Markdown(renderer=renderer)

    markdown = "![alt text](/drawable-mdpi/ic_menu_paste.png)"
    actual = m.render(markdown)

    # <p><img src="data:image/png;base64,iVBORw0KGgoAAAANSU...TkSuQCC" alt="Random Ingenuity"></p>


-------
Testing
-------

Just run the test script::

    $ ./test.sh
    test_embed_images_local (test_embed_images.TestEmbedImages) ... ok
    test_embed_images_url (test_embed_images.TestEmbedImages) ... ok
    test_get_base64_with_image_filepath (test_embed_images.TestEmbedImages) ... ok
    test_get_base64_with_image_url (test_embed_images.TestEmbedImages) ... ok
    test_get_embedded_image_filepath (test_embed_images.TestEmbedImages) ... ok
    test_get_embedded_image_filepath__xhtml (test_embed_images.TestEmbedImages) ... ok
    test_get_embedded_image_url (test_embed_images.TestEmbedImages) ... ok
    test_get_embedded_image_url__xhtml (test_embed_images.TestEmbedImages) ... ok
    test_get_http2 (test_embed_images.TestEmbedImages) ... ok
    test_get_http3 (test_embed_images.TestEmbedImages) ... ok
    test_http (test_embed_images.TestEmbedImages) ... ok
    test_http__instance_cached (test_embed_images.TestEmbedImages) ... ok
    test_markdown (test_embed_images.TestEmbedImages) ... ok

    ----------------------------------------------------------------------
    Ran 13 tests in 0.016s

    OK
