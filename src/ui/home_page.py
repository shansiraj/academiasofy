import streamlit as st
from src.modules.searcher import search
from src.modules.pdf_reader import extract_relevant_snippet, extract_metadata
from src.modules.file_mapper import load_file_map

def main():

    file_map = load_file_map()

    # Streamlit app layout
    st.set_page_config(page_title="Research Search Engine", layout="wide")

    # Sidebar
    with st.sidebar:
        
        st.markdown(
            """
            <style>
            [data-testid="stSidebar"] {
                background-color: #212B39; /* Light gray background color */
                padding-top: 0px;
            }
            .center-text {
                text-align: center;
                color: white;
                font-size: 14px;
            }
            .white-line {
                border: 1px solid white;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )
                
        st.sidebar.image("img/logo.png", use_container_width=True)
        st.markdown('<p class="center-text">This Search Engine searches a collection of PDF research papers across multiple domain-specific folders in the AcademiaSoft Research Paper Repository, with each paper named using a unique document ID for easy identification.</p>', unsafe_allow_html=True)
        st.markdown('<hr class="white-line">', unsafe_allow_html=True)
        st.markdown('<p class="center-text">Developed by D. Shan Siraj</p>', unsafe_allow_html=True)
        st.markdown('<p class="center-text">STNO: COMSCDS231P-023</p>', unsafe_allow_html=True)

    st.title("AcademiaSofy: Research Paper Search Engine")
    query = st.text_input("Search for research papers:")

    if query:

        # Perform search
        results = search(query)
        
        if results:
            st.write("Search Results:")
            print (results)
            for doc, score in results:

                st.markdown(
                    f"""
                    <p style="font-weight: bold; display: inline;">Paper: </p>
                    <p style="font-weight: bold; color: blue; display: inline;">{doc}</p>
                    <p style="font-weight: bold; color: red; display: inline;"> (Score: {score})</p>
                    """, unsafe_allow_html=True
                )

                if doc in file_map:
                    pdf_path = file_map[doc]
                    print(f"File path: {pdf_path}")
                else:
                    print(f"{doc} not found.")
                
                # Extract metadata (e.g., name and abstract)
                metadata = extract_metadata(pdf_path)
                name = metadata.get("name", "Unknown Title")
                abstract = metadata.get("abstract", "Abstract not available.")
                
                # Display metadata
                if name != None and name.strip()!="":
                    st.subheader(name)
                if abstract != None and abstract.strip()!="":
                    st.write(f"Abstract: {abstract}")
                
                # Extract relevant snippet
                relevant_snippet = extract_relevant_snippet(query, pdf_path)

                st.markdown(
                            f"""
                            <p style="font-weight: bold; display: inline;">Text Extract: </p>
                            {relevant_snippet}
                            """, unsafe_allow_html=True)
                
                try:
                    # Add download link
                    with open(pdf_path, "rb") as file:
                        st.download_button(
                            label=f"Download Paper",
                            data=file,
                            file_name=doc,
                            mime="application/pdf"
                        )
                except Exception as exp:
                    st.write("Downloading not supported")

                st.markdown('---')
        else:
            st.write("No results found.")

if __name__ == "__main__":
    main()
