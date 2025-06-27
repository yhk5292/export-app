# app.py
import streamlit as st
import pandas as pd
from datetime import date, timedelta
from io import BytesIO

st.set_page_config(page_title="디지털 수출 성과 관리", layout="wide")
st.title("📦 디지털 수출 성과 관리 대시보드")

checklist_data = {
    "활동 항목": [
        "주력 제품 선정 완료", "타겟 국가 1~2곳 선정", "제품 사진 확보",
        "제품 설명 자료(PDF) 완성", "홍보 문구 (영문) 작성",
        "디지털 플랫폼 가입 및 셋팅 완료", "제품 등록",
        "바이어 대상 이메일/메시지 발송", "SNS 업로드",
        "KOTRA 상담회 신청", "바이어 미팅 요청",
        "샘플 제안 또는 피드백 수신", "후속 미팅 또는 견적 제안 완료",
        "최초 거래 성사 또는 계약 체결", "성과 정리 및 다음 단계 계획 수립"
    ],
    "진행 상태": ["미완료"] * 15,
    "예상 일정": [date.today() + timedelta(days=i*2) for i in range(15)]
}
df = pd.DataFrame(checklist_data)

st.sidebar.header("📋 필터")
status_filter = st.sidebar.multiselect(
    "진행 상태 선택", ["미완료", "진행 중", "완료"], default=["미완료", "진행 중", "완료"]
)

for i, row in df.iterrows():
    col1, col2 = st.columns([3, 1])
    with col1:
        st.write(f"**{row['활동 항목']}** (예정일: {row['예상 일정']})")
    with col2:
        new_status = st.selectbox("상태", ["미완료", "진행 중", "완료"], index=0, key=i)
        df.at[i, "진행 상태"] = new_status

df_filtered = df[df["진행 상태"].isin(status_filter)]

completed = df[df["진행 상태"] == "완료"].shape[0]
total = df.shape[0]
progress = int((completed / total) * 100)
st.sidebar.markdown(f"### ✅ 전체 진행률: {progress}%")
st.sidebar.progress(progress / 100)

with st.expander("📊 전체 항목 보기"):
    st.dataframe(df, use_container_width=True)

st.markdown("---")
st.subheader("📥 데이터 저장")

def to_excel(dataframe):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        dataframe.to_excel(writer, index=False, sheet_name='성과체크리스트')
    processed_data = output.getvalue()
    return processed_data

excel_data = to_excel(df)
st.download_button(label="📄 엑셀 파일 다운로드",
                   data=excel_data,
                   file_name="디지털수출_성과관리.xlsx",
                   mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

st.markdown("---")
st.subheader("🤖 AI 요약 및 다음 제안")

summary = f"전체 {total}개 항목 중 {completed}개가 완료되었습니다."
next_steps = df[df["진행 상태"] != "완료"].head(3)["활동 항목"].tolist()

st.write("📌 **진행 요약:**", summary)
if next_steps:
    st.write("📌 **다음 우선순위 제안:**")
    for i, task in enumerate(next_steps, 1):
        st.markdown(f"{i}. {task}")
else:
    st.success("🎉 모든 항목이 완료되었습니다!")

st.markdown("---")
st.subheader("📅 예정 일정 요약")
st.write(df[["활동 항목", "예상 일정", "진행 상태"]])
