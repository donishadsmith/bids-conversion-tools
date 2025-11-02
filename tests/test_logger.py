import logging

from bidsprep.logger import setup_logger


def test_setup_logger(caplog):
    """Test for ``setup_logger``"""
    logger = setup_logger("test")
    assert isinstance(logger, logging.Logger)

    with caplog.at_level(logging.INFO):
        logger.info("TEST")

    assert "TEST" in caplog.text
