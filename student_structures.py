"""Purposeful lookup, CGPA range, and heap ranking structures."""
from __future__ import annotations

import heapq
from dataclasses import dataclass, field
from typing import Iterable

from data_loader import Student, normalize_erp


class CGPANode:
    def __init__(self, student: Student):
        self.key = (student.cgpa, student.erp.casefold())
        self.student = student
        self.left: CGPANode | None = None
        self.right: CGPANode | None = None


class CGPATree:
    """Unbalanced BST keyed by (CGPA, normalized ERP), retaining duplicate GPAs."""
    def __init__(self, students: Iterable[Student] = ()):
        self.root: CGPANode | None = None
        for student in students:
            self.insert(student)

    def insert(self, student: Student) -> None:
        node = CGPANode(student)
        if self.root is None:
            self.root = node
            return
        current = self.root
        while True:
            if node.key < current.key:
                if current.left is None:
                    current.left = node
                    return
                current = current.left
            else:
                if current.right is None:
                    current.right = node
                    return
                current = current.right

    def in_range(self, minimum: float | None = None, maximum: float | None = None) -> list[Student]:
        result: list[Student] = []
        def visit(node: CGPANode | None) -> None:
            if node is None:
                return
            if minimum is None or node.student.cgpa >= minimum:
                visit(node.left)
            if (minimum is None or node.student.cgpa >= minimum) and (maximum is None or node.student.cgpa <= maximum):
                result.append(node.student)
            if maximum is None or node.student.cgpa <= maximum:
                visit(node.right)
        visit(self.root)
        return result


def build_lookup(students: Iterable[Student]) -> dict[str, Student]:
    return {normalize_erp(student.erp): student for student in students}


def find_student(index: dict[str, Student], erp: str) -> Student | None:
    query = erp.strip()
    student = index.get(normalize_erp(query))
    if student is None and query.isdecimal():
        student = index.get(normalize_erp(f"ST-{int(query):03d}"))
    return student


_METRICS = {"CGPA": lambda s: s.cgpa, "Operating Systems": lambda s: s.operating_systems,
            "DSA": lambda s: s.dsa, "Mathematics": lambda s: s.mathematics}


def top_students(students: Iterable[Student], count: int, metric: str) -> list[Student]:
    """Max-priority retrieval with ERP ascending tie-breaks."""
    if metric not in _METRICS:
        raise ValueError(f"Unknown ranking metric: {metric}")
    heap = [(-_METRICS[metric](s), s.erp.casefold(), s) for s in students]
    heapq.heapify(heap)
    return [heapq.heappop(heap)[2] for _ in range(min(count, len(heap)))]
