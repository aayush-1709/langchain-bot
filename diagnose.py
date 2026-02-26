try:
    import langchain
    print(f"LangChain version: {langchain.__version__}")
    
    try:
        from langchain.chains import ConversationalRetrievalChain
        print("Successfully imported ConversationalRetrievalChain from langchain.chains")
    except ImportError as e:
        print(f"Failed to import from langchain.chains: {e}")
        
    try:
        from langchain_community.chains import ConversationalRetrievalChain
        print("Successfully imported ConversationalRetrievalChain from langchain_community.chains")
    except ImportError as e:
        print(f"Failed to import from langchain_community.chains: {e}")

except ImportError:
    print("LangChain is not installed.")
