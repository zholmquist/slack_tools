import subprocess
import sys

from rich.console import Console

console = Console()


class CopyableStrMixin(str):
    def to_clipboard(self):
        """Copy the URL to the clipboard."""
        console.log('🔗 Copying to clipboard...', style='bold', emoji=True, end='\n\n')
        try:
            if sys.platform == 'darwin':  # macOS
                subprocess.run(['pbcopy'], text=True, input=str(self), check=False)
            elif sys.platform.startswith('linux'):
                subprocess.run(
                    'xclip -selection clipboard',
                    shell=True,
                    text=True,
                    input=str(self),
                    check=False,
                )
            elif sys.platform.startswith('win'):
                subprocess.run(
                    'clip', shell=True, text=True, input=str(self), check=False
                )
            else:
                raise NotImplementedError('Clipboard copy not supported on this OS.')
        except Exception as e:
            console.log(f'Error copying to clipboard: {e}', style='bold red')

        console.log('🎉 Copied to clipboard.', style='bold green', emoji=True)
