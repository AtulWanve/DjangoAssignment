from dataclasses import dataclass
from typing import List, Tuple, Optional

@dataclass
class Space:
    width: float
    height: float
    length: float

    def can_fit(self, item_w: float, item_h: float, item_l: float) -> bool:
        return self.width >= item_w and self.height >= item_h and self.length >= item_l


@dataclass
class Item:
    width: float
    height: float
    length: float

    def get_rotations(self) -> List[Tuple[float, float, float]]:
        """Returns all 6 unique 3D rotations of the item's dimensions."""
        dims = [self.width, self.height, self.length]
        # We sort them to avoid checking identical rotations if it's a cube
        import itertools
        rotations = list(set(itertools.permutations(dims)))
        # Sort so we try the "flattest" orientations first (largest footprint)
        rotations.sort(key=lambda x: (x[0], x[1]), reverse=True)
        return rotations


class Packer:
    def __init__(self, box_w: float, box_h: float, box_l: float):
        self.spaces: List[Space] = [Space(box_w, box_h, box_l)]

    def pack_item(self, item: Item) -> bool:
        """
        Attempts to pack an item into the available spaces.
        Returns True if successful, False if the item cannot fit anywhere.
        """
        rotations = item.get_rotations()

        for i, space in enumerate(self.spaces):
            for rot_w, rot_h, rot_l in rotations:
                if space.can_fit(rot_w, rot_h, rot_l):
                    # It fits! Remove this space and create up to 3 new ones (Guillotine Split)
                    del self.spaces[i]
                    self._split_space(space, rot_w, rot_h, rot_l)
                    return True
        return False

    def _split_space(self, space: Space, item_w: float, item_h: float, item_l: float):
        """
        Splits the remaining empty air in `space` into 3 new rectangular spaces
        after placing an item of dimensions item_w x item_h x item_l in its corner.
        """
        # 1. Top Space (Directly above the item)
        if space.height > item_h:
            self.spaces.append(Space(item_w, space.height - item_h, item_l))

        # 2. Right Space (To the right of the item, full height of the original space, length of item)
        if space.width > item_w:
            self.spaces.append(Space(space.width - item_w, space.height, item_l))

        # 3. Front Space (In front of the item, full width, full height, remaining length)
        if space.length > item_l:
            self.spaces.append(Space(space.width, space.height, space.length - item_l))

        # Note: We sort spaces by volume (smallest first) to encourage tight packing
        # and prevent fragmenting our largest spaces early on.
        self.spaces.sort(key=lambda s: s.width * s.height * s.length)


def pack_order_into_box(box, products) -> bool:
    """
    Given a Django Box instance and a list of Product instances,
    determines if all products can be packed into the box.
    """
    total_weight = sum(p.weight for p in products)
    if total_weight > box.max_weight:
        return False

    packer = Packer(box.width, box.height, box.length)

    # Sort products by volume descending (pack biggest items first)
    sorted_products = sorted(products, key=lambda p: p.width * p.height * p.length, reverse=True)

    for product in sorted_products:
        item = Item(product.width, product.height, product.length)
        if not packer.pack_item(item):
            return False

    return True
