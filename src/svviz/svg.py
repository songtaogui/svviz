
class SVG(object):
    def __init__(self, width, height, headerExtras=""):
        self.width = width
        self.height = height

        self.header = []
        self.svg = []
        self.footer = ["""</g></svg>"""]
        self.headerExtras = headerExtras
        self._addHeader()

    def getDefaultZIndex(self, zindex):
        """ allows insertion at the beginning of the svg list (ie before all the other items, therfore below them) """
        if zindex is None:
            zindex = len(self.svg)
        return zindex

    def _addHeader(self):
        self.header.append("""<?xml version="1.0" encoding="utf-8" ?><svg baseProfile="full" height="100%" version="1.1" """
            """width="100%" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" {extras} """
            """xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink"><defs />""".format(h=self.height, w=self.width, extras=self.headerExtras))
        self.header.append("<g class=\"svg_viewport\">")

    def _addOptions(self, **kwdargs):
        options = []
        for key, arg in kwdargs.iteritems():
            if arg is not None and arg != "":
                options.append("""{key}="{arg}" """.format(key=key, arg=arg))
        return " ".join(options)

    def line(self, x1, x2, y1, y2, stroke="", fill="", **kwdargs):
        more = self._addOptions(stroke=stroke, fill=fill, **kwdargs)
        self.svg.append("""<line x1="{x1}" x2="{x2}" y1="{y1}" y2="{y2}" {more}/>""".format(x1=x1, x2=x2, y1=self.height-y1, y2=self.height-y2, more=more))

    def rect(self, x, y, width, height, stroke="", fill="", zindex=None, **kwdargs):
        zindex = self.getDefaultZIndex(zindex)
        more = self._addOptions(stroke=stroke, fill=fill, **kwdargs)
        self.svg.insert(zindex, """<rect x="{x}" y="{y}" width="{w}" height="{h}" {more}/>\n""".format(x=x, y=self.height-y, w=width, h=height, more=more))

    def text(self, x, y, text, size=10, anchor="middle", fill="", family="Arial", **kwdargs):
        kwdargs["font-family"] = family
        more = self._addOptions(fill=fill, **kwdargs)
        self.svg.append("""<text x="{x}" y="{y}" font-size="{size}" text-anchor="{anchor}" {more}>{text}</text>\n""".format(x=x, y=self.height-y, size=size, anchor=anchor, more=more, text=text))

    def completed(self):
        return self.header + self.svg + self.footer

    def __str__(self):
        return "".join(self.completed())

    def write(self, path):
        output = open(path, "w")
        output.write(str(self))
