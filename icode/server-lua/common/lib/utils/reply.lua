local cjson = require("cjson")
local typeutil = require("utils.type_util")
local errors = require("utils.errors")

local _M = {}

function _M._say_const_err(err, detail)
    local _unknown_err = errors.PARAM_INVALID

    if not err then
        ngx.log(ngx.ERR, "error to output is nil")
        err = _unknown_err
    end
    if not typeutil.is_tab(err) then
        ngx.log(ngx.ERR, "error to output is not a table, type: ", type(err))
        err = _unknown_err
    end

    local _status = err.status or _unknown_err.status
    local result = {
        code = err.code or _unknown_err.code,
        message = err.message or _unknown_err.message,
        data = {},
        detail = detail,
    }
    ngx.log(ngx.INFO, "say error, status: ", _status, "result: ", cjson.encode(result))
    ngx.status = _status
    ngx.say(cjson.encode(result))
    ngx.exit(_status)
end

function _M.say_error(err)
    if typeutil.is_tab(err) then
        _M._say_const_err(err)
    end

    if typeutil.is_str(err) then
        local emsg = err
        ngx.log(ngx.INFO, "error mg: ", emsg)
        _M._say_const_err(errors.UNKNOWN_ERR, emsg)
    end

end

function _M.say_ok(data)
    local _status = errors.OK.status
    local result = {
        code = errors.OK.code,
        message = errors.OK.message,
        detail = cjson.NULL,
        data = data or {},
    }
    local ok, res = pcall(cjson.encode, result)
    ngx.log(ngx.INFO, "say ok, status: ", _status, "result: ", cjson.encode(result))

    ngx.status = _status
    ngx.say(res)
    ngx.exit(_status)
end

return _M
