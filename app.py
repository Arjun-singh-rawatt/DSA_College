from __future__ import annotations

import math
import streamlit as st

from data_loader import DATA_PATH, DataLoadError, Student, load_students
from student_structures import CGPATree, build_lookup, find_student, top_students

st.set_page_config(page_title="Student Performance Dashboard", page_icon="📊", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
html, body, [class*="css"] { font-family: Inter, ui-sans-serif, system-ui, -apple-system, sans-serif; }
.stApp { background: #f7f9fc; color: #111827; }
[data-testid="stSidebar"] { background: #f1f5fb; border-right: 1px solid #e1e7f0; }
[data-testid="stSidebarUserContent"] { padding-top: .35rem !important; }
[data-testid="stSidebar"] > div:first-child { padding-top: .25rem; }
[data-testid="stSidebar"] { color: #111827 !important; }
[data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] b,
[data-testid="stSidebar"] div, [data-testid="stSidebar"] label { color: #111827; }
[data-testid="stMetric"] { background: #fff; border: 1px solid #dfe5ee; border-radius: 12px; padding: 16px 18px; min-height: 112px; box-shadow: 0 1px 2px #172b4d08; }
[data-testid="stMetricLabel"] { color: #64718b; font-size: 14px; }
[data-testid="stMetricValue"] { color: #101828; font-weight: 750; }
[data-testid="stVerticalBlockBorderWrapper"] { background: white; border-color: #dfe5ee !important; border-radius: 12px; }
div.stButton > button[kind="primary"] { background: #0875f5; border-color: #0875f5; border-radius: 7px; font-weight: 600; }
div.stButton > button[kind="primary"], div.stButton > button[kind="primary"] p { color: #fff !important; }
[data-testid="stSidebar"] div.stButton > button[kind="primary"] { min-height: 42px; padding: 8px 12px; }
[data-testid="stSidebar"] div.stButton > button[kind="primary"] p { font-family: Inter, ui-sans-serif, system-ui, sans-serif !important; font-size: 14px !important; font-weight: 600 !important; line-height: 1.25 !important; margin: 0 !important; text-align: center; }
div.stButton > button:not([kind="primary"]) { background: #fff !important; color: #172033 !important; border: 1px solid #cbd5e1 !important; border-radius: 7px; }
div.stButton > button:not([kind="primary"]):hover { background: #f1f5fb !important; color: #111827 !important; border-color: #94a3b8 !important; }
div.stButton > button:disabled, div.stButton > button:disabled p { color: #475569 !important; opacity: 1 !important; }
div.stButton > button p { color: inherit !important; }
[data-testid="stDataFrame"] { border: 1px solid #e3e8ef; border-radius: 8px; overflow: hidden; }
.muted { color: #66738b; }
/* Streamlit's fixed top toolbar is 60px tall and overlays the main block container.
   48px of container padding plus its 16px first-block gap places the heading at y=64px. */
[data-testid="stMainBlockContainer"] { padding-top: 3rem !important; }
[data-testid="stMainBlockContainer"] h1 { margin-top: 0 !important; padding-top: 0 !important; }
/* The sidebar reserves a 60px header above stSidebarUserContent. The branding
   markdown is positioned into that header slot; its navigation flow stays below. */
.sidebar-brand { position: absolute; top: -78px; left: 0; }
@media (max-width: 700px) {
  [data-testid="stMainBlockContainer"] { padding: 3rem .8rem 2rem !important; }
  [data-testid="stSidebarUserContent"] { padding-top: .25rem !important; }
}
</style>
""", unsafe_allow_html=True)

SUBJECTS = ["Operating Systems", "DSA", "Mathematics"]

def initialize():
    try:
        students = load_students()
        st.session_state.students = students
        st.session_state.lookup = build_lookup(students)
        st.session_state.tree = CGPATree(students)
        st.session_state.load_error = None
        st.session_state.rows = sorted(students, key=lambda s: s.erp.casefold())
        st.session_state.mode = "All students"
        st.session_state.detail = None
        st.session_state.notice = ""
        st.session_state.page = 1
    except DataLoadError as exc:
        st.session_state.students = []
        st.session_state.lookup = {}
        st.session_state.tree = CGPATree()
        st.session_state.load_error = str(exc)
        st.session_state.rows = []
        st.session_state.mode = "All students"
        st.session_state.detail = None
        st.session_state.page = 1

if "students" not in st.session_state:
    initialize()

with st.sidebar:
    st.markdown("<div class='sidebar-brand' style='display:flex;gap:12px;align-items:center;margin:0 4px 20px'><div style='flex:0 0 48px;background:#1479f8;color:white;border-radius:12px;width:48px;height:48px;display:flex;align-items:center;justify-content:center;gap:3px'><i style='display:block;width:4px;height:10px;background:white;border-radius:1px'></i><i style='display:block;width:4px;height:17px;background:white;border-radius:1px'></i><i style='display:block;width:4px;height:13px;background:white;border-radius:1px'></i></div><b style='color:#111827;font-size:15px;line-height:1.25'>Intelligent Student<br>Performance Analysis<br>System</b></div>", unsafe_allow_html=True)
    st.button("Dashboard", icon=":material/dashboard:", type="primary", use_container_width=True, disabled=True)
    st.button("Demonstration  -  Coming soon", use_container_width=True, disabled=True)
    st.markdown("<div style='position:fixed;bottom:25px;color:#344054;border-top:1px solid #dfe5ee;padding-top:14px;width:210px'><b>Teacher</b><br><span style='color:#66738b;margin-left:0'>Faculty</span></div>", unsafe_allow_html=True)

head, action = st.columns([6, 1.2], vertical_alignment="center")
with head:
    st.title("Student Performance Dashboard")
    if st.session_state.load_error:
        st.markdown("<span class='muted'>Monitor academic performance and analyze student records.</span>", unsafe_allow_html=True)
    else:
        st.markdown(f"<span class='muted'>Monitor academic performance and analyze student records.</span>　<span style='color:#13803d;background:#e5f7eb;padding:6px 11px;border-radius:7px;font-size:13px'>● Local dataset loaded · {len(st.session_state.students)} records</span>", unsafe_allow_html=True)
with action:
    if st.button("Refresh data", use_container_width=True):
        initialize()
        if st.session_state.load_error:
            st.error(st.session_state.load_error)
        else:
            st.session_state.notice = "Dataset refreshed successfully."
            st.rerun()

if st.session_state.load_error:
    st.error(st.session_state.load_error)
    st.caption(f"Expected format: ERP|Name|CGPA|OperatingSystems|DSA|Mathematics · {DATA_PATH}")
else:
    students: list[Student] = st.session_state.students
    avg_cgpa = sum(s.cgpa for s in students) / len(students)
    best = max(students, key=lambda s: (s.cgpa, tuple(-ord(c) for c in s.erp.casefold())))
    metrics = st.columns(3)
    metrics[0].metric("Total Students", f"{len(students)}", "Across all records")
    metrics[1].metric("Average CGPA", f"{avg_cgpa:.2f}", f"Based on {len(students)} students")
    metrics[2].metric("Highest CGPA", f"{best.cgpa:.2f}", f"ERP: {best.erp}")

    st.markdown("<div style='height:2px'></div>", unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown("### Search and Filters")
        st.caption("Search for a student, find top performers, or filter by marks and CGPA range.")
        search_col, n_col, rank_col = st.columns([1.3, 1.2, 0.9])
        with search_col:
            st.markdown("**Search by ERP / Roll No.**")
            query = st.text_input("ERP or roll number", placeholder="Enter ERP or roll number", label_visibility="collapsed", key="search_text")
            search_clicked = st.button("Search student", type="primary", use_container_width=True, key="search_button")
        with n_col:
            st.markdown("**Top N students**")
            top_n = st.number_input("Top N", min_value=1, max_value=len(students), value=min(5, len(students)), step=1, label_visibility="collapsed")
            top_clicked = st.button("Find top students", type="primary", use_container_width=True)
        with rank_col:
            st.markdown("**Rank students by**")
            metric = st.selectbox("Ranking metric", ["CGPA", *SUBJECTS], label_visibility="collapsed")

        st.divider()
        cg_col, marks_col, exact_col = st.columns([1.1, 1.6, 1.0])
        with cg_col:
            st.markdown("**CGPA range**")
            a, b = st.columns(2)
            cg_min_text = a.text_input("Minimum CGPA", placeholder="Minimum", key="cg_min")
            cg_max_text = b.text_input("Maximum CGPA", placeholder="Maximum", key="cg_max")
            range_clicked = st.button("Find matching students", type="primary", use_container_width=True, key="range_button")
        with marks_col:
            st.markdown("**Subject marks range**")
            a, b, c = st.columns([1.1, 0.9, 0.9])
            subject = a.selectbox("Subject", SUBJECTS)
            mark_min_text = b.text_input("Minimum marks", placeholder="Minimum", key="mark_min")
            mark_max_text = c.text_input("Maximum marks", placeholder="Maximum", key="mark_max")
        with exact_col:
            st.markdown("**Exact marks**")
            exact_text = st.text_input("Exact mark", placeholder="e.g. 40", key="exact_mark")
            count_clicked = st.button("Count matches", type="primary", use_container_width=True)

    def parse_bound(text, label, low, high, as_int=False):
        if not text.strip(): return None
        try:
            number = int(text) if as_int else float(text)
        except ValueError:
            raise ValueError(f"{label} must be {'an integer' if as_int else 'a number'}.")
        if not low <= number <= high: raise ValueError(f"{label} must be between {low} and {high}.")
        return number

    error = None
    try:
        cg_min = parse_bound(cg_min_text, "Minimum CGPA", 0, 10)
        cg_max = parse_bound(cg_max_text, "Maximum CGPA", 0, 10)
        mark_min = parse_bound(mark_min_text, "Minimum marks", 0, 100, True)
        mark_max = parse_bound(mark_max_text, "Maximum marks", 0, 100, True)
        if cg_min is not None and cg_max is not None and cg_min > cg_max: raise ValueError("Minimum CGPA cannot exceed maximum CGPA.")
        if mark_min is not None and mark_max is not None and mark_min > mark_max: raise ValueError("Minimum marks cannot exceed maximum marks.")
    except ValueError as exc:
        error = str(exc)
        cg_min = cg_max = mark_min = mark_max = None

    def filtered():
        candidates = st.session_state.tree.in_range(cg_min, cg_max)
        return [s for s in candidates if (mark_min is None or s.mark(subject) >= mark_min) and (mark_max is None or s.mark(subject) <= mark_max)]

    if error:
        st.warning(error)
        st.session_state.rows = []
        st.session_state.mode = "Invalid range"
        st.session_state.detail = None
        st.session_state.page = 1
    else:
        # Range controls are live. A changed range supersedes any previous one-off query.
        range_signature = (cg_min, cg_max, subject, mark_min, mark_max)
        if st.session_state.get("range_signature") != range_signature:
            st.session_state.range_signature = range_signature
            st.session_state.rows = sorted(filtered(), key=lambda s: s.erp.casefold())
            st.session_state.mode = "Range-filtered students"
            st.session_state.detail = None
            st.session_state.notice = ""
            st.session_state.page = 1
        if search_clicked:
            found = find_student(st.session_state.lookup, query)
            st.session_state.detail = found
            st.session_state.rows = [found] if found else []
            st.session_state.mode = "Student search"
            st.session_state.notice = f"No student found for '{query.strip()}'. Check the ERP or roll number." if found is None else ""
            st.session_state.page = 1
        elif top_clicked:
            candidates = filtered()
            st.session_state.rows = top_students(candidates, int(top_n), metric)
            st.session_state.mode = f"Top {int(top_n)} by {metric}"
            st.session_state.detail = None
            st.session_state.notice = ""
            st.session_state.page = 1
        elif count_clicked:
            try:
                exact = parse_bound(exact_text, "Exact marks", 0, 100, True)
                if exact is None: raise ValueError("Enter an exact mark between 0 and 100.")
                st.session_state.rows = [s for s in st.session_state.tree.in_range(cg_min, cg_max) if s.mark(subject) == exact]
                st.session_state.mode = f"Exact {subject} mark: {exact}"
                st.session_state.detail = None
                st.session_state.notice = f"{len(st.session_state.rows)} students scored exactly {exact} in {subject}."
                st.session_state.page = 1
            except ValueError as exc:
                st.error(str(exc))
        elif range_clicked:
            st.session_state.rows = sorted(filtered(), key=lambda s: s.erp.casefold())
            st.session_state.mode = "CGPA and subject marks range"
            st.session_state.detail = None
            st.session_state.notice = f"{len(st.session_state.rows)} students match the selected CGPA and {subject} marks ranges."
            st.session_state.page = 1

    if st.session_state.notice:
        st.info(st.session_state.notice)
    if st.session_state.detail:
        student = st.session_state.detail
        with st.container(border=True):
            st.markdown(f"### {student.name} - {student.erp}")
            d = st.columns(4)
            d[0].metric("CGPA", f"{student.cgpa:.2f}")
            d[1].metric("Operating Systems", student.operating_systems)
            d[2].metric("DSA", student.dsa)
            d[3].metric("Mathematics", student.mathematics)

    with st.container(border=True):
        title, count = st.columns([3, 1], vertical_alignment="center")
        title.markdown("### Results")
        title.caption(st.session_state.mode)
        count.markdown(f"<div style='text-align:right;color:#66738b;padding-top:12px'>Showing {len(st.session_state.rows)} matching records</div>", unsafe_allow_html=True)
        records = st.session_state.rows
        pages = max(1, math.ceil(len(records) / 8))
        st.session_state.page = min(max(1, st.session_state.get("page", 1)), pages)
        start = (st.session_state.page - 1) * 8
        page_rows = records[start:start + 8]
        if page_rows:
            st.dataframe([{"ERP / Roll No.": s.erp, "CGPA": f"{s.cgpa:.2f}", "Operating Systems": s.operating_systems, "DSA": s.dsa, "Mathematics": s.mathematics} for s in page_rows], hide_index=True, use_container_width=True)
        else:
            st.info("No records match the current criteria.")
        foot, controls = st.columns([4, 2], vertical_alignment="center")
        foot.caption(f"Showing {start + 1 if records else 0}-{min(start + 8, len(records))} of {len(records)} results")
        with controls:
            p1, p2, p3 = st.columns(3)
            if p1.button("Previous", disabled=st.session_state.page <= 1, use_container_width=True):
                st.session_state.page -= 1; st.rerun()
            p2.markdown(f"<div style='text-align:center;padding-top:8px'>{st.session_state.page} / {pages}</div>", unsafe_allow_html=True)
            if p3.button("Next", disabled=st.session_state.page >= pages, use_container_width=True):
                st.session_state.page += 1; st.rerun()
