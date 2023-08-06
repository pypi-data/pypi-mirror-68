"""VS module names"""

# MKV0001

from .classes import (
    MKVAttachment,
    MKVAttachments,
    MKVCommand,
    MKVCommandParser,
    MKVCommandNew,
    SourceFile,
    SourceFiles,
    VerifyMKVCommand,
    VerifyStructure,
)
from .mkvutils import (
    getMKVMerge,
    getMKVMergeVersion,
    numberOfTracksInCommand,
    resolveOverwrite,
    stripEncaseQuotes,
    unQuote,
)
