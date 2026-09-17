# Intelligent Student Performance Analysis System

## 1. Project Overview

The **Intelligent Student Performance Analysis System** is a DSA-based academic performance management and analysis system designed to organize student records and provide simple performance-related insights.

The system focuses on efficient storage, searching, ordering, ranking, and relationship traversal using fundamental Data Structures and Algorithms.

For the current prototype, a small dataset of **10 students** is considered. Each student record contains:

- Student Name
- Roll Number
- CGPA
- DSA Marks
- Operating Systems (OS) Marks

The system does not attempt to classify students into labels such as "weak", "average", or "excellent". Instead, it focuses on organizing academic information and efficiently retrieving useful performance information.

---

## 2. Problem Statement

Managing student academic records using only basic sequential storage can become inefficient when searching, ordering, ranking, and analyzing records.

The proposed system applies appropriate DSA techniques to solve these operations efficiently.

The system is designed to answer questions such as:

- What are the details of a particular student?
- How are students ordered according to CGPA?
- Who are the top-performing students?
- What is the performance of students in DSA and Operating Systems?
- How can the relationship between DSA and Operating Systems be represented and traversed?

---

## 3. Motivation

Students and faculty regularly work with academic information such as marks and CGPA. Although the dataset used in this prototype is small, the project demonstrates how different data structures can be selected according to different computational requirements.

Instead of using one data structure for every operation, the system maps individual requirements to suitable DSA concepts.

For example:

- Fast student lookup → `unordered_map`
- CGPA-based organization → `BST`
- Top-student retrieval → `Max Heap / Priority Queue`
- Subject relationship representation → `Graph`
- Relationship traversal → `BFS / DFS`

This makes the project a practical demonstration of DSA concepts in an academic domain.

---

## 4. Objectives

The major objectives of the project are:

1. Store student academic records efficiently.
2. Provide fast access to student records using roll number.
3. Organize students according to CGPA.
4. Retrieve top-performing students using a priority-based structure.
5. Represent the relationship between DSA and Operating Systems using a graph.
6. Demonstrate BFS and DFS traversal on the subject relationship graph.
7. Study and compare the time complexity of the selected DSA operations.

---

## 5. Dataset

The prototype currently considers **10 student records**.

Each record contains the following fields:

| Field | Description |
|---|---|
| Name | Name of the student |
| Roll Number | Unique student identifier used for lookup |
| CGPA | Overall academic performance measure |
| DSA Marks | Marks obtained in Data Structures and Algorithms |
| OS Marks | Marks obtained in Operating Systems |

### Example Record

```text
Roll No. : 2501330120001
Name     : Student A
CGPA     : 8.42
DSA      : 86
OS       : 78
