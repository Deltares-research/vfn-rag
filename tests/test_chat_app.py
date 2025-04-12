from llm_rag.chat_model import get_data


class TestGetData:

    def test_default(self):
        documents = get_data()
        assert isinstance(documents, list)
        assert len(documents) == 2
