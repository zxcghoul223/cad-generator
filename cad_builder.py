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


BUILDERS = {
    "box": build_box,
    "bracket": build_bracket,
}


def build(part_name: str, params: dict):
    builder = BUILDERS.get(part_name)
    if builder is None:
        raise ValueError(f"unknown part: {part_name}")
    return builder(**params)


def export(part, path: str):
    exporters.export(part, path)
