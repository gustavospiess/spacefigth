from .. import space
import pytest  # type: ignore
import random as rand
import math


@pytest.mark.parametrize('entry_a', [rand.random() for _ in range(3)])
@pytest.mark.parametrize('entry_b', [rand.random() for _ in range(3)])
def test_position_sum(entry_a, entry_b):
    position_a = space.Position3D(entry_a, 0, 0)
    position_b = space.Position3D(entry_b, 0, 0)
    position_ab = position_a.add(position_b)
    position_ba = position_b.add(position_a)
    assert position_ab.x == entry_a + entry_b
    assert position_ab == position_ba
    assert hash(position_ab) == hash(position_ba)
    assert repr(position_ab) == repr(position_ba)


@pytest.mark.parametrize('entry_a', [rand.random() for _ in range(3)])
@pytest.mark.parametrize('entry_b', [rand.random() for _ in range(3)])
@pytest.mark.parametrize('entry_c', [rand.random() for _ in range(3)])
def test_line_segment_distance(entry_a, entry_b, entry_c):
    """the distance for the tree lines ab, bc and ca where a, b and c are align
    is summed to twice the distance of the bigger segment"""
    pos_a = space.Position3D(entry_a, 0, 0)
    pos_b = space.Position3D(entry_b, 0, 0)
    pos_c = space.Position3D(entry_c, 0, 0)

    seg_ab = space.LineSegment(pos_a, pos_b)
    seg_ac = space.LineSegment(pos_a, pos_c)
    seg_bc = space.LineSegment(pos_b, pos_c)

    segment_list = [seg_ab, seg_bc, seg_ac]
    distance_list = [segment.distance for segment in segment_list]
    bigger = max(distance_list)

    assert round(bigger*2, 5) == round(sum(distance_list), 5)


def test_line_segment_scale_1D():
    pos_o = space.Position3D(0, 0, 0)
    pos_a = space.Position3D(4, 0, 0)
    seg = space.LineSegment(pos_o, pos_a)

    scale_seg = seg.resize(1)
    assert scale_seg.destin.x == 1


def test_line_segment_scale_2D():
    pos_o = space.Position3D(0, 0, 0)
    pos_a = space.Position3D(1, 1, 0)
    seg = space.LineSegment(pos_o, pos_a)

    scale_seg = seg.resize(1)
    assert scale_seg.destin.x == scale_seg.destin.y
    assert round(scale_seg.destin.x, 5) == round(math.sin(math.pi/4), 5)
    assert round(scale_seg.destin.y, 5) == round(math.cos(math.pi/4), 5)


def test_line_segment_scale_3D():
    pos_o = space.Position3D(0, 0, 0)
    pos_a = space.Position3D(1, 1, 1)
    seg = space.LineSegment(pos_o, pos_a)

    scale_seg = seg.resize(1)
    assert scale_seg.destin.x == scale_seg.destin.y == scale_seg.destin.z
    assert round(scale_seg.destin.x, 5) == round(math.sqrt(1/3), 5)
    assert round(scale_seg.destin.y, 5) == round(math.sqrt(1/3), 5)
    assert round(scale_seg.destin.z, 5) == round(math.sqrt(1/3), 5)


def test_line_segment_scale_3D_irregular():
    pos_o = space.Position3D(0, 0, 0)
    pos_a = space.Position3D(1, 2, 3)
    seg = space.LineSegment(pos_o, pos_a)

    scale_seg = seg.resize(1)
    assert round(scale_seg.destin.x, 5) == round(math.sqrt(1/14), 5)
    assert round(scale_seg.destin.y, 5) == round(math.sqrt(4/14), 5)
    assert round(scale_seg.destin.z, 5) == round(math.sqrt(9/14), 5)


def test_line_segment_scale_3D_irregular_out_of_origin():
    pos_o = space.Position3D(1, 1, 1)
    pos_a = space.Position3D(2, 3, 4)
    seg = space.LineSegment(pos_o, pos_a)

    scale_seg = seg.resize(1)
    assert round(scale_seg.destin.x, 5) == 1 + round(math.sqrt(1/14), 5)
    assert round(scale_seg.destin.y, 5) == 1 + round(math.sqrt(4/14), 5)
    assert round(scale_seg.destin.z, 5) == 1 + round(math.sqrt(9/14), 5)


def test_line_segment_distance_to():
    pos_o = space.Position3D(0, 0, 0)
    pos_a = space.Position3D(2, 0, 0)
    pos_b = space.Position3D(1, 0, 0)
    seg = space.LineSegment(pos_o, pos_a)
    distance = seg.distance_to(pos_b)
    pos = seg.closest_point_inline(pos_b)

    assert distance == 0
    assert pos == pos_b


def test_line_segment_distance_to_2():
    pos_o = space.Position3D(0, 0, 0)
    pos_a = space.Position3D(2, 0, 0)
    pos_b = space.Position3D(0, 1, 0)
    seg = space.LineSegment(pos_o, pos_a)
    distance = seg.distance_to(pos_b)
    pos = seg.closest_point_inline(pos_b)

    assert distance == 1
    assert pos == (0, 0, 0)


def test_line_segment_distance_to_3():
    pos_o = space.Position3D(0, 0, 0)
    pos_a = space.Position3D(2, 0, 0)
    pos_b = space.Position3D(1, 1, 0)
    seg = space.LineSegment(pos_o, pos_a)
    distance = seg.distance_to(pos_b)
    pos = seg.closest_point_inline(pos_b)

    assert distance == 1
    assert pos == (1, 0, 0)
