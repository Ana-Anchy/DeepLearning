# DeepLearning

# 📚 PDF RAG-Chatbot with Gemini

## 🧑‍💻 Project Overview

This project implements a **Retrieval-Augmented Generation (RAG)** chatbot designed to answer questions about a **PDF-based thesis**. The chatbot utilizes **Google Gemini API** for **semantic search** and **answer generation** based on content extracted from the PDF.

The aim of the project is to explore how an AI chatbot can interact with academic texts (theses) and provide dynamic, contextually relevant answers to questions.

---

## 🏗️ Project Workflow

### 🔬 **Data Collection & Preprocessing**
- **PDF Document**: The source of the data is an **exam thesis** in PDF format, which serves as the primary document for the chatbot's answers.
- **Text Extraction**: The content from the PDF is extracted using Python libraries like **PyPDF2** and stored in manageable text chunks.
- **Chunking**: The PDF text is split into chunks for more efficient retrieval during the chatbot’s operations.

---

### 🧹 **Data Processing**
- **Chunking**: 
    - The PDF is processed into **text chunks**, typically around 500-1000 characters.
    - **Embedding**: Text chunks are passed through the **Google Gemini API** for **embedding** and semantic analysis.
    - **Preprocessing** includes cleaning the data, removing unnecessary characters, and structuring it for use in the chatbot.

---

### 🤖 **Model Development**
- **RAG (Retrieval-Augmented Generation)**: Combines a **retriever** (for semantic search) and a **generator** (for generating answers).
    - **Retriever**: Finds relevant chunks from the PDF based on the question.
    - **Generator**: Uses those chunks to generate relevant and contextually accurate answers.
- **Google Gemini API**: Used to handle both the retrieval and generation tasks.
- **Early Stopping**: Prevented overfitting by stopping the training when performance plateaued.

---

### 🧪 **Model Evaluation & Testing**
- **Evaluation System**: Used a **manual evaluation** system to score the chatbot’s performance on generated answers. The evaluation is based on **relevance**, **accuracy**, and **clarity**.
- **Testing Questions**:
    - *What is the purpose of the thesis?*
    - *What methodology was used?*
    - *What is the conclusion of the thesis?*

These questions were asked during testing to see how accurately the chatbot could respond to questions directly related to the thesis content.

- **Scoring**: Each answer was rated on a scale of **0-10** based on how relevant and accurate the chatbot's response was.

---

## 📝 **Key Features**
- **Semantic Search**: The chatbot utilizes **semantic search** to identify relevant sections of the PDF based on user queries.
- **Embedding**: The text from the PDF is transformed into **embeddings** to better understand and match the user's questions.
- **Model Evaluation**: The chatbot is evaluated based on its ability to generate accurate responses.
- **Usability**: The chatbot can handle questions related to academic work, making it useful for research environments and educational purposes.

---

## 🚀 **How to Run the Project**

### Requirements
- Python 3.6+
- Libraries: 
    - `tensorflow`
    - `google-generativeai`
    - `numpy`
    - `pyPDF2`
    - `pickle`
    - `python-dotenv`
  
### Steps:
1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/yourrepo.git
    cd yourrepo
    ```

2. Install required packages:
    ```bash
    pip install -r requirements.txt
    ```

3. Set up your **API key** in a `.env` file:
    ```
    API_KEY=your-google-gemini-api-key
    ```

4. Run the chatbot:
    ```bash
    python pdf_rag_chatbot.py
    ```

---

## 🧑‍💻 **Future Improvements**
- **Scaling Up**: Add support for multiple PDF documents or larger datasets.
- **Error Handling**: Improve the error handling for scenarios when the API cannot generate accurate answers.
- **User Interface**: Create a web-based interface using **Streamlit** or **Flask** for a more user-friendly experience.
- **Enhanced Evaluation**: Introduce automated evaluation metrics for better performance monitoring.

---

## 🔗 **Links & References**
- **Google Gemini API Documentation**: [https://developers.google.com/gen-ai](https://developers.google.com/gen-ai)
  

---

### 🤝 **Contributions**
Feel free to fork the project and submit pull requests for improvements or bug fixes. Contributions are welcome!

