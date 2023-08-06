import click

FRUITCONFIG_NAME = "fruitconfig.py"
FRUIT_DIR_NAME = ".fruit"
FRUIT_DIR_CONFIG = f"{FRUIT_DIR_NAME}/__init__.py"

WIDTH = (click.get_terminal_size()[0] - 10)

SEP_TARGET          = "=" * WIDTH
SEP_STEP            = "-" * WIDTH

FMT_STEPHEADER      = "🥝 Step {number}: {name}\n" + "-"* WIDTH
FMT_TARGETHEADER    = "🍉 Making '{target}' ...\n" + "=" * WIDTH
FMT_SUBTARGETHEADER = "🍎 Making sub-target '{target}' ..." + ">"* WIDTH

SHELLCHAR = '$ '

ICON_SUCC = "✅"
ICON_FAIL    = "❌"
ICON_SKIP    = "⏭"
ICON_BANANA  = "🍌" 

FMT_SKIPMESSAGE     = ICON_SKIP + "  The step was skipped. {reason}"
FMT_FAILMESSAGE     = ICON_BANANA + "  The step failed! {reason}"