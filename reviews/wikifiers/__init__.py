from collections import namedtuple

from typing import List

Entity = namedtuple('Entity', ['phrase', 'kb_id', 'kb_url'])


class Wikifier:

    def wikify(self, text) -> List[Entity]:
        raise NotImplementedError
