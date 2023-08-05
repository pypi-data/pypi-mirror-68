# coding=utf-8
import os
from mkdocs.config import config_options
from mkdocs.plugins import BasePlugin
from mkdocs import utils

class RenderOtherfilePlugin(BasePlugin):
    config_scheme = (
        ('on', config_options.Type(bool, default=False)),
        ('ext', config_options.Type(list, default=[]))
    )
    
    def _check_config_params(self):
        set_parameters = self.config.keys()
        allowed_parameters = dict(self.config_scheme).keys()
        if set_parameters != allowed_parameters:
            unknown_parameters = [x for x in set_parameters if x not in allowed_parameters]
            raise AssertionError("Unknown parameter(s) set: %s" % ", ".join(unknown_parameters))
    
    def on_pre_build(self, config):
        self._check_config_params()
        listext = self.config['ext']
        utils.markdown_extensions.extend(listext)
        return
    def on_files(self, files, config):
        for file in files._files:
            src_path = file.src_path
            filename, ext = os.path.splitext(src_path)
            listext = self.config['ext']
            if ext in listext:
                dest_path, html1 = os.path.splitext(file.dest_path)
                abs_dest_path, html2 = os.path.splitext(file.abs_dest_path)

                file.dest_path = dest_path + ext + html1
                file.abs_dest_path = abs_dest_path + ext + html2
                file.url = dest_path.replace("\\", '/') + ext + html1
                file.name = file.name + ext

        return files 
    def on_page_markdown(self, markdown, page, config, files):
        """
        The page_markdown event is called after the page's markdown is loaded 
        from file and can be used to alter the Markdown source text. 
        The meta- data has been stripped off and is available as page.meta 
        at this point.
        
        See:
        https://www.mkdocs.org/user-guide/plugins/#on_page_markdown
        
        Args:
            markdown (str): Markdown source text of page as string
            page (Page): mkdocs.nav.Page instance
            config (dict): global configuration object
            files (list): global files collection
        
        Returns:
            markdown (str): Markdown source text of page as string
        """
        listext = self.config['ext']
        src_file_path = page.file.abs_src_path
        prepath, ext = os.path.splitext(src_file_path)
        lang = ext.lstrip('.')
        filename = page.file.name
        if ext in listext:
            new_markdown = "# {0}\n\n```{1}\n".format(filename, lang) + markdown + "\n```"
            return new_markdown
        else:
            return markdown
