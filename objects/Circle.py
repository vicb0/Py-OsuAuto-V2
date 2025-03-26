from objects.Metadata import Metadata
from objects.HitObject import HitObject


class Circle(HitObject):
    def __init__(self, x, y, offset):
        super().__init__(x, y, offset)
        
        self.object_type = 1

    def stack(self):
        self.point.x -= self.stack_id * Metadata.stack_offset
        self.point.y -= self.stack_id * Metadata.stack_offset
