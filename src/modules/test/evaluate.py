import numpy as np
import pandas as pd
from sklearn.metrics import ndcg_score
from src.modules.searcher import search

# List of queries
queries = [
    # Short Queries:
    "Economic modeling advancements",
    "Feature engineering",
    "AI in healthcare",
    "Quantum discord",
    "Geometric deep learning",
    # Long Queries:
    "How do modern models integrate machine learning and econometrics to analyze global carbon budgets and decision-making frameworks?",
    "How can advanced feature engineering improve predictive modeling and environmental systems integration?",
    "How does artificial intelligence impact healthcare systems and ethical considerations in medicine?",
    "How does quantum discord influence modern quantum information theory?",
    "How do transformation-invariant representations contribute to geometric deep learning frameworks?",
    # Queries with stop words:
    "What are the latest applications of stochastic frontier models and deep learning in economic analysis?",
    "What are the latest advances in machine learning and feature engineering?",
    "What are the latest advancements in artificial intelligence for healthcare and medicine?",
    "What are evolutionary insights from ancient DNA research?",
    "What is strategic bidding in frequency containment markets?",
    # Queries without stop words:
    "Stochastic frontier models deep learning economic analysis",
    "Machine learning feature engineering advances",
    "Latest advancements AI healthcare medicine",
    "Evolutionary insights ancient DNA research",
    "Strategic bidding frequency containment markets",
    # Queries different keywords:
    "Efficiency modeling vs revenue estimation in economics",
    "Simulation hybrid networks ns-3 LIMoSim",
    "COVID-19 immunopathogenesis treatments",
    "Galaxy morphology classification",
    "3D motion estimation with stereo data",
]

query_ground_truth = [
    # Economics
    # Engineering
    # Health and Medicine
    # Natural Sciences
    # Science and Technology

    # Query 1 (Short Query): "Economic modeling advancements"
    {
        "2412.08342v1.pdf": 5,  # Approximate Revenue from Finite Range
        "2412.08831v1.pdf": 4,  # Panel Stochastic Frontier Models with Latent Group
        "2412.08850v1.pdf": 3,  # Emulating the Global Change Analysis Model with Deep Learning
        "2412.09321v1.pdf": 3,  # Learning to be Indifferent in Complex Decisions
        "2412.09226v1.pdf": 2   # The Global Carbon Budget as a Cointegrated System
    },
    # Query 1 (Short Query): "Feature engineering"
    {
        "1701.07852v2.pdf": 5,  # An Empirical Analysis of Feature Engineering for Predictive Modeling
        "3514228.pdf": 4,       # Integrating Scientific Knowledge with Machine Learning for Engineering and Environmental Systems
        "2101.06374v4.pdf": 3,  # A Conditional Generative Model for Dynamic Trajectory Generation
        "2003.09829v1.pdf": 2,  # Simulating Hybrid Aerial- and Ground-based Vehicular Networks with ns-3 and LIMoSim
        "2012.04895v1.pdf": 1   # Contribution of residual quasiparticles to superconducting thin-film resonators
    },
    # Query 1 (Short Query): "AI in healthcare"
    {
        "2001.09778v2.pdf": 5,  # Artificial intelligence in medicine and healthcare
        "s41392-020-00243-2.pdf": 4,  # COVID-19 - immunopathogenesis and Immunotherapeutics
        "westjmed00102-0060.pdf": 3,  # Brain Tumors
        "annsurg00049-0057.pdf": 2,  # Intravenous Contrast Medium and Pancreatic Microcirculation
        "13831-1-10-20220501.pdf": 1   # Food Additives and Good Food Production
    },
    # Query 1 (Short Query): "Quantum discord"
    {
        "2007.12345v1.pdf": 5,  # Comment on quantum-discord states
        "2412.09358v1.pdf": 2,  # Galaxy Morphological Classification with Manifold Learning
        "2412.09542v1.pdf": 1,  # Controlled Four-Parameter Method for Wave Systems
        "2412.09592v1.pdf": 1,  # JWST PRIMER
        "2412.08498v1.pdf": 1   # Immune cell clustering
    },
    # Query 1 (Short Query): "Geometric deep learning"
    {
        "2112.12345v1.pdf": 5,  # Revisiting Transformation Invariant Geometric Deep Learning
        "2412.09621v1.pdf": 2,  # Stereo4D: Learning How Things Move in 3D
        "2412.09625v1.pdf": 1,  # Illusion3D: 3D Multiview Illusion
        "2412.09627v1.pdf": 1,  # Closed-Loop Autonomous Driving
        "2412.09181v1.pdf": 1   # Strategic Bidding
    },

    # Query 2 (Long Query): "How do modern models integrate machine learning and econometrics to analyze global carbon budgets and decision-making frameworks?"
    {
        "2412.08850v1.pdf": 5,  # Emulating the Global Change Analysis Model with Deep Learning
        "2412.09226v1.pdf": 4,  # The Global Carbon Budget as a Cointegrated System
        "2412.08831v1.pdf": 3,  # Panel Stochastic Frontier Models with Latent Group
        "2412.09321v1.pdf": 3,  # Learning to be Indifferent in Complex Decisions
        "2412.08342v1.pdf": 2   # Approximate Revenue from Finite Range
    },
    # Query 2 (Long Query): "How can advanced feature engineering improve predictive modeling and environmental systems integration?"
    {
        "1701.07852v2.pdf": 5,  # An Empirical Analysis of Feature Engineering for Predictive Modeling
        "3514228.pdf": 4,       # Integrating Scientific Knowledge with Machine Learning for Engineering and Environmental Systems
        "2003.09829v1.pdf": 3,  # Simulating Hybrid Aerial- and Ground-based Vehicular Networks with ns-3 and LIMoSim
        "2101.06374v4.pdf": 2,  # A Conditional Generative Model for Dynamic Trajectory Generation
        "2012.04895v1.pdf": 1   # Contribution of residual quasiparticles to superconducting thin-film resonators
    },
    # Query 2 (Long Query): "How does artificial intelligence impact healthcare systems and ethical considerations in medicine?"
    {
        "2001.09778v2.pdf": 5,  # Artificial intelligence in medicine and healthcare
        "s41392-020-00243-2.pdf": 4,  # COVID-19 - immunopathogenesis and Immunotherapeutics
        "annsurg00049-0057.pdf": 3,  # Intravenous Contrast Medium and Pancreatic Microcirculation
        "westjmed00102-0060.pdf": 2,  # Brain Tumors
        "13831-1-10-20220501.pdf": 1   # Food Additives and Good Food Production
    },
    # Query 2 (Long Query): "How does quantum discord influence modern quantum information theory?"
    {
        "2007.12345v1.pdf": 5,  # Comment on quantum-discord states
        "2412.09542v1.pdf": 3,  # Controlled Four-Parameter Method for Wave Systems
        "2412.09358v1.pdf": 2,  # Galaxy Morphological Classification with Manifold Learning
        "bioinformatics_24_1_1.pdf": 1,  # Computational epigenetics
        "2412.09592v1.pdf": 1   # JWST PRIMER
    },
    # Query 2 (Long Query): "How do transformation-invariant representations contribute to geometric deep learning frameworks?"
    {
        "2112.12345v1.pdf": 5,  # Revisiting Transformation Invariant Geometric Deep Learning
        "2412.09625v1.pdf": 3,  # Illusion3D: 3D Multiview Illusion
        "2412.09621v1.pdf": 2,  # Stereo4D: Learning How Things Move in 3D
        "2412.09181v1.pdf": 1,  # Strategic Bidding
        "2412.09627v1.pdf": 1   # Closed-Loop Autonomous Driving
    },

    # Query 3 (Query with Stop Words): "What are the latest applications of stochastic frontier models and deep learning in economic analysis?"
    {
        "2412.08831v1.pdf": 5,  # Panel Stochastic Frontier Models with Latent Group
        "2412.08850v1.pdf": 5,  # Emulating the Global Change Analysis Model with Deep Learning
        "2412.09321v1.pdf": 3,  # Learning to be Indifferent in Complex Decisions
        "2412.08342v1.pdf": 2,  # Approximate Revenue from Finite Range
        "2412.09226v1.pdf": 2   # The Global Carbon Budget as a Cointegrated System
    },

    # Query 3 (Query with Stop Words): "What are the latest advances in machine learning and feature engineering?"
    {
        "1701.07852v2.pdf": 5,  # An Empirical Analysis of Feature Engineering for Predictive Modeling
        "3514228.pdf": 4,       # Integrating Scientific Knowledge with Machine Learning for Engineering and Environmental Systems
        "2101.06374v4.pdf": 3,  # A Conditional Generative Model for Dynamic Trajectory Generation
        "2003.09829v1.pdf": 2,  # Simulating Hybrid Aerial- and Ground-based Vehicular Networks with ns-3 and LIMoSim
        "2012.04895v1.pdf": 1   # Contribution of residual quasiparticles to superconducting thin-film resonators
    },
    # Query 3 (Query with Stop Words): "What are the latest advancements in artificial intelligence for healthcare and medicine?"
    {
        "2001.09778v2.pdf": 5,  # Artificial intelligence in medicine and healthcare
        "s41392-020-00243-2.pdf": 4,  # COVID-19 - immunopathogenesis and Immunotherapeutics
        "westjmed00102-0060.pdf": 3,  # Brain Tumors
        "annsurg00049-0057.pdf": 2,  # Intravenous Contrast Medium and Pancreatic Microcirculation
        "13831-1-10-20220501.pdf": 1   # Food Additives and Good Food Production
    },
    # Query 3 (Query with Stop Words): "What are evolutionary insights from ancient DNA research?"
    {
        "2412.06521v1.pdf": 5,  # Ancient DNA from Lycoptera fossils
        "2412.07678v1.pdf": 4,  # Can linguists better understand DNA?
        "bioinformatics_24_1_1.pdf": 3,  # Computational epigenetics
        "2412.08498v1.pdf": 2,  # Immune cell clustering in proteomics
        "2412.09560v1.pdf": 1   # Large Language Models for Materials Research
    },
    # Query 3 (Query with Stop Words): "What is strategic bidding in frequency containment markets?"
    {
        "2412.09181v1.pdf": 5,  # Strategic Bidding in Frequency-Containment Markets
        "2112.12345v1.pdf": 1,  # Revisiting Geometric Deep Learning
        "2412.09621v1.pdf": 1,  # Stereo4D: Learning How Things Move
        "2412.09627v1.pdf": 1,  # Closed-Loop Autonomous Driving
        "2412.09625v1.pdf": 1   # Illusion3D: 3D Multiview Illusion
    },

    # Query 4 (Query without Stop Words): "Stochastic frontier models deep learning economic analysis"
    {
        "2412.08831v1.pdf": 5,  # Panel Stochastic Frontier Models with Latent Group
        "2412.08850v1.pdf": 4,  # Emulating the Global Change Analysis Model with Deep Learning
        "2412.09226v1.pdf": 2,  # The Global Carbon Budget as a Cointegrated System
        "2412.09321v1.pdf": 2,  # Learning to be Indifferent in Complex Decisions
        "2412.08342v1.pdf": 1   # Approximate Revenue from Finite Range
    },
    # Query 4 (Query without Stop Words): "Machine learning feature engineering advances"
    {
        "1701.07852v2.pdf": 5,  # An Empirical Analysis of Feature Engineering for Predictive Modeling
        "3514228.pdf": 4,       # Integrating Scientific Knowledge with Machine Learning for Engineering and Environmental Systems
        "2101.06374v4.pdf": 3,  # A Conditional Generative Model for Dynamic Trajectory Generation
        "2003.09829v1.pdf": 2,  # Simulating Hybrid Aerial- and Ground-based Vehicular Networks with ns-3 and LIMoSim
        "2012.04895v1.pdf": 1   # Contribution of residual quasiparticles to superconducting thin-film resonators
    },
    # Query 4 (Query without Stop Words): "Latest advancements AI healthcare medicine"
    {
        "2001.09778v2.pdf": 5,  # Artificial intelligence in medicine and healthcare
        "s41392-020-00243-2.pdf": 4,  # COVID-19 - immunopathogenesis and Immunotherapeutics
        "westjmed00102-0060.pdf": 3,  # Brain Tumors
        "annsurg00049-0057.pdf": 2,  # Intravenous Contrast Medium and Pancreatic Microcirculation
        "13831-1-10-20220501.pdf": 1   # Food Additives and Good Food Production
    },
    # Query 4 (Query without Stop Words): "Evolutionary insights ancient DNA research"
    {
        "2412.06521v1.pdf": 5,  # Ancient DNA from Lycoptera fossils
        "2412.07678v1.pdf": 4,  # Can linguists better understand DNA?
        "bioinformatics_24_1_1.pdf": 3,  # Computational epigenetics
        "2412.08498v1.pdf": 2,  # Immune cell clustering in proteomics
        "2412.09358v1.pdf": 1   # Galaxy Morphological Classification
    },
    # Query 4 (Query without Stop Words): "Strategic bidding frequency containment markets"
    {
        "2412.09181v1.pdf": 5,  # Strategic Bidding in Frequency-Containment Markets
        "2112.12345v1.pdf": 2,  # Revisiting Geometric Deep Learning
        "2412.09621v1.pdf": 1,  # Stereo4D: Learning How Things Move
        "2412.09627v1.pdf": 1,  # Closed-Loop Autonomous Driving
        "2412.09625v1.pdf": 1   # Illusion3D: 3D Multiview Illusion
    },

    # Query 5 (Different Keywords): "Efficiency modeling vs revenue estimation in economics"
    {
        "2412.08342v1.pdf": 5,  # Approximate Revenue from Finite Range
        "2412.08831v1.pdf": 5,  # Panel Stochastic Frontier Models with Latent Group
        "2412.09321v1.pdf": 3,  # Learning to be Indifferent in Complex Decisions
        "2412.08850v1.pdf": 3,  # Emulating the Global Change Analysis Model with Deep Learning
        "2412.09226v1.pdf": 2   # The Global Carbon Budget as a Cointegrated System
    },
    # Query 5 (Different Keywords): "Simulation hybrid networks ns-3 LIMoSim"
    {
        "2003.09829v1.pdf": 5,  # Simulating Hybrid Aerial- and Ground-based Vehicular Networks with ns-3 and LIMoSim
        "2101.06374v4.pdf": 4,  # A Conditional Generative Model for Dynamic Trajectory Generation
        "3514228.pdf": 3,       # Integrating Scientific Knowledge with Machine Learning for Engineering and Environmental Systems
        "1701.07852v2.pdf": 2,  # An Empirical Analysis of Feature Engineering for Predictive Modeling
        "2012.04895v1.pdf": 1   # Contribution of residual quasiparticles to superconducting thin-film resonators
    },
    # Query 5 (Different Keywords): "COVID-19 immunopathogenesis treatments"
    {
        "s41392-020-00243-2.pdf": 5,  # COVID-19 - immunopathogenesis and Immunotherapeutics
        "2001.09778v2.pdf": 4,  # Artificial intelligence in medicine and healthcare
        "annsurg00049-0057.pdf": 3,  # Intravenous Contrast Medium and Pancreatic Microcirculation
        "westjmed00102-0060.pdf": 2,  # Brain Tumors
        "13831-1-10-20220501.pdf": 1   # Food Additives and Good Food Production
    },
    # Query 5 (Different Keywords): "Galaxy morphology classification"
    {
        "2412.09358v1.pdf": 5,  # Galaxy Morphological Classification with Manifold Learning
        "2412.09435v1.pdf": 4,  # FBQ0951+2635: Lensing galaxy structure
        "2412.09592v1.pdf": 3,  # JWST PRIMER
        "2007.12345v1.pdf": 2,  # Comment on quantum-discord states
        "2412.09542v1.pdf": 1   # Controlled Four-Parameter Method
    },
    # Query 5 (Different Keywords): "3D motion estimation with stereo data"
    {
        "2412.09621v1.pdf": 5,  # Stereo4D: Learning How Things Move in 3D
        "2412.09625v1.pdf": 4,  # Illusion3D: 3D Multiview Illusion
        "2412.09627v1.pdf": 3,  # Closed-Loop Autonomous Driving
        "2112.12345v1.pdf": 2,  # Revisiting Geometric Deep Learning
        "2412.09181v1.pdf": 1   # Strategic Bidding
    },
]

def main():

    results_table = []

    for idx, query in enumerate(queries):
        # Perform the search for the current query
        results = search(query)
        
        # Retrieve ground truth relevance for the current query
        ground_truth_relevance = query_ground_truth[idx]

        # Extract file names from the search results
        file_names = [file[0] for file in results]
        tfidf_scores = [file[1] for file in results]
        
        # Ensure the length matches by truncating or padding
        ground_truth_values = list(ground_truth_relevance.values())
        predicted_values= [ground_truth_relevance.get(file, 0) for file in file_names]
        
        # Truncate or pad predicted relevance to match ground truth length
        if len(predicted_values) > len(ground_truth_values):
            predicted_values = predicted_values[:len(ground_truth_values)]
        elif len(predicted_values) < len(ground_truth_values):
            predicted_values += [0] * (len(ground_truth_values) - len(predicted_values))
        
        # Compute nDCG
        ndcg = ndcg_score([ground_truth_values], [predicted_values])

        # Get the TF-IDF score of the first file
        first_tfidf_score = tfidf_scores[0] if tfidf_scores else 0.0

        # Store the results for this query in the table
        results_table.append({
            "Query": query,
            "Actual Relevance": ground_truth_values,
            "Predicted Relevance": predicted_values,
            "TF-IDF Score (First File)": first_tfidf_score,
            "nDCG Score": ndcg
        })
        
        # Create a DataFrame from the results
        results_df = pd.DataFrame(results_table)
        print(results_df)
        results_df.to_csv("query_results.csv", index=False)