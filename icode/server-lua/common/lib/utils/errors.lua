
local _M = {
    OK = {status = 200, code = "100000", message = "ok"},
    UNKNOWN_ERR = {status = 500, code = "100001", message = "unknown error"},

    PARAM_INVALID = {status = 400, code = "100101", message = "param invalid"},
}

return _M
