flowchart TD
    A[User Input] -->|Sent to Backend| B[Flask Backend]
    B -->|Pass Input| C[FAISS Index Query]
    C -->|Retrieve Relevant Context| D[Retrieved Context]
    D -->|Combine with Input| E[LLaMA Model]
    E -->|Generate Response| F[Response to User]
    
    subgraph Preprocessing
        G[Extract Text from PDF] --> H[Generate Embeddings with LLaMA]
        H --> I[Store Embeddings in FAISS Index]
    end

    B -.->|Already Preprocessed| Preprocessing
