"""

Sphinx extension: dr.info
~~~~~~~~~~~~~~~~~~~~~~~~~

This extension overwrite the `info` directive of docutils to append bootstrap `alert` classes for rendering HTML with bootstrap.

"""
from docutils import nodes
from docutils.parsers.rst import Directive
from docutils.parsers.rst.directives import unchanged
from sphinx.locale import _

def setup(app):
    app.add_node(
        Info,
        html=(
            html_visit_node,
            html_depart_node
        )
    )
    app.add_directive('info', InfoDirective)

class Info(nodes.Admonition, nodes.Element):
    pass

class InfoDirective(Directive):
    has_content = True
    required_arguments = 0
    optional_arguments = 1
    option_spec = {'mode': unchanged}

    def run(self):

        mode = 'info'
        if 'mode' in self.options.keys() and self.options['mode'] in ['info','warning','danger']:
            mode = self.options['mode']

        env = self.state.document.settings.env

        targetid = "dr-info-%d" % env.new_serialno('dr-info')
        targetnode = nodes.target('','', ids=[targetid])

        node = Info('\n'.join(self.content))
        node.set_class("note")
        node.set_class("alert")
        node.set_class("alert-%s" % mode)
        node += nodes.title(_(mode.upper()), _(mode.upper()))

        self.state.nested_parse(self.content, self.content_offset, node)

        return [targetnode, node]

def html_visit_node(self, node):
    self.visit_admonition(node)

def html_depart_node(self, node):
    self.depart_admonition(node)