local cjson = require("cjson")
local typeutil = require("utils.type_util")
local errors = require("utils.errors")

local _M = {}


function _M._valid_detail(detail)
    if detail or typeutil.is_str(detail) then
        return detail
    else
        ngx.log(ngx.ERR, "reply detail is invalid, type: ", type(detail))
        return nil
    end
end

function _M._valid_status(status)
    if status and typeutil.is_num(status) then
        return status
    else
        ngx.log(ngx.ERR, "reply status is invalid, type: ", type(status))
        _M.say_internal_err()
    end
end

function _M.say_internal_err(detail)
    local _detail = _M._valid_detail(detail)
    local _err = errors.INTERNAL_ERR
    local _status = _err.status
    local _result = cjson.encode({
        code = _err.code,
        message = _err.message,
        detail = _detail,
        data = {},
    })
    ngx.log(ngx.INFO, "reply resp, status: ", _status, ", result: ", _result)
    ngx.status = _status
    ngx.say(_result)
    ngx.exit(_status)
end

function _M._say_result(status, result, detail)
    local _detail = _M._valid_detail(detail)
    -- ngx exit if failed
    local _status = _M._valid_status(status)

    local ok, _result = pcall(cjson.encode, result)
    if not ok then
        ngx.log(ngx.ERR, "encode reply result error: ", _result)
        _M.say_internal_err()
    end
    ngx.log(ngx.INFO, "reply resp, status: ", _status, "result: ", _result)
    ngx.status = _status
    ngx.say(_result)
    ngx.exit(_status)
end

function _M._say_const_err(err, detail)
    local err = err

    if not err then
        ngx.log(ngx.ERR, "error to output is nil")
        err = errors.INTERNAL_ERR
    end
    if not typeutil.is_tab(err) then
        ngx.log(ngx.ERR, "error to output is not a table, type: ", type(err))
        err = errors.INTERNAL_ERR
    end

    if not (err.status and err.code and err.message) then
        ngx.log(ngx.ERR, "undefined table error, status: ", err.status,
            ", code: ", err.code, " message: ", err.message)
        err = errors.INTERNAL_ERR
    end

    local _status = err.status
    local result = {
        code = err.code,
        message = err.message,
        data = {},
        detail = detail,
    }
    ngx.log(ngx.INFO, "reply resp, status: ", _status, ", result: ", cjson.encode(result))
    ngx.status = _status
    ngx.say(cjson.encode(result))
    ngx.exit(_status)
end

function _M.say_error(err)
    if typeutil.is_tab(err) then
        _M._say_const_err(err)
    end

    if typeutil.is_str(err) then
        ngx.log(ngx.INFO, "error msg: ", err)
        _M._say_const_err(errors.UNDEFINE_ERR, err)
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
    ngx.log(ngx.INFO, "reply resp, status: ", _status, "result: ", cjson.encode(result))

    ngx.status = _status
    ngx.say(res)
    ngx.exit(_status)
end

return _M
