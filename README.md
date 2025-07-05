# LangGraph Service Desk Assistant

A sophisticated AI-powered service desk assistant built with LangGraph that can handle ticket management, calendar scheduling, and knowledge base queries. The system uses a multi-agent workflow with RAG (Retrieval-Augmented Generation) capabilities to provide intelligent customer service automation.

## Features

- **Ticket Management**: Create, update, and query support tickets
- **Calendar Integration**: Schedule events and query calendar information
- **Knowledge Base**: Access policies, product information, and historical data
- **RAG-Enhanced Responses**: Retrieval-augmented generation for accurate, context-aware answers
- **Multi-Agent Workflow**: Intelligent intent classification and routing
- **Hallucination Detection**: Built-in verification to ensure response accuracy
- **Interactive Chat Interface**: Conversational AI with memory and context

## Architecture

The system uses a state-based workflow with the following components:

- **Intent Classification**: Automatically categorizes user queries
- **Ticket Tools**: Create, update, and search tickets
- **Calendar Tools**: Schedule and query events
- **Context Tools**: Access knowledge base information
- **Verification Layer**: Hallucination detection and response validation

## Prerequisites

- Python 3.8+
- Google AI API key (for Gemini model)
- Required Python packages (see installation)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/p0in-t/langgraph-service-desk-assistant.git
cd langgraph-service-desk-assistant
```

2. Install required packages:
```bash
pip install langchain langchain-openai langchain-community langchain-google-genai
pip install langgraph faiss-cpu sentence-transformers
pip install numpy pandas python-dateutil
```

3. Set up your Google AI API key:
   - Get your API key from [Google AI Studio](https://aistudio.google.com/)
   - Replace the API key in the notebook

## Usage

1. **Generate Sample Data** (optional):
```bash
python generate_data.py
```

2. **Run the Assistant**:
   Open `smart_customer_service_rag_assistant.ipynb` in Jupyter Notebook and run all cells. The assistant will start in interactive mode.

3. **Example Interactions**:
   - Create a ticket: "I need help with my printer not working"
   - Schedule an event: "Schedule a meeting for tomorrow at 2 PM in conference room A"
   - Query tickets: "Show me all tickets from last week"
   - Get ticket info: "What's the status of ticket 10001?"
   - Update ticket: "Change ticket 10001 to Resolved"

## File Structure

```
langgraph-service-desk-assistant/
├── smart_customer_service_rag_assistant.ipynb  # Main application
├── generate_data.py                           # Sample data generator
├── data/                                      # Data directory
│   ├── tickets.txt                           # Ticket storage
│   ├── generated_tickets.txt                 # Large amount of generated tickets
│   ├── calendar.txt                          # Calendar events
│   ├── policies.txt                          # Policy documents
│   └── product_data.txt                      # Product information
└── README.md                                 # This file
```

## Key Components

### Tools Available

- **CheckCurrentDate**: Get today's date
- **CreateTicket**: Create new support tickets
- **UpdateTicketStatus**: Modify ticket status
- **FindTicketViaID**: Search tickets by ID
- **FindTicketsViaDescription**: Search tickets by content
- **FindTicketsViaDate**: Search tickets by date range
- **ScheduleEvent**: Create calendar events
- **FindEventsViaDate**: Query events by date
- **FindEventsViaDateRange**: Query events by date range
- **FindEventsViaDescription**: Search events by description
- **GetContext**: Access knowledge base

### Supported Operations

- **Ticket Management**: Create, read, update tickets with status tracking
- **Calendar Management**: Schedule events with conflict detection
- **Information Retrieval**: Search across tickets, events, and knowledge base
- **Query Classification**: Intelligent routing based on user intent
- **Response Validation**: Hallucination detection for accurate responses

## Configuration

The system uses several configurable parameters:

- **Model**: Google Gemini 2.0 Flash (configurable)
- **Embeddings**: sentence-transformers/all-mpnet-base-v2
- **Memory Limit**: 10 messages (conversation history)

## Customization

To adapt the assistant for your specific needs:

1. **Modify Tools**: Add or remove tools in the `tools` list
2. **Update Prompts**: Customize classification and response prompts
3. **Change Models**: Replace Gemini with other LangChain-compatible models
4. **Add Data Sources**: Extend the RAG system with additional document types
5. **Workflow Modification**: Adjust the state graph for different routing logic

## Acknowledgments

- Built with [LangChain](https://langchain.readthedocs.io/) and [LangGraph](https://langchain-ai.github.io/langgraph/)
- Uses [Google Gemini](https://ai.google.dev/) for language model capabilities
- Embeddings powered by [Sentence Transformers](https://www.sbert.net/)
