import os
from dotenv import load_dotenv
load_dotenv(override=True)
from pydantic import BaseModel
from typing import List, Annotated
from langgraph.graph import StateGraph, END, START
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import ToolNode
from langgraph.graph.message import add_messages
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from .tools import all_tools
from .prompts.prompts import college_assistant_system_prompt

class AgentState(BaseModel):
    messages: Annotated[List[BaseMessage], add_messages]

class Agent():
    """
    LangGraph agent for handling college student queries.

    Attributes:
        name (str): Name of the agent
        model (str): HuggingFace model repo id
        system_prompt (str): System prompt for the agent
        temperature (float): Sampling temperature
    """

    def __init__(
        self,
        name: str,
        model: str = "Qwen/Qwen2.5-72B-Instruct",
        system_prompt: str = college_assistant_system_prompt,
        temperature: float = 0.5,
    ):
        self.name = name
        self.tools = all_tools
        self.model = model
        self.system_prompt = system_prompt
        self.temperature = temperature

        endpoint = HuggingFaceEndpoint(
            repo_id=self.model,
            task="text-generation",
            huggingfacehub_api_token=os.getenv("HUGGING_FACE_API_TOKEN"),
            temperature=self.temperature,
        )

        self.llm = ChatHuggingFace(llm=endpoint).bind_tools(self.tools)
        self.runnable = self.build_graph()

    def build_graph(self):
        """Build LangGraph graph."""

        def main_node(state: AgentState) -> dict:
            response = self.llm.invoke(
                [SystemMessage(content=self.system_prompt)] + state.messages
            )
            return {"messages": [response]}

        def router(state: AgentState) -> str:
            last_message = state.messages[-1]
            if not last_message.tool_calls:
                return END
            else:
                return "tools"

        workflow = StateGraph(AgentState)
        workflow.add_node("main", main_node)
        workflow.add_node("tools", ToolNode(self.tools))
        workflow.add_edge(START, "main")
        workflow.add_conditional_edges("main", router, ["tools", END])
        workflow.add_edge("tools", "main")
        return workflow.compile(checkpointer=MemorySaver())

    def invoke(self, query: str, **kwargs):
        return self.runnable.invoke(
            {"messages": [HumanMessage(content=query)]}, **kwargs
        )

    def inspect_graph(self):
        """
        Visualize the LangGraph graph structure.
        Saves the graph as a PNG and opens it with the default image viewer.
        """
        import tempfile, webbrowser

        png_data = self.build_graph().get_graph(xray=True).draw_mermaid_png()
        tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
        tmp.write(png_data)
        tmp.close()
        webbrowser.open(f"file:///{tmp.name}")
