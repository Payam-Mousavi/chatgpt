import tkinter as tk
from tkinter import filedialog

import sys
print(sys.executable)


from langchain.document_loaders import UnstructuredPDFLoader, OnlinePDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.chains.question_answering import load_qa_chain
import pinecone
PINECONE_API_ENV = "northamerica-northeast1-gcp"
from dotenv import load_dotenv


def browse_pdf():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    pdf_link.set(file_path)

def preprocess_pdf():
    global docsearch
    config = load_dotenv()

    loader = UnstructuredPDFLoader(pdf_link.get())
    data = loader.load()

    # Chunking:
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(data)

    # Creating embeddings:
    embeddings = OpenAIEmbeddings()

    # initialize pinecone
    pinecone.init(environment=PINECONE_API_ENV)
    index_name = "langchan-demo"

    # Search in Pincecone using cosine similarity:
    docsearch = Pinecone.from_texts([t.page_content for t in texts], embeddings, index_name=index_name)


def answer_query():
    global docsearch, answer
    entered_query = query.get()
    docs = docsearch.similarity_search(entered_query, include_metadata=True)

    # llm = OpenAI(temperature=0, model_name="text-davinci-003")
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
    chain = load_qa_chain(llm, chain_type="stuff")

    output = chain.run(input_documents=docs, question=entered_query)
    # Insert the new content at the beginning of the text field
    answer_text.insert(tk.INSERT, output)

def clear_fields():
    query.set("")
    answer_text.delete(1.0, tk.END)

root = tk.Tk()
root.title("Chat with the PDF!")

# Link to PDF
pdf_link = tk.StringVar()
pdf_frame = tk.Frame(root)
pdf_frame.pack(pady=10)
tk.Label(pdf_frame, text="Link to PDF:").pack(side=tk.LEFT)
pdf_entry = tk.Entry(pdf_frame, textvariable=pdf_link, width=50)
pdf_entry.pack(side=tk.LEFT)
tk.Button(pdf_frame, text="Browse", command=browse_pdf).pack(side=tk.LEFT)

# Pre-processing button
tk.Button(root, text="Pre-process PDF", command=preprocess_pdf).pack(pady=10)

# Enter Query
query = tk.StringVar()
query_frame = tk.Frame(root)
query_frame.pack(pady=10)
tk.Label(query_frame, text="Enter Query:").pack(side=tk.LEFT)
query_entry = tk.Entry(query_frame, textvariable=query, width=50)
query_entry.pack(side=tk.LEFT)

# Answer
answer_frame = tk.Frame(root)
answer_frame.pack(pady=10)
tk.Label(answer_frame, text="Answer:").pack(side=tk.LEFT)

# Create a Text widget for the answer and a Scrollbar widget
answer_text = tk.Text(answer_frame, wrap=tk.WORD, height=10, width=50)
scrollbar = tk.Scrollbar(answer_frame, command=answer_text.yview)
answer_text.config(yscrollcommand=scrollbar.set)

# Pack the Text and Scrollbar widgets
answer_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.pack(side=tk.LEFT, fill=tk.Y)

# Buttons
buttons_frame = tk.Frame(root)
buttons_frame.pack(pady=10)
tk.Button(buttons_frame, text="Answer", command=answer_query).pack(side=tk.LEFT, padx=5)
tk.Button(buttons_frame, text="Clear", command=clear_fields).pack(side=tk.LEFT)
tk.Button(buttons_frame, text="Exit", command=root.destroy).pack(side=tk.LEFT, padx=5)

root.mainloop()
