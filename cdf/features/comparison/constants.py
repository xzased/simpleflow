from enum import Enum

# Separator for encoding the url_id with the url string
# 2 conditions:
#   - not a valid char in url string
#   - does not alter the url string ordering
# with above in mind, `\0` seems to be the best choice
SEPARATOR = '\0'


class MatchingState(Enum):
    MATCH = 1
    DISCOVER = 2
    DISAPPEAR = 3