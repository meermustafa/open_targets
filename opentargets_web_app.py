import streamlit as st
import requests
import json

# Define the Open Targets API endpoint
OPEN_TARGETS_API_URL = "https://api.platform.opentargets.org/api/v4/graphql"

# Define the GraphQL query
QUERY_TEMPLATE = """
query associatedDiseases {
  target(ensemblId: "%s") {
    id
    approvedSymbol
    associatedDiseases {
      count
      rows {
        disease {
          id
          name
        }
        
      }
    }
  }
}
"""

# Define a function to execute the GraphQL query
def execute_query(gene, n):
    query = QUERY_TEMPLATE % (gene)
    response = requests.post(OPEN_TARGETS_API_URL, json={'query': query})
    response_data = response.json()
    associateDiseases = response_data['data']['target']['associatedDiseases']['rows']
    return associateDiseases[:n]


# Define the Streamlit app
def app():
    st.title("Top Diseases Linked to a Gene")

    # Get user input for gene and number of diseases to retrieve
    gene = st.text_input("Enter a gene (e.g. HBB):")
    size = st.slider("Number of diseases to retrieve:", min_value=1, max_value=50, value=10)

    # Execute the GraphQL query and display the results
    if gene:
        try:
            ensembl_id = get_ensembl_id(gene)
            st.write(ensembl_id)
            diseases = execute_query(ensembl_id, size)
            if diseases:
                st.subheader("Top Diseases Linked to %s" % gene)
                for i, disease in enumerate(diseases):
                    st.write("%d. %s (ID: %s)" % (i+1, disease['disease']['name'], disease['disease']['id']))
            else:
                st.write("No diseases found for gene %s" % gene)
        except:

            st.write("Error retrieving data from Open Targets API. Please try again later.")

def get_ensembl_id(gene_symbol):
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    url = f"https://rest.ensembl.org/xrefs/symbol/homo_sapiens/{gene_symbol}?object_type=gene"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if len(data) > 0:
            return str(data[0]["id"])
    return None


app()
test = get_ensembl_id("ABCA4")
execute_query(test, 2)