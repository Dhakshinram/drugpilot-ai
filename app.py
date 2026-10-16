
import requests
import streamlit as st

API_URL = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"

st.set_page_config(
    page_title="DrugPilot AI",
    page_icon="🔬",
    layout="wide",
)

st.title("🔬 DrugPilot AI")
st.caption("Evidence-first scientific literature research")

st.markdown("""
Welcome to **DrugPilot AI**.

Search scientific literature, inspect research abstracts,
and open original source records. AI-powered analysis
will be added in the next milestone.
""")

st.divider()

query = st.text_input(
    "Enter a research topic",
    value="EGFR AND non-small cell lung cancer",
    placeholder="Example: cancer and gene expression",
)

limit = st.slider(
    "Maximum papers to retrieve",
    min_value=5,
    max_value=20,
    value=10,
)

if st.button("Search Research Papers", type="primary"):

    if not query.strip():
        st.warning("Please enter a research topic.")

    else:
        try:
            with st.spinner("Searching Europe PMC..."):

                response = requests.get(
                    API_URL,
                    params={
                        "query": query.strip(),
                        "format": "json",
                        "pageSize": limit,
                        "resultType": "core",
                    },
                    timeout=30,
                )

                response.raise_for_status()

                papers = response.json().get(
                    "resultList", {}
                ).get("result", [])

            st.subheader(
                f"Research Results: {len(papers)} papers found"
            )

            if not papers:
                st.info(
                    "No papers found. Try a broader search term."
                )

            for number, paper in enumerate(papers, start=1):

                title = paper.get("title") or "Untitled paper"
                year = paper.get("pubYear") or "Year unavailable"

                abstract = (
                    paper.get("abstractText")
                    or "No abstract is available in this record."
                )

                pmid = paper.get("pmid")
                doi = paper.get("doi")

                if pmid:
                    source_url = (
                        f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"
                    )
                elif doi:
                    source_url = f"https://doi.org/{doi}"
                else:
                    source_url = "https://europepmc.org/"

                with st.expander(f"{number}. {title} ({year})"):
                    st.markdown("**Abstract**")
                    st.write(abstract)

                    st.markdown(
                        f"[Read the source record]({source_url})"
                    )

                    if pmid:
                        st.caption(f"PubMed ID: {pmid}")

                    if doi:
                        st.caption(f"DOI: {doi}")

            st.caption(
                "Always consult original studies and their limitations. "
                "A search result alone does not establish a claim."
            )

        except requests.RequestException as error:
            st.error(
                "Unable to retrieve papers. Check your internet "
                "connection and try again."
            )
            st.caption(f"Technical details: {error}")

        except (ValueError, KeyError):
            st.error(
                "The research service returned unexpected data."
            )
