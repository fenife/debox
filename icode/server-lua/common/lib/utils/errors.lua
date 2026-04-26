local _M = {
    OK = { status = 200, code = "100000", message = "ok" },
    INTERNAL_ERR = { status = 500, code = "100001", message = "internal error" },
    UNDEFINE_ERR = { status = 500, code = "100002", message = "undefine error" },

    PARAM_INVALID = { status = 400, code = "100101", message = "param invalid" },
}

function _M.new_error(status, code, message)
    local err = {
        status = status,
        code = code,
        message = message,
    }
    return err
end

return _M
