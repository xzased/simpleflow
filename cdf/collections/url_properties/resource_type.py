import re
import itertools

from BQL.parser.properties_mapping import validate_query_grammar, query_to_python

ALLOWED_RULES_FIELDS = ('query', 'value', 'abstract', 'rule_id', 'inherits_from')
MANDATORY_RULES_FIELDS = ('query', 'value')

__all__ = ['compile_resource_type_settings', 'validate_resource_type_settings', 'ResourceTypeSettingsException']


def compile_resource_type_settings(settings):
    """
    Return a list of dictionnaries or a `ResourceTypeSettingsException` if the settings are not valid

    Format :
    [
        {'query': lambda ..,
         'value': 'value',
         'rule_id': 'xxx'},
        {'query': lambda ...,
         'inherits_from: 'xxx',
         'rule_id': 'yyy'}
    ]
    """
    compiled_rules = []

    # An exception will be raised if the settings are not valid
    validate_resource_type_settings(settings)

    for host, rules in settings.iteritems():
        for rule in rules:
            if host.startswith('*.'):
                host_query = 'ENDS(host, "%s")' % host[1:]
            else:
                host_query = 'host = "%s"' % host

            # if rule inherits from another one, we don't need to check again the host
            _rule = {'query': query_to_python(' AND '.join((host_query, rule['query'])) if not 'inherits_from' in rule else rule['query']),
                     'value': rule['value']
                     }
            for field in ('inherits_from', 'rule_id', 'abstract'):
                if field in rule:
                    _rule[field] = rule[field]
            compiled_rules.append(_rule)

    return compiled_rules


def validate_resource_type_settings(settings):
    """
    Validates a settings

    -- settings : a dictionnary where keys are hostnames and values are tuples of rules
        {'host1': (rule1, rule2...), 'host2': (rule3, rule4..)}

        Rule format :
        {'query': 'A BQL query',
         'value': 'a_value',
        }

        ====
        HOST
        ====
        We can add a wildcard (ex: *.mysite.com) at the beginning of an host to match multiple hosts.
        The wildcard must be directly followed by a dot.

        ====
        RULE
        ====
        A `rule_id` field can be set to let the rule being inherited in another one
        If the rule must not be matched but only its children, add `abstract` field to True

        The inherited rule set `inherits_from `field with the rule_id as value

    Return `True` if the settings format is valid, else raises ResourceTypeSettingsException

    """
    errors = {'host': [],
              'query': [],
              'field': []
              }

    for host, rules in settings.iteritems():
        if re.search('^(.+)\*', host):
            errors['host'].append('Host %s should contains wildcard only at the beginning' % host)
        elif host.startswith('*') and not host.startswith('*.'):
            errors['host'].append('Wildcard at %s should be directly followed by a dot' % host)

        for i, rule in enumerate(rules):
            # Check fields names
            for field in rule.keys():
                if field not in ALLOWED_RULES_FIELDS:
                    errors['field'].append('`%s` is not a valid field in host %s rule %d' % (field, host, i))

            # Check for mandatory fields
            for field in MANDATORY_RULES_FIELDS:
                if field not in rule.keys():
                    errors['field'].append('`%s` is mandatory in host %s rule %d' % (field, host, i))

            # Check query validity
            if 'query' in rule:
                _valid, _msg = validate_query_grammar(rule['query'])
                if not _valid:
                    errors['query'].append('Error in query, host %s rule %d : %s' % (host, i, _msg))

    if len(list(itertools.chain(*errors.values()))) == 0:
        return True
    raise ResourceTypeSettingsException(errors)


class ResourceTypeSettingsException(Exception):

    def __init__(self, errors):
        self._errors = errors

    @property
    def errors(self):
        return [e for e in itertools.chain(*self._errors.values())]

    @property
    def host_errors(self):
        return self._errors['host']

    @property
    def query_errors(self):
        return self._errors['query']

    @property
    def field_errors(self):
        return self._errors['field']