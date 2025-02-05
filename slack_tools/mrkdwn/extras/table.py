from typing import Literal, Self

from slack_tools.mrkdwn.base import MarkdownStr


class TableRow:
    """A markdown table row."""

    def __init__(self, *items: str) -> None:
        self.items = [str(item).strip() for item in items]


class TableHeader(TableRow):
    """A header row with optional alignments."""

    def __init__(self, *items: str | tuple[str, str]) -> None:
        texts: list[str] = []
        self.alignments: list[str | None] = []
        for item in items:
            if isinstance(item, tuple):
                text, align = item
                texts.append(str(text).strip())
                self.alignments.append(align)
            else:
                texts.append(str(item).strip())
                self.alignments.append(None)
        super().__init__(*texts)


HeaderItem = str | tuple[str, str]
TableItem = str | list[str] | tuple[str, ...] | TableHeader | TableRow


class TableHeaderFactory:
    """Factory to create TableHeader via indexing."""

    def __getitem__(self, items: tuple[HeaderItem, ...]) -> TableHeader:
        return TableHeader(*items)


class MarkdownTable(MarkdownStr):
    """A markdown table builder with bracket API."""

    th: TableHeaderFactory
    _render_as: Literal['inline', 'block'] = 'block'

    def __new__(cls, *args, **kwargs) -> Self:
        instance = super().__new__(cls, '')
        instance.header = None
        instance.rows = []
        instance.padding_size = 1
        instance.th = TableHeaderFactory()
        return instance

    def __getitem__(
        self, items: TableItem | list[TableItem] | tuple[TableItem, ...]
    ) -> Self:
        """Set table rows via bracket indexing."""
        self.header = None
        self.rows = []
        if isinstance(items, (list, tuple)):
            for item in items:
                if isinstance(item, TableHeader):
                    self.header = item
                elif isinstance(item, TableRow):
                    self.rows.append(item)
                elif isinstance(item, (list, tuple)):
                    # Convert plain iterables to TableRow.
                    self.rows.append(TableRow(*item))
                else:
                    self.rows.append(TableRow(str(item)))
        else:
            if isinstance(items, TableHeader):
                self.header = items
            elif isinstance(item, TableRow):
                self.rows.append(items)
            else:
                self.rows.append(TableRow(str(items)))

        # Generate the table string
        all_rows: list[TableRow] = []
        if self.header:
            all_rows.append(self.header)
        all_rows.extend(self.rows)
        if not all_rows:
            return super().__new__(self.__class__, '')

        num_cols = len(all_rows[0].items)

        # Determine maximum width for each column.
        col_widths = [
            max(len(row.items[i]) for row in all_rows) + self.padding_size
            for i in range(num_cols)
        ]

        def fmt_row(row: TableRow) -> str:
            cells = [cell.ljust(col_widths[i]) for i, cell in enumerate(row.items)]
            return '| ' + ' | '.join(cells) + ' |'

        lines: list[str] = []
        if self.header:
            lines.append(fmt_row(self.header))
            sep_cells = []
            for i in range(num_cols):
                width = col_widths[i]
                align = self.header.alignments[i]
                if align == 'center':
                    cell = ':' + '-' * (width - 2) + ':' if width >= 2 else '-' * width
                elif align == 'left':
                    cell = ':' + '-' * (width - 1)
                elif align == 'right':
                    cell = '-' * (width - 1) + ':'
                else:
                    cell = '-' * width
                sep_cells.append(cell)
            lines.append('| ' + ' | '.join(sep_cells) + ' |')
        for row in self.rows:
            lines.append(fmt_row(row))

        return super().__new__(self.__class__, '\n'.join(lines))

    def padding(self, padding: int) -> Self:
        self.padding_size = padding
        return self
