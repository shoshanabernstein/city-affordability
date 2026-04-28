import streamlit as st
import pandas as pd
from ai import ask_ai
from database import get_countries_list
from api import get_country_info, country_card

# --- UI COMPONENTS ---
def show_header():
    st.title("🌍 Where Can I Afford to Live?")
    st.caption("Compare cities based on your salary and cost of living")

def show_filters():
    with st.sidebar:
        st.header("🔧 Filters")

        
        countries = st.multiselect(
            "Countries",
            get_countries_list(),
            default=["United States"]
        )

        monthly_salary = st.slider(
            "Monthly Salary ($)",
            2000,
            20000,
            5000
        )

    return countries, monthly_salary

def show_metrics(sorted_cities):
    if not sorted_cities:
        st.warning("No cities found. Try selecting different filters.")
        return
    best = sorted_cities[0]["city"]
    worst = sorted_cities[-1]["city"]
    avg = round(sum(c["score"] for c in sorted_cities) / len(sorted_cities), 2)

    col1, col2, col3 = st.columns(3)
    col1.metric("🏆 Best City", best)
    col2.metric("⚠️ Worst City", worst)
    col3.metric("📊 Avg Score", avg)

def show_tabs(sorted_cities):
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["🏆 Rankings", "📊 Data", "📈 Chart", "🤖 Ask AI", "🌍 Countries"])

    df = pd.DataFrame(sorted_cities)

    # Rankings
    with tab1:
        st.subheader("🏆 Top Cities")

        top3 = sorted_cities[:3]

        if not top3:
            st.warning("No cities available.")
            return

        # 🥇 WINNER (big card)
        winner = top3[0]

        with st.container(border=True):
            st.markdown(f"# 🥇 {winner['city']}, {winner['country']}")
            
            col1, col2, col3 = st.columns(3)

            col1.metric("💸 Monthly Cost", f"${winner['monthly_cost']}")
            col2.metric("💰 Remaining", f"${winner['remaining_monthly_budget']}")
            col3.metric("📊 Score", winner['score'])

            st.markdown(f"**Status:** {winner['status']}")

        st.markdown("---")

        # 🥈🥉 RUNNERS-UP
        cols = st.columns(2)

        for i, city in enumerate(top3[1:]):
            with cols[i]:
                with st.container(border=True):
                    rank = i + 2
                    medal = "🥈" if rank == 2 else "🥉"

                    st.markdown(f"### {medal} {city['city']}")
                    st.markdown(f"**Country:** {city['country']}")
                    st.markdown(f"💸 Monthly Cost: ${city['monthly_cost']}")
                    st.markdown(f"💰 Remaining: ${city['remaining_monthly_budget']}")
                    st.markdown(f"📊 Score: {city['score']}")
                    st.markdown(f"**Status:** {city['status']}")
    with tab2:
        st.subheader("All Cities")
        
        st.dataframe(df, use_container_width=True)

    with tab3:
        st.subheader("Affordability Scores")
        st.bar_chart(df.set_index("city")["score"])

    with tab4:
        show_ai_panel(sorted_cities)

    with tab5:
        show_countries(df)


def show_city_details(sorted_cities):
    st.subheader("🌆 Explore Cities")

    for city in sorted_cities[:15]:
        with st.expander(f"{city['city']} - Score: {city['score']}"):
            st.write(f"Country: {city['country']}")
            st.write(f"Cost Index: {city['cost_of_living_index']}")
            st.write(f"Affordability Score: {city['score']}")
            st.write(f"Affordable?: {city['status']}")

def show_chart(df):
    st.bar_chart(df.set_index("city")["score"])


def show_ai_panel(sorted_cities):
    st.subheader("🤖 Ask AI")

    question = st.text_input("Ask something about these cities:")

    if st.button("Ask"):
        if not sorted_cities:
            st.warning("No data available.")
            return
        
        with st.spinner("Thinking..."):
            answer = ask_ai(question, sorted_cities)
            st.write(answer)

def show_countries(df):
    st.header("🌍 Country Explorer")

    countries = sorted(df["country"].unique())
    selected = st.selectbox("Select a country", countries)

    if selected:
        # optional cleanup for API compatibility
        country_map = {
            "USA": "United States",
            "UK": "United Kingdom"
        }

        selected = country_map.get(selected, selected)

        info = get_country_info(selected)

        if info:
            country_card(info)
        else:
            st.error("Country not found")

        col1, col2, col3 = st.columns(3)

