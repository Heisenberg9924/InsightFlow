import requests

BASE_URL = "http://127.0.0.1:8000"


def upload_document(file):

    files = {
        "file": (
            file.name,
            file,
            "application/pdf",
        )
    }

    response = requests.post(
        f"{BASE_URL}/upload",
        files=files,
    )

    response.raise_for_status()

    return response.json()


def chat(
    document_id,
    question,
    conversation_id=None,
):

    payload = {
        "document_id": document_id,
        "question": question,
        "conversation_id": conversation_id,
    }

    response = requests.post(
        f"{BASE_URL}/chat",
        json=payload,
    )

    response.raise_for_status()

    return response.json()


def get_conversations():

    response = requests.get(
        f"{BASE_URL}/conversations"
    )

    response.raise_for_status()

    return response.json()


def get_messages(conversation_id):

    response = requests.get(
        f"{BASE_URL}/conversations/{conversation_id}"
    )

    response.raise_for_status()

    return response.json()