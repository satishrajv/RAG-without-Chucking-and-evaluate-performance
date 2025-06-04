import os

def create_project_structure():
    # Define the project structure
    project_structure = {
                    "data_ingestion": ["azure_watcher.py", "pdf_loader.py", "chunker.py", "ingestion_pipeline.py"],
            "embeddings": ["embedder.py", "vector_store.py", "index_builder.py"],
            "retrieval": ["retriever.py", "reranker.py", "evaluator.py"],
            "llm_interface": ["prompt_template.py", "llm_query.py", "docx_renderer.py"],
            "notebooks": ["1_getting_started.ipynb", "2_pipeline_demo.ipynb"],
            "": [".env", "requirements.txt", "README.md", "main.py"]  # Root files
        
    }

    # Create directories and files
    for project, contents in project_structure.items():
        if not os.path.exists(project):
            os.makedirs(project)
            print(f"Created directory: {project}")

        for folder, files in contents.items():
            folder_path = os.path.join(project, folder) if folder else project
            if folder and not os.path.exists(folder_path):
                os.makedirs(folder_path)
                print(f"Created directory: {folder_path}")

            for file in files:
                file_path = os.path.join(folder_path, file)
                if not os.path.exists(file_path):
                    with open(file_path, "w") as f:
                        f.write("")  # Create empty file
                    print(f"Created file: {file_path}")

if __name__ == "__main__":
    print("Creating AgenticAI-RAG project structure...")
    create_project_structure()
    print("Project structure created successfully!")