
local reply = require("utils.reply")
local errors = require("utils.errors")


local function handle ()
    local action = ngx.var.arg_action

    if not action or action == "a" then 
        local data = {hello = 123}
        reply.say_ok(data)
    end

    if action == "b" then
        reply.say_error(errors.INTERNAL_ERR)
    end

    if action == "c" then
        reply.say_error(errors.PARAM_INVALID)
    end
    
    if action == "d" then
        local emsg = "error d"
        reply.say_error(emsg)
    end

    if action == "e" then
        local err  = {code = nil, message = "error e"}
        reply.say_error(err)
    end

end

handle()
