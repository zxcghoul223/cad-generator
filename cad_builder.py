import math

import cadquery as cq
from cadquery import exporters


def build_box(**p):
    """Parametric box."""
    w, h, t = p["w"], p["h"], p["t"]
    return cq.Workplane("XY").box(w, h, t)


def build_bracket(**p):
    """Parametric bracket: plate with a hole."""
    w, h, t, hole_d = p["w"], p["h"], p["t"], p["hole_d"]
    return (
        cq.Workplane("XY")
        .box(w, h, t)
        .faces(">Z")
        .workplane()
        .hole(hole_d)
    )


def _star_vertices(points: int, r_out: float, r_in: float):
    """Вершины звезды: points внешних лучей, чередуя внешний/внутренний радиус."""
    if points < 2:
        raise ValueError("points must be >= 2")
    if not (0 < r_in < r_out):
        raise ValueError("need 0 < r_in < r_out")
    total = points * 2
    step = 2 * math.pi / total
    start = math.pi / 2
    verts = []
    for i in range(total):
        angle = start + i * step
        radius = r_out if i % 2 == 0 else r_in
        verts.append((radius * math.cos(angle), radius * math.sin(angle)))
    return verts


def build_star(**p):
    points = int(p["points"])
    r_out, r_in, t = p["r_out"], p["r_in"], p["t"]
    verts = _star_vertices(points, r_out, r_in)
    return cq.Workplane("XY").polyline(verts).close().extrude(t)


BUILDERS = {
    "box": build_box,
    "bracket": build_bracket,
    "star": build_star,
}


def build(part_name: str, params: dict):
    builder = BUILDERS.get(part_name)
    if builder is None:
        raise ValueError(f"unknown part: {part_name}")
    return builder(**params)


def export(part, path: str):
    exporters.export(part, path)
