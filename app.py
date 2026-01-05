%%writefile app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# --- PAGE CONFIG ---
st.set_page_config(page_title="Student Analytics", layout="wide", initial_sidebar_state="collapsed")

# --- MODERN PROFESSIONAL CSS UI ---
st.markdown("""
<style>
/* --- General Styles --- */
.stApp { background-color: #F8F9FB; font-family: 'Segoe UI', sans-serif; }

/* --- Navbar Styles --- */
.navbar {
    display: flex;
    justify-content: center;
    gap: 30px;
    font-weight: 600;
    font-size: 16px;
    position: sticky;
    top: 0;
    background-color: #ffffffcc;
    padding: 12px 0;
    z-index: 999;
    border-bottom: 1px solid #E5E7EB;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    backdrop-filter: blur(8px);
    transition: all 0.3s ease;
}

/* Navbar links */
.navbar a {
    text-decoration: none;
    color: #111827;
    padding: 8px 20px;
    border-radius: 8px;
    transition: all 0.3s ease;
    font-weight: 600;
    position: relative;
}

/* Hover effect */
.navbar a:hover {
    background-color: #F3F4F6;
    color: #1F2937;
}

/* Active link underline */
.navbar a.active::after {
    content: "";
    position: absolute;
    left: 0;
    bottom: -4px;
    width: 100%;
    height: 3px;
    background: #4A90E2;
    border-radius: 2px;
}

/* KPI Card Styling */
.metric-container {
    background-color: white;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    border-left: 5px solid #4A90E2;
    margin-bottom: 20px;
    text-align: center;
    transition: transform 0.2s, box-shadow 0.2s;
}
.metric-container:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 20px rgba(0,0,0,0.12);
}
.metric-label { color: #6B7280; font-size: 14px; font-weight: 600; text-transform: uppercase; margin-bottom: 5px; }
.metric-value { color: #1F2937; font-size: 28px; font-weight: 700; }

/* Section Headers */
.section-header {   background: white;
            padding: 1rem 1.5rem;
            border-radius: 12px;
            font-size: 1.25rem;
            font-weight: 600;
            color: #111827;
            margin: 2rem 0 1rem 0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08); }
  .subtitle {
            color: rgba(255,255,255,0.9);
            font-size: 1rem;
            margin-top: 0.5rem;
        }

/* Scorecards */
.scorecard {
    padding: 15px;
    border-radius: 10px;
    color: white;
    text-align: center;
    margin-bottom: 10px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.1);
    transition: transform 0.2s, box-shadow 0.2s;
}
.scorecard:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 24px rgba(0,0,0,0.2);
}

/* --- NEW STYLES --- */

/* Course Distribution Cards */
.course-card {
    background: linear-gradient(145deg, #ffffff, #f3f4f6);
    padding: 25px;
    border-radius: 15px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.1);
    border-left: 6px solid #10B981;
    text-align: center;
    transition: transform 0.2s, box-shadow 0.2s;
    margin-bottom: 20px;
}
.course-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 24px rgba(0,0,0,0.15);
}
.course-card .course-name { font-size: 16px; font-weight: 700; margin-bottom: 10px; color:#111827; }
.course-card .course-count { font-size: 28px; font-weight: 700; color:#10B981; }

/* Summary Insights Box */
.summary-box {
    background-color: white;
    border-radius: 15px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.1);
    padding: 20px;
    margin-bottom: 20px;
    line-height: 1.6;
}

/* Horizontal Engagement Bars */
.engagement-bar {
    height: 35px;
    border-radius: 10px;
    margin-bottom: 10px;
    color: white;
    font-weight: 600;
    display: flex;
    align-items: center;
    justify-content: center;
}

/* Colors for engagement levels */
.low { background: #EF4444; }
.medium { background: #FBBF24; }
.high { background: #10B981; }

/* Smooth scroll */
html {
    scroll-behavior: smooth;
}

/* Mobile responsiveness */
@media screen and (max-width: 768px) {
    .navbar {
        flex-direction: column;
        gap: 10px;
    }
}
</style>

<script>
// Highlight active navbar link on scroll
window.addEventListener('scroll', function() {
    const sections = ['overview', 'performance', 'chatbot'];
    const scrollPos = window.scrollY + 100; // offset for navbar height

    sections.forEach(id => {
        const section = document.getElementsByName(id)[0];
        const link = document.querySelector('.navbar a[href="#' + id + '"]');
        if(section) {
            const top = section.offsetTop;
            const bottom = top + section.offsetHeight;
            if(scrollPos >= top && scrollPos < bottom){
                document.querySelectorAll('.navbar a').forEach(a => a.classList.remove('active'));
                link.classList.add('active');
            }
        }
    });
});
</script>

<div class="navbar">
    <a href="#overview" class="active">Overview</a>
    <a href="#performance">Performance</a>
    <a href="#chatbot">Chatbot</a>
</div>
""", unsafe_allow_html=True)


# --- DATA LOADING ---
@st.cache_data
def load_data():
    file_name = "Students_Dataset.xlsx"
    if os.path.exists(file_name):
        return pd.read_excel(file_name)
    elif os.path.exists("Students_Dataset.xlsx - Sheet1.csv"):
        return pd.read_csv("Students_Dataset.xlsx - Sheet1.csv")
    return None

df = load_data()

if df is not None:

    # --- FILTERS ---
    st.markdown("### Filters")
    col1, col2, col3 = st.columns(3)
    with col1:
        selected_class = st.selectbox("Select Class Level", options=["All"] + sorted(df["class_level"].unique()))
    with col2:
        selected_gender = st.selectbox("Select Gender", options=["All"] + sorted(df["student_gender"].unique()))
    with col3:
        selected_course = st.selectbox("Select Course", options=["All"] + sorted(df["course_name"].unique()))

    # Apply filters
    filtered_df = df.copy()
    if selected_class != "All":
        filtered_df = filtered_df[filtered_df["class_level"] == selected_class]
    if selected_gender != "All":
        filtered_df = filtered_df[filtered_df["student_gender"] == selected_gender]
    if selected_course != "All":
        filtered_df = filtered_df[filtered_df["course_name"] == selected_course]

    # --- OVERVIEW SECTION ---
    st.markdown('<a name="overview"></a>', unsafe_allow_html=True)
    st.markdown('<p class ="section-header" style="font-size:32px; font-weight:800; color:#111827; margin-bottom:0;">Academic Performance Overview</p>', unsafe_allow_html=True)
    st.markdown('<p class=" subtitle" style="color:#6B7280; margin-bottom:30px;">Real-time insights into student engagement and course metrics</p>', unsafe_allow_html=True)

    # --- TOP KPIs ---
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    with kpi1:
        st.markdown(f'''<div class="metric-container">
            <div class="metric-label">Total Students</div>
            <div class="metric-value">{filtered_df["student_id"].nunique()}</div>
        </div>''', unsafe_allow_html=True)
    with kpi2:
        st.markdown(f'''<div class="metric-container" style="border-left-color: #10B981;">
            <div class="metric-label">Total Courses</div>
            <div class="metric-value">{filtered_df["course_name"].nunique()}</div>
        </div>''', unsafe_allow_html=True)
    with kpi3:
        st.markdown(f'''<div class="metric-container" style="border-left-color: #F59E0B;">
            <div class="metric-label">Assessments</div>
            <div class="metric-value">{len(filtered_df)}</div>
        </div>''', unsafe_allow_html=True)
    with kpi4:
        avg_att = filtered_df['attendance_rate'].mean()
        st.markdown(f'''<div class="metric-container" style="border-left-color: #8B5CF6;">
            <div class="metric-label">Avg Attendance</div>
            <div class="metric-value">{avg_att:.1f}%</div>
        </div>''', unsafe_allow_html=True)

    # --- CHARTS ROW 1 ---
    st.markdown('<p class="section-header">Demographics & Enrollment</p>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)

    with c1:
        gender_df = filtered_df.drop_duplicates('student_id')['student_gender'].value_counts().reset_index()
        gender_df.columns = ['student_gender', 'count']
        fig_pie = px.pie(gender_df, values='count', names='student_gender', hole=0.6,
                         color_discrete_sequence=['#4A90E2', '#F472B6'])
        fig_pie.update_layout(margin=dict(t=0, b=0, l=0, r=0), showlegend=True, height=350)
        st.write("**Gender Distribution**")
        st.plotly_chart(fig_pie, width="stretch")

    with c2:
        class_df = filtered_df.drop_duplicates('student_id')['class_level'].value_counts().sort_index().reset_index()
        class_df.columns = ['class_level', 'count']
        fig_bar = px.bar(class_df, x='class_level', y='count', text_auto=True,
                         color_discrete_sequence=['#4A90E2'])
        fig_bar.update_layout(margin=dict(t=20, b=20, l=0, r=0), height=350, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.write("**Students by Class Level**")
        st.plotly_chart(fig_bar, width="stretch")

    # --- ROW 2: Engagement & Participation ---
    st.markdown('<p class="section-header">Engagement & Participation</p>', unsafe_allow_html=True)
    c3, c4 = st.columns([1, 2])

    with c3:
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=avg_att,
            gauge={'axis': {'range': [0, 100]},
                   'bar': {'color': "#111827"},
                   'steps': [
                       {'range': [0, 60], 'color': "#FEE2E2"},
                       {'range': [60, 85], 'color': "#FEF3C7"},
                       {'range': [85, 100], 'color': "#D1FAE5"}]}))
        fig_gauge.update_layout(height=280, margin=dict(t=50, b=20, l=30, r=30))
        st.write("**Attendance Health**")
        st.plotly_chart(fig_gauge, width="stretch")

    with c4:
        course_df = filtered_df['course_name'].value_counts().reset_index()
        course_df.columns = ['course_name', 'count']
        fig_course = px.bar(course_df, x='count', y='course_name', orientation='h',
                            color_discrete_sequence=['#10B981'])
        fig_course.update_layout(margin=dict(t=20, b=20, l=0, r=0), height=300, plot_bgcolor='rgba(0,0,0,0)')
        st.write("**Course Distribution**")
        st.plotly_chart(fig_course, width="stretch")



    # --- COURSE DISTRIBUTION CARDS ---
    st.markdown('<p class="section-header">Course Distribution Cards</p>', unsafe_allow_html=True)
    course_counts = filtered_df.groupby('course_name')['student_id'].nunique().reset_index()
    course_counts.columns = ['course_name', 'num_students']

    # Display cards in rows of 3
    for i in range(0, len(course_counts), 3):
        cols = st.columns(3)
        for j, row in course_counts.iloc[i:i+3].iterrows():
            with cols[j % 3]:
                st.markdown(f'''
                <div class="metric-container" style="border-left-color: #10B981;">
                    <div class="metric-label">{row['course_name']}</div>
                    <div class="metric-value">{row['num_students']}</div>
                </div>
                ''', unsafe_allow_html=True)

    # --- ATTENDANCE OVERVIEW CHART ---
    st.markdown('<p class="section-header">Attendance Overview per Course</p>', unsafe_allow_html=True)
    attendance_df = filtered_df.groupby('course_name')['attendance_rate'].mean().reset_index()
    attendance_df = attendance_df.sort_values(by='attendance_rate', ascending=False)

    fig_attendance = px.bar(
        attendance_df,
        x='course_name',
        y='attendance_rate',
        text_auto='.1f',
        color='attendance_rate',
        color_continuous_scale='Tealgrn'
    )
    fig_attendance.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        yaxis_title='Average Attendance (%)',
        xaxis_title='Course',
        height=400,
        margin=dict(t=20, b=20, l=0, r=0)
    )
    st.plotly_chart(fig_attendance, use_container_width=True)


    # --- ENGAGEMENT DISTRIBUTION (Horizontal Bar Chart) ---
    st.markdown('<p class="section-header">Engagement Distribution</p>', unsafe_allow_html=True)
    filtered_df['engagement_score'] = (filtered_df['attendance_rate']/100 + filtered_df['raised_hand_count']/filtered_df['raised_hand_count'].max() + filtered_df['moodle_views']/filtered_df['moodle_views'].max() + filtered_df['resources_downloads']/filtered_df['resources_downloads'].max())/4
    bins = [0,0.33,0.66,1]; labels = ['Low','Medium','High']
    filtered_df['engagement_level'] = pd.cut(filtered_df['engagement_score'], bins=bins, labels=labels)
    engagement_counts = filtered_df.groupby('engagement_level')['student_id'].nunique().reset_index()

    fig_engagement_bar = px.bar(engagement_counts, x='student_id', y='engagement_level', orientation='h', text='student_id', color='engagement_level', color_discrete_map={'Low': '#EF4444', 'Medium': '#FBBF24', 'High': '#10B981'}, title='Number of Students by Engagement Level')
    fig_engagement_bar.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', xaxis_title='Number of Students', yaxis_title='Engagement Level', height=350, margin=dict(t=40, b=20, l=0, r=0), showlegend=False)
    fig_engagement_bar.update_traces(texttemplate='%{text} students', textposition='outside', marker_line_color='rgba(0,0,0,0.2)', marker_line_width=1)
    st.plotly_chart(fig_engagement_bar, use_container_width=True)

    total_students = engagement_counts['student_id'].sum()
    engagement_counts['percentage'] = (engagement_counts['student_id'] / total_students * 100).round(1)

    col1, col2, col3 = st.columns(3)
    low_pct = engagement_counts[engagement_counts['engagement_level'] == 'Low']['percentage'].values
    low_pct = low_pct[0] if len(low_pct) > 0 else 0
    medium_pct = engagement_counts[engagement_counts['engagement_level'] == 'Medium']['percentage'].values
    medium_pct = medium_pct[0] if len(medium_pct) > 0 else 0
    high_pct = engagement_counts[engagement_counts['engagement_level'] == 'High']['percentage'].values
    high_pct = high_pct[0] if len(high_pct) > 0 else 0

    with col1: st.markdown(f'''<div style="text-align: center; padding: 15px; background-color: #FEF2F2; border-radius: 10px; border-left: 4px solid #EF4444;"><div style="font-size: 12px; color: #6B7280;">Low Engagement</div><div style="font-size: 24px; font-weight: 700; color: #EF4444;">{low_pct}%</div></div>''', unsafe_allow_html=True)
    with col2: st.markdown(f'''<div style="text-align: center; padding: 15px; background-color: #FFFBEB; border-radius: 10px; border-left: 4px solid #FBBF24;"><div style="font-size: 12px; color: #6B7280;">Medium Engagement</div><div style="font-size: 24px; font-weight: 700; color: #FBBF24;">{medium_pct}%</div></div>''', unsafe_allow_html=True)
    with col3: st.markdown(f'''<div style="text-align: center; padding: 15px; background-color: #ECFDF5; border-radius: 10px; border-left: 4px solid #10B981;"><div style="font-size: 12px; color: #6B7280;">High Engagement</div><div style="font-size: 24px; font-weight: 700; color: #10B981;">{high_pct}%</div></div>''', unsafe_allow_html=True)
   # --- ENGAGEMENT SCORECARDS ---
    st.markdown('<p class="section-header">Engagement Scorecards</p>', unsafe_allow_html=True)
    e1, e2, e3 = st.columns(3)

    with e1:
        st.markdown(f'''<div class="scorecard" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
            <div style="font-size: 14px; opacity: 0.9;">✋ Avg Raised Hands</div>
            <div style="font-size: 32px; font-weight: 700;">{filtered_df['raised_hand_count'].mean():.1f}</div>
        </div>''', unsafe_allow_html=True)

    with e2:
        st.markdown(f'''<div class="scorecard" style="background: linear-gradient(135deg, #2af598 0%, #009efd 100%);">
            <div style="font-size: 14px; opacity: 0.9;">💻 Avg Moodle Views</div>
            <div style="font-size: 32px; font-weight: 700;">{filtered_df['moodle_views'].mean():.1f}</div>
        </div>''', unsafe_allow_html=True)

    with e3:
        st.markdown(f'''<div class="scorecard" style="background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);">
            <div style="font-size: 14px; opacity: 0.9;">📥 Avg Resources</div>
            <div style="font-size: 32px; font-weight: 700;">{filtered_df['resources_downloads'].mean():.1f}</div>
        </div>''', unsafe_allow_html=True)


       # --- SUMMARY INSIGHTS ---
    st.markdown('<p class="section-header">Summary Insights</p>', unsafe_allow_html=True)
    # Example: % students with high engagement per class
    class_summary = filtered_df.groupby('class_level')['engagement_level'].value_counts(normalize=True).mul(100).round(1).reset_index()
    class_summary.columns = ['class_level','engagement_level','percent']
    insights = ""
    for cls in class_summary['class_level'].unique():
        cls_data = class_summary[class_summary['class_level']==cls]
        for _, row in cls_data.iterrows():
            insights += f"Class {cls}: {row['percent']}% students are {row['engagement_level']} engagement.  \n"
    st.markdown(insights)


else:
    st.error("Dataset not found. Please upload 'Students_Dataset.xlsx'.")
