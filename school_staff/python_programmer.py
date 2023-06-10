from langchain.chains.constitutional_ai.models import ConstitutionalPrinciple
from langchain.chains.constitutional_ai.base import ConstitutionalChain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv, find_dotenv
from langchain.chains.llm import LLMChain
from langchain.llms import OpenAI
load_dotenv(find_dotenv())
from io import StringIO
import sys

class PythonProgrammer:

    def __init__(self):
        template = '''Generate mathematical equations from the below statement and write in every statement in new line in the form of python code in order to calculate.
        Dont miss any import statements of the functions that you would require:

        Question: There is a family of 4 people that includes father, mother, daughter and son. Darghter earns $6550 per month, 1/3 of what her brother earns. 
        Mother earns twice as their childrens combined salary. Father earns thrice of what mother earns. what's the total amount of money the family 
        earn in a month?
        Answer: 
        import math
        daughter_salary = 6550
        brother_salary = daughter_salary * 3
        children_combined_salary = daughter_salary + brother_salary
        mother_salary = children_combined_salary * 2
        father_salary = mother_salary * 3
        total_family_salary = daughter_salary + brother_salary + mother_salary + father_salary
        print(total_family_salary)
        
        Question: {question}
        Answer: 
[write code here without indentation error]
        '''
        prompt = PromptTemplate(
            template=template,
            input_variables=["question"],
        )

        llm = OpenAI(temperature=0)
        self.chain = LLMChain(llm=llm, prompt=prompt)

        # general = ConstitutionalPrinciple(
        #     name="Logic",
        #     critique_request="Review your previous answer and find logical problems with your answer.",
        #     revision_request="Based on the problems you found, improve your answer.",
        # )
        # principles = [general]

        # self.constitutional_chain = ConstitutionalChain.from_llm(
        #     chain=chain,
        #     constitutional_principles=principles,
        #     llm=llm,
        #     verbose=True,
        # )
    
    def solve(self, question):
        output = self.chain.run(question)
        print(output)
        tmp = sys.stdout
        my_result = StringIO()
        sys.stdout = my_result
        exec(output)
        sys.stdout = tmp
        return my_result.getvalue()

