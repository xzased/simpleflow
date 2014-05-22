from cdf.metadata.url.url_metadata import (
    INT_TYPE, BOOLEAN_TYPE, STRUCT_TYPE,
    ES_NO_INDEX, ES_DOC_VALUE,
    LIST, AGG_CATEGORICAL, AGG_NUMERICAL
)
from cdf.core.streams.base import StreamDefBase
from cdf.analysis.urls.utils import is_link_internal
from cdf.log import logger
from cdf.features.links.helpers.masks import list_to_mask
from cdf.utils.convert import _str_to_bool
from cdf.query.constants import RENDERING
from .helpers.masks import follow_mask
from .settings import GROUPS


__all__ = ["OutlinksRawStreamDef", "OutlinksStreamDef"]


def _get_nofollow_combination_key(keys):
    return '_'.join(sorted(keys))


class OutlinksRawStreamDef(StreamDefBase):
    FILE = 'urllinks'
    HEADERS = (
        ('id', int),
        ('link_type', str),
        ('bitmask', int),
        ('dst_url_id', int),
        ('external_url', str)
    )


class OutlinksStreamDef(OutlinksRawStreamDef):
    """
    We just change the type of "follow"
    """
    HEADERS = (
        ('id', int),
        ('link_type', str),
        ('follow', follow_mask),
        ('dst_url_id', int),
        ('external_url', str)
    )
    URL_DOCUMENT_MAPPING = {
        # internal outgoing links (destination is a internal url)
        "outlinks_internal.nb.total": {
            "verbose_name": "Number of Internal Incoming Links",
            "group": GROUPS.outlinks_internal,
            "order": 1,
            "type": INT_TYPE,
            "settings": {
                ES_DOC_VALUE,
                AGG_NUMERICAL
            }
        },
        "outlinks_internal.nb.unique": {
            "verbose_name": "Unique Number of Internal Incoming Links",
            "group": GROUPS.outlinks_internal,
            "order": 2,
            "type": INT_TYPE,
            "settings": {
                ES_DOC_VALUE,
                AGG_NUMERICAL
            }
        },
        "outlinks_internal.nb.follow.unique": {
            "verbose_name": "Unique Number of Follow Internal Incoming Links",
            "group": GROUPS.outlinks_internal,
            "order": 4,
            "type": INT_TYPE,
            "settings": {
                ES_DOC_VALUE,
                AGG_NUMERICAL
            }
        },
        "outlinks_internal.nb.follow.total": {
            "verbose_name": "Number of Internal Follow Outlinks",
            "group": GROUPS.outlinks_internal,
            "order": 3,
            "type": INT_TYPE,
            "settings": {
                ES_DOC_VALUE,
                AGG_NUMERICAL
            }
        },
        "outlinks_internal.nb.nofollow.total": {
            "verbose_name": "Number of Internal NoFollow Outlinks",
            "group": GROUPS.outlinks_internal_nofollow,
            "order": 5,
            "type": INT_TYPE,
            "settings": {
                ES_DOC_VALUE,
                AGG_NUMERICAL
            }
        },
        "outlinks_internal.nb.nofollow.combinations.link": {
            "verbose_name": "Number of Internal NoFollow Outlinks strictly in link nofollow",
            "group": GROUPS.outlinks_internal_nofollow,
            "order": 6,
            "type": INT_TYPE,
            "settings": {
                ES_DOC_VALUE,
                AGG_NUMERICAL
            }
        },
        "outlinks_internal.nb.nofollow.combinations.meta": {
            "verbose_name": "Number of Internal NoFollow Outlinks strictly in meta nofollow",
            "group": GROUPS.outlinks_internal_nofollow,
            "order": 7,
            "type": INT_TYPE,
            "settings": {
                ES_DOC_VALUE,
                AGG_NUMERICAL
            }
        },
        "outlinks_internal.nb.nofollow.combinations.robots": {
            "verbose_name": "Number of Internal NoFollow Outlinks strictly disallowed by robots.txt",
            "group": GROUPS.outlinks_internal_nofollow,
            "order": 8,
            "type": INT_TYPE,
            "settings": {
                ES_DOC_VALUE,
                AGG_NUMERICAL
            }
        },
        "outlinks_internal.nb.nofollow.combinations.link_meta": {
            "verbose_name": "Number of Internal NoFollow Outlinks both in link and meta nofollow",
            "group": GROUPS.outlinks_internal_nofollow,
            "order": 9,
            "type": INT_TYPE,
            "settings": {
                ES_DOC_VALUE,
                AGG_NUMERICAL
            }
        },
        "outlinks_internal.nb.nofollow.combinations.link_robots": {
            "verbose_name": "Number of Internal NoFollow Outlinks both in link nofollow and disallowed by robots.txt",
            "group": GROUPS.outlinks_internal_nofollow,
            "order": 10,
            "type": INT_TYPE,
            "settings": {
                ES_DOC_VALUE,
                AGG_NUMERICAL
            }
        },
        "outlinks_internal.nb.nofollow.combinations.meta_robots": {
            "verbose_name": "Number of Internal NoFollow Outlinks both in meta nofollow and disallowed by robots.txt",
            "group": GROUPS.outlinks_internal_nofollow,
            "type": INT_TYPE,
            "order": 11,
            "settings": {
                ES_DOC_VALUE,
                AGG_NUMERICAL
            }
        },
        "outlinks_internal.nb.nofollow.combinations.link_meta_robots": {
            "verbose_name": "Number of Internal NoFollow Outlinks both in link, meta nofollow and disallowed by robots.txt",
            "group": GROUPS.outlinks_internal_nofollow,
            "type": INT_TYPE,
            "order": 12,
            "settings": {
                ES_DOC_VALUE,
                AGG_NUMERICAL
            }
        },
        "outlinks_internal.urls": {
            "verbose_name": "Sample of Internal outlinks",
            "group": GROUPS.outlinks_internal,
            "order": 13,
            "type": INT_TYPE,
            "settings": {ES_NO_INDEX, LIST, RENDERING.URL},
        },
        "outlinks_internal.urls_exists": {
            "type": BOOLEAN_TYPE,
            "default_value": None
        },

        # external outgoing links (destination is a external url)
        "outlinks_external.nb.total": {
            "verbose_name": "Number of External Outlinks",
            "group": GROUPS.outlinks_external,
            "order": 1,
            "type": INT_TYPE,
            "settings": {
                ES_DOC_VALUE,
                AGG_NUMERICAL
            }
        },
        "outlinks_external.nb.follow.total": {
            "verbose_name": "Number of External Follow Outlinks",
            "group": GROUPS.outlinks_external,
            "order": 2,
            "type": INT_TYPE,
            "settings": {
                ES_DOC_VALUE,
                AGG_NUMERICAL
            }
        },
        "outlinks_external.nb.nofollow.total": {
            "verbose_name": "Number of External NoFollow Outlinks",
            "group": GROUPS.outlinks_external_nofollow,
            "order": 1,
            "type": INT_TYPE,
            "settings": {
                ES_DOC_VALUE,
                AGG_NUMERICAL
            }
        },
        "outlinks_external.nb.nofollow.combinations.link": {
            "verbose_name": "Number of External NoFollow Outlinks strictly in link nofollow",
            "group": GROUPS.outlinks_external_nofollow,
            "order": 2,
            "type": INT_TYPE,
            "settings": {
                ES_DOC_VALUE,
                AGG_NUMERICAL
            }
        },
        "outlinks_external.nb.nofollow.combinations.meta": {
            "verbose_name": "Number of External NoFollow Outlinks strictly in meta nofollow",
            "group": GROUPS.outlinks_external_nofollow,
            "order": 3,
            "type": INT_TYPE,
            "settings": {
                ES_DOC_VALUE,
                AGG_NUMERICAL
            }
        },
        "outlinks_external.nb.nofollow.combinations.link_meta": {
            "verbose_name": "Number of External NoFollow Outlinks both in link and meta nofollow",
            "group": GROUPS.outlinks_external_nofollow,
            "order": 4,
            "type": INT_TYPE,
            "settings": {
                ES_DOC_VALUE,
                AGG_NUMERICAL
            }
        },

        # outgoing canonical link, one per page
        # if multiple, first one is taken into account
        "canonical.to.url": {
            "verbose_name": "Canonical To",
            "group": GROUPS.canonical,
            "order": 1,
            "type": STRUCT_TYPE,
            "values": {
                "url_str": {"type": "string"},
                "url_id": {"type": "integer"},
            },
            "settings": {
                ES_NO_INDEX, RENDERING.URL
            }
        },
        "canonical.to.equal": {
            "verbose_name": "Canonical is the Same Url",
            "group": GROUPS.canonical,
            "order": 2,
            "type": BOOLEAN_TYPE,
            "settings": {AGG_CATEGORICAL}
        },
        "canonical.to.url_exists": {
            "type": "boolean",
            "default_value": None
        },

        # incoming canonical link
        "canonical.from.nb": {
            "verbose_name": "Number of Incoming Canonical",
            "group": GROUPS.canonical,
            "order": 3,
            "type": INT_TYPE,
            "settings": {
                ES_DOC_VALUE,
                AGG_CATEGORICAL,
                AGG_NUMERICAL
            }
        },
        "canonical.from.urls": {
            "verbose_name": "Canonical From",
            "group": GROUPS.canonical,
            "order": 4,
            "type": INT_TYPE,
            "settings": {ES_NO_INDEX, LIST, RENDERING.URL}
        },
        "canonical.from.urls_exists": {
            "type": "boolean",
            "default_value": None
        },

        # outgoing redirection
        "redirect.to.url": {
            "verbose_name": "Redirects to",
            "group": GROUPS.redirects,
            "order": 1,
            "type": STRUCT_TYPE,
            "values": {
                "url_str": {"type": "string"},
                "url_id": {"type": "integer"},
                "http_code": {"type": "integer"}
            },
            "settings": {
                ES_NO_INDEX,
                RENDERING.URL
            }
        },
        "redirect.to.url_exists": {
            "type": BOOLEAN_TYPE,
            "default_value": None,
        },

        # incoming redirection
        "redirect.from.nb": {
            "verbose_name": "Number of Incoming Redirects",
            "group": GROUPS.redirects,
            "order": 3,
            "type": INT_TYPE,
            "settings": {
                ES_DOC_VALUE,
                AGG_CATEGORICAL,
                AGG_NUMERICAL
            }
        },
        "redirect.from.urls": {
            "verbose_name": "Redirected From",
            "group": GROUPS.redirects,
            "order": 4,
            "type": INT_TYPE,
            "settings": {ES_NO_INDEX, LIST, RENDERING.URL}
        },
        "redirect.from.urls_exists": {
            "type": "boolean",
            "default_value": None
        }
    }

    def pre_process_document(self, document):
        # resolve a (dest, mask) to its index in `inlinks_internal` list
        document["processed_outlink_link"] = set()
        # a temp set to track all `seen` dest url of outgoing links
        document["processed_outlink_url"] = set()

    def process_document(self, document, stream):
        url_src, link_type, follow_keys, url_dst, external_url = stream

        if link_type == "a":
            # is_internal = url_dst > 0
            is_internal = is_link_internal(follow_keys, url_dst)
            is_follow = len(follow_keys) == 1 and follow_keys[0] == "follow"
            outlink_type = "outlinks_internal" if is_internal else "outlinks_external"
            mask = list_to_mask(follow_keys)

            outlink_nb = document[outlink_type]['nb']
            outlink_nb['total'] += 1

            # target dict changes with link follow status
            follow = outlink_nb['follow' if is_follow else 'nofollow']
            follow['total'] += 1
            if is_internal and is_follow:
                # increment follow counters
                if not (url_dst, mask) in document['processed_outlink_link']:
                    follow['unique'] += 1
            elif not is_follow:
                # increment nofollow combination counters
                key = _get_nofollow_combination_key(follow_keys)
                follow['combinations'][key] += 1

            # internal outlinks
            # still need dest url id check since we can have internal url
            # blocked by robots.txt
            if is_internal and url_dst > 0:
                outlink_urls = document['outlinks_internal']['urls']
                exists = (url_dst, mask) in document['processed_outlink_link']
                if len(outlink_urls) < 300 and not exists:
                    outlink_urls.append([url_dst, mask])

                # add this link's dest to the processed set
                document['processed_outlink_url'].add(url_dst)
                document['processed_outlink_link'].add((url_dst, mask))

                document['outlinks_internal']['urls_exists'] = True

        elif link_type.startswith('r'):
            http_code = link_type[1:]
            redirects_to = document['redirect']['to']
            redirects_to['url'] = {}
            if url_dst == -1:
                redirects_to['url']['url_str'] = external_url
            else:
                redirects_to['url']['url_id'] = url_dst
            redirects_to['url']['http_code'] = int(http_code)
            redirects_to['url_exists'] = True

        elif link_type == "canonical":
            canonical_to = document['canonical']['to']
            if canonical_to.get('equal', None) is None:
                # We take only the first canonical found
                canonical_to['equal'] = url_src == url_dst
                canonical_to['url'] = {}
                if url_dst > 0:
                    canonical_to['url']['url_id'] = url_dst
                else:
                    canonical_to['url']['url_str'] = external_url
                canonical_to['url_exists'] = True

    def post_process_document(self, document):
        # If not "outlinks_internal" : we want to store a non-crawled url
        if not 'outlinks_internal' in document:
            return

        document['outlinks_internal']['nb']['unique'] = len(document['processed_outlink_url'])

        # delete intermediate data structures
        del document['processed_outlink_url']
        del document["processed_outlink_link"]


class InlinksRawStreamDef(StreamDefBase):
    FILE = 'urlinlinks'
    HEADERS = (
        ('id', int),
        ('link_type', str),
        ('bitmask', int),
        ('src_url_id', int),
        ('text_hash', str),
        ('text', str),
    )


class InlinksStreamDef(InlinksRawStreamDef):
    HEADERS = (
        ('id', int),
        ('link_type', str),
        ('follow', follow_mask),
        ('src_url_id', int),
        ('text_hash', str),
        ('text', str),
    )
    URL_DOCUMENT_DEFAULT_GROUP = GROUPS.inlinks
    URL_DOCUMENT_MAPPING = {
        # incoming links, must be internal
        "inlinks_internal.nb.total": {
            "verbose_name": "Number of Internal Incoming Links",
            "type": INT_TYPE,
            "order": 1,
            "settings": {
                ES_DOC_VALUE,
                AGG_NUMERICAL
            }
        },
        "inlinks_internal.nb.unique": {
            "verbose_name": "Unique Number of Internal Incoming Links",
            "type": INT_TYPE,
            "order": 2,
            "settings": {
                ES_DOC_VALUE,
                AGG_NUMERICAL
            }
        },
        "inlinks_internal.nb.follow.unique": {
            "verbose_name": "Unique Number of Follow Internal Incoming Links",
            "type": INT_TYPE,
            "order": 4,
            "settings": {
                ES_DOC_VALUE,
                AGG_NUMERICAL
            }
        },
        "inlinks_internal.nb.follow.total": {
            "verbose_name": "Number of Internal Incoming Follow Links",
            "type": INT_TYPE,
            "order": 3,
            "settings": {
                ES_DOC_VALUE,
                AGG_NUMERICAL
            }
        },
        "inlinks_internal.nb.nofollow.total": {
            "verbose_name": "Number of Internal Incoming NoFollow Links",
            "group": GROUPS.inlinks_nofollow,
            "order": 5,
            "type": INT_TYPE,
            "settings": {
                ES_DOC_VALUE,
                AGG_NUMERICAL
            }
        },
        "inlinks_internal.nb.nofollow.combinations.link": {
            "verbose_name": "Number of NoFollow links strictly in link nofollow",
            "group": GROUPS.inlinks_nofollow,
            "order": 6,
            "type": INT_TYPE,
            "settings": {
                ES_DOC_VALUE,
                AGG_NUMERICAL
            }
        },
        "inlinks_internal.nb.nofollow.combinations.meta": {
            "verbose_name": "Number of NoFollow links strictly in meta nofollow",
            "group": GROUPS.inlinks_nofollow,
            "order": 7,
            "type": INT_TYPE,
            "settings": {
                ES_DOC_VALUE,
                AGG_NUMERICAL
            }
        },
        "inlinks_internal.nb.nofollow.combinations.link_meta": {
            "verbose_name": "Number of NoFollow links both in link and meta nofollow",
            "group": GROUPS.inlinks_nofollow,
            "order": 8,
            "type": INT_TYPE,
            "settings": {
                ES_DOC_VALUE,
                AGG_NUMERICAL
            }
        },
        "inlinks_internal.urls": {
            "verbose_name": "Sample of internal inlinks urls",
            "group": GROUPS.inlinks,
            "order": 9,
            "type": INT_TYPE,
            "settings": {ES_NO_INDEX, LIST, RENDERING.URL}
        },
        "inlinks_internal.urls_exists": {
            "type": "boolean",
            "default_value": None
        }
    }

    def pre_process_document(self, document):
        # temporary structures for analytic processing
        document["processed_inlink_link"] = set()
        # a temp set to track all `seen` src url of incoming links
        document["processed_inlink_url"] = set()

    def process_document(self, document, stream):
        url_dst, link_type, follow_keys, url_src, txt_hash, txt = stream

        if link_type == "a":
            is_follow = len(follow_keys) == 1 and follow_keys[0] == "follow"
            mask = list_to_mask(follow_keys)

            inlink_nb = document['inlinks_internal']['nb']
            inlink_nb['total'] += 1

            follow = inlink_nb['follow' if is_follow else 'nofollow']
            follow['total'] += 1

            if is_follow:
                if not (url_src, mask) in document["processed_inlink_link"]:
                    follow['unique'] += 1
            else:
                key = _get_nofollow_combination_key(follow_keys)
                if 'robots' in key:
                    logger.warn('Skip `robots` mask in inlink mask')
                else:
                    follow['combinations'][key] += 1

            inlink_urls = document['inlinks_internal']['urls']
            exists = (url_src, mask) in document['processed_inlink_link']
            if len(inlink_urls) < 300 and not exists:
                inlink_urls.append([url_src, mask])

            # add src to processed set
            document['processed_inlink_url'].add(url_src)
            document['processed_inlink_link'].add((url_src, mask))

            document['inlinks_internal']['urls_exists'] = True

        elif link_type.startswith('r'):
            # TODO dangerous assumption of crawl's string format to be 'r3xx'
            http_code = int(link_type[1:])
            redirects_from = document['redirect']['from']
            redirects_from['nb'] += 1
            if len(redirects_from['urls']) < 300:
                redirects_from['urls'].append([url_src, http_code])
            redirects_from['urls_exists'] = True

        elif link_type == "canonical":
            canonical_from = document['canonical']['from']

            # only count for none self canonical
            if url_dst != url_src:
                canonical_from['nb'] += 1
                if len(canonical_from['urls']) < 300:
                    canonical_from['urls'].append(url_src)
                canonical_from['urls_exists'] = True

    def post_process_document(self, document):
        # If not "inlinks_internal" : we want to store a non-crawled url
        if not 'inlinks_internal' in document:
            return

        document['inlinks_internal']['nb']['unique'] = len(document['processed_inlink_url'])

        # delete intermediate data structures
        del document['processed_inlink_url']
        del document["processed_inlink_link"]


class OutlinksCountersStreamDef(StreamDefBase):
    FILE = 'url_out_links_counters'
    HEADERS = (
        ('id', int),
        ('follow', follow_mask),
        ('is_internal', _str_to_bool),
        ('score', int),
        ('score_unique', int),
    )


class OutredirectCountersStreamDef(StreamDefBase):
    FILE = 'url_out_redirect_counters'
    HEADERS = (
        ('id', int),
        ('is_internal', _str_to_bool)
    )


class OutcanonicalCountersStreamDef(StreamDefBase):
    FILE = 'url_out_canonical_counters'
    HEADERS = (
        ('id', int),
        ('equals', _str_to_bool)
    )


class InlinksCountersStreamDef(StreamDefBase):
    FILE = 'url_in_links_counters'
    HEADERS = (
        ('id', int),
        ('follow', follow_mask),
        ('score', int),
        ('score_unique', int),
    )


class InredirectCountersStreamDef(StreamDefBase):
    FILE = 'url_in_redirect_counters'
    HEADERS = (
        ('id', int),
        ('score', int)
    )


class IncanonicalCountersStreamDef(StreamDefBase):
    FILE = 'url_in_canonical_counters'
    HEADERS = (
        ('id', int),
        ('score', int)
    )


class BadLinksStreamDef(StreamDefBase):
    FILE = 'urlbadlinks'
    HEADERS = (
        ('id', int),
        ('dst_url_id', int),
        ('http_code', int)
    )
    URL_DOCUMENT_DEFAULT_GROUP = GROUPS.outlinks_internal
    URL_DOCUMENT_MAPPING = {
        # erroneous outgoing internal links
        "outlinks_errors.3xx.nb": {
            "type": INT_TYPE,
            "verbose_name": "Number of error links in 3xx",
            "order": 100,
            "settings": {
                ES_DOC_VALUE,
                AGG_NUMERICAL
            }
        },
        "outlinks_errors.3xx.urls": {
            "type": INT_TYPE,
            "verbose_name": "Sample of error links in 3xx",
            "order": 101,
            "settings": {ES_NO_INDEX, LIST}
        },
        "outlinks_errors.3xx.urls_exists": {
            "type": "boolean",
            "default_value": None
        },

        "outlinks_errors.4xx.nb": {
            "type": INT_TYPE,
            "verbose_name": "Number of error links in 4xx",
            "order": 102,
            "settings": {
                ES_DOC_VALUE,
                AGG_NUMERICAL
            }
        },
        "outlinks_errors.4xx.urls": {
            "type": INT_TYPE,
            "verbose_name": "Sample of error links in 4xx",
            "order": 103,
            "settings": {ES_NO_INDEX, LIST}
        },
        "outlinks_errors.4xx.urls_exists": {
            "type": "boolean",
            "default_value": None
        },

        "outlinks_errors.5xx.nb": {
            "type": INT_TYPE,
            "verbose_name": "Number of error links in 5xx",
            "order": 104,
            "settings": {
                ES_DOC_VALUE,
                AGG_NUMERICAL
            }
        },
        "outlinks_errors.5xx.urls": {
            "type": INT_TYPE,
            "verbose_name": "Sample of error links in 5xx",
            "order": 105,
            "settings": {ES_NO_INDEX, LIST}
        },
        "outlinks_errors.5xx.urls_exists": {
            "type": "boolean",
            "default_value": None
        },
        # total error_links number
        "outlinks_errors.total": {
            "type": "integer",
            "verbose_name": "Number of error links in 3xx/4xx/5xx",
            "order": 99,
            "settings": {
                ES_DOC_VALUE,
                AGG_NUMERICAL
            }
        },
    }

    def process_document(self, document, stream_badlinks):
        _, url_dest_id, http_code = stream_badlinks

        errors = document['outlinks_errors']

        error_kind = None
        if 300 <= http_code < 400:
            error_kind = '3xx'
        elif 400 <= http_code < 500:
            error_kind = '4xx'
        elif http_code >= 500:
            error_kind = '5xx'

        errors[error_kind]['nb'] += 1
        error_urls = errors[error_kind]['urls']
        if len(error_urls) < 10:
            error_urls.append(url_dest_id)

        # increment the consolidate value
        errors['total'] += 1

        errors[error_kind]['urls_exists'] = True


class BadLinksCountersStreamDef(StreamDefBase):
    FILE = 'urlbadlinks_counters'
    HEADERS = (
        ('id', int),
        ('http_code', int),
        ('score', int)
    )
