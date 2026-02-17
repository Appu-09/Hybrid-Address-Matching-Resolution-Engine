**Hybrid Address Matching & Resolution Engine**

A production-style address matching system built to accurately detect duplicate and similar addresses using a hybrid approach combining rule-based validation and fuzzy similarity scoring.

🔗 Live Demo: https://hybrid-address-matching-resolution-engine-nqt9fdrgvbewf9x9flmc.streamlit.app/



📌 **Problem Statement**

Real-world address data is messy.

Addresses may contain:

1. Abbreviations (Rd vs Road)

2. Typos

3. Different word order

4. Missing components

5. Extra tokens like “Flat”, “Plot”, etc.

Simple string comparison fails in such scenarios.
This project solves that using structured extraction + intelligent similarity scoring.

🧠 **Solution Approach**

This system uses a hybrid matching strategy:

1️⃣ **Address Normalization**

* Converts text to lowercase

* Expands locality abbreviations (Rd → Road, St → Street)

* Cleans tokens for structured comparison

2️⃣ **Component Extraction**

* Extracts structured elements from raw address text:

* PIN Code

* City

* House Number

* Locality

* Full text (for fuzzy matching)

3️⃣ **Weighted Scoring System**

* Each component contributes to final confidence:

Component	Weight
PIN Match	- 40
City Match -  20
House Number - 15
Locality -	15
Fuzzy Similarity - 10%

If PIN conflicts → immediate NO MATCH

**Final decision**:

Score ≥ Threshold → MATCH

Score < Threshold → NO MATCH

4️⃣ **Fuzzy Matching**
* Uses token sort similarity to handle:

* Word order differences

* Minor spelling variations

* Extra tokens

🚀 **Features**

-> Rule-based validation

-> Fuzzy token similarity

-> Abbreviation normalization

-> Confidence scoring breakdown

-> Batch address matching

-> Interactive Streamlit UI

🛠 **Tech Stack**

* Python

* Pandas

* RapidFuzz

* Regular Expressions (Regex)

* Streamlit

🖥 **Application Interface**

The web app allows users to:

Enter two addresses

Click “Check Match”

View:

MATCH / NO MATCH

Confidence Score

Detailed score breakdown

Designed to simulate real-world deduplication workflows.
