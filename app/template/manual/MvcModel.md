# 可任意更换
drape框架的设计原则之一，
就是可任意更换。
我们不限定用户使用的模块，
也不会在用户不知情的情况下做额外的事情，
给用户以充分的自主与自由。

Python提供的orm、sql之类的模块非常多，
而且都非常优秀。
drape没必要在Model上提供过分完备的支持。

例如，
喜欢SQLAlchemy的用户可以轻易地将Model更换成SQLAlchemy。

# LinkedModel
LinkedModel是drape提供的唯一一个Model类。

## 1.依赖
LinkedModel类依赖MySQLdb模块

## 2.链接操作
可以通过链式操作方便地完成sql查询等操作

## 3.自动反射表的字段名
如果不指定查询的字段名，
LinkedModel类会自动反射表的字段名。
并且为了避免字段名冲突，
会自动地加上表名作为前缀。

## 4.例子
如下的代码：

	submitList = aSubmitModel \
			.alias('sm') \
			.join('userinfo','ui','ui.uid = sm.uid') \
			.join('problem','pr','sm.pid = pr.pid') \
			.join('problem_num','pn','pr.pid = pn.pid') \
			.join('judge_result','jr','jr.sid=sm.id) \
			.order('`addtime` DESC') \
			.where({'ui.uid':3}) \
			.limit(length=10,offset=160) \
			.select()

会被自动地执行下面的sql语句并返回查询结果：

	select
		`sm`.`id`,
		`sm`.`pid`,
		`sm`.`uid`,
		`sm`.`judgeResultId`,
		`sm`.`addtime`,
		`sm`.`language`,
		`sm`.`code`,
		`ui`.`uid` as `ui.uid`,
		`ui`.`nickname` as `ui.nickname`,
		`ui`.`email` as `ui.email`,
		`ui`.`avatar` as `ui.avatar`,
		`pr`.`pid` as `pr.pid`,
		`pr`.`title` as `pr.title`,
		`pr`.`addtime` as `pr.addtime`,
		`pr`.`time_limit` as `pr.time_limit`,
		`pr`.`memory_limit` as `pr.memory_limit`,
		`pr`.`description` as `pr.description`,
		`pr`.`input` as `pr.input`,
		`pr`.`output` as `pr.output`,
		`pr`.`sample_input` as `pr.sample_input`,
		`pr`.`sample_output` as `pr.sample_output`,
		`pr`.`hint` as `pr.hint`,
		`pr`.`source` as `pr.source`,
		`pr`.`authorid` as `pr.authorid`,
		`pn`.`pnum` as `pn.pnum`,
		`pn`.`pid` as `pn.pid`,
		`jr`.`id` as `jr.id`,
		`jr`.`sid` as `jr.sid`,
		`jr`.`juid` as `jr.juid`,
		`jr`.`result` as `jr.result`,
		`jr`.`addtime` as `jr.addtime`
	from `submit` as sm
	left join `userinfo` as ui on (ui.uid = sm.uid)
	left join `problem` as pr on (sm.pid = pr.pid)
	left join `problem_num` as pn on (pr.pid = pn.pid)
	left join `judge_result` as jr on (jr.sid=sm.id)
	where ui.uid = 3
	order by `addtime` DESC
	limit 160,10
