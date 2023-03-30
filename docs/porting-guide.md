# Badger 2040: Porting Guide <!-- omit in toc -->

The original Badger 2040 release predated the all-encompassing PicoGraphics and used its own custom drawing library.

Badger has since been updated to use PicoGraphics, and some parts of your code will need to change to be compatible.

- [Badger OS Changes](#badger-os-changes)
  - [Structure \& Filesystem](#structure--filesystem)
  - [Add Your Own](#add-your-own)
- [Function Changes](#function-changes)
  - [Thick Lines](#thick-lines)
  - [Images](#images)


## Badger OS Changes

### Structure & Filesystem

Apps have been moved to `examples/` to keep things tidy.

Many apps have top level directories for their associated files, these include:

* `badges/` for badge .txt files and images
* `images/` for image viewer .jpg files
* `books/` for text books
* `icons/` for weather icons

### Add Your Own

You no longer need to edit `launcher.py` to include your own custom apps, just place them in `examples/app_name.py` and include a corresponding `examples/icon-app_name.py`.

## Function Changes

The switch from Badger's own library to PicoGraphics changed a few minor things:

* `pen()` is now `set_pen()`
* `update_speed()` is now `set_update_speed()`
* `thickness()` is now `set_thickness()` and *only* applies to Hershey fonts

Additionally some features have been outright dropped:

* `image()` and `icon()` are deprecated, use JPEGs instead.
* `invert()` is no longer supported.

If you're porting from Badger 2040 to Badger 2040 W, note that it does not have a `USER` button. You'll have to adjust your control scheme accordingly.

### Thick Lines

While `set_thickness()` no longer applies to drawing operations, you can draw thick lines using `line(x1, y1, x2, y2, thickness)`.

### Images

Using `.bin` files for images is discouraged, albeit still possible. They were always tricky to convert and not cross-compatible with other displays.

Now you can use `jpegdec` to load and display a JPEG image:

```python
import badger2040
import jpegdec

badger = badger2040.Badger2040()
jpeg = jpegdec.JPEG(badger.display)

jpeg.open_file("image_file.jpg")
jpeg.decode(x, y)
```

JPEG files will be dithered to 1-bit and you might find that low-quality JPEGs have the odd random black pixel caused by compression artifacts. Bump up the quality until you're happy with the result.