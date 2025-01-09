# ERP-System-NLP

Welcome to the **ERP-System-NLP** project! This system leverages Natural Language Processing (NLP) to enhance the operations of an ERP system. It integrates with various modules of an ERP system to streamline processes, automate workflows, and improve data accessibility using NLP technologies.

## Project Overview

The goal of this project is to integrate NLP into an ERP system to facilitate intuitive interactions, such as querying information, generating reports, and automating decision-making processes.

The system consists of:
1. **Frontend**: A user interface where users can interact with the ERP system.
2. **Backend**: A server responsible for processing requests, managing data, and providing functionality.
3. **NLP Module**: An NLP-powered layer for interpreting and processing user queries.

### Diagram

![System Diagram](./fig/system_diagram.png)

This diagram illustrates the interaction between the different components of the ERP system.

## How to Run

To get the ERP System up and running, follow these steps:

### Frontend
Run the `python ui.py` file to start the user interface.

```bash
python ui.py
uvicorn another_main:app --host 0.0.0.0 --port 8000

