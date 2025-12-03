from __future__ import annotations

from typing import Iterable, Sequence, Set, Tuple


def states_in_box(
    symb_model,
    box_min: Sequence[float],
    box_max: Sequence[float],
    *,
    contain: bool = False,
) -> Set[Tuple[int, ...]]:
    """
    Collect symbolic states whose partitions intersect (or are contained in) the box.

    Parameters
    ----------
    symb_model : SymbolicModel
        Symbolic model providing discretization data.
    box_min, box_max : sequence of float
        Opposite corners of the box in continuous coordinates.
    contain : bool
        If True, only keep partitions fully contained inside the box.
        If False, keep any partition that intersects the box.
    """

    selected_states: Set[Tuple[int, ...]] = set()
    ksi_all: Iterable[Tuple[int, ...]] = symb_model.getAllStates()
    for ksi in ksi_all:
        if not symb_model.discretizator.KSI.isNullState(ksi):
            state_min, state_max = symb_model.discretizator.KSI.getPartitionMinAndMax(ksi)
            if _boxes_compatible(state_min, state_max, box_min, box_max, contain):
                selected_states.add(ksi)
    return selected_states


def subtract_box(
    base_states: Set[Tuple[int, ...]],
    symb_model,
    box_min: Sequence[float],
    box_max: Sequence[float],
    *,
    contain: bool = False,
) -> Set[Tuple[int, ...]]:
    """
    Remove all states intersecting the box from base_states.

    Parameters are identical to `states_in_box`.
    """

    states_to_remove = states_in_box(symb_model, box_min, box_max, contain=contain)
    return base_states.difference(states_to_remove)


def _boxes_compatible(
    state_min: Sequence[float],
    state_max: Sequence[float],
    box_min: Sequence[float],
    box_max: Sequence[float],
    contain: bool,
) -> bool:
    for idx in range(len(state_min)):
        if contain:
            if not (box_min[idx] <= state_min[idx] and state_max[idx] <= box_max[idx]):
                return False
        else:
            if state_max[idx] <= box_min[idx] or state_min[idx] >= box_max[idx]:
                return False
    return True

