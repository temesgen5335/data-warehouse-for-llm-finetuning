# Scalable Data Warehouse for LLM Finetuning: API Design for High Throughput Data Ingestion and RAG Retrieval

## Introduction

This project aims to create a scalable data warehouse for Language Model (LLM) fine-tuning. The data warehouse will store and manage the data collected in the specified language, in this case Amharic, which will be used for training and fine-tuning LLM. Docker has been used to ensure a seamless setup and deployment process.
## Features

- **Amharic Language Support**: Our data warehouse is specifically designed to handle and manage data in the Amharic language. This makes it an ideal choice for projects involving the training of large language models on Amharic data.

- **Highly Scalable Data Storage**: Our data warehouse is engineered to handle massive data volumes, making it an ideal choice for projects involving the training of large language models.

-  **Efficient Data Management**: This project provides a different tools for efficient data management, including features for data ingestion and transformation. This ensures that the Amharic data is always ready for training the LLM.

- **User-friendly Interface built with ReactJS**: The project provides a user-friendly interface for interacting with the data warehouse. This makes it easy for users to manage, search, and access the data required for training the LLM.

- **Docker Integration**: Docker has been used in the project to provide a smooth setup and deployment process. This allows users to quickly get the project up and running on their systems, regardless of their operating system.

- **Flexibility in language integration**: The project is designed to be flexible, especially the rest of the other parts like API, dashboard and storage except the preprocessing which becomes unique for each language. Therefore, it can be easily extended to support other languages.

## Requirements Before Installation
  - Docker: This is used for creating, deploying, and running applications by using containers.
  - Docker Compose: This is a tool for defining and managing multi-container Docker applications.
  - Python: The project requires a Python version ~= 3.10.12

### Setup and Installation
1. **Clone the Repository**
    ```bash
    git clone git@github.com:10AcademyG4/data-warehouse-for-llm-finetuning.git
    cd data-warehouse-for-llm-finetuning
    ```

2. **Create a Virtual Environment and Install Dependencies**
```bash
python3.10 -m venv venv
source venv/bin/activate  # For Unix or MacOS
venv\Scripts\activate     # For Windows
pip install -r requirements.txt
```

4. **Environment Variables**
    - Create a `.env` file in the root directory and add the following environment variables:


5. **Build the application**

   - Run the following commands to get the container up and running and start the application:
      ```bash
     make up
      ```

6. **Access the Application**
   - The FastAPI api can be accessed from the url `http://localhost:8000` on your local machine.

## Testing
- To run the tests, execute the following command:
    ```bash
    make test
    ```
- This will run the tests using the `pytest` framework on the files in the `tests`  and also files with the naming convention `test_*.py` in project directory.
- The Api tests are written to test the endpoints of the FastAPI application.
    
## Conclusion
The scalable data warehouse for LLM fine-tuning is an essential tool for managing the data used for training large language models. By following the installation steps outlined in this guide, you can set up the data warehouse and start leveraging its features in your LLM training workflow.


## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```
