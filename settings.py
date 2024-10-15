SETTINGS = {
    "SYSTEM": {
        "DEFAULT_FUNC_SUFFIX": "py",

        "RANDOM_SYSTEM": {
            "MINIMUM_NUMBER_START": 1,
            "MAX_NUMBER_OFFSET": 9,
            "ASCII_LOWERCASE": 'abcdefghijklmnopqrstuvwxyz',
            "ASCII_UPPERCASE": 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
            "DIGITS": '0123456789',
            "UNDERLINE": "_",
        },

        "FILE_SYSTEM": {
            'RANDOM_PROCESS_BLOCK_ENABLE': False,
            'EDIT_PROCESS_BLOCK_ENABLE': True,
            'MAX_PROCESS_BLOCK_SIZE': 1024,
            'DEFAULT_CONTENT_ENABLE': False,
            'DEFAULT_CONTENT_SIZE': 0,
        },

        'FOLDER': {
            'OUTPUT_FILE_FOLDER': "dst",
            'INPUT_FILE_FOLDER': "src",
            'LOG_FILE_FOLDER': "logs",
            'READ_FILE_FOLDER': "read",
            'CORE_CODE_FILE_FOLDER': "core",
            'TAMPER_FILE_FOLDER': "tamper",
            'MODULE_FILE_FOLDER': "module",
        },

    },

    'RUNNING': {
        'INPUT_FILENAME': "payload.xml",
        'OUTPUT_FILENAME': "out.bat",

        "ENTER_FUNCTION": {
            'READ_ENTER_FUNCTION': 'read',
            'TAMPER_ENTER_FUNCTION': "encode",
            'MODULE_ENTER_FUNCTION': "run",
        },

        "START_SIGNAL": {
            'READ_ENTER_FUNCTION_START': 'read_data',
        },

        'TAMPER_LIST': [
            'tamper2base64',
        ],
        "MODULE_LIST": [
            'echo_openssl_base64',

        ],
        "READ_FUNCTION": "whole_file2bytes",
    }
}
