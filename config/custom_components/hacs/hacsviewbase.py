"""Blueprint for HacsViewBase."""
from homeassistant.components.http import HomeAssistantView
from .hacsbase import HacsBase


class HacsViewBase(HomeAssistantView, HacsBase):
    """Base View Class for HACS."""

    requires_auth = False

    def load_element(self, element):
        """return element content."""
        location = "{}/custom_components/hacs/frontend/elements/{}.html".format(self.config_dir, element)
        with open(location, "r") as elementfile:
            content = elementfile.read()
            elementfile.close()
        return content

    @property
    def base_content(self):
        """Base content."""
        return """
            <head>
                {}
            </head>
            <body>
            {}
            <div id="main" class="hacs-content">
            {}
        """.format(
            self.imports, self.header, self.progress_bar
        )

    @property
    def imports(self):
        """Load imports."""
        return """
        <link rel="stylesheet" href="{static}/materialize.min.css.gz">
        <link rel="stylesheet" href="{static}/all.min.css.gz">
        <script src="{static}/materialize.min.js.gz"></script>
        <link rel="stylesheet" href="{static}/hacs.css">
        <script src="{static}/hacs.js"></script>
        """.format(
            static=self.url_path["static"]
        )

    @property
    def header(self):
        """Load header."""
        return """
        <div class="navbar-fixed">
          <nav class="nav-extended hacs-nav">
            <div class="nav-content">
              <ul class="right tabs tabs-transparent">
                <li class="tab"><a href="{}">overview</a></li>
                <li class="tab"><a href="{}">store</a></li>
                <li class="tab right"><a href="{}">settings</a></li>
              </ul>
            </div>
          </nav>
        </div>
        """.format(
            self.url_path["overview"], self.url_path["store"], self.url_path["settings"]
        )

    @property
    def progress_bar(self):
        """Load progress bar."""
        display = "block" if self.store.task_running else "none"
        return """
        <div style="display: {}"><p>Background task running, refresh the page in a little while.</p></div>
        <div class="progress hacs-bar-background" id="progressbar" style="display: {}">
            <div class="indeterminate hacs-bar"></div>
        </div>
        <div class="loading hidden">
        <div class='uil-ring-css' style='transform:scale(0.79);'>
            <div></div>
        </div>
        </div>
        """.format(
            display, display
        )

    @property
    def footer(self):
        """Return the end of the document."""
        return "</div></body>"
