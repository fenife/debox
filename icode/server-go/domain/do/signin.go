/*
Domain Object (do)
do 对象不像 entity object 实体对象，不包含ID，当函数中出现无法用entity表示的输入输出对象时，可以在 do 里定义
*/

package do

import "time"

const signinInternalLimit = 30 // 登陆限制，多少秒内只能登陆一次，一般小于 userCacheExpired

type UserSignInInfo struct {
	Token  string `json:"token"`
	UserId uint64 `json:"user_id"`
	SignTs int64  `json:"sign_ts"`
}

func (s *UserSignInInfo) IsSignInLimit() bool {
	return time.Now().Unix()-s.SignTs < signinInternalLimit
}
