from game.components.collider import Collider
from util.vec2 import Vec2


class Physics:
    def __init__(self, colliders: list[Collider]):
        self.colliders = colliders

    def find_cols(self, col: Collider, layers: list[int]):
        hits = []
        for other in self.colliders:
            if other.layer in layers and Physics.col_col(col, other):
                hits.append(other)

        return hits

    def point_in_collider(collider: Collider, point: Vec2) -> bool:
        if collider.type == "circle":
            return (point - collider.pos).r < collider.radius
        else:
            return point.x > collider.bl.x and point.x < collider.tr.x and point.y > collider.bl.y and point.y < collider.tr.y

    def circle_rect(circle: Collider, rect: Collider):
        closestPoint = Vec2(min(max(circle.pos.x, rect.left), rect.right), min(max(circle.pos.y, rect.bottom), rect.top))
        return (circle.pos - closestPoint).r < circle.radius

    def rect_rect(rect1, rect2):
        return (
            Physics.point_in_collider(rect1, rect2.bl)
            or Physics.point_in_collider(rect1, rect2.tl)
            or Physics.point_in_collider(rect1, rect2.br)
            or Physics.point_in_collider(rect1, rect2.tr)
            or Physics.point_in_collider(rect2, rect1.bl)
            or Physics.point_in_collider(rect2, rect1.tl)
            or Physics.point_in_collider(rect2, rect1.br)
            or Physics.point_in_collider(rect2, rect1.tr)
        )

    def circle_circle(circ1: Collider, circ2: Collider):
        return (circ1.pos - circ2.pos).r < circ1.radius + circ2.radius

    def col_col(col_a: Collider, col_b: Collider) -> bool:
        if col_a.type == "rect":
            if col_b.type == "rect":
                return Physics.rect_rect(col_a, col_b)
            else:
                return Physics.circle_rect(col_b, col_a)
        else:
            if col_b.type == "rect":
                return Physics.circle_rect(col_a, col_b)
            else:
                return Physics.circle_circle(col_a, col_b)

    def move(self, col: Collider, disp: Vec2, layers: list[int]):
        origin = col.pos.copy()

        col.pos += disp * Vec2(1, 0)

        for other in self.colliders:
            if other == col or not other.layer in layers:
                continue
            if Physics.col_col(col, other):
                col.pos.set(origin)

        origin2 = col.pos.copy()

        col.pos += disp * Vec2(0, 1)

        for other in self.colliders:
            if other == col or not other.layer in layers:
                continue
            if Physics.col_col(col, other):
                col.pos.set(origin2)
        return (col.pos - origin).r
