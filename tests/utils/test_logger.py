from llm_rag.utils.logger import Logger


def test_create_logger():
    logger = Logger("llama")
    assert logger.logger.name == "llama"
    assert logger.logger.level == 0
    assert len(logger.logger.handlers) == 1
    assert logger.logger.handlers[0].level == 0
