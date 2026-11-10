import shutil
from pathlib import Path
from bot.plugingen.models import Project
from bot.plugingen.services.file_service import FileService

def test_project_model():
    p = Project("MyPlugin", "1.0.0", "A test plugin")
    assert p.get_name() == "MyPlugin"
    assert p.get_version() == "1.0.0"
    assert p.get_description() == "A test plugin"
    assert "MyPlugin-" in str(p.get_path())

def test_file_service_code_block_extraction():
    p = Project("TestExt", "1.0.0", "Desc")
    fs = FileService()

    markdown_code = """Here is the plugin code:
```java
package io.test;

public class TestExt {
    public static void main(String[] args) {}
}
```
Hope this helps!"""

    try:
        fs.save(p, "src/main/java/io/test/TestExt.java", markdown_code)
        target = p.get_path() / "sourcecode" / "TestExt" / "src" / "main" / "java" / "io" / "test" / "TestExt.java"
        assert target.exists()
        content = target.read_text(encoding="utf-8")
        assert "package io.test;" in content
        assert "Hope this helps!" not in content
    finally:
        if p.get_path().exists():
            shutil.rmtree(p.get_path(), ignore_errors=True)
