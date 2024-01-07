from pathlib import Path

md_content = """\
# Page {name}

Some content here. Some content *there*. Some content **everywhere**.
Some content here. Some content *there*. Some content **everywhere**.
Some content here. Some content *there*. Some content **everywhere**.
Some content here. Some content *there*. Some content **everywhere**.
Some content here. Some content *there*. Some content **everywhere**.

Some content here. Some content *there*. Some content **everywhere**.
Some content here. Some content *there*. Some content **everywhere**.
Some content here. Some content *there*. Some content **everywhere**.
Some content here. Some content *there*. Some content **everywhere**.
Some content here. Some content *there*. Some content **everywhere**.
Some content here. Some content *there*. Some content **everywhere**.
Some content here. Some content *there*. Some content **everywhere**.
Some content here. Some content *there*. Some content **everywhere**.
Some content here. Some content *there*. Some content **everywhere**.
Some content here. Some content *there*. Some content **everywhere**.
Some content here. Some content *there*. Some content **everywhere**.
Some content here. Some content *there*. Some content **everywhere**.
Some content here. Some content *there*. Some content **everywhere**.
Some content here. Some content *there*. Some content **everywhere**.
Some content here. Some content *there*. Some content **everywhere**.
Some content here. Some content *there*. Some content **everywhere**.
Some content here. Some content *there*. Some content **everywhere**.
Some content here. Some content *there*. Some content **everywhere**.
Some content here. Some content *there*. Some content **everywhere**.
Some content here. Some content *there*. Some content **everywhere**.
Some content here. Some content *there*. Some content **everywhere**.
Some content here. Some content *there*. Some content **everywhere**.
Some content here. Some content *there*. Some content **everywhere**.
Some content here. Some content *there*. Some content **everywhere**.
Some content here. Some content *there*. Some content **everywhere**.
"""

md_index = """\
# {name} Folder

This is the index for the folder.

```{toctree}
{items}
```
"""


def bulk_load():
    """Write a bunch of folders of Markdown."""
    toctree = "{toctree}"

    # Make the top-level dir
    total_dirs = 10
    docs_dir = Path(__file__).parent.parent / "docs" / "sample"
    docs_dir.mkdir(exist_ok=True)
    with open(docs_dir / "index.md", "w") as output:
        top_docs = [f"f{i}/index" for i in range(total_dirs)]
        top_toctree_items = "\n".join(top_docs)
        output.write(
            md_index.format(
                name="Samples",
                toctree=toctree,
                items=top_toctree_items,
            )
        )

    for dirs in range(total_dirs):
        target = f"f{dirs}"
        target_dir = docs_dir / target
        target_dir.mkdir(exist_ok=True)

        # Write a bunch of output docs
        num_docs = 100
        for i in range(num_docs):
            with open(target_dir / f"{i}.md", "w") as output:
                output.write(md_content.format(name=str(i)))

        # Now make a toctree
        all_docs = [f"{i}" for i in range(num_docs)]
        toctree_items = "\n".join(all_docs)
        with open(target_dir / "index.md", "w") as output:
            output.write(
                md_index.format(
                    name=target,
                    toctree=toctree,
                    items=toctree_items,
                )
            )


if __name__ == "__main__":
    bulk_load()
