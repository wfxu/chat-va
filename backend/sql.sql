-- 创建消息表
CREATE TABLE IF NOT EXISTS messages (
	u_id INTEGER NOT NULL,
	m_id INTEGER NOT NULL,
	dateTime DATETIME NOT NULL,
	content TEXT NOT NULL,
	is_user INTEGER default 0,
	error INTEGER default 0,
	loading INTEGER default 0
);

-- 创建用户表
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY

)