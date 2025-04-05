package req

type SignupReq struct {
	Name     string `json:"name" binding:"required,gte=3,lte=20"`
	Password string `json:"password" binding:"required,gte=3,lte=32"`
}

type SignInReq struct {
	Name     string `json:"name" binding:"required,gte=3,lte=20"`
	Password string `json:"password" binding:"required,gte=3,lte=32"`
}
