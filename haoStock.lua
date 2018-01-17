#!/usr/bin/lua

--用来分割字符串
function split( str,reps )
    local resultStrList = {}
    string.gsub(str,'[^'..reps..']+',function ( w )
        table.insert(resultStrList,w)
    end)
    return resultStrList
end

function get_date()
    local date = os.date("%Y%m%d")
	return date
end

--检查当日是否是开市的日子
function verify_date()
    local http = require("socket.http")
    local url = "http://qt.gtimg.cn/q=sh000001"
	local resp = http.request(url)
	local mytab = split(resp,'~')
	local stock_date =string.sub(mytab[31],1,8)
	if stock_date == get_date() then
	    return stock_date 
	else
	    return nil
	end
end

--产生最终文件
function gen_file(file_name,code_file)
    local http = require("socket.http")
	local pre_url = "http://qt.gtimg.cn/q="
    local file_w = io.open(file_name,"w")
	local file_r = io.open(code_file,"r")
	local lines = {}
	io.input(file_r)
	io.output(file_w)
	io.write("name,turnover rate,previous trading day close,opening,price,StockCode\n")
    for line in io.lines() do   --通过迭代器访问每一个数据
        lines[#lines + 1] = line
    end
    for _,l in ipairs(lines) do
	    local url = pre_url..l
	    local resp = http.request(url)
        --print(resp)
		if resp then
    	    local mytab = split(resp,'~')
	    	if mytab[2] then
		        io.write(mytab[2],",")
		        io.write(mytab[39],",")
	            io.write(mytab[5],",")
	            io.write(mytab[6],",")
	            io.write(mytab[4],",")
		        io.write(l,"\n")
		    end
	    end
    end
	io.close(file_r)
	io.close(file_w)
end

--发送邮件及附件
function sendmail(file_name)
    local smtp = require("socket.smtp")
    local mime = require("mime")
    local ltn12 = require("ltn12")
	local rcpt = {
    "<xxx@xxx>"			--此处为收件人
    }
    local source = smtp.message{
        headers = {
            from = "asd<dasfa@xxx>", 	--填上发件人
            to = "you<xxx@xxx>",	--填上收件人
            subject = "这是"..get_date().."股票情况"
        },
        body = {
            [1] = { 
            body = mime.eol(0, [[
                name代表股票名,
				price代表统计时的股价,
				previous trading day close代表前一交易日收盘价,
				opening代表今日开盘价,
				turnover rate代表换手率,
				StockCode代表股票代码
                ]])
            },
            [2] = { 
                headers = {
                    ["content-type"] = 'application/octet-stream; name='..file_name,
                    ["content-disposition"] = 'attachment; filename='..file_name,
                    ["content-description"] = '股票数据',
                    ["content-transfer-encoding"] = "BASE64"
                },
                body = ltn12.source.chain(
                    ltn12.source.file(io.open(file_name, "rb")),
                    ltn12.filter.chain(
                        mime.encode("base64"),
                        mime.wrap()
                    )
                )
            },
        }
    }

    r, e = smtp.send{
        from = "<asda@163.com>",	--发件人邮箱
        rcpt = rcpt,
        source = source,
	    server = "smtp.163.com",	--smtp服务器地址
        user = "usermail",	--此处填写发送邮箱的用户名
        password = "password"	--此处填邮箱的密码
    }
    if not r then
        print(e)
--    else
--        print("send ok!")
    end
	return 0
end

--获取http://quote.eastmoney.com/stocklist.html
function get_stockcodehtml(html_file)
    local http = require("socket.http")
	local ltn12 = require("ltn12")
	local file = io.open(html_file,"w")
	--io.output(file)
	local res, code, response_headers = http.request{
        url = "http://quote.eastmoney.com/stocklist.html",
        sink = ltn12.sink.file(file)
        --proxy = "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)"
    }
	if code == 200 then
        return true
	else
	    return false
	end
end

--解析出所有股票代码
function get_stockcode(html_file,code_file)
    local file_r = io.open(html_file,"r")
	local file_w = io.open(code_file,"w")
	local stockcode = "s[hz]%d%d%d%d%d%d"
	local lines = {}
	io.input(file_r)
	io.output(file_w)
    for line in io.lines() do   --通过迭代器访问每一个数据
        lines[#lines + 1] = line
    end
    table.sort(lines)  --排序，Lua标准库的table库提供的函数。
    for _,l in ipairs(lines) do
	    local spos,epos = string.find(l,stockcode)
	    if spos and epos then
            io.write(string.sub(l,spos,epos),"\n")
		end
    end
	io.close(file_r)
	io.close(file_w)
end

--更新股票代码
function update_stockcode(html_file,code_file)
    if get_stockcodehtml(html_file) then
        get_stockcode(html_file,code_file)
    else
        print("fail")
    end
	os.remove(html_file)
end

function main()
    local stock_date = verify_date()
	if not stock_date then
	    return
	else
	    update_stockcode("/tmp/stock.html","/tmp/stockcode")	--文件位置根据实际系统情况修改
	    local file_name = "/tmp/"..stock_date..".csv"
	    gen_file(file_name,"/tmp/stockcode")
		sendmail(file_name)
		print("sendmail ok.")
		os.remove(file_name)
	end
	return 0
end


main()
