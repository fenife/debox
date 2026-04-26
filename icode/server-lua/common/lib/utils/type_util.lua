local _M = {}

function _M.is_str(obj)
    return type(obj) == "string"
end

function _M.is_num(obj)
    return type(obj) == "number"
end

function _M.is_tab(obj)
    return type(obj) == "table"
end

function _M.is_func(obj)
    return type(obj) == "function"
end

return _M
