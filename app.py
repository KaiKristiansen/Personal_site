import streamlit as st
import pandas as pd
import os

# ============================================================
# VANCOUVER NEIGHBORHOOD FINDER v2
# Real data + AI-powered explanations
# ============================================================

# --- Page setup ---
st.set_page_config(page_title="Vancouver Neighborhood Finder", page_icon="🏙️", layout="centered")
st.title("Vancouver Neighborhood Finder")
st.write("Adjust the sliders to show what matters most to you, then hit the button!")

# --- Real neighborhood data (scored 1-10, based on 2025-2026 research) ---
# Sources: Walk Score, Zumper, liv.rent, VPD GeoDASH, Destination Vancouver
neighborhoods = {
    "Mount Pleasant": {
        "rent": 5,             # ~$2,525/mo
        "walkability": 9,      # Walk Score 88
        "gym_access": 6,       # Community centre, some boutiques
        "cafes": 10,           # Specialty coffee hub (Matchstick, Modus, etc.)
        "transit": 8,          # Transit Score ~80, near SkyTrain
        "safety": 4,           # ~1,900 incidents/yr (proximity to DTES)
        "nightlife": 8,        # Biltmore, breweries, Fox Cabaret
        "quietness": 4,        # Busy Main St corridor
        "distance_to_downtown": 7,  # ~3 km
        "vibe": 9,             # Hipster/creative, murals, indie shops
    },
    "Kitsilano": {
        "rent": 3,             # ~$2,700/mo
        "walkability": 9,      # Walk Score 92
        "gym_access": 9,       # Ron Zalko, TurF, Ride Cycle, many options
        "cafes": 9,            # ~100 cafes in ~2 sq miles
        "transit": 7,          # Transit Score 74
        "safety": 6,           # 1,238 incidents/yr
        "nightlife": 5,        # Casual bars, wine bars
        "quietness": 7,        # Residential streets quiet
        "distance_to_downtown": 5,  # ~5 km
        "vibe": 8,             # Beach lifestyle, yoga, active
    },
    "Yaletown": {
        "rent": 2,             # ~$2,800/mo
        "walkability": 10,     # Walk Score 97
        "gym_access": 8,       # Dynasty Gym, Jaybird, Ride Cycle
        "cafes": 8,            # Upscale cafes along Hamilton/Mainland
        "transit": 10,         # Transit Score ~95, Canada Line
        "safety": 6,           # CBD grouped stats; residential area is safe
        "nightlife": 8,        # Upscale lounges, near Granville strip
        "quietness": 3,        # Urban core noise, construction
        "distance_to_downtown": 10, # 0.5 km — IS downtown
        "vibe": 7,             # Sleek/upscale, converted warehouses
    },
    "Commercial Drive": {
        "rent": 9,             # ~$2,008/mo
        "walkability": 9,      # Walk Score 88
        "gym_access": 5,       # Community centre, few independents
        "cafes": 10,           # Birthplace of Vancouver coffee culture
        "transit": 8,          # Transit Score 76, SkyTrain at Commercial-Broadway
        "safety": 5,           # 1,441 incidents/yr
        "nightlife": 7,        # Bar Corso, Mezcaleria, live music
        "quietness": 4,        # Busy street scene
        "distance_to_downtown": 6,  # ~4 km
        "vibe": 9,             # Bohemian/multicultural, strong community
    },
    "Gastown": {
        "rent": 2,             # ~$2,800/mo (grouped with CBD)
        "walkability": 10,     # Walk Score 98
        "gym_access": 7,       # Downtown proximity, Equinox nearby
        "cafes": 8,            # Revolver, Timbertrain, specialty roasters
        "transit": 10,         # Transit Score ~95, multiple SkyTrain stations
        "safety": 3,           # Adjacent to DTES, high street-level incidents
        "nightlife": 10,       # Best pub crawl area in Vancouver
        "quietness": 2,        # Nightlife, tourism, truck routes
        "distance_to_downtown": 10, # 0.5 km — IS downtown
        "vibe": 7,             # Historic/trendy, cobblestones, boutiques
    },
    "West End": {
        "rent": 6,             # ~$2,475/mo
        "walkability": 9,      # Walk Score 95
        "gym_access": 7,       # Community centre, Aquatic Centre, YYOGA
        "cafes": 7,            # Many cafes on Denman/Davie
        "transit": 9,          # Transit Score 89
        "safety": 3,           # 2,735 incidents/yr (density/nightlife driven)
        "nightlife": 7,        # Davie Village scene, proximity to clubs
        "quietness": 5,        # Dense but residential
        "distance_to_downtown": 9,  # ~1 km
        "vibe": 8,             # Urban village, LGBTQ+ friendly, beach access
    },
    "Hastings-Sunrise": {
        "rent": 10,            # ~$1,895/mo — cheapest neighborhood
        "walkability": 7,      # Walk Score 70
        "gym_access": 4,       # Community centre, limited private options
        "cafes": 4,            # Growing but sparse
        "transit": 7,          # Transit Score 66
        "safety": 8,           # 845 incidents/yr
        "nightlife": 2,        # Very few bars, mostly residential
        "quietness": 8,        # Very residential, tree-lined
        "distance_to_downtown": 4,  # ~6.5 km
        "vibe": 6,             # Family-oriented, up-and-coming, diverse
    },
    "Fairview": {
        "rent": 4,             # ~$2,625/mo
        "walkability": 9,      # Walk Score 93
        "gym_access": 5,       # YMCA-type options, some studios
        "cafes": 5,            # Broadway corridor, chains + independents
        "transit": 8,          # Transit Score 81
        "safety": 6,           # ~1,100 incidents/yr
        "nightlife": 3,        # Not a nightlife destination
        "quietness": 5,        # Broadway busy, residential pockets quieter
        "distance_to_downtown": 7,  # ~3 km
        "vibe": 5,             # Central/practical, City Hall, VGH
    },
    "Kerrisdale": {
        "rent": 7,             # ~$2,375/mo
        "walkability": 7,      # Walk Score 65
        "gym_access": 5,       # Community centre, some studios
        "cafes": 5,            # Village shops, not a coffee destination
        "transit": 6,          # Transit Score 59
        "safety": 10,          # 358 incidents/yr — safest neighborhood
        "nightlife": 1,        # Village pubs only
        "quietness": 10,       # Quintessential quiet residential
        "distance_to_downtown": 2,  # ~8 km
        "vibe": 6,             # Village charm, affluent, tree-lined
    },
    "East Vancouver": {
        "rent": 8,             # ~$2,100/mo
        "walkability": 7,      # Walk Score ~73
        "gym_access": 4,       # Community centres, few boutique options
        "cafes": 5,            # Scattered, depends on sub-area
        "transit": 7,          # Transit Score ~65
        "safety": 9,           # 489 incidents/yr (Kensington-Cedar Cottage)
        "nightlife": 3,        # Scattered pubs
        "quietness": 8,        # Mostly residential, quiet streets
        "distance_to_downtown": 3,  # ~7 km
        "vibe": 7,             # Diverse, murals, local festivals, community
    },
}

# --- Real data context for AI explanations ---
neighborhood_context = {
    "Mount Pleasant": "Avg rent ~$2,525/mo. Walk Score 88. Known for Main St indie shops, breweries (Brassneck, 33 Acres), and specialty coffee. ~3 km to downtown.",
    "Kitsilano": "Avg rent ~$2,700/mo. Walk Score 92. Beach lifestyle, yoga studios, active community. ~100 cafes in ~2 sq miles. ~5 km to downtown.",
    "Yaletown": "Avg rent ~$2,800/mo. Walk Score 97. Converted warehouses, upscale dining, Canada Line station. IS downtown (0.5 km).",
    "Commercial Drive": "Avg rent ~$2,008/mo. Walk Score 88. Bohemian/multicultural, birthplace of Van coffee culture. SkyTrain at Commercial-Broadway. ~4 km to downtown.",
    "Gastown": "Avg rent ~$2,800/mo. Walk Score 98. Historic cobblestones, best nightlife crawl. Adjacent to DTES (safety concern). IS downtown (0.5 km).",
    "West End": "Avg rent ~$2,475/mo. Walk Score 95. Dense urban village, LGBTQ+ friendly Davie Village, English Bay beach. ~1 km to downtown.",
    "Hastings-Sunrise": "Avg rent ~$1,895/mo (cheapest). Walk Score 70. Family-oriented, up-and-coming, PNE area. ~6.5 km to downtown.",
    "Fairview": "Avg rent ~$2,625/mo. Walk Score 93. Central/practical near City Hall and VGH. Good transit (Score 81). ~3 km to downtown.",
    "Kerrisdale": "Avg rent ~$2,375/mo. Walk Score 65. Safest neighborhood (358 incidents/yr). Quiet village charm, affluent. ~8 km to downtown.",
    "East Vancouver": "Avg rent ~$2,100/mo. Walk Score ~73. Diverse community, murals, local festivals. 2nd safest (489 incidents/yr). ~7 km to downtown.",
}

# --- Nice display names for factors ---
factor_labels = {
    "rent": "Affordable Rent",
    "walkability": "Walkability",
    "gym_access": "Gym Access",
    "cafes": "Cafes",
    "transit": "Transit",
    "safety": "Safety",
    "nightlife": "Nightlife",
    "quietness": "Quietness",
    "distance_to_downtown": "Close to Downtown",
    "vibe": "Vibe / Culture",
}

# --- Sidebar: weight sliders ---
st.sidebar.header("What matters to you?")
st.sidebar.write("Set each factor from 0 (don't care) to 10 (very important).")

weights = {}
for factor_key, factor_name in factor_labels.items():
    weights[factor_key] = st.sidebar.slider(factor_name, 0, 10, 5)

# --- AI explanation function ---
def get_ai_explanation(ranked, weights, neighborhoods, neighborhood_context):
    """Call Claude API to generate a smart explanation of the results."""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return None

    try:
        from anthropic import Anthropic
        client = Anthropic(api_key=api_key)

        # Build the prompt with real data
        top_3 = ranked[:3]
        user_priorities = sorted(weights.items(), key=lambda x: x[1], reverse=True)
        top_priorities = [(factor_labels[k], v) for k, v in user_priorities if v > 0][:5]

        prompt = f"""You are a friendly Vancouver neighborhood advisor. A user just ranked neighborhoods based on their lifestyle priorities. Give a SHORT explanation (4-6 sentences max).

User's top priorities (factor: weight out of 10):
{chr(10).join(f"- {name}: {w}/10" for name, w in top_priorities)}

Results (ranked best to worst):
1. {top_3[0][0]} (score: {top_3[0][1]}/10)
2. {top_3[1][0]} (score: {top_3[1][1]}/10)
3. {top_3[2][0]} (score: {top_3[2][1]}/10)

Real neighborhood info:
- {top_3[0][0]}: {neighborhood_context[top_3[0][0]]}
- {top_3[1][0]}: {neighborhood_context[top_3[1][0]]}
- {top_3[2][0]}: {neighborhood_context[top_3[2][0]]}

Explain why #{1} won, mention a key trade-off vs #{2}, and give one practical tip. Be conversational and specific to Vancouver. Do NOT use bullet points — write in short paragraphs."""

        message = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=300,
            messages=[{"role": "user", "content": prompt}],
        )
        return message.content[0].text
    except Exception as e:
        return f"(AI unavailable: {e})"


# --- Scoring ---
if st.button("Find My Best Neighborhood"):

    # Check if all weights are zero
    total_weight = sum(weights.values())
    if total_weight == 0:
        st.warning("Move at least one slider above 0!")
    else:
        # Calculate weighted score for each neighborhood
        results = {}
        for name, scores in neighborhoods.items():
            weighted_sum = 0
            for factor_key in scores:
                weighted_sum += scores[factor_key] * weights[factor_key]
            results[name] = round(weighted_sum / total_weight, 2)

        # Sort from best to worst
        ranked = sorted(results.items(), key=lambda x: x[1], reverse=True)

        # --- Display results ---
        st.header("Your Top Neighborhoods")

        for rank, (name, score) in enumerate(ranked, start=1):
            if rank == 1:
                st.subheader(f"🥇 {name} — {score}/10")
            elif rank == 2:
                st.subheader(f"🥈 {name} — {score}/10")
            elif rank == 3:
                st.subheader(f"🥉 {name} — {score}/10")
            else:
                st.write(f"**#{rank} {name}** — {score}/10")

        # --- AI Explanation ---
        st.divider()
        st.header("Why This Pick?")

        with st.spinner("Thinking..."):
            ai_response = get_ai_explanation(ranked, weights, neighborhoods, neighborhood_context)

        if ai_response and not ai_response.startswith("(AI unavailable"):
            st.write(ai_response)
        else:
            # Fallback: template-based explanation if no API key
            winner_name = ranked[0][0]
            winner_scores = neighborhoods[winner_name]
            runner_up_name = ranked[1][0]
            runner_up_scores = neighborhoods[runner_up_name]

            top_factors = sorted(weights.items(), key=lambda x: x[1], reverse=True)[:3]
            top_factor_names = [factor_labels[f[0]] for f in top_factors if f[1] > 0]
            best_traits = sorted(winner_scores.items(), key=lambda x: x[1], reverse=True)[:3]
            best_trait_names = [factor_labels[t[0]] for t in best_traits]

            summary = f"**{winner_name}** is your best match because "
            if top_factor_names:
                summary += f"you prioritize **{', '.join(top_factor_names)}**, "
            summary += f"and it scores highest in **{', '.join(best_trait_names)}**."

            advantages = []
            for factor_key, label in factor_labels.items():
                if runner_up_scores[factor_key] > winner_scores[factor_key] and weights[factor_key] > 3:
                    advantages.append(label.lower())
            if advantages:
                summary += (
                    f"\n\nConsider **{runner_up_name}** if you value "
                    f"**{', '.join(advantages[:2])}** more — it edges ahead there."
                )

            st.write(summary)

            if ai_response and ai_response.startswith("(AI unavailable"):
                st.caption("Set your ANTHROPIC_API_KEY environment variable to get AI-powered explanations!")

        # --- Comparison table ---
        st.divider()
        st.header("Full Comparison")

        table_data = {}
        for name, scores in neighborhoods.items():
            table_data[name] = {factor_labels[k]: v for k, v in scores.items()}

        df = pd.DataFrame(table_data).T
        df.index.name = "Neighborhood"
        df = df.loc[[name for name, _ in ranked]]  # sort by rank
        st.dataframe(df, width="stretch")

        # --- Data sources ---
        st.divider()
        st.caption("Data sources: Walk Score, Zumper, liv.rent, VPD GeoDASH, Destination Vancouver (2025-2026)")
