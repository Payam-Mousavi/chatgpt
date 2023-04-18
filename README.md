# chatgpt
Exploring LLM and ChatGPT  

I am exploring LangChain mostly using OpenAI's API as well as Pinecone (for storing embeddings).  
You can create the environment using:  

```
conda env create -f environment.yml  
```

Due to some package conflicts, after you create the environment using the `.yml` file, install the following two packages manually:  
```
pip3 install pinecone-client   
pip install unstructured-inference
```

Note that you will need to use your own API keys (for OpenAI and Pinecone). Be careful not to check in your keys into Git! One way to handle this is by using the `dotenv` library to set the API keys as environment variables. To do this, create a `.env` file and add your API keys there. Make sure that you add the `.env` file into your `.gitignore`. For more information see the documentation: https://www.geeksforgeeks.org/python-os-getenv-method/

To run the gui_demo:  
```
python gui_demo.py  
```
