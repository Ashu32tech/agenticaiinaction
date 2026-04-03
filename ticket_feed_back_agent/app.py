import streamlit as st
import pandas as pd
from dotenv import load_dotenv

from feed_back_pipeline import run

load_dotenv(override=True)

st.title("CrewAI + MCP System (Direct)")

file = st.file_uploader("Upload CSV", type=["csv"])

if file:
    df = pd.read_csv(file)
    st.write(df)

    if st.button("Run"):
        res = []

        for _, r in df.iterrows():
            out = run(r.to_dict())   # 👈 DIRECT CALL
            res.append(out)

        st.write(pd.DataFrame(res))
