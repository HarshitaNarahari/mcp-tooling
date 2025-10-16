from a2a.types import AgentCard
from config import AGENT1_PORT, AGENT2_PORT, AGENT3_PORT, AGENT4_PORT

# ------------------ Agent2: Search Agent ------------------

agent2_skills = [
    {
        'id': 'search_task',
        'name': 'Search Task Handler',
        'description': 'Handles general knowledge or search-like queries. Delegates to Math Agent if the query looks mathematical.',
        'tags': ['search', 'knowledge', 'demo'],
        'inputModes': ['text/plain'],
        'outputModes': ['text/plain'],
        'examples': ['Who invented the telescope?', 'Capital of Japan'],
    }
]

agent2_card_dict = {
    'name': 'Agent2',
    'description': 'Specialist agent for search and general knowledge queries. Delegates to Math Agent when needed.',
    'url': f'http://localhost:{AGENT2_PORT}/a2a/v1',
    'preferredTransport': 'JSONRPC',
    'protocolVersion': '0.3.0',
    'version': '1.0.0',
    'capabilities': {
        'streaming': False,
        'pushNotifications': False,
        'stateTransitionHistory': False,
    },
    'defaultInputModes': ['text/plain'],
    'defaultOutputModes': ['text/plain'],
    'skills': agent2_skills,
}

agent2_card = AgentCard.model_validate(agent2_card_dict)


# ------------------ Agent3: Math Agent ------------------

agent3_skills = [
    {
        'id': 'math_solver',
        'name': 'Math Solver',
        'description': 'Handles math-related queries and computations. Delegates to Search Agent if the task looks like a knowledge query.',
        'tags': ['math', 'calculation', 'demo'],
        'inputModes': ['text/plain'],
        'outputModes': ['text/plain'],
        'examples': ['2+2', 'What is 15 * 7?', 'Divide 144 by 12'],
    }
]

agent3_card_dict = {
    'name': 'Agent3',
    'description': 'Specialist agent for math tasks. Delegates to Search Agent if the request looks more like general knowledge.',
    'url': f'http://localhost:{AGENT3_PORT}/a2a/v1',
    'preferredTransport': 'JSONRPC',
    'protocolVersion': '0.3.0',
    'version': '1.0.0',
    'capabilities': {
        'streaming': False,
        'pushNotifications': False,
        'stateTransitionHistory': False,
    },
    'defaultInputModes': ['text/plain'],
    'defaultOutputModes': ['text/plain'],
    'skills': agent3_skills,
}

agent3_card = AgentCard.model_validate(agent3_card_dict)


# ------------------ Agent4: Content Generator Agent ------------------

agent4_skills = [
    {
        'id': 'content_generator',
        'name': 'Content Generator',
        'description': 'Generates creative or structured content such as blog posts, summaries, story ideas, and social media captions.',
        'tags': ['content', 'writing', 'creative', 'demo'],
        'inputModes': ['text/plain'],
        'outputModes': ['text/plain'],
        'examples': [
            'Write a 100-word story about a space adventure.',
            'Generate a blog post outline about AI trends.',
            'Create a catchy social media caption for a coffee brand.'
        ],
    }
]

agent4_card_dict = {
    'name': 'Agent4',
    'description': 'Specialist agent for generating creative content, summaries, or structured text outputs.',
    'url': f'http://localhost:{AGENT4_PORT}/a2a/v1',
    'preferredTransport': 'JSONRPC',
    'protocolVersion': '0.3.0',
    'version': '1.0.0',
    'capabilities': {
        'streaming': False,
        'pushNotifications': False,
        'stateTransitionHistory': False,
    },
    'defaultInputModes': ['text/plain'],
    'defaultOutputModes': ['text/plain'],
    'skills': agent4_skills,
}

agent4_card = AgentCard.model_validate(agent4_card_dict)


# ------------------ Agent1: Router Agent ------------------

agent1_skills = [
    {
        'id': 'task_router',
        'name': 'Task Router',
        'description': 'Receives a task from the user and routes it to the appropriate specialist agent (Search, Math, or Content Generator).',
        'tags': ['router', 'orchestration', 'demo'],
        'inputModes': ['text/plain'],
        'outputModes': ['text/plain'],
        'examples': [
            'What is 2+2?',
            'Who is the president of France?',
            'Write a short poem about the ocean.'
        ],
    }
]

agent1_card_dict = {
    'name': 'Agent1',
    'description': 'Acts as a router that accepts user tasks and delegates them to the Search Agent, Math Agent, or Content Generator Agent.',
    'url': f'http://localhost:{AGENT1_PORT}/a2a/v1',
    'preferredTransport': 'JSONRPC',
    'protocolVersion': '0.3.0',
    'version': '1.0.0',
    'capabilities': {
        'streaming': False,
        'pushNotifications': False,
        'stateTransitionHistory': False,
    },
    'defaultInputModes': ['text/plain'],
    'defaultOutputModes': ['text/plain'],
    'skills': agent1_skills,
}

agent1_card = AgentCard.model_validate(agent1_card_dict)


# ------------------ Routing Map ------------------

ROUTING_MAP = {
    "search": agent2_card,
    "math": agent3_card,
    "content": agent4_card
}
