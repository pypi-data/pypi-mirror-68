# -*- coding: utf-8 -*-
#
# Copyright (C) 2010-2014 Rob Guttman <guttman@alum.mit.edu>
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution.
#

import re

from trac.core import Component, ExtensionPoint, Interface, implements
from trac.perm import IPermissionGroupProvider, PermissionSystem

try:
    from trac.util import to_list
except ImportError:
    from dynfields.compat import to_list

# Import translation functions.
# Fallbacks make Babel still optional and provide Trac 0.11 compatibility.
try:
    from trac.util.translation import domain_functions
except ImportError:
    from trac.util.html import html as tag_
    from trac.util.translation import gettext
    _ = gettext

    def add_domain(a, b, c=None):
        pass
else:
    add_domain, _, tag_ = \
        domain_functions('dynfields', ('add_domain', '_', 'tag_'))


if not hasattr(PermissionSystem, 'get_permission_groups'):

    PermissionSystem.group_providers = ExtensionPoint(IPermissionGroupProvider)

    def get_permission_groups(self, user):
        groups = set([user])
        for provider in self.group_providers:
            for group in provider.get_permission_groups(user):
                groups.add(group)

        perms = PermissionSystem(self.env).get_all_permissions()
        repeat = True
        while repeat:
            repeat = False
            for subject, action in perms:
                if subject in groups and not action.isupper() and \
                        action not in groups:
                    groups.add(action)
                    repeat = True
        return groups

    PermissionSystem.get_permission_groups = get_permission_groups


class IRule(Interface):
    """An extension point interface for adding rules.  Rule processing
    is split into two parts: (1) rule specification (python), (2) rule
    implementation (JS).

    The python and JS parts are linked by instantiating the JS rule
    implementation with the corresponding python rule's class name.
    For example, the JS rule implementation corresponding with the
    HideRule python class must be instantiated as follows in rules.js:

      var hiderule = new Rule('HideRule');
    """

    def get_trigger(self, req, target, key, opts):
        """Return the field name that triggers the rule, or None if not found
        for the given target field and ticket-custom options key and dict.
        For example, if the 'version' field is to be hidden based on the
        ticket type, then the returned trigger field name should be 'type'."""

    def update_spec(self, req, key, opts, spec):
        """Update the spec dict with the rule's specifications needed for
        the JS implementation.  The spec dict is defaulted to include the
        rule's name (rule_name), the trigger field's name (trigger), the
        target field's name (target), and the preference or default value
        if applicable (value)."""

    def update_pref(self, req, trigger, target, key, opts, pref):
        """Update the pref dict with the data needed for preferences.
        The primary dict keys to change are:

          label (of checkbox)
          type ('none' or 'select')

        Default values for the above are provided as well as for the
        keys below (which should usually not be changed):

          id (based on unique key)
          enabled ('1' or '0')
          options (list of options if type is 'select')
          value (saved preference or default value)
        """


class Rule(object):
    """Abstract class for common rule properties and utilities."""

    OVERWRITE = '(overwrite)'

    @property
    def name(self):
        """Returns the rule instance's class name.  The corresponding
        JS rule must be instantiated with this exact name."""
        return self.__class__.__name__

    @property
    def title(self):
        """Returns the rule class' title used for display purposes.
        This default implementation returns the rule's name with any
        camel case split into words and the last word made plural.
        This property/method can be overridden as needed.
        """
        # split CamelCase to Camel Case
        title = self._split_camel_case(self.name)
        if not title.endswith('s'):
            title += 's'
        return title

    @property
    def desc(self):
        """Returns the description of the rule.  This default implementation
        returns the first paragraph of the docstring as the desc.
        """
        return self.__doc__.split('\n')[0]

    # private methods
    def _capitalize(self, word):
        if len(word) <= 1:
            return word.upper()
        return word[0].upper() + word[1:]

    def _split_camel_case(self, s):
        return re.sub('((?=[A-Z][a-z])|(?<=[a-z])(?=[A-Z]))', ' ', s)

    def _extract_overwrite(self, target, key, opts):
        """Extract any <overwrite> prefix from value string."""
        value = opts[key]
        if value.endswith(self.OVERWRITE):
            value = value.replace(self.OVERWRITE, '').rstrip()
            overwrite = True
        else:
            overwrite = opts.getbool('%s.overwrite' % target)
        return value, overwrite


class ClearRule(Component, Rule):
    """Clears one field when another changes.

    Example trac.ini specs:

      [ticket-custom]
      version.clear_on_change_of = milestone
    """

    implements(IRule)

    @property
    def title(self):
        title = _("Clear Rules")
        return title

    @property
    def desc(self):
        desc = _("Clears one field when another changes.")
        return desc

    def get_trigger(self, req, target, key, opts):
        if key == '%s.clear_on_change_of' % target:
            return opts[key]
        return None

    def update_spec(self, req, key, opts, spec):
        target = spec['target']
        spec['op'] = 'clear'
        spec['clear_on_change'] = \
            opts.getbool(target + '.clear_on_change', True)

    def update_pref(self, req, trigger, target, key, opts, pref):
        # TRANSLATOR: checkbox label text for clear rules
        pref['label'] = _("Clear %(target)s when %(trigger)s changes",
                          target=target, trigger=trigger)


class CopyRule(Component, Rule):
    """Copies a field (when changed) to another field (if empty and visible).

    Example trac.ini specs:

      [ticket-custom]
      captain.copy_from = owner

    In this example, if the owner value changes, then the captain field's
    value gets set to that value if the captain field is empty and visible
    (the default).  By default, the current value if set will not be
    overwritten.  To overwrite the current value, add "(overwrite)" as
    follows:

      [ticket-custom]
      captain.copy_from = owner (overwrite)
    """

    implements(IRule)

    @property
    def title(self):
        title = _("Copy Rules")
        return title

    @property
    def desc(self):
        desc = _("Copies field content (when changed) to another field "
                 "(if empty and visible).")
        return desc

    def get_trigger(self, req, target, key, opts):
        if key == '%s.copy_from' % target:
            return self._extract_overwrite(target, key, opts)[0]
        return None

    def update_spec(self, req, key, opts, spec):
        target = spec['target']
        spec['op'] = 'copy'
        spec['overwrite'] = self._extract_overwrite(target, key, opts)[1]

    def update_pref(self, req, trigger, target, key, opts, pref):
        # TRANSLATOR: checkbox label text for copy rules
        pref['label'] = _("Copy %(trigger)s to %(target)s",
                          trigger=trigger, target=target)


class DefaultRule(Component, Rule):
    """Defaults a field to a user-specified value if empty.

    Example trac.ini specs:

      [ticket-custom]
      cc.default_value = (pref)
      cc.append = true

    If the field is a non-empty text field and 'append' is true, then the
    field is presumed to be a comma-delimited list and the preference value
    is appended if not already present.
    """

    implements(IRule)

    @property
    def title(self):
        title = _("Default Value Rules")
        return title

    @property
    def desc(self):
        desc = _("Defaults a field to a user-specified value.")
        return desc

    def get_trigger(self, req, target, key, opts):
        if key == '%s.default_value' % target:
            return target
        return None

    def update_spec(self, req, key, opts, spec):
        spec['op'] = 'default'
        spec['append'] = False if opts.get(spec['target']) == 'select' else \
                         opts.getbool(spec['target'] + '.append')

    def update_pref(self, req, trigger, target, key, opts, pref):
        # "Default trigger to <select options>"
        # TRANSLATOR: checkbox label text for default value rules
        pref['label'] = _("Default %(target)s to", target=target)
        if opts.get(target) == 'select':
            pref['type'] = 'select'
        else:
            pref['type'] = 'text'


class HideRule(Component, Rule):
    """Hides a field based on another's value, group membership, or always.

    Example trac.ini specs:

      [ticket-custom]
      version.show_when_type = enhancement
      milestone.hide_when_type = defect
      duedate.show_if_group = production
      milestone.hide_if_group = production
      alwayshide.hide_always = True
      alwayshide.clear_on_hide = False
    """

    implements(IRule)
    group_providers = ExtensionPoint(IPermissionGroupProvider)

    @property
    def title(self):
        title = _("Hide Rules")
        return title

    @property
    def desc(self):
        desc = _("Hides a field based on another field's value (or always).")
        return desc

    def get_trigger(self, req, target, key, opts):
        rule_re = re.compile(r"%s.(?P<op>(show|hide))_when_(?P<trigger>.*)"
                             % target)
        match = rule_re.match(key)
        if match:
            return match.groupdict()['trigger']

        # group rule
        rule_re = re.compile(r"%s.(?P<op>(show|hide))_if_group" % target)
        match = rule_re.match(key)
        if match:
            ps = PermissionSystem(self.env)
            groups1 = set(opts[key].split('|'))
            groups2 = ps.get_permission_groups(req.authname)
            if match.groupdict()['op'] == 'hide':
                return 'type' if groups1.intersection(groups2) else None
            else:
                return None if groups1.intersection(groups2) else 'type'

        # try finding hide_always rule
        if key == "%s.hide_always" % target:
            return 'type'  # requires that 'type' field is enabled
        return None

    def update_spec(self, req, key, opts, spec):
        target = spec['target']
        trigger = spec['trigger']

        spec_re = re.compile(r"%s.(?P<op>(show|hide))_when_%s"
                             % (target, trigger))
        match = spec_re.match(key)
        if match:
            spec['op'] = match.groupdict()['op']
            spec['trigger_value'] = opts[key]
            spec['hide_always'] = self._is_always_hidden(req, key, opts, spec)
        else:  # assume 'hide_always' or group rule
            spec['op'] = 'show'
            spec['trigger_value'] = 'invalid_value'
            spec['hide_always'] = True
        spec['clear_on_hide'] = opts.getbool(target + '.clear_on_hide', True)
        spec['link_to_show'] = opts.getbool(target + '.link_to_show')

    def update_pref(self, req, trigger, target, key, opts, pref):
        spec = {'trigger': trigger, 'target': target}
        self.update_spec(req, key, opts, spec)
        # TRANSLATOR: char/word to replace '|' = logic OR in 'value|value'
        trigval = spec['trigger_value'].replace('|', _(" or "))
        if spec['op'] == 'hide':
            # TRANSLATOR: checkbox label text for conditional hide rules
            pref['label'] = _("Hide %(target)s when %(trigger)s = %(trigval)s",
                              target=target, trigger=trigger, trigval=trigval)
        else:
            # TRANSLATOR: checkbox label text for conditional show rules
            pref['label'] = _("Show %(target)s when %(trigger)s = %(trigval)s",
                              target=target, trigger=trigger, trigval=trigval)

        # special case when trigger value is not a select option
        value, options = opts.get_value_and_options(req, trigger, key)
        value = spec['trigger_value']
        if options and value and value not in options and '|' not in value:
            # "Always hide/show target"
            if spec['op'] == 'hide':
                pref['label'] = _("Always show %(target)s", target=target)
            else:
                pref['label'] = _("Always hide %(target)s", target=target)

    def _is_always_hidden(self, req, key, opts, spec):
        trigger = spec['trigger']
        value, options = opts.get_value_and_options(req, trigger, key)
        value = spec['trigger_value']
        if options and value and value not in options and '|' not in value:
            return spec['op'] == 'show'
        return False


class ValidateRule(Component, Rule):
    """Checks a field for an invalid value.

    Example trac.ini specs:

      [ticket-custom]
      milestone.invalid_if =
      phase.invalid_if = releasing
      phase.invalid_when = .codereviewstatus .pending (msg:Pending reviews.)
    """

    implements(IRule)

    def get_trigger(self, req, target, key, opts):
        if key.startswith('%s.invalid_if' % target):
            return target
        return None

    def update_spec(self, req, key, opts, spec):
        target = spec['target']
        spec['op'] = 'validate'
        spec['value'] = opts[key]

        # check for suffix
        suffix_re = re.compile(r"(?P<suffix>\.[0-9]+)$")
        match = suffix_re.search(key)
        suffix = match.groupdict()['suffix'] if match else ''

        # extract when spec
        spec['when'] = opts.get("%s.invalid_when%s" % (target, suffix), '')
        spec['msg'] = ''
        if spec['when']:
            when_re = re.compile(r"^(?P<selector>.+) \(msg:(?P<msg>.+)\)$")
            match = when_re.match(spec['when'])
            if match:
                spec['when'] = match.groupdict()['selector']
                spec['msg'] = match.groupdict()['msg']

    def update_pref(self, req, trigger, target, key, opts, pref):
        suffix = opts[key] and "= %s" % opts[key] or "is empty"
        pref['label'] = "Invalid if %s %s" % (target, suffix)


class SetRule(Component, Rule):
    """Sets a field based on another field's value.

    Example trac.ini specs:

      [ticket-custom]
      milestone.set_to_!_when_phase = implementation|verifying

    The "!" is used only for select fields to specify the first non-empty
    option; a common use case is to auto-select the current milestone.
    By default, the current value if set will not be overwritten.  To
    overwrite the current value, add "(overwrite)" as follows:

      [ticket-custom]
      milestone.set_to_!_when_phase = implementation|verifying (overwrite)
    """

    implements(IRule)

    def get_trigger(self, req, target, key, opts):
        rule_re = re.compile(r"%s.set_to_(.*)_when_(?P<not>not_)?"
                             r"(?P<trigger>.+)" % target)
        match = rule_re.match(key)
        if match:
            return match.groupdict()['trigger']

    def update_spec(self, req, key, opts, spec):
        target, trigger = spec['target'], spec['trigger']
        spec_re = re.compile(r"%s.set_to_(?P<to>.*)_when_(?P<not>not_)?%s"
                             % (target, trigger))
        match = spec_re.match(key)
        if not match:
            return
        spec['set_to'] = match.groupdict()['to']
        if spec['set_to'].lower() in ('1', 'true'):
            spec['set_to'] = True
        elif spec['set_to'].lower() in ('0', 'false'):
            spec['set_to'] = False
        elif spec['set_to'] == '?' and 'value' in spec:
            spec['set_to'] = spec['value']
        trigger_value, spec['overwrite'] = \
            self._extract_overwrite(target, key, opts)
        spec['trigger_value'] = []
        spec['trigger_not_value'] = []
        for val in to_list(trigger_value, '|'):
            if match.groupdict()['not']:
                spec['trigger_not_value'].append(val)
            else:
                spec['trigger_value'].append(val)

    def update_pref(self, req, trigger, target, key, opts, pref):
        spec = {'target': target, 'trigger': trigger}
        self.update_spec(req, key, opts, spec)
        # "When trigger = value set target to"
        if spec['trigger_value']:
            comp = '='
            trigval = ' or '.join(spec['trigger_value'])
        else:
            comp = '!='
            trigval = ' or '.join(spec['trigger_not_value'])
        if spec['set_to'] == '?':
            set_to = ''
            pref['type'] = 'select' if opts.get(target) == 'select' else 'text'
        elif spec['set_to'] == '!':
            set_to = 'the first non-empty option'
        elif spec['set_to'] == '':
            set_to = '(empty)'
        else:
            set_to = spec['set_to']
        pref['label'] = "When %s %s %s, set %s to %s"\
                        % (trigger, comp, trigval, target, set_to)
