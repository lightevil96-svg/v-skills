"""Protect the ChatGPT built-in Generate Image rule against future regressions.

These are documentation consistency checks, not tests of image quality,
native tool availability, Live2D authoring or VTube Studio runtime.
"""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FILES = (
    "AGENTS.md",
    "skills/vtuber-model-builder/SKILL.md",
    "prompts/VTUBER_AI_PRODUCTION_AGENT.md",
    "prompts/VTUBER_MODEL_AGENT.md",
    "docs/vtuber/START_HERE_AGENT.md",
)


class ChatGPTImagePolicyTest(unittest.TestCase):
    def test_all_agent_entrypoints_prefer_native_image_generation(self):
        for relative in FILES:
            with self.subTest(file=relative):
                contents = (ROOT / relative).read_text(encoding="utf-8").lower()
                self.assertIn("chatgpt", contents)
                self.assertIn("generate image", contents)
                self.assertIn("image_gen", contents)
                self.assertTrue("third-party" in contents or "outside" in contents or "external" in contents)
                self.assertIn("permission", contents)

    def test_raster_is_not_mislabeled_as_native_rig(self):
        for relative in FILES:
            with self.subTest(file=relative):
                contents = (ROOT / relative).read_text(encoding="utf-8").lower()
                self.assertIn("raster", contents)
                self.assertIn(".moc3", contents)
                self.assertIn(".cmo3", contents)


if __name__ == "__main__":
    unittest.main()
