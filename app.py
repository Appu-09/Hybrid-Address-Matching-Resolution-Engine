import streamlit as st
import re
from fuzzywuzzy import fuzz

# -------------------------
# Address Matching Function
# -------------------------
def decide_match_v6(addr1, addr2, threshold=70):

    def extract_components(address):
        address = address.lower()

        pin = re.search(r"\b\d{6}\b", address)
        pin = pin.group() if pin else None

        city = "hyderabad" if "hyderabad" in address else None

        house = re.search(r"\b\d+\w?\b", address)

        house = house.group() if house else None

        return {
            "pin": pin,
            "city": city,
            "house": house,
            "full": address
        }

    comp1 = extract_components(addr1)
    comp2 = extract_components(addr2)

    if comp1["pin"] and comp2["pin"] and comp1["pin"] != comp2["pin"]:
        return {
            "decision": "NO MATCH",
            "confidence_score": 0,
            "breakdown": {"pin": "conflict"}
        }

    score = 0
    breakdown = {}

    if comp1["pin"] == comp2["pin"]:
        score += 40
        breakdown["pin"] = 40

    if comp1["city"] == comp2["city"]:
        score += 20
        breakdown["city"] = 20

    if comp1["house"] == comp2["house"]:
        score += 15
        breakdown["house"] = 15

    fuzzy_score = fuzz.token_sort_ratio(comp1["full"], comp2["full"])
    fuzzy_points = fuzzy_score * 0.1
    score += fuzzy_points
    breakdown["fuzzy"] = round(fuzzy_points, 2)

    decision = "MATCH" if score >= threshold else "NO MATCH"

    return {
        "decision": decision,
        "confidence_score": round(score, 2),
        "breakdown": breakdown
    }


# -------------------------
# Streamlit UI
# -------------------------

st.set_page_config(page_title="Address Match Checker", layout="centered")

st.title("🏠 Address Match Checker")
st.write("Compare two addresses and check if they match.")

addr1 = st.text_area("Enter Address 1")
addr2 = st.text_area("Enter Address 2")

if st.button("Check Match"):
    if addr1 and addr2:
        result = decide_match_v6(addr1, addr2)

        st.subheader("Result")
        st.write(f"**Decision:** {result['decision']}")
        st.write(f"**Confidence Score:** {result['confidence_score']}")
        st.json(result["breakdown"])
    else:
        st.warning("Please enter both addresses.")
