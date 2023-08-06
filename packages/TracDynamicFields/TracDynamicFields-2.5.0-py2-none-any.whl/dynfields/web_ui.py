# -*- coding: utf-8 -*-
#
# Copyright (C) 2010-2014 Rob Guttman <guttman@alum.mit.edu>
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution.
#

import re
from pkg_resources import resource_filename

from trac.core import Component, ExtensionPoint, implements
from trac.prefs.api import IPreferencePanelProvider
from trac.web.api import IRequestFilter
from trac.web.chrome import (
    Chrome, ITemplateProvider, add_script, add_script_data, add_stylesheet)

from dynfields.options import Options
from dynfields.rules import IRule, add_domain, _


class DynamicFieldsModule(Component):
    """A module that dynamically alters ticket fields based an extensible
    set of rules.  Uses jQuery for full implementation.
    """

    implements(IPreferencePanelProvider, IRequestFilter, ITemplateProvider)

    rules = ExtensionPoint(IRule)

    target_re = re.compile(r"(?P<target>[^.]+).*")

    def __init__(self):
        # bind the 'dynfields' catalog to the specified locale directory
        locale_dir = resource_filename(__name__, 'locale')
        add_domain(self.env.path, locale_dir)

    # ITemplateProvider methods

    def get_htdocs_dirs(self):
        return [('dynfields', resource_filename(__name__, 'htdocs'))]

    def get_templates_dirs(self):
        return [resource_filename(__name__, 'templates')]

    # IRequestFilter methods

    def pre_process_request(self, req, handler):
        return handler

    def post_process_request(self, req, template, data, content_type):
        if template in ('ticket.html', 'query.html'):
            add_script_data(req, {'triggers': self._get_triggers(req)})
            for script in ('dynfields.js', 'rules.js', 'layout.js'):
                add_script(req, 'dynfields/%s' % script)
            add_stylesheet(req, 'dynfields/layout.css')
        return template, data, content_type

    # IPreferencePanelProvider methods

    def get_preference_panels(self, req):
        if self._get_prefs_data(req):  # only show if there are preferences
            # TRANSLATOR: the preferences tab label
            yield 'dynfields', _("Dynamic Fields")

    def render_preference_panel(self, req, panel):
        opts = Options(self.env)
        if req.method == 'POST':
            opts.set_prefs(req)
        prefs_data = self._get_prefs_data(req, opts)
        data = {'data': prefs_data, 'saved': req.method == 'POST'}
        template = 'prefs_panel.html'
        if hasattr(Chrome(self.env), 'jenv'):
            return template, data, None
        else:
            return template, data

    # Internal methods

    def _get_prefs_data(self, req, opts=None):
        """Returns the pref data, a dict of rule class titles whose values
        include lists of rule spec preference dicts each with these keys:

          id (based on unique key)
          label (of checkbox)
          enabled ('1' or '0')
          type ('none', 'select', or 'text')
          options (list of options if type is 'select')
          value (saved preference or default value)
        """
        if opts is None:
            opts = Options(self.env)
        data = {}
        for rule in self.rules:
            for key in opts:
                if not opts.has_pref(key):
                    continue
                target = self.target_re.match(key).groupdict()['target']
                trigger = rule.get_trigger(req, target, key, opts)
                if not trigger:
                    continue

                # this rule spec has a pref - so get it!
                pref = opts.get_pref(req, target, key)
                rule.update_pref(req, trigger, target, key, opts, pref)
                data.setdefault(rule.title, {'desc': rule.desc, 'prefs': []})
                data[rule.title]['prefs'].append(pref)
        return data

    def _get_triggers(self, req):
        """Converts trac.ini config to dict of triggers with rule specs."""
        triggers = {}
        opts = Options(self.env)
        for key in opts:
            # extract the target field
            target = self.target_re.match(key).groupdict()['target']

            # extract rule specifications from configs
            for rule in self.rules:
                trigger = rule.get_trigger(req, target, key, opts)
                if not trigger:
                    continue
                if not opts.is_enabled(req, key):
                    continue
                value, _ = opts.get_value_and_options(req, target, key)
                spec = {'rule_name': rule.name, 'trigger': trigger,
                        'target': target, 'value': value}
                rule.update_spec(req, key, opts, spec)
                triggers.setdefault(trigger, []).append(spec)

        return triggers
