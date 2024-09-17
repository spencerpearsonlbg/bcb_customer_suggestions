import pandas as pd
import streamlit as st
from gradio_interface.gradio_call import call_gradio_api 


def get_customer_advice(
    formatted_business_data,
    product_data,
    formated_transactions,
):
    prompter = prompting(
        formatted_business_data,
        product_data,
        formated_transactions,
    )
    prompt = prompter.generate_prompt()

    result = call_gradio_api(prompt)

    st.session_state['customer_advice'] = result


class prompting():
    def __init__(
        self,
        formatted_business_data,
        product_data,
        formated_transactions,
    ) -> None:
        self.formatted_business_data = formatted_business_data
        self.product_data = product_data
        self.formated_transactions = formated_transactions

        self.system_instruction = (
            "You are to analyse a series of csv files from an individual companies data to give "
            "banking advice to this customer. The aim of the advice is to give them hints to how "
            "they can better manage their business banking products. If their is no obvious advice "
            "that you can give them, you should also make this clear."
            """
            Response format:
            You do not need to explain your response
            Only response with the advice text
            The response should be under 150 characters
            """
            
        )

    def format_product_data(self, data):
        formatted_product_data = pd.DataFrame(
            {
                "Product": data["product"],
                "Account Number": data["account_number"],
                "Balance": data["balance"],
                "Rate": data["rate"],
                "Term": data["term"],
            }
        ).T
        return formatted_product_data

    def generate_prompt(self):
        return  f"""{self.system_instruction}

        Business data:
        {self.formatted_business_data}

        Business data:
        {self.format_product_data(self.product_data)}
         
        Business transactions data:
        {self.formated_transactions}"""
    