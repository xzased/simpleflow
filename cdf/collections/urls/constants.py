QUERY_URLS_FIELDS = (
    "url",
    "protocol",
    "path",
    "query",
    "query_string_keys",
    "query_string_keys_order",
    "query_string_items",
    "date_crawled",
    "depth",
    "http_code",
    "delay1",
    "delay2",
    "outlinks_internal_follow_nb",
    "outlinks_internal_nofollow_nb",
    "outlinks_external_follow_nb",
    "outlinks_external_nofollow_nb",
    "bytesize",
    "inlinks_nb",
    "inlinks_follow_nb",
    "metadata.title",
    "metadata.description",
    "metadata.h1",
    "metadata.h2",
    "metadata_nb.title",
    "metadata_nb.description",
    "metadata_nb.h1",
    "metadata_nb.h2",
    "metadata_duplicate.h1",
    "metadata_duplicate.title",
    "metadata_duplicate.description",
    "metadata_duplicate_nb.h1",
    "metadata_duplicate_nb.title",
    "metadata_duplicate_nb.description",
    "outlinks_follow_urls",
    "outlinks_nofollow_urls",
    "inlinks_follow_urls",
    "inlinks_nofollow_urls",
    "redirect_from",
    "redirect_to",
    "canonical_url",
    "redirects_nb"
)

QUERY_TAGGING_FIELDS = (
    'resource_type',
)

QUERY_URLS_IDS = (
    "metadata_duplicate.h1",
    "metadata_duplicate.title",
    "metadata_duplicate.description",
    "redirect_to.url",
)