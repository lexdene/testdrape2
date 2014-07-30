do(jq=jQuery)->
  repeat_string = (str, time)->
    new Array(time + 1).join(str)
  format_number = (n, len)->
    str_n = '' + n

    switch
      when len > str_n.length
        repeat_string('0', len - str_n.length) + str_n
      when len < str_n.length
        str_n.substring str_n.length - len
      else
        str_n
  format_date = (date, format)->
    regexp = /%([0-9]?)([yMdhms])/g
    format.replace regexp, (aword, len, item)->
      if len == ''
        len = 2
      else
        len = parseInt len

      item_val = switch item
        when 'y' then date.getFullYear()
        when 'M' then date.getMonth() + 1
        when 'd' then date.getDate()
        when 'h' then date.getHours()
        when 'm' then date.getMinutes()
        when 's' then date.getSeconds()

      format_number item_val, len

  create_date_formater = (now)->
    if not now
      throw "now is empty"

    now = new Date now

    today = new Date now
    today.setHours 0
    today.setMinutes 0
    today.setSeconds 0
    today.setMilliseconds 0

    yesterday = today - 24 * 3600 * 1000

    (to_time)->
      to_time = new Date to_time
      diff = (now - to_time) / 1000;

      switch
        when to_time < yesterday
          # before yesterday
          format_date to_time, '%4y-%M-%d %h:%m:%s'
        when to_time < today
          # yesterday
          '昨天' + format_date to_time, '%h:%m:%s'
        when diff < 60
          # less then 1 minute
          '刚刚'
        when diff < 3600
          # less then 1 hour
          Math.floor(diff / 60) + '分钟前'
        else
          # more then 1 hour
          '今天' + format_date to_time, '%h:%m:%s'

  jq.extend
    create_date_formater: create_date_formater
