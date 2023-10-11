"""Pytest tests to validate the functionality without going through frontend"""
import logging

from pathlib import Path

import pytest
from util import search_by_text, search_by_image

LOGGER = logging.getLogger(__name__)


@pytest.mark.parametrize('input_text', ['A little puppy',
                                        'a sparse market',
                                        'a market with many people',  # This is giving same image as the one above it
                                        'many people',
                                        'person playing',
                                        'stars in the sky',
                                        'king of the jungle',
                                        'A loyal animal',  # This gives lion's image instead of dog
                                        'scooby the pet',
                                        'graduating students',
                                        'students chilling in college',
                                        'children in classroom',
                                        'couple marrying'])
def test_search_by_text(input_text):
    result = search_by_text(input_text)
    LOGGER.info(f"Input text: {input_text}, Result: {result}")
    assert len(result) == 3


@pytest.mark.parametrize('input_image', Path("static/Test/").glob("*.jfif"))
def test_search_by_image(input_image):
    result = search_by_image(input_image)
    LOGGER.info(f"Input image: {input_image}, Result: {result}")
    assert len(result) == 3
