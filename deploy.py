import glob

from traitlets.config.loader import Config
import nbformat as nbf
from nbconvert.exporters import HTMLExporter
from nbconvert.preprocessors import TagRemovePreprocessor

# Setup config
c = Config()

# Configure tag removal - be sure to tag your cells to remove  using the
# words remove_cell to remove cells. You can also modify the code to use
# a different tag word
c.TagRemovePreprocessor.remove_cell_tags = ("hide-cell",)
c.TagRemovePreprocessor.remove_all_outputs_tags = ('hide-output',)
c.TagRemovePreprocessor.remove_input_tags = ('hide-input',)
c.TagRemovePreprocessor.enabled = True

# Configure and run out exporter
c.HTMLExporter.preprocessors = ["nbconvert.preprocessors.TagRemovePreprocessor"]

html_exporter = HTMLExporter(config=c)
html_exporter.register_preprocessor(TagRemovePreprocessor(config=c), True)

body, resources = html_exporter.from_filename("src/index.ipynb")
with open(f"docs/index.html", "w") as f:
    f.write(body)
all_filePath = glob.glob("src/gp/*/*/*.ipynb")
for filePath in all_filePath:
    uniqueName = filePath.replace("/", "").replace(".ipynb", "").replace("src", "")
    body, resources = html_exporter.from_filename(filePath)
    with open(f"docs/{uniqueName}.html", "w") as f:
        f.write(body)
