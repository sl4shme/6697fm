json = (loadfile "./libs/JSON.lua")()
do

function run(msg, matches)
local raw_json = json:encode(msg)
local handle = io.popen("/usr/bin/python /home/ubuntu/telegram-bot/6697fm/core.py '" .. raw_json .. "'") 
local result = handle:read("*a")
handle:close()
return result
end

return {
  description = "Sends links to 6697Fm.", 
  usage = "",
  patterns = {
    ".*https?://.*",
  },
  run = run 
}

end
