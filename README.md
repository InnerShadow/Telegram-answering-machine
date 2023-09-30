# Telegram Answering Machine

**Welcome to Telegram Answering Machine!**

Get ready to embrace tranquility with my powerful application!

🤫 Let the neural network work its magic, generating responses to those you'd rather avoid on Telegram. Your peace, our priority!

💬 _Shhh..._ Enjoy the serene quietude and let the machine handle the chatter! 💤

🔑 **Register Your Application with Telegram** 🔑

If this is your first time launching the application, you need to register your application on Telegram's website. Here's how:

1. Go to [Telegram's website](https://my.telegram.org/auth) and log in or create an account.
2. Obtain your 'api hash' and 'api id' which are necessary to continue using this application.

Follow these steps and secure the credentials needed for a seamless experience with the Telegram Answering Machine!

## Table of Contents

- [Telegram Answering Machine](#telegram-answering-machine)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
  - [Usage](#usage)
    - [How to Use It](#how-to-use-it)
  - [Key Components](#key-components)
    - [QA\_model.py](#qa_modelpy)
      - [Neural Network Structure](#neural-network-structure)
    - [MonitoringByName.py](#monitoringbynamepy)
      - [Ignoring Multiple Victims](#ignoring-multiple-victims)
      - [Connecting Different Models to Each Victim](#connecting-different-models-to-each-victim)
      - [Asynchronous Python](#asynchronous-python)

## Features

- Create and manage victims and models.
- Train and use models to automate responses.
- Set default responses for unrecognized messages.
- Monitor and ignore messages based on selected models.

## Getting Started

### Prerequisites

- Python 3.x
- Required Python libraries (install using pip):

```bash
pip install -r requirements.txt
```

### Installation

1. Clone the repository:

```bash
git clone https://github.com/InnerShadow/Telegram-answering-machine
cd telegram-answering-machine
```

2. Install the required Python libraries:

```bash
pip install -r requirements.txt
```

## Usage

### How to Use It

To start ignoring someone, follow these steps:

1. Train a new model:
   - Navigate to Models -> Train new model and set up the parameters. The model will be ready for use after this step.

2. Create a victim and connect a model:
   - Go to Victim menu -> Get new victim -> Select victim by ID -> Select a victim -> Set model by ID -> Select a model -> Back to the victim menu -> Add to ignoring list.
   - Repeat this step to add as many victims as you want.

3. Run the ignoring process:
   - Go back to the 'MAIN MENU' and choose the 'Run ignoring' option. All selected victims will be ignored.

Explore more features using the 'help' option in each module.

## Key Components

### QA\_model.py

This module comprises functions for saving, loading, and training the question-answering (QA) model.

#### Neural Network Structure

The neural network structure implemented in `QA_model.py` is a sequence-to-sequence (seq2seq) model, a widely used architecture for various natural language processing tasks, including question-answering.

- **Encoder:**
  - Input Layer: Accepts input sequences (questions).
  - Embedding Layer: Converts input sequences into dense vectors of fixed size (`latent_dim`).
  - LSTM Layer: Processes the embeddings and extracts sequential features.

- **Decoder:**
  - Input Layer: Accepts input sequences (answers).
  - Embedding Layer: Converts input sequences into dense vectors of fixed size (`latent_dim`).
  - LSTM Layer: Processes the embeddings and extracts sequential features.
  - Attention Layer: Computes attention weights to emphasize relevant parts of the input.

- **Context Representation:**
  - Input Layer: Accepts concatenated context vectors (from previous conversations).
  - Embedding Layer: Converts context sequences into dense vectors.
  - LSTM Layer: Processes context embeddings to represent the context.

- **Decoder Output:**
  - Dense Layer: Computes the final output probabilities for each word in the vocabulary.
  - Activation: Softmax

- **Model Compilation:**
  - Optimizer: Adam with a learning rate of `0.001`.
  - Loss Function: Categorical Cross-Entropy

The complete neural network structure is designed to effectively handle the question-answering task, utilizing attention mechanisms and context representation for improved performance.

### MonitoringByName.py

This module includes functions for handling and monitoring incoming messages, generating responses, and managing activity based on specific users' names.

#### Ignoring Multiple Victims

The `MonitoringByName.py` module supports ignoring messages from multiple victims simultaneously, enhancing the utility of the application for managing communication with various users.

#### Connecting Different Models to Each Victim

Users can connect distinct models to each victim, providing the ability to utilize models that may not have been explicitly trained for a particular victim. This adaptability ensures efficient handling of messages based on the available models and their associated characteristics.

#### Asynchronous Python

The Telegram Answering Machine utilizes asynchronous programming in Python to handle concurrent operations efficiently.  Key components and functionalities within the application are designed to leverage the asynchronous nature of Python, enabling smooth execution and effective handling of tasks such as message monitoring victims.

