import pytest
from unittest.mock import patch, MagicMock
import os
import sys

# Add the project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.graph import scout_node, analyst_node, strategist_node
from src.state import IdeaRadarState

from langchain_core.messages import AIMessage

def test_scout_node_with_mock_data():
    # Test fallback when no API key is present
    state: IdeaRadarState = {"topic": "Testing", "raw_data": [], "identified_problems": [], "selected_problem": {}, "blueprint": ""}
    with patch.dict(os.environ, clear=True): # Clear env to ensure no API key
        result = scout_node(state)
        
    assert "raw_data" in result
    assert len(result["raw_data"]) > 0
    assert "Mock data:" in result["raw_data"][0]

@patch("src.graph.TavilyClient")
def test_scout_node_with_tavily(mock_tavily_class):
    mock_instance = MagicMock()
    mock_instance.search.return_value = {
        "results": [
            {"content": "Reddit post about test problem 1."},
            {"content": "Reddit post about test problem 2."}
        ]
    }
    mock_tavily_class.return_value = mock_instance
    
    state: IdeaRadarState = {"topic": "Testing", "raw_data": [], "identified_problems": [], "selected_problem": {}, "blueprint": ""}
    with patch.dict(os.environ, {"TAVILY_API_KEY": "fake_key"}):
        result = scout_node(state)
        
    assert "raw_data" in result
    assert len(result["raw_data"]) == 2
    assert "test problem 1" in result["raw_data"][0]

@patch("src.graph.ChatOllama.invoke")
def test_analyst_node(mock_invoke):
    # Instead of patching ChatOllama class, we patch its invoke method
    mock_invoke.return_value = AIMessage(content='[{"problem_name": "Mocked Problem", "sentiment": "Angry", "market_score": 95}]')

    state: IdeaRadarState = {"topic": "Testing", "raw_data": ["User complaint 1"], "identified_problems": [], "selected_problem": {}, "blueprint": ""}
    result = analyst_node(state)
    
    assert "identified_problems" in result
    assert len(result["identified_problems"]) == 1
    assert result["identified_problems"][0]["problem_name"] == "Mocked Problem"

@patch("src.graph.ChatOllama.invoke")
def test_strategist_node(mock_invoke):
    mock_invoke.return_value = AIMessage(content="# Founder's Dossier: Mocked Problem\n\n## 1. Market Opportunity\nGreat opportunity.")

    state: IdeaRadarState = {
        "topic": "Testing", 
        "raw_data": [], 
        "identified_problems": [], 
        "selected_problem": {"problem_name": "Mocked Problem", "sentiment": "Angry", "market_score": 95}, 
        "blueprint": "",
        "next_agent": ""
    }
    
    result = strategist_node(state)
    
    assert "blueprint" in result
    assert "# Founder's Dossier: Mocked Problem" in result["blueprint"]
