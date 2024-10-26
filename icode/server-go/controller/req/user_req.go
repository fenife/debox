package req

type GetUserListReq struct {
	Name string `json:"name" binding:"required,gte=3,lte=20"`
}
