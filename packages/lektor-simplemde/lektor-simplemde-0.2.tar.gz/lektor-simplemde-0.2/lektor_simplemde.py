import email

import pkg_resources
from flask import Blueprint, render_template_string
from lektor.admin.modules import dash
from lektor.pluginsystem import Plugin


TEMPLATE = '''
{% extends "dash.html" %}
{% block scripts %}
  {{ super() }}
  <link rel="stylesheet" href="//cdn.jsdelivr.net/simplemde/latest/simplemde.min.css">
  <script src="//cdn.jsdelivr.net/simplemde/latest/simplemde.min.js"></script>
  <script>
    (new MutationObserver(function() {
        [...document.getElementsByTagName('textarea')].forEach(e => {
            if (e.className === 'form-control') {
                e.classList.add('simplemde-attached');
                setTimeout(() => new SimpleMDE({ element: e }));
            };
        });
    })).observe(
        document.getElementsByTagName('body')[0],
        {
            subtree: true,
            childList: true
        },
    );
  </script>
{% endblock %}
'''


def get_description(mod):
    distribution = pkg_resources.get_distribution(mod)
    if distribution.has_metadata('PKG-INFO'):
        meta = distribution.get_metadata('PKG-INFO')
    elif distribution.has_metadata('METADATA'):
        meta = distribution.get_metadata('METADATA')
    else:
        return None
    return email.message_from_string(meta).get('Summary', None)


class SimpleMdePlugin(Plugin):
    name = 'SimpleMDE'
    description = get_description(__module__)

    def patched_endpoint(self, *args, **kwargs):
        return render_template_string(TEMPLATE)

    def on_server_spawn(self, **kwargs):
        while len(dash.bp.deferred_functions) > 1:
            dash.bp.deferred_functions.pop()
        for path, endpoint in dash.endpoints:
            dash.bp.add_url_rule(path, endpoint, self.patched_endpoint)
