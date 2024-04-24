import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
from src.mcq_generator.utils import read_file,get_table_data
import streamlit as st
from langchain.callbacks import get_openai_callback
from src.mcq_generator.MCQGenerator import generate_evaluate_chain
from src.mcq_generator.logger import logging

# loading json file
with open('C:\Users\shiva.reddy\GEN_AI\Response.json','r') as file:
    RESPONSE_JSON=json.load(file)

# creating a title for the app
st.title('MCQs creator Application with LangChain')

# create a form using st.form
with st.form('user_inputs'):
    # file upload
    uploaded_file=st.file_upload('Upload a PDF or txt file')

    # input fields
    mcq_count=st.number_input('No of MCQs',min_value=3,max_value=50)

    # subject
    subject=st.text_input('Insert Subject',max_chars=20)

    # quiz tone
    tone=st.text_input('Complexity level of questions', max_chars=20,placeholder='Simple')

    # Add button
    button=st.form_submit_button('Create MCQs')

    # check if the button is clicked and all fields have input
    if button and upload_file is not None and mcq_count and subject and tone:
        with st.spinner('loading...'):
            try:
                text=read_file(uploaded_file)
                # count tokens and the cost of the API call
                with get_openai_callback() as cb:
                    response=generate_evaluate_chain(
                        {
                            'text':text,
                            'number':mcq_count,
                            'subject':subject,
                            'tone':tone,
                            'response_json':json.dumps(RESPONSE_JSON)
                        }
                    )
            except Exception as e:
                traceback.print_exception(type(e),e,e.__traceback__)
                st.error('Error')
    
    else:
        print(f"Total tokens: {cb.total_tokens}")
        print(f"Prompt tokens: {cb.prompt_tokens}")
        print(f"Completion tokens: {cb.completion_tokens}")
        print(f"Total cost: {cb.total_cost}") # in dollars

        if isinstance(response,dict):
            # extract the quiz data from the response
            quiz=response.get('quiz',None)
            if quiz is not None:
                table_data=get_table_data(quiz)
                if table_data is not None:
                    df = pd.DataFrame(table_data)
                    df.index=df.index+1
                    st.table(df)
                    # Display the review in a text box as well
                    st.text_area(label='Review',value=response['review'])
                else:
                    st.write(response)
            
            else:
                st.write(response)

# to run a streamlit app
# streamlit run filename.py

