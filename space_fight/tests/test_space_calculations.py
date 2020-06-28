from .. import space
import pytest  # type: ignore
import random as rand
import math


@pytest.mark.parametrize('entry_a', [rand.random() for _ in range(3)])
@pytest.mark.parametrize('entry_b', [rand.random() for _ in range(3)])
def test_position_sum(entry_a, entry_b):
    position_a = space.Position(entry_a, 0, 0)
    position_b = space.Position(entry_b, 0, 0)
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
    pos_a = space.Position(entry_a, 0, 0)
    pos_b = space.Position(entry_b, 0, 0)
    pos_c = space.Position(entry_c, 0, 0)

    seg_ab = space.LineSegment(pos_a, pos_b)
    seg_ac = space.LineSegment(pos_a, pos_c)
    seg_bc = space.LineSegment(pos_b, pos_c)

    segment_list = [seg_ab, seg_bc, seg_ac]
    distance_list = [segment.distance for segment in segment_list]
    bigger = max(distance_list)

    assert round(bigger*2, 5) == round(sum(distance_list), 5)


def test_line_segment_scale_1D():
    pos_o = space.Position(0, 0, 0)
    pos_a = space.Position(4, 0, 0)
    seg = space.LineSegment(pos_o, pos_a)

    scale_seg = seg.scale(1)
    assert scale_seg.destin.x == 1


def test_line_segment_scale_2D():
    pos_o = space.Position(0, 0, 0)
    pos_a = space.Position(1, 1, 0)
    seg = space.LineSegment(pos_o, pos_a)

    scale_seg = seg.scale(1)
    assert scale_seg.destin.x == scale_seg.destin.y
    assert round(scale_seg.destin.x, 5) == round(math.sin(math.pi/4), 5)
    assert round(scale_seg.destin.y, 5) == round(math.cos(math.pi/4), 5)


def test_line_segment_scale_3D():
    pos_o = space.Position(0, 0, 0)
    pos_a = space.Position(1, 1, 1)
    seg = space.LineSegment(pos_o, pos_a)

    scale_seg = seg.scale(1)
    assert scale_seg.destin.x == scale_seg.destin.y == scale_seg.destin.z
    assert round(scale_seg.destin.x, 5) == round(math.sqrt(1/3), 5)
    assert round(scale_seg.destin.y, 5) == round(math.sqrt(1/3), 5)
    assert round(scale_seg.destin.z, 5) == round(math.sqrt(1/3), 5)


def test_line_segment_scale_3D_irregular():
    pos_o = space.Position(0, 0, 0)
    pos_a = space.Position(1, 2, 3)
    seg = space.LineSegment(pos_o, pos_a)

    scale_seg = seg.scale(1)
    assert round(scale_seg.destin.x, 5) == round(math.sqrt(1/14), 5)
    assert round(scale_seg.destin.y, 5) == round(math.sqrt(4/14), 5)
    assert round(scale_seg.destin.z, 5) == round(math.sqrt(9/14), 5)


def test_line_segment_scale_3D_irregular_out_of_origin():
    pos_o = space.Position(1, 1, 1)
    pos_a = space.Position(2, 3, 4)
    seg = space.LineSegment(pos_o, pos_a)

    scale_seg = seg.scale(1)
    assert round(scale_seg.destin.x, 5) == 1 + round(math.sqrt(1/14), 5)
    assert round(scale_seg.destin.y, 5) == 1 + round(math.sqrt(4/14), 5)
    assert round(scale_seg.destin.z, 5) == 1 + round(math.sqrt(9/14), 5)
