from os import environ


def env(key, type_, default=None):
    if key not in environ:
        return default

    val = environ[key]

    if type_ == str:
        return val
    elif type_ == bool:
        if val.lower() in ["1", "true", "yes", "y", "ok", "on"]:
            return True
        if val.lower() in ["0", "false", "no", "n", "nok", "off"]:
            return False
        raise ValueError(
            "Invalid environment variable '%s' (expected a boolean): '%s'" % (key, val)
        )
    elif type_ == int:
        try:
            return int(val)
        except ValueError:
            raise ValueError(
                "Invalid environment variable '%s' (expected an integer): '%s'" % (key, val)
            ) from None


WALK-LOGGER_AUTOINIT = env("WALK-LOGGER_AUTOINIT", bool, True)

WALK-LOGGER_FORMAT = env(
    "WALK-LOGGER_FORMAT",
    str,
    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
)
WALK-LOGGER_FILTER = env("WALK-LOGGER_FILTER", str, None)
WALK-LOGGER_LEVEL = env("WALK-LOGGER_LEVEL", str, "DEBUG")
WALK-LOGGER_COLORIZE = env("WALK-LOGGER_COLORIZE", bool, None)
WALK-LOGGER_SERIALIZE = env("WALK-LOGGER_SERIALIZE", bool, False)
WALK-LOGGER_BACKTRACE = env("WALK-LOGGER_BACKTRACE", bool, True)
WALK-LOGGER_DIAGNOSE = env("WALK-LOGGER_DIAGNOSE", bool, True)
WALK-LOGGER_ENQUEUE = env("WALK-LOGGER_ENQUEUE", bool, False)
WALK-LOGGER_CATCH = env("WALK-LOGGER_CATCH", bool, True)

WALK-LOGGER_TRACE_NO = env("WALK-LOGGER_TRACE_NO", int, 5)
WALK-LOGGER_TRACE_COLOR = env("WALK-LOGGER_TRACE_COLOR", str, "<cyan><bold>")
WALK-LOGGER_TRACE_ICON = env("WALK-LOGGER_TRACE_ICON", str, "✏️")  # Pencil

WALK-LOGGER_DEBUG_NO = env("WALK-LOGGER_DEBUG_NO", int, 10)
WALK-LOGGER_DEBUG_COLOR = env("WALK-LOGGER_DEBUG_COLOR", str, "<blue><bold>")
WALK-LOGGER_DEBUG_ICON = env("WALK-LOGGER_DEBUG_ICON", str, "🐞")  # Lady Beetle

WALK-LOGGER_INFO_NO = env("WALK-LOGGER_INFO_NO", int, 20)
WALK-LOGGER_INFO_COLOR = env("WALK-LOGGER_INFO_COLOR", str, "<bold>")
WALK-LOGGER_INFO_ICON = env("WALK-LOGGER_INFO_ICON", str, "ℹ️")  # Information

WALK-LOGGER_SUCCESS_NO = env("WALK-LOGGER_SUCCESS_NO", int, 25)
WALK-LOGGER_SUCCESS_COLOR = env("WALK-LOGGER_SUCCESS_COLOR", str, "<green><bold>")
WALK-LOGGER_SUCCESS_ICON = env("WALK-LOGGER_SUCCESS_ICON", str, "✔️")  # Heavy Check Mark

WALK-LOGGER_WARNING_NO = env("WALK-LOGGER_WARNING_NO", int, 30)
WALK-LOGGER_WARNING_COLOR = env("WALK-LOGGER_WARNING_COLOR", str, "<yellow><bold>")
WALK-LOGGER_WARNING_ICON = env("WALK-LOGGER_WARNING_ICON", str, "⚠️")  # Warning

WALK-LOGGER_ERROR_NO = env("WALK-LOGGER_ERROR_NO", int, 40)
WALK-LOGGER_ERROR_COLOR = env("WALK-LOGGER_ERROR_COLOR", str, "<red><bold>")
WALK-LOGGER_ERROR_ICON = env("WALK-LOGGER_ERROR_ICON", str, "❌")  # Cross Mark

WALK-LOGGER_CRITICAL_NO = env("WALK-LOGGER_CRITICAL_NO", int, 50)
WALK-LOGGER_CRITICAL_COLOR = env("WALK-LOGGER_CRITICAL_COLOR", str, "<RED><bold>")
WALK-LOGGER_CRITICAL_ICON = env("WALK-LOGGER_CRITICAL_ICON", str, "☠️")  # Skull and Crossbones
