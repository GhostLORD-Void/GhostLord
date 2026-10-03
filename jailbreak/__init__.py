"""GhostLord Jailbreak Module.

AI security research module for jailbreak analysis and defense.
Provides prompt injection, role hijacking, encoding bypass,
context manipulation, multi-turn orchestration, and detection.
"""

__version__ = "3.0.0"
__author__ = "GhostLord"

from jailbreak.prompt_inject import PromptInjector
from jailbreak.role_hijack import RoleHijacker
from jailbreak.encoding_bypass import EncodingBypass
from jailbreak.context_inject import ContextInjector
from jailbreak.chain import JailbreakChain
from jailbreak.defense import JailbreakDetector
