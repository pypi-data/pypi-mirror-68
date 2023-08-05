import logging

from typing import Callable


LoggerFactory = Callable[[str], logging.Logger]
