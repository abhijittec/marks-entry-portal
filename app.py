import streamlit as st
import pandas as pd
import os

FILE_NAME = "Students_Project_Marks.xlsx"

# Page configuration for cross-device responsiveness
st.set_page_config(page_title="Project Marks Portal", layout="centered", initial_sidebar_state="collapsed")

# Simple security implementation (Update credentials for your faculty)
FACULTY_PASSWORD = "FacultyPanel2026"

def check_password():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    
    if not st.session_state.authenticated:
        st.title("🔒 Faculty Entry Portal")
        pwd = st.text_input("Enter Faculty Access Password:", type="password")
        if st.button("Login"):
            if pwd == FACULTY_PASSWORD:
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Incorrect password. Please try again.")
        return False
    return True

if check_password():
    # Load DataFrame safely
    if not os.path.exists(FILE_NAME):
        st.error(f"Database error: '{FILE_NAME}' not found on the server cluster.")
        st.stop()
        
    df = pd.read_excel(FILE_NAME, header=None)

    st.title("🎓 Project Marks Entry Desk")
    st.markdown("Select a student slot to view data, fill evaluations, and commit updates instantly.")

    # 1. Selection Core
    sno = st.selectbox("🎯 Choose Student Slot (S.No):", options=[str(i) for i in range(1, 116)])
    row_idx = int(sno) + 2  # Offsets headers

    # Schema configuration
    FIELDS = {
        1: ('Registration No.', None), 2: ('Student Name', None), 3: ('Section', None), 4: ('Internal Guide', None),
        5: ('MT Ind: TK', 5), 6: ('MT Ind: PM', 10), 7: ('MT Ind: DD', 10), 8: ('MT Ind: RW', 5),
        10: ('MT Uni: TK', 5), 11: ('MT Uni: PM', 10), 12: ('MT Uni: DD', 5),
        14: ('MT Report: TK', 5), 15: ('MT Report: PM', 10), 16: ('MT Report: DD', 10),
        18: ('MT Panel: TK', 5), 19: ('MT Panel: DD', 5), 20: ('MT Panel: RD', 5), 21: ('MT Panel: RW', 5), 22: ('MT Panel: PS', 5),
        25: ('Final Ind: TK', 20), 26: ('Final Ind: PM', 60), 27: ('Final Ind: DD', 20), 28: ('Final Ind: RD', 10),
        30: ('Final Uni: PM', 10), 31: ('Final Uni: DD', 10),
        33: ('Final Report: DD', 10), 34: ('Final Report: RD', 15), 35: ('Final Report: RW', 10),
        37: ('Final Ext: DD', 20), 38: ('Final Ext: RD', 20), 39: ('Final Ext: RW', 20),
        41: ('Final Panel: TK', 20), 42: ('Final Panel: DD', 10), 43: ('Final Panel: RD', 10), 44: ('Final Panel: PS', 35)
    }

    updated_vals = {}

    st.markdown("---")
    
    # 2. Student Meta Section
    st.subheader("📋 Student Profile")
    
    # Let Streamlit handle responsive column layouts automatically
    meta_cols = st.columns([2, 2, 1, 2])
    
    with meta_cols[0]:
        updated_vals[1] = st.text_input(FIELDS[1][0], value=str(df.iloc[row_idx, 1]) if pd.notna(df.iloc[row_idx, 1]) else "")
    with meta_cols[1]:
        updated_vals[2] = st.text_input(FIELDS[2][0], value=str(df.iloc[row_idx, 2]) if pd.notna(df.iloc[row_idx, 2]) else "")
    with meta_cols[3]:
        updated_vals[3] = st.text_input(FIELDS[3][0], value=str(df.iloc[row_idx, 3]) if pd.notna(df.iloc[row_idx, 3]) else "")
    with meta_cols[3]:
        updated_vals[4] = st.text_input(FIELDS[4][0], value=str(df.iloc[row_idx, 4]) if pd.notna(df.iloc[row_idx, 4]) else "")

    # 3. Input Panels split up transparently
    with st.expander("⏱️ Part A: Mid-Term Evaluation Inputs (Max 100)", expanded=True):
        mt_cols = st.columns(2)
        with mt_cols[0]:
            st.markdown("**Guide Metrics**")
            for c in [5,6,7,8,10,11,12]:
                cur = float(df.iloc[row_idx, c]) if pd.notna(df.iloc[row_idx, c]) else 0.0
                updated_vals[c] = st.number_input(f"{FIELDS[c][0]} (Max {FIELDS[c][1]})", 0.0, float(FIELDS[c][1]), cur, step=0.5)
        with mt_cols[1]:
            st.markdown("**Report & Panel Viva Metrics**")
            for c in [14,15,16,18,19,20,21,22]:
                cur = float(df.iloc[row_idx, c]) if pd.notna(df.iloc[row_idx, c]) else 0.0
                updated_vals[c] = st.number_input(f"{FIELDS[c][0]} (Max {FIELDS[c][1]})", 0.0, float(FIELDS[c][1]), cur, step=0.5)

    with st.expander("🏆 Part B: Final Presentation Inputs (Max 300)", expanded=False):
        fn_cols = st.columns(2)
        with fn_cols[0]:
            st.markdown("**Internal/Industry Evaluators**")
            for c in [25,26,27,28,30,31,33,34,35]:
                cur = float(df.iloc[row_idx, c]) if pd.notna(df.iloc[row_idx, c]) else 0.0
                updated_vals[c] = st.number_input(f"{FIELDS[c][0]} (Max {FIELDS[c][1]})", 0.0, float(FIELDS[c][1]), cur, step=0.5)
        with fn_cols[1]:
            st.markdown("**External Board & Panel Viva**")
            for c in [37,38,39,41,42,43,44]:
                cur = float(df.iloc[row_idx, c]) if pd.notna(df.iloc[row_idx, c]) else 0.0
                updated_vals[c] = st.number_input(f"{FIELDS[c][0]} (Max {FIELDS[c][1]})", 0.0, float(FIELDS[c][1]), cur, step=0.5)

    # 4. Save and Recalculate Sequence
    st.markdown("###")
    if st.button("💾 Submit & Synchronize Marks to Sheet", use_container_width=True, type="primary"):
        for col, val in updated_vals.items():
            df.iloc[row_idx, col] = val
            
        # Lambda function for safety checks during calculations
        f_val = lambda c: float(df.iloc[row_idx, c] if pd.notna(df.iloc[row_idx, c]) else 0)
        
        # Aggregate Mid Term Metrics
        df.iloc[row_idx, 9] = f_val(5) + f_val(6) + f_val(7) + f_val(8)
        df.iloc[row_idx, 13] = f_val(10) + f_val(11) + f_val(12)
        df.iloc[row_idx, 17] = f_val(14) + f_val(15) + f_val(16)
        df.iloc[row_idx, 23] = f_val(18) + f_val(19) + f_val(20) + f_val(21) + f_val(22)
        df.iloc[row_idx, 24] = f_val(9) + f_val(13) + f_val(17) + f_val(23)
        
        # Aggregate Final Presentation Metrics
        df.iloc[row_idx, 29] = f_val(25) + f_val(26) + f_val(27) + f_val(28)
        df.iloc[row_idx, 32] = f_val(30) + f_val(31)
        df.iloc[row_idx, 36] = f_val(33) + f_val(34) + f_val(35)
        df.iloc[row_idx, 40] = f_val(37) + f_val(38) + f_val(39)
        df.iloc[row_idx, 45] = f_val(41) + f_val(42) + f_val(43) + f_val(44)
        df.iloc[row_idx, 46] = f_val(29) + f_val(32) + f_val(36) + f_val(40) + f_val(45)
        
        # Final Compiled Sums
        df.iloc[row_idx, 47] = f_val(24) + f_val(46)
        
        # Output save
        df.to_excel(FILE_NAME, index=False, header=False)
        st.success(f"Success! Calculations recorded for Slot {sno}. Live Totals -> MT: {df.iloc[row_idx,24]} | Final: {df.iloc[row_idx,46]} | Combined Grand Total: {df.iloc[row_idx,47]}")