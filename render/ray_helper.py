from contextlib import contextmanager
from inspect import isbuiltin
from typing import Callable, Any, Generator, Self

import raylib as rayc


layer: dict[int, list[tuple[Callable, list, dict]]] = {}


class _DrawFunctionBase:
    from raylib import (
        DrawBillboard, DrawBillboardPro, DrawBillboardRec, DrawBoundingBox, DrawCapsule,
        DrawCapsuleWires, DrawCircle, DrawCircle3D, DrawCircleGradient, DrawCircleLines,
        DrawCircleLinesV, DrawCircleSector, DrawCircleSectorLines, DrawCircleV, DrawCube, DrawCubeV,
        DrawCubeWires, DrawCubeWiresV, DrawCylinder, DrawCylinderEx, DrawCylinderWires,
        DrawCylinderWiresEx, DrawEllipse, DrawEllipseLines, DrawFPS, DrawGrid, DrawLine, DrawLine3D,
        DrawLineBezier, DrawLineEx, DrawLineStrip, DrawLineV, DrawMesh, DrawMeshInstanced, DrawModel,
        DrawModelEx, DrawModelPoints, DrawModelPointsEx, DrawModelWires, DrawModelWiresEx, DrawPixel,
        DrawPixelV, DrawPlane, DrawPoint3D, DrawPoly, DrawPolyLines, DrawPolyLinesEx, DrawRay,
        DrawRectangle, DrawRectangleGradientEx, DrawRectangleGradientH, DrawRectangleGradientV,
        DrawRectangleLines, DrawRectangleLinesEx, DrawRectanglePro, DrawRectangleRec,
        DrawRectangleRounded, DrawRectangleRoundedLines, DrawRectangleRoundedLinesEx, DrawRectangleV,
        DrawRing, DrawRingLines, DrawSphere, DrawSphereEx, DrawSphereWires, DrawSplineBasis,
        DrawSplineBezierCubic, DrawSplineBezierQuadratic, DrawSplineCatmullRom, DrawSplineLinear,
        DrawSplineSegmentBasis, DrawSplineSegmentBezierCubic, DrawSplineSegmentBezierQuadratic,
        DrawSplineSegmentCatmullRom, DrawSplineSegmentLinear, DrawText, DrawTextCodepoint,
        DrawTextCodepoints, DrawTextEx, DrawTextPro, DrawTexture, DrawTextureEx, DrawTextureNPatch,
        DrawTexturePro, DrawTextureRec, DrawTextureV, DrawTriangle, DrawTriangle3D, DrawTriangleFan,
        DrawTriangleLines, DrawTriangleStrip, DrawTriangleStrip3D
    )


class Pen(_DrawFunctionBase):
    _instance: dict[int, "Pen"] = {}

    def __new__(cls, index: int) -> Self:
        instance = cls._instance.get(index, None)
        if instance is None:
            cls._instance[index] = (instance := super().__new__(cls))
            print("Pen created! layer: %s" % index)

        return instance


    def __init__(self, index: int) -> None:
        self.index = index

        for func_name, func in _DrawFunctionBase.__dict__.items():
            if not isbuiltin(func): continue
            setattr(
                self, func_name, self._build_func(func)
            )

    def _build_func(self, func: Callable) -> Callable:
        return lambda *args, **kwargs: layer.setdefault(self.index, []).append((func, args, kwargs))


def overlay_init(width: int, height: int, title: str = "AK32767") -> None:
    rayc.SetConfigFlags(
        rayc.FLAG_WINDOW_TRANSPARENT | rayc.FLAG_WINDOW_MOUSE_PASSTHROUGH | rayc.FLAG_WINDOW_TOPMOST | rayc.FLAG_WINDOW_UNDECORATED)
    rayc.InitWindow(width, height, title.encode("utf8"))


def overlay_loop() -> bool:
    return not rayc.WindowShouldClose()


@contextmanager
def on_draw() -> Generator[None, None, None]:
    rayc.BeginDrawing()
    rayc.ClearBackground(rayc.BLANK)
    try:
        yield None
    finally:
        if len(layer):
            try:
                for index in sorted(layer.keys()):
                    for func_name, args, kwargs in layer.pop(index):
                        func_name(*args, **kwargs)
            except Exception as err:
                print("[ray] cannot draw! %s" % err)
            finally: layer.clear()

        rayc.EndDrawing()


@contextmanager
def create_layer(index: int) -> Generator[Pen, None, None]:
    layer.setdefault(index, [])

    try:
        yield Pen(index)
    finally:
        ...