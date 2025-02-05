from slack_tools.mrkdwn_kit import MarkdownKit
from slack_tools.utils.templates import Template

md = MarkdownKit(extras=True)


README_MD = md.compose(
    md.h1('Components'),
    md.h2('Surfaces'),
    md.table[
        md.table.th[
            'Name',
            'Type',
            'Class Name',
            ('Completed?', 'center'),
        ],
        ['Home', 'surface', 'Home', md.todo('x')],
        ['Modal', 'surface', 'Modal', md.todo()],
        ['Workflow Step', 'surface', 'WorkflowStep', md.todo()],
    ],
    md.h2('Composition Objects'),
    md.table[
        md.table.th[
            'Name',
            'Type',
            'Class Name',
            ('Completed?', 'center'),
        ],
        ['Confirmation Dialog', '', 'ConfirmationDialog', md.todo()],
        ['Conversation Filter', '', 'ConversationFilter', md.todo()],
        ['Dispatch Action', '', 'DispatchActionConfig', md.todo()],
        ['Option', '', 'Option', md.todo()],
        ['Option Group', '', 'OptionGroup', md.todo()],
        ['Text', '', 'Text', md.todo()],
        ['Trigger', '', 'Trigger', md.todo()],
        ['Workflow', '', 'Workflow', md.todo()],
        ['Slack File', '', 'SlackFile', md.todo()],
    ],
    md.h2('Action Payload'),
    md.table[
        md.table.th[
            'Name',
            'Type',
            'Class Name',
            ('Completed?', 'center'),
        ],
        ['-', '-', '-', md.todo()],
    ],
    md.h2('Blocks'),
    md.p('Okay'),
    md.table[
        md.table.th[
            'Name',
            'Type',
            'Class Name',
            ('Completed?', 'center'),
        ],
        ['Actions', 'actions', 'Actions', md.todo()],
        ['Context', 'context', 'Context', md.todo()],
        ['Divider', 'divider', 'Divider', md.todo()],
        ['File', 'file', 'File', md.todo()],
        ['Header', 'header', 'Header', md.todo()],
        ['Image', 'image', 'Image', md.todo()],
        ['Input', 'input', 'Input', md.todo()],
        ['Markdown', 'markdown', 'Markdown', md.todo()],
        ['Rich Text', 'rich_text', 'RichText', md.todo()],
        ['Section', 'section', 'Section', md.todo()],
        ['Video', 'video', 'Video', md.todo()],
    ],
    md.h2('Elements'),
    md.table[
        md.table.th[
            'Name',
            'Type',
            'Class Name',
            ('Completed?', 'center'),
        ],
        ['Button', 'element', 'Button', md.todo()],
        ['Checkbox', 'element', 'Checkbox', md.todo()],
        ['Date Picker', 'element', 'DatePicker', md.todo()],
        ['Datetime Picker', 'element', 'DateTimePicker', md.todo()],
        ['Email Input', 'element', 'EmailInput', md.todo()],
        ['File Input', 'element', 'FileInput', md.todo()],
        ['Multi Static Select', 'element', 'MultiStaticSelect', md.todo()],
        ['Multi External Select', 'element', 'MultiExternalSelect', md.todo()],
        ['Multi Users Select', 'element', 'MultiUsersSelect', md.todo()],
        [
            'Multi Conversations Select',
            'element',
            'MultiConversationsSelect',
            md.todo(),
        ],
        ['Multi Channels Select', 'element', 'MultiChannelsSelect', md.todo()],
        ['Number Input', 'element', 'NumberInput', md.todo()],
        ['Overflow', 'element', 'Overflow', md.todo()],
        ['Plain Text Input', 'element', 'PlainTextInput', md.todo()],
        ['Radio Buttons', 'element', 'RadioButtons', md.todo()],
        ['Rich Text Input', 'element', 'RichTextInput', md.todo()],
        ['Static Select', 'element', 'StaticSelect', md.todo()],
        ['External Select', 'element', 'ExternalSelect', md.todo()],
        ['Users Select', 'element', 'UsersSelect', md.todo()],
        ['Conversations Select', 'element', 'ConversationsSelect', md.todo()],
        ['Channels Select', 'element', 'ChannelsSelect', md.todo()],
        ['Time Picker', 'element', 'TimePicker', md.todo()],
        ['URL Input', 'element', 'URLInput', md.todo()],
        ['Workflow Button', 'element', 'WorkflowButton', md.todo()],
    ],
)


template = Template()

# Write to README.md
print(template.render('{{ README_TABLE }}', README_TABLE=README_MD))
