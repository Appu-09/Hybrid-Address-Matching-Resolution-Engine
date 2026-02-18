import streamlit as st
import re
from fuzzywuzzy import fuzz

# -------------------------
# Address Matching Function
# -------------------------
def decide_match_v7(addr1, addr2, threshold=50):

    def extract_components(address):
        address = address.lower()

        # PINCODE (strict 6-digit)
        pin_match = re.search(r"\b\d{6}\b", address)
        pin = pin_match.group() if pin_match else None

        # CITY (expandable list)
        city = None
        cities = ["hyderabad", "bangalore", "mumbai", "delhi"]
        for c in cities:
            if c in address:
                city = c
                break

        # HOUSE NUMBER
        house_match = re.search(r"\b\d+\w?\b", address)
        house = house_match.group() if house_match else None

        return {
            "pin": pin,
            "city": city,
            "house": house,
            "full": address
        }

    comp1 = extract_components(addr1)
    comp2 = extract_components(addr2)

    # Immediate NO MATCH if PINs exist and conflict
    if comp1["pin"] and comp2["pin"] and comp1["pin"] != comp2["pin"]:
        return {
            "decision": "NO MATCH",
            "confidence_score": 0,
            "breakdown": {"pin": "conflict"}
        }

    score = 0
    breakdown = {}

    # PIN Match (40 points)
    if comp1["pin"] and comp2["pin"] and comp1["pin"] == comp2["pin"]:
        score += 40
        breakdown["pin"] = 40

    # City Match (20 points)
    if comp1["city"] and comp2["city"] and comp1["city"] == comp2["city"]:
        score += 20
        breakdown["city"] = 20

    # House Match (15 points)
    if comp1["house"] and comp2["house"] and comp1["house"] == comp2["house"]:
        score += 15
        breakdown["house"] = 15

    # Fuzzy Similarity (0–40 points now)
    fuzzy_score = fuzz.token_sort_ratio(comp1["full"], comp2["full"])
    fuzzy_points = fuzzy_score * 0.4
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
        result = decide_match_v7(addr1, addr2)

        st.subheader("Result")
        st.write(f"**Decision:** {result['decision']}")
        st.write(f"**Confidence Score:** {result['confidence_score']}")
        st.json(result["breakdown"])
    else:
        st.warning("Please enter both addresses.")
