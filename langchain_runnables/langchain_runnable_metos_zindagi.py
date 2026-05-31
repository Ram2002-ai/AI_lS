from abc import ABC,abstractclassmethod
import random

# runnable parent class
class Runnabele(ABC):

    @abstractclassmethod
    def invoke(input_data):
        pass


class NakliLLM(Runnabele):

    def __init__(self):
        print('LLM Created')

    def invoke(self,prompt):
        response_list=[
            "Delhi is the capital of India",
            "IPL is a cricket leauge",
            "AI stands for artificial Intelligence"
        ]

        return {'response':random.choice(response_list)}
    
    def predict(self,promt):
        response_list=[
            "Delhi is the capital of India",
            "IPL is a cricket leauge",
            "AI stands for artificial Intelligence"
        ]

        return {'response':random.choice(response_list)}



class NakliPromptTemplate(Runnabele):

    def __init__(self,template,input_variables):
        self.template=template
        self.input_variables=input_variables

    def invoke(self,input_dict):
        return self.template.format(**input_dict)
    
    def format(self,input_dict):
        return self.template.format(**input_dict)
    
# output parser
class NakliStrOutputParser(Runnabele):

    def __init__(self):
        pass

    def invoke(self,input_data):
        return input_data['response']


# Runnable connector (Runnable)

class RunnableConnector(Runnabele):

    def __init__(self,runnable_list):
        self.runnable_lsit=runnable_list

    def invoke(self,input_data):
        for runnable in self.runnable_lsit:
            input_data=runnable.invoke(input_data)

            return input_data
        
template=NakliPromptTemplate(
    template="Write a {length} peom about {topic}",
    input_variables=['length','topic']
)

llm=NakliLLM()

parser=NakliStrOutputParser()

chain=RunnableConnector([template,llm,parser])

chain.invoke({"length":'long','topic':'india'})

template1=NakliPromptTemplate(
    template="Write a joke about {topic}",
    input_variables=['topic']
)

template2=NakliPromptTemplate(
    template="Explain the following joke {response}",
    input_variables=['response']
)

llm=NakliLLM()

parser=NakliStrOutputParser()

chain1=RunnableConnector([template1,llm])
chain2=RunnableConnector([template2,llm,parser])

final_chain=RunnableConnector([chain1,chain2])

result=final_chain.invoke({'topic':'cricket'})

print(result)