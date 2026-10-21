import importlib.util
import contextlib
import io
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


SCRIPT = Path(__file__).resolve().parents[1] / "audit-skill-references.py"
spec = importlib.util.spec_from_file_location("audit_skill_references", SCRIPT)
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)


class ReferenceAuditTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.wrapper = self.root / "repo/skills/group/demo"
        self.source = self.root / "repo/vendor/source"
        self.wrapper.mkdir(parents=True)
        self.source.mkdir(parents=True)
        self.installed = self.root / "home/.codex/skills/demo"
        self.installed.parent.mkdir(parents=True)
        self.installed.symlink_to(self.wrapper, target_is_directory=True)

    def write(self, base, path, text="resource"):
        target = base / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text)
        return target

    def bundle(self, body="body"):
        (self.wrapper / ".upstream").symlink_to("../../../vendor/source")
        self.write(self.wrapper, "SKILL.md", "Read [body](.upstream/SKILL.md).")
        self.write(self.source, "SKILL.md", body)

    def test_installed_and_chained_links_read_body_and_nested_resources(self):
        self.bundle("Read [guide](references/guide.md).")
        self.write(self.source, "references/guide.md", "Use [icon](../assets/icon.bin) and `../scripts/run.py`.")
        self.write(self.source, "assets/icon.bin")
        self.write(self.source, "scripts/run.py")
        shared = self.root / "home/.agents/skills/demo"
        shared.parent.mkdir(parents=True)
        shared.symlink_to(self.installed, target_is_directory=True)
        for entry in (self.installed, shared):
            result = audit.audit_entry(entry / "SKILL.md")
            self.assertEqual([], result["issues"])
            self.assertEqual(5, len(result["files"]))
            self.assertIn((self.source / "assets/icon.bin").resolve(), result["files"])

    def test_missing_body_fails(self):
        self.bundle()
        (self.source / "SKILL.md").unlink()
        result = audit.audit_entry(self.installed / "SKILL.md")
        self.assertTrue(any(".upstream/SKILL.md" in issue for issue in result["issues"]))

    def test_missing_indirect_resource_and_script_fail(self):
        self.bundle("Read [guide](references/guide.md).")
        self.write(self.source, "references/guide.md", "See [icon](../assets/icon.png) and `../scripts/run.py`.")
        result = audit.audit_entry(self.installed / "SKILL.md")
        self.assertEqual(2, len(result["issues"]))
        self.assertTrue(any("icon.png" in issue for issue in result["issues"]))
        self.assertTrue(any("run.py" in issue for issue in result["issues"]))

    def test_inline_bundle_paths_in_nested_guide_use_upstream_skill_root(self):
        self.bundle("Read [guide](references/guide.md).")
        self.write(self.source, "references/guide.md", "Use `scripts/run.py` and `references/other.md`.")
        self.write(self.source, "references/other.md", "other")
        self.write(self.source, "scripts/run.py")
        result = audit.audit_entry(self.installed / "SKILL.md")
        self.assertEqual([], result["issues"])
        self.assertEqual(5, len(result["files"]))

    def test_examples_urls_outputs_and_cycles_are_not_missing_dependencies(self):
        self.bundle("""See [self](SKILL.md#top), [web](https://example.org/file.md),
`[argument](本地路径)`, and `./lessons/`.
```markdown
[example](references/not-a-real-file.md)
```
Use `references/<topic>.md` for placeholders.
""")
        result = audit.audit_entry(self.installed / "SKILL.md")
        self.assertEqual([], result["issues"])
        self.assertEqual(2, len(result["files"]))

    def test_legacy_parent_traversal_reports_normalization_risk(self):
        self.write(self.wrapper, "SKILL.md", "Read `../../../vendor/source/SKILL.md`.")
        self.write(self.source, "SKILL.md", "body")
        result = audit.audit_entry(self.installed / "SKILL.md")
        self.assertTrue(any("normalization" in issue for issue in result["issues"]))

    def test_extensionless_and_space_containing_markdown_targets(self):
        self.bundle("See [license](LICENSE), [guide](<references/my guide.md>), and [missing](references/README).")
        self.write(self.source, "LICENSE")
        self.write(self.source, "references/my guide.md", "guide")
        result = audit.audit_entry(self.installed / "SKILL.md")
        self.assertEqual(4, len(result["files"]))
        self.assertEqual(1, len(result["issues"]))
        self.assertIn("references/README", result["issues"][0])

    def test_missing_cross_package_document_fails(self):
        self.write(self.wrapper, "SKILL.md", "See [spec](../../../docs/protocol.md).")
        result = audit.audit_entry(self.installed / "SKILL.md")
        self.assertTrue(any("protocol.md" in issue for issue in result["issues"]))

    def test_cli_returns_failure_when_an_installed_resource_disappears(self):
        self.bundle("Read [guide](references/guide.md).")
        guide = self.write(self.source, "references/guide.md", "guide")
        command = [sys.executable, str(SCRIPT), "--entry", str(self.installed / "SKILL.md")]
        passed = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(0, passed.returncode, passed.stdout)
        guide.unlink()
        failed = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(1, failed.returncode, failed.stdout)
        self.assertIn("references/guide.md", failed.stdout)

    def run_main(self, *arguments):
        output = io.StringIO()
        with patch("sys.argv", [str(SCRIPT), *map(str, arguments)]), contextlib.redirect_stdout(output):
            code = audit.main()
        return code, output.getvalue()

    def test_recursive_discovery_audits_unlinked_nested_skill(self):
        self.write(self.wrapper, "SKILL.md", "Router")
        nested = self.write(self.wrapper, "child/SKILL.md", "Read [guide](references/missing.md).")
        code, output = self.run_main("--root", self.installed.parent)
        self.assertEqual(1, code, output)
        self.assertIn("references/missing.md", output)
        self.assertIn(str(self.installed / "child/SKILL.md"), output)
        self.write(nested.parent, "references/missing.md", "guide")
        self.assertEqual(0, self.run_main("--root", self.installed.parent)[0])

    def test_discovery_skips_hidden_bundles_and_stops_symlink_cycles(self):
        self.bundle()
        self.write(self.wrapper, "child/SKILL.md", "child")
        (self.wrapper / "loop").symlink_to(self.wrapper, target_is_directory=True)
        entries = list(audit.discover_entries(self.installed.parent))
        self.assertEqual({(self.wrapper / "SKILL.md").resolve(), (self.wrapper / "child/SKILL.md").resolve()},
                         {entry.resolve() for entry in entries})

    def test_recursive_discovery_keeps_dangling_installation_errors(self):
        (self.installed.parent / "broken").symlink_to(self.root / "missing")
        code, output = self.run_main("--root", self.installed.parent)
        self.assertEqual(1, code, output)
        self.assertIn("broken/SKILL.md", output)

    def test_markdown_titles_and_reference_styles_detect_missing_files(self):
        bodies = [
            '[guide](references/missing.md "Guide")',
            "[guide](references/missing.md 'Guide')",
            '[guide](references/missing.md (Guide))',
            '[guide][g]\n\n[g]: references/missing.md "Guide"',
            '[guide][]\n\n[guide]: references/missing.md',
            '[Guide]\n\n[guide]: references/missing.md',
            '[guide][g]\n\n[g]:\n  references/missing.md\n',
            '[Guide [v1]](references/missing.md)',
        ]
        for body in bodies:
            with self.subTest(body=body):
                self.write(self.wrapper, "SKILL.md", body)
                result = audit.audit_entry(self.installed / "SKILL.md")
                self.assertEqual(1, len(result["issues"]), result)
                self.assertIn("references/missing.md", result["issues"][0])

    def test_markdown_parentheses_escapes_titles_and_reference_destinations(self):
        self.bundle('''[asset](assets/chart(1).svg "Chart")
[escaped](assets/chart\\(1\\).svg)
[guide][ G u i d e ]

[g u i d e]: <references/my guide.md> 'Guide'
''')
        self.write(self.source, "assets/chart(1).svg", "<svg/>")
        self.write(self.source, "references/my guide.md", "guide")
        result = audit.audit_entry(self.installed / "SKILL.md")
        self.assertEqual([], result["issues"])
        self.assertEqual(4, len(result["files"]))

    def test_reference_examples_and_unused_definitions_are_ignored(self):
        self.bundle('''`[guide][g]`
```markdown
[guide][g]
```
[g]: references/example-only.md
''')
        self.assertEqual([], audit.audit_entry(self.installed / "SKILL.md")["issues"])

    def test_reference_definition_cannot_interrupt_a_paragraph(self):
        self.bundle('Paragraph\n[g]: references/missing.md\n\nSee [g].')
        self.assertEqual([], audit.audit_entry(self.installed / "SKILL.md")["issues"])

    def test_direct_upstream_guides_use_owning_root_regardless_of_link_order(self):
        self.bundle("Read [guide](references/guide.md).")
        self.write(self.source, "references/guide.md", "Use `scripts/run.py`.")
        self.write(self.source, "scripts/run.py")
        self.write(self.wrapper, "references/local.md", "Use `scripts/local.py`.")
        self.write(self.wrapper, "scripts/local.py")
        for order in (("body", "guide"), ("guide", "body")):
            links = {"body": "[body](.upstream/SKILL.md)", "guide": "[guide](.upstream/references/guide.md)"}
            self.write(self.wrapper, "SKILL.md", "\n".join(links[key] for key in order)
                       + "\n[local](references/local.md)")
            result = audit.audit_entry(self.installed / "SKILL.md")
            self.assertEqual([], result["issues"], order)
            self.assertEqual(6, len(result["files"]))
        (self.source / "scripts/run.py").unlink()
        result = audit.audit_entry(self.installed / "SKILL.md")
        self.assertTrue(any("scripts/run.py" in issue for issue in result["issues"]))

    def test_default_roots_can_be_absent_but_explicit_root_must_exist(self):
        self.write(self.wrapper, "SKILL.md", "body")
        with patch.object(audit.Path, "home", return_value=self.root / "home"):
            code, output = self.run_main()
            self.assertEqual(0, code, output)
            self.assertIn("1 entrypoints", output)
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as raised:
            self.run_main("--root", self.root / "missing")
        self.assertEqual(2, raised.exception.code)

    def test_default_broken_root_is_an_error(self):
        self.write(self.wrapper, "SKILL.md", "body")
        shared = self.root / "home/.agents/skills"
        shared.parent.mkdir()
        shared.symlink_to(self.root / "missing")
        with patch.object(audit.Path, "home", return_value=self.root / "home"):
            with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as raised:
                self.run_main()
        self.assertEqual(2, raised.exception.code)

    def test_inline_paths_preserve_uri_characters_literally(self):
        names = ["guide%20v1.md", "guide#v1.md", "guide?v1.md", "guide=v1.md", "$schema.md", "guide%3Ctopic%3E.md"]
        for name in names:
            with self.subTest(name=name):
                resource = self.write(self.wrapper, "references/" + name, "guide")
                self.write(self.wrapper, "SKILL.md", f"Read `references/{name}`.")
                result = audit.audit_entry(self.installed / "SKILL.md")
                self.assertEqual([], result["issues"])
                self.assertIn(resource.resolve(), result["files"])
                resource.unlink()
                result = audit.audit_entry(self.installed / "SKILL.md")
                self.assertEqual(1, len(result["issues"]), result)
                self.assertIn(name, result["issues"][0])

    def test_markdown_uris_decode_paths_once_and_remove_query_and_fragment(self):
        pairs = [("guide%20v1.md", "guide v1.md"), ("guide%23v1.md", "guide#v1.md"),
                 ("guide%3Fv1.md", "guide?v1.md"), ("guide%2520v1.md", "guide%20v1.md"),
                 ("guide%253Ctopic%253E.md", "guide%3Ctopic%3E.md"), ("$schema.md", "$schema.md"),
                 ("guide=v1.md?cache=1#section", "guide=v1.md")]
        for uri, name in pairs:
            with self.subTest(uri=uri):
                resource = self.write(self.wrapper, "references/" + name, "guide")
                self.write(self.wrapper, "SKILL.md", f"Read [guide](references/{uri}).")
                result = audit.audit_entry(self.installed / "SKILL.md")
                self.assertEqual([], result["issues"])
                self.assertIn(resource.resolve(), result["files"])
                resource.unlink()
                self.assertEqual(1, len(audit.audit_entry(self.installed / "SKILL.md")["issues"]))

    def test_placeholders_are_filtered_after_markdown_uri_decoding(self):
        placeholders = ["<topic>", "{topic}", "${topic}", "<skill-name>", "{skill_name}", "<领域>", "{领域}", "{0}"]
        for marker in placeholders:
            for body in (f"[guide](references/{marker}.md)", f"`references/{marker}.md`"):
                with self.subTest(body=body):
                    self.write(self.wrapper, "SKILL.md", body)
                    self.assertEqual([], audit.audit_entry(self.installed / "SKILL.md")["issues"])

    def test_file_symlink_relative_references_are_independent_of_link_order(self):
        common = self.write(self.wrapper, "shared.md", "[next](./next.md) and [self](./guide.md)")
        for name in ("a", "b"):
            alias = self.wrapper / "references" / name / "guide.md"
            alias.parent.mkdir(parents=True)
            alias.symlink_to(common)
        self.write(self.wrapper, "references/a/next.md", "next")
        for order in (("a", "b"), ("b", "a")):
            self.write(self.wrapper, "SKILL.md", "\n".join(f"[guide](references/{name}/guide.md)" for name in order))
            result = audit.audit_entry(self.installed / "SKILL.md")
            self.assertEqual(1, len(result["issues"]), (order, result))
            self.assertIn("references/b/next.md", result["issues"][0])
        self.write(self.wrapper, "references/b/next.md", "next")
        for order in (("a", "b"), ("b", "a")):
            self.write(self.wrapper, "SKILL.md", "\n".join(f"[guide](references/{name}/guide.md)" for name in order))
            self.assertEqual([], audit.audit_entry(self.installed / "SKILL.md")["issues"])

    def test_file_symlink_markdown_alias_is_checked_after_a_binary_alias(self):
        common = self.write(self.wrapper, "shared", "[missing](references/missing.md)")
        for name in ("guide.txt", "guide.md"):
            (self.wrapper / name).symlink_to(common)
        for order in (("guide.txt", "guide.md"), ("guide.md", "guide.txt")):
            self.write(self.wrapper, "SKILL.md", "\n".join(f"[guide]({name})" for name in order))
            result = audit.audit_entry(self.installed / "SKILL.md")
            self.assertEqual(1, len(result["issues"]), (order, result))

    def test_nested_installed_link_becomes_an_error_after_target_is_deleted(self):
        collection = self.root / "installed/group"
        collection.mkdir(parents=True)
        target = self.write(self.root, "nested-source/SKILL.md", "body")
        (collection / "child").symlink_to(target.parent, target_is_directory=True)
        self.assertEqual(0, self.run_main("--root", collection.parent)[0])
        target.unlink()
        target.parent.rmdir()
        code, output = self.run_main("--root", collection.parent)
        self.assertEqual(1, code, output)
        self.assertIn("group/child", output)

    def test_visible_nested_resource_links_fail_but_hidden_links_are_skipped(self):
        self.write(self.wrapper, "SKILL.md", "body")
        (self.wrapper / ".hidden").symlink_to(self.root / "missing")
        self.assertEqual(0, self.run_main("--root", self.installed.parent)[0])
        assets = self.wrapper / "assets"
        assets.mkdir()
        (assets / "broken.svg").symlink_to(self.root / "missing.svg")
        code, output = self.run_main("--root", self.installed.parent)
        self.assertEqual(1, code, output)
        self.assertIn("assets/broken.svg", output)


if __name__ == "__main__":
    unittest.main()
