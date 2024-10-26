package resp

type SignInResp struct {
	UserName  string `json:"username"`
	UserToken string `json:"user_token"`
}
